"""Exec module for managing Standalone Runners. Runners"""
from typing import Any

__contracts__ = ["auto_state"]

__func_alias__ = {"list_": "list"}


async def get(
    hub, ctx, resource_id: str, *, name: str = None, **kwargs
) -> dict[str, Any]:
    """
    Get a list of all runners in the GitLab instance (project and shared). Access
    is restricted to users with administrator access.


    Args:
        resource_id(str):
             unique ID.

    Returns:
        dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            unmanaged_resource:
              exec.run:
                - path: gitlab.standalone.runner.get
                - kwargs:
                  resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.standalone.runner.get resource_id=value
    """
    data = {k: v for k, v in locals().items() if k not in ("hub", "ctx", "resource_id")}
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "get",
        success_codes=[200, 201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/runners/{resource_id}",
        data=data,
    )
    if ret.result:
        ret.ret["name"] = name
        ret.ret = hub.tool.gitlab.standalone.runner.raw_to_present(ret.ret)
    return ret


async def list_(hub, ctx, **kwargs) -> dict[str, Any]:
    """
    Get a list of runners available to the user.


    Args:

    Returns:
        dict[str, Any]

    Examples:

        Resource State:

        .. code-block:: sls

            unmanaged_resources:
              exec.run:
                - path: gitlab.standalone.runner.list

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.standalone.runner.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe gitlab.standalone.runner

    """
    result = dict(ret=[], result=True, comment=[])

    async for ret in hub.tool.gitlab.request.paginate(
        ctx, url=f"{ctx.acct.endpoint_url}/runners/all", **kwargs
    ):
        resource = hub.tool.gitlab.standalone.runner.raw_to_present(ret)
        result["ret"].append(resource)

    return result


async def create(
    hub,
    ctx,
    resource_id: str,
    *,
    projects: list[int] = None,
    groups: list[int] = None,
    description: str = None,
    paused: bool = None,
    tags: list[str] = None,
    run_untagged: bool = None,
    locked: bool = None,
    access_level: str = None,
    maximum_timeout: int = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Create a runner under the current user

    Args:
        resource_id(str):
            The ID of a runner.

        description(str, Optional):
            The description of the runner. Defaults to None.

        paused(bool, Optional):
            Specifies if the runner should ignore new jobs. Defaults to None.

        tags(list[str], Optional):
            The tags for the runner. Defaults to None.

        run_untagged(bool, Optional):
            Specifies if the runner can execute untagged jobs. Defaults to None.

        locked(bool, Optional):
            Specifies if the runner is locked. Defaults to None.

        access_level(str, Optional):
            The access level of the runner; not_protected or ref_protected. Defaults to None.

        maximum_timeout(int, Optional):
            Maximum timeout that limits the amount of time (in seconds) that runners can run jobs. Defaults to None.

        kwargs(dict, Optional):
            Any keyword arguments to be passed as data to the resource. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              gitlab.standalone.runner.present:
                - resource_id: value
                - project_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.standalone.runner.create resource_id=value
    """
    data = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "resource_id", "type", "tags", "projects", "groups")
    }

    data["tag_list"] = tags
    data["runner_type"] = "instance_type"

    ret = await hub.tool.gitlab.request.json(
        ctx,
        "post",
        success_codes=[201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/user/runners",
        data=data,
    )
    if ret.result:
        get = await hub.exec.gitlab.runner.get(ctx, ret.ret["id"])
        ret.ret = get.ret
    return ret


async def update(
    hub,
    ctx,
    resource_id: str,
    projects: list[int] = None,
    groups: list[int] = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Update details of a runner.

    Args:
        resource_id(str):
            A unique identifier for the resource.

        project_id(int):
            The ID of a runner.

        kwargs(dict, Optional):
            Any keyword arguments to be passed as data to the resource. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              gitlab.standalone.runner.present:
                - resource_id: value
                - projects:
                    - project_id_1
                - groups:
                    - group_id_1

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.standalone.runner.update resource_id=value, project_id=value
    """
    ret = dict(result=True, comment=[], ret=None)
    if any(
        key in kwargs
        for key in (
            "description",
            "active",
            "paused",
            "tags",
            "run_untagged",
            "locked",
            "access_level",
            "maximum_timeout",
        )
    ):
        kwargs["tag_list"] = kwargs.get("tags")
        ret = await hub.tool.gitlab.request.json(
            ctx,
            "put",
            url=f"{ctx.acct.endpoint_url}/runners/{resource_id}",
            success_codes=[200, 204, 304],
            data=kwargs,
        )

    # Add this runner to all the projects defined in the list
    if projects:
        for project_id in projects:
            ret = await hub.tool.gitlab.request.json(
                ctx,
                "post",
                url=f"{ctx.acct.endpoint_url}/projects/{project_id}/{resource_id}",
                success_codes=[200, 204, 304],
            )
            if not ret.result:
                return ret

    # Add this runner to all the groups defined in the list
    if groups:
        for group_id in groups:
            ret = await hub.tool.gitlab.request.json(
                ctx,
                "post",
                url=f"{ctx.acct.endpoint_url}/groups/{group_id}/{resource_id}",
                success_codes=[200, 204, 304],
            )
            if not ret.result:
                return ret

    return ret


async def delete(hub, ctx, resource_id: str, **kwargs) -> dict[str, Any]:
    """
    Disable a project runner from the project. It works only if the project isn’t
    the only project associated with the specified runner. If so, an error is
    returned. Use the call to delete a runner instead.

    Args:
        resource_id(str):
            The ID of a runner.

        project_id(int):
            The ID or URL-encoded path of the project owned by the authenticated user.

        kwargs(dict, Optional):
            Any keyword arguments to be passed as data to the resource. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              gitlab.standalone.runner.absent:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.standalone.runner.delete resource_id=value, project_id=value
    """
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "delete",
        url=f"{ctx.acct.endpoint_url}/runners/{resource_id}",
        success_codes=[202, 204, 404],
    )
    return ret
