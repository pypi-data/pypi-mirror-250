GET = r"""
    ret = await hub.tool.gitlab.request.json(
        ctx, "get",
        url = f"{ctx.acct.endpoint_url}{{ function.hardcoded.path }}/{resource_id}",
        success_codes=[200]
    )
    if not ret.result:
        ret.ret = {}
    else:
        ret.ret = hub.tool.{{ function.ref }}.raw_to_present(ret.ret)
    return ret
"""

LIST = r"""
    result = dict(ret=[], result=True, comment=[])

    {% if function.hardcoded.short_list_path %}

    async for project in hub.tool.gitlab.request.paginate(ctx, url=f"{ctx.acct.endpoint_url}{{ function.hardcoded.short_list_path }}", **kwargs):
        project_id = project.id
        async for ret in hub.tool.gitlab.request.paginate(ctx, url=f"{ctx.acct.endpoint_url}{{ function.hardcoded.path }}", **kwargs):
            resource = hub.tool.{{ function.ref }}.raw_to_present(ret)
            result["ret"].append(resource)
    {% else %}
    async for ret in hub.tool.gitlab.request.paginate(ctx, url=f"{ctx.acct.endpoint_url}{{ function.hardcoded.path }}", **kwargs):
        resource = hub.tool.{{ function.ref }}.raw_to_present(ret)
        result["ret"].append(resource)
    {% endif %}
    return result
"""

CREATE = r"""
    data = {k: v for k, v in locals().items() if k not in ("hub", "ctx", "resource_id")}
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "post",
        success_codes=[201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/{{ function.hardcoded.path }}",
        data=data,
    )
    ret.ret = hub.tool.{{ function.ref }}.raw_to_present(ret.ret)
    return ret
"""

UPDATE = r"""
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "put",
        url=f"{ctx.acct.endpoint_url}{{ function.hardcoded.path }}/{resource_id}",
        success_codes=[200, 204, 304],
        data=dict(id=resource_id, **kwargs)
    )
    return ret
"""


DELETE = r"""
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "delete",
        url=f"{ctx.acct.endpoint_url}{{ function.hardcoded.path }}/{resource_id}",
        success_codes=[202, 204, 404],
        data={{ parameter.mapping.kwargs|default({}) }}
    )
    return ret
"""


RAW_TO_PRESENT = """
    if not isinstance(resource, dict):
        raise TypeError(resource)

    clean_resource = {
        {%- for k,v in function.hardcoded.create_parameter.items() %}
            "{{ k }}": resource.get("{{ k }}"),
        {%- endfor %}
    }

    # Remove empty values
    clean_resource = {k: v for k, v in clean_resource.items() if v is not None}
    return clean_resource
"""

TEST_RESOURCE_INIT = '''
@pytest.fixture(scope="module", autouse=True)
def resource_init(resource):
    """
    Initialize the necessary attributes of the resource to create it
    """
    resource.__ref__ = "{{ function.ref }}"
'''

TEST_PRESENT = '''
@pytest.mark.dependency(name="present")
def test_present(idem_cli, resource, __test: TestFlag):
    """
    Verify the ability to create a resource and achieve a steady initial state
    """
    if "NO_CHANGE" in __test.name and "resource_id" not in resource:
        raise pytest.skip("No resource_id from present state")

    # Run the state with the idem cli
    with resource as sls:
        ret = idem_cli("state", sls)

    # Verify that the subprocess succeeded
    assert ret["result"], ret["stderr"]
    assert ret["json"], "Output did not result in readable json"

    # Verify that the individual state succeeded
    state_ret = next(iter(ret["json"].values()))
    assert state_ret["result"], state_ret["comment"]

    # The __test fixture ran this four times, verify that each run produced the right output
    if __test is TestFlag.TEST:
        assert (
            f"Would create '{resource.__ref__}:{resource.name}'" in state_ret["comment"]
        )
        assert not state_ret["old_state"]
        assert state_ret["new_state"]
    elif __test is TestFlag.RUN:
        assert f"Created '{resource.__ref__}:{resource.name}'" in state_ret["comment"]
        assert not state_ret["old_state"]
        assert state_ret["new_state"]
        # The first time we run the present state for real,
        #   we need to update make sure the resource's attributes propagate to the other functions
        resource.update(state_ret.new_state)
    elif __test is TestFlag.TEST_NO_CHANGE or __test is TestFlag.RUN_NO_CHANGE:
        assert (
            f"'{resource.__ref__}:{resource.name}' already exists"
            in state_ret["comment"]
        )
        assert state_ret["new_state"]
        assert state_ret["new_state"] == state_ret["old_state"]
        assert not state_ret["changes"]
'''

TEST_GET = '''
@pytest.mark.dependency(depends=["present"])
def test_get(idem_cli, resource):
    """
    Verify that we can get the resource using the "idem exec" cli call.
    """
    ret = idem_cli("exec", "{{ function.ref }}.get", resource.resource_id)

    # Verify that the subprocess ran successfully
    assert ret["result"], ret["stderr"]
    assert ret["json"], "Output did not result in readable json"

    # Verify the output of the exec module
    get_ret = ret["json"]
    assert get_ret["result"], get_ret["comment"]
    assert get_ret["ret"] == resource
'''

TEST_LIST = '''
@pytest.mark.dependency(depends=["present"])
def test_list(idem_cli, resource):
    """
    Verify that we can list the resource using the "idem exec" cli call.
    """
    ret = idem_cli("exec", "{{ function.ref }}.list")

    # Verify that the subprocess ran successfully
    assert ret["result"], ret["stderr"]
    assert ret["json"], "Output did not result in readable json"

    # Verify that the resource created by the present state exists in the list
    list_ret = ret["json"]
    assert list_ret["result"], list_ret["comment"]
    for data in list_ret["ret"]:
        if resource.resource_id == data["resource_id"]:
            break
    else:
        assert False, "Resource_id not found in list"
'''

TEST_DESCRIBE = '''
@pytest.mark.dependency(depends=["present"])
def test_describe(resource, idem_cli):
    """
    Verify the ability to describe the resource and run "idem state"
    on the output of describe with no changes made.
    """
    describe_ret = idem_cli("describe", "{{ function.ref }}")

    # Verify tat the subprocess ran successfully
    assert describe_ret["result"], describe_ret["stderr"]
    assert describe_ret["json"], "Output did not result in readable json"

    # Find the resource created in the present state in the output of "idem describe"
    assert str(resource.resource_id) in describe_ret["json"]

    # Create a new present state based on the output of describe
    resource_state = {
        str(resource.resource_id): dict(describe_ret["json"][str(resource.resource_id)])
    }

    # Write the output of describe to a new sls file
    with tempfile.NamedTemporaryFile(suffix=".sls", delete=True) as fh:
        fh.write(yaml.dump(resource_state).encode())
        fh.flush()

        # Run the SLS file, no changes should have been made
        ret = idem_cli("state", fh.name)

    # Verify that the subprocess was successful
    assert ret["result"], ret["stderr"]
    assert ret["json"], "Output did not result in readable json"

    # Verify that the individual state was successful
    state_ret = next(iter(ret["json"].values()))

    assert state_ret["result"], state_ret["comment"]
    assert (
        f"'{resource.__ref__}:{resource.name}' already exists" in state_ret["comment"]
    )

    # Verify that no changes were made
    assert state_ret["new_state"]
    assert state_ret["new_state"] == state_ret["old_state"]
    assert not state_ret["changes"]
'''

TEST_UPDATE = '''
@pytest.mark.dependency(depends=["present"])
def test_update(__test, resource, idem_cli):
    """
    Verify the ability to change each individual attribute of the resource
    """
'''

TEST_ABSENT = '''
def test_absent(resource, __test, idem_cli):
    """
    Destroy the resource created by the present state
    """
    if "resource_id" not in resource:
        raise pytest.skip("No resource_id from present state")

    # Run the present state with the "--invert" flag
    with resource as sls:
        ret = idem_cli("state", sls, "--invert")

    # Verify that the subprocess ran successfully
    assert ret["result"], ret["stderr"]
    assert ret["json"], "Output did not result in readable json"

    # Verify the output of hte individual state
    state_ret = next(iter(ret["json"].values()))
    assert state_ret["result"], state_ret["comment"]

    # The __test fixture ran this four times, verify that each run produced the right output
    if __test is TestFlag.TEST:
        assert (
            f"Would delete '{resource.__ref__}:{resource.name}'" in state_ret["comment"]
        )
        return
    elif __test is TestFlag.RUN:
        assert f"Deleted '{resource.__ref__}:{resource.name}'" in state_ret["comment"]
        assert state_ret["old_state"]
        assert not state_ret["new_state"]
    elif __test is TestFlag.TEST_NO_CHANGE or __test is TestFlag.RUN_NO_CHANGE:
        assert (
            f"'{resource.__ref__}:{resource.name}' already absent"
            in state_ret["comment"]
        )
        assert not state_ret["new_state"]
        assert state_ret["new_state"] == state_ret["old_state"]
        assert not state_ret["changes"]
'''
