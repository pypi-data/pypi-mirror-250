__func_alias__ = {"list_": "list"}


async def get(hub, ctx, resource_id: str = None, **kwargs) -> dict[str, any]:
    """
    Get the properties of the given namespace.

    If a namespace_id is passed, the properties of the given namespaces will be retrieved.
    If a full path to a namespace is passed, all namespaces will be listed and
    the one matching the full path passed in as resource_id will be returned.
    If no resource_id is given, then the default namespace for the user will be returned

    Examples:
        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.namespace.get
    """
    if resource_id:
        # This is namespace_id
        if str(resource_id).isnumeric():
            ret = await hub.tool.gitlab.request.json(
                ctx,
                "get",
                url=f"{ctx.acct.endpoint_url}/namespaces/{resource_id}",
                success_codes=[200],
            )

            ret.ret = hub.tool.gitlab.standalone.namespace.raw_to_present(ret.ret)
        # Retrieve the namespace by matching the full path
        else:
            ret = await hub.exec.gitlab.namespace.list(ctx)

            if not ret.result:
                return ret

            for ns in ret.ret:
                if ns["full_path"] == resource_id:
                    ret.ret = hub.tool.gitlab.standalone.namespace.raw_to_present(ns)
                    break
            else:
                ret.result = False
                ret.ret = {}
                ret.comment.append(f"Could not find namespace: {resource_id}")
    # Grab the default namespace for the authenticated user
    else:
        # The first one in the "owned" namespaces is the default for account in ctx
        ret = await hub.tool.gitlab.request.first_owned(
            ctx, url=f"{ctx.acct.endpoint_url}/namespaces?owned_only=true"
        )

        if not ret.result:
            return ret

        if ret.ret:
            ret.comment.append(
                f"Retrieved the default namespace for authenticated user"
            )
            ret.ret = hub.tool.gitlab.standalone.namespace.raw_to_present(ret.ret[0])

    return ret


async def list_(hub, ctx, **kwargs) -> list[dict[str, any]]:
    """
    Get the properties of the given namespace

    Examples:
        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.namespace.list
    """
    result = dict(ret=[], result=True, comment=[])
    async for ret in hub.tool.gitlab.request.paginate(
        ctx, url=f"{ctx.acct.endpoint_url}/namespaces", **kwargs
    ):
        resource = hub.tool.gitlab.standalone.namespace.raw_to_present(ret)
        result["ret"].append(resource)

    return result
