"""Exec module for managing Project Branches. Branches"""
from typing import Any

__contracts__ = ["auto_state"]

__func_alias__ = {"list_": "list"}

TREQ = {
    "present": {
        "require": [
            "gitlab.project.commit.present",
        ]
    },
}


async def get(
    hub, ctx, resource_id: str, *, project_id: int, **kwargs
) -> dict[str, Any]:
    """

    Returns:
        dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            unmanaged_resource:
              exec.run:
                - path: gitlab.project.branch.get
                - kwargs:
                  - resource_id: value
                  - project_id: value


        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.branch.get <resource_id> project_id=<value>
    """

    ret = await hub.tool.gitlab.request.json(
        ctx,
        "get",
        success_codes=[200, 201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/projects/{project_id}/repository/branches/{resource_id}",
    )
    if ret.result:
        ret.ret = hub.tool.gitlab.project.branch.raw_to_present(ret.ret)
        ret.ret["project_id"] = project_id
    return ret


async def list_(
    hub,
    ctx,
    **kwargs,
) -> dict[str, Any]:
    """
    Args:

        kwargs(dict, Optional):
            Any keyword arguments to be passed as data to the resource. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:

        Resource State:

        .. code-block:: sls

            unmanaged_resources:
              exec.run:
                - path: gitlab.project.branch.list

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.branch.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe gitlab.project.branch
    """

    result = dict(ret=[], result=True, comment=[])

    async for project in hub.tool.gitlab.request.paginate(
        ctx, url=f"{ctx.acct.endpoint_url}/projects", **kwargs
    ):
        project_id = project.id
        async for ret in hub.tool.gitlab.request.paginate(
            ctx,
            url=f"{ctx.acct.endpoint_url}/projects/{project_id}/repository/branches",
            **kwargs,
        ):
            resource = hub.tool.gitlab.project.branch.raw_to_present(ret)
            resource["project_id"] = project_id
            result["ret"].append(resource)

    return result


async def create(
    hub, ctx, resource_id: str, *, name: str = None, target: str = None, project_id: int
) -> dict[str, Any]:
    """
    Args:
        resource_id(str):
            The name of the branch.

        project_id(int):
            The ID or URL-encoded path of the project owned by the authenticated user.

        target(str):
            Create a branch from a commit SHA.

        kwargs(dict, Optional):
            Any keyword arguments to be passed as data to the resource. Defaults to None.
    Returns:
        dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              gitlab.project.branch.present:
                -

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.branch.create
    """

    data = dict(
        branch=resource_id or name,
        ref=(
            await hub.exec.gitlab.project.commit.get(ctx, target, project_id=project_id)
        ).ret.resource_id,
    )
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "post",
        success_codes=[201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/projects/{project_id}/repository/branches",
        data=data,
    )
    if ret.result:
        ret.ret = hub.tool.gitlab.project.branch.raw_to_present(ret.ret)
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
              gitlab.project.branch.present:
                -

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.branch.update
    """
    # Normalize the branch name, or sha to be a commit id
    before_branch_id = (
        await hub.exec.gitlab.project.commit.get(
            ctx, ctx.old_state.get("target"), project_id=project_id
        )
    ).ret.resource_id
    new_branch_id = (
        await hub.exec.gitlab.project.commit.get(
            ctx, kwargs.get("target"), project_id=project_id
        )
    ).ret.resource_id

    # If the message or branch id didn't change, then we don't want to recreate a branch
    if before_branch_id == new_branch_id:
        return dict(result=True, ret=None, comment=[])

    # There is no update for branches, so we delete and recreate it
    get_ret = await hub.exec.gitlab.project.branch.get(
        ctx, resource_id=resource_id, project_id=project_id
    )
    if get_ret.result:
        delete_ret = await hub.exec.gitlab.project.branch.delete(
            ctx, resource_id=resource_id, project_id=project_id, **kwargs
        )
        if not delete_ret.result:
            return delete_ret

    create_ret = await hub.exec.gitlab.project.branch.create(
        ctx, resource_id=resource_id, project_id=project_id, **kwargs
    )
    return create_ret


async def delete(
    hub,
    ctx,
    resource_id: str,
    *,
    project_id: int,
    **kwargs,
) -> dict[str, Any]:
    """
    Parameters:


    Args:
        resource_id(str):
            A unique identifier for the resource.

        project_id(int):
            ID or URL-encoded path of the project owned by the authenticated user.

        branch(str):
            Name of the branch.

        kwargs(dict, Optional):
            Any keyword arguments to be passed as data to the resource. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              gitlab.project.branch.absent:
                - resource_id: value
                - project_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.branch.delete resource_id=value, project_id=value, branch=value, _=value
    """

    ret = await hub.tool.gitlab.request.json(
        ctx,
        "delete",
        url=f"{ctx.acct.endpoint_url}/projects/{project_id}/repository/branches/{resource_id}",
        success_codes=[202, 204, 404],
    )
    return ret
