"""Exec module for managing Project Protected Branches. Protected branches"""
from typing import Any

__contracts__ = ["auto_state"]

__func_alias__ = {"list_": "list"}


async def get(hub, ctx, resource_id: str, project_id: int, **kwargs) -> dict[str, Any]:
    """
    Gets a list of protected branches from a project
    as they are defined in the UI. If a wildcard is set, it is returned instead of the exact name
    of the branches that match that wildcard.


    Args:
        resource_id(str):
            The name of the branch or wildcard.

        project_id(int):
            The ID or URL-encoded path of the project owned by the authenticated user.

    Returns:
        dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            unmanaged_resource:
              exec.run:
                - path: gitlab.project.protected_branch.get
                - kwargs:
                  resource_id: value
                  project_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.protected_branch.get resource_id=value, project_id=value
    """

    ret = await hub.tool.gitlab.request.json(
        ctx,
        "get",
        success_codes=[200, 201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/projects/{project_id}/protected_branches/{resource_id}",
    )
    if ret.result:
        ret.ret = hub.tool.gitlab.project.protected_branch.raw_to_present(ret.ret)
        ret.ret["project_id"] = project_id

    return ret


async def list_(hub, ctx, **kwargs) -> dict[str, Any]:
    """
    Gets a list of protected branches from a project
    as they are defined in the UI. If a wildcard is set, it is returned instead of the exact name
    of the branches that match that wildcard.


    Returns:
        dict[str, Any]

    Examples:

        Resource State:

        .. code-block:: sls

            unmanaged_resources:
              exec.run:
                - path: gitlab.project.protected_branch.list


        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.protected_branch.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe gitlab.project.protected_branch
    """

    result = dict(ret=[], result=True, comment=[])

    async for project in hub.tool.gitlab.request.paginate(
        ctx, url=f"{ctx.acct.endpoint_url}/projects", **kwargs
    ):
        project_id = project.id
        async for ret in hub.tool.gitlab.request.paginate(
            ctx,
            url=f"{ctx.acct.endpoint_url}/projects/{project_id}/protected_branches",
            **kwargs,
        ):
            resource = hub.tool.gitlab.project.protected_branch.raw_to_present(ret)
            resource["project_id"] = project_id
            result["ret"].append(resource)

    return result


async def create(
    hub,
    ctx,
    resource_id: str,
    *,
    project_id: int,
    name: str = None,
    allow_force_push: bool = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Returns:
        dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              gitlab.project.protected_branch.present:
                -

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.protected_branch.create
    """

    data = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "resource_id", "project_id", "name")
    }
    data["name"] = resource_id or name
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "post",
        success_codes=[201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/projects/{project_id}/protected_branches",
        data=data,
    )
    if ret.result:
        ret.ret = hub.tool.gitlab.project.protected_branch.raw_to_present(ret.ret)
        ret.ret["project_id"] = project_id
    return ret


async def update(
    hub, ctx, resource_id: str, *, project_id: int, **kwargs
) -> dict[str, Any]:
    """

    Returns:
        dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              gitlab.project.protected_branch.present:
                -

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.protected_branch.update
    """

    ret = await hub.tool.gitlab.request.json(
        ctx,
        "patch",
        url=f"{ctx.acct.endpoint_url}/projects/{project_id}/protected_branches/{resource_id}",
        success_codes=[200, 204, 304],
        data=kwargs,
    )
    return ret


async def delete(
    hub, ctx, resource_id: str, *, project_id: int, **kwargs
) -> dict[str, Any]:
    """

    Returns:
        dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              gitlab.project.protected_branch.absent:
                - resource_id: value
                - project_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.protected_branch.delete <resource_id> project_id=<valaue>
    """

    ret = await hub.tool.gitlab.request.json(
        ctx,
        "delete",
        url=f"{ctx.acct.endpoint_url}/projects/{project_id}/protected_branches/{resource_id}",
        success_codes=[202, 204, 404],
        data={},
    )
    return ret
