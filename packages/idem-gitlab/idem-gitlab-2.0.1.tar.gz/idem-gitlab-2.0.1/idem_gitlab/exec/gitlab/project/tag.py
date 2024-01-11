"""Exec module for managing Project Tags. Tags"""
from typing import Any

__contracts__ = ["auto_state"]

__func_alias__ = {"list_": "list"}

TREQ = {
    "present": {
        "require": [
            "gitlab.project.commit.present",
            "gitlab.project.branch.present",
        ]
    },
}


async def get(
    hub, ctx, resource_id: str, *, project_id: int, **kwargs
) -> dict[str, Any]:
    """
    Parameters:

    Args:
        resource_id(str):
             unique ID.

        project_id(int):
            The ID or URL-encoded path of the project owned by the authenticated user.

    Returns:
        dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            unmanaged_resource:
              exec.run:
                - path: gitlab.project.tag.get
                - kwargs:
                  resource_id: value
                  project_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.tag.get resource_id=value, project_id=value
    """
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "get",
        success_codes=[200, 201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/projects/{project_id}/repository/tags/{resource_id}",
        data=kwargs,
    )
    if ret.result and ret.ret:
        ret.ret["project_id"] = project_id
        ret.ret = hub.tool.gitlab.project.tag.raw_to_present(ret.ret)
    return ret


async def list_(hub, ctx, **kwargs) -> dict[str, Any]:
    """
    Parameters:


    Args:
        project_id(int):
            The ID or URL-encoded path of the project owned by the authenticated user.

    Returns:
        dict[str, Any]

    Examples:

        Resource State:

        .. code-block:: sls

            unmanaged_resources:
              exec.run:
                - path: gitlab.project.tag.list

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.tag.list project_id=value

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe gitlab.project.tag
    """
    result = dict(ret=[], result=True, comment=[])

    async for project in hub.tool.gitlab.request.paginate(
        ctx, url=f"{ctx.acct.endpoint_url}/projects", **kwargs
    ):
        project_id = project.id
        async for ret in hub.tool.gitlab.request.paginate(
            ctx,
            url=f"{ctx.acct.endpoint_url}/projects/{project_id}/repository/tags",
            **kwargs,
        ):
            ret["project_id"] = project_id
            resource = hub.tool.gitlab.project.tag.raw_to_present(ret)
            result["ret"].append(resource)

    return result


async def create(
    hub,
    ctx,
    resource_id: str,
    *,
    project_id: int,
    target: str = None,
    message: str = None,
    protected: bool = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Args:
        resource_id(str):
            The name of a tag.

        project_id(int):
            The ID or URL-encoded path of the project owned by the authenticated user.

        target(str):
            Create a tag from a commit SHA or branch name.

        message(str, Optional):
            Create an annotated tag. Defaults to None.

        kwargs(dict, Optional):
            Any keyword arguments to be passed as data to the resource. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              gitlab.project.tag.present:
                - resource_id: value
                - project_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.tag.create resource_id=value, project_id=value
    """
    data = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "resource_id", "target")
    }

    # Normalize the target, if none was provided, get the most recent
    data["target"] = (
        await hub.exec.gitlab.project.commit.get(ctx, target, project_id=project_id)
    ).ret.resource_id

    data["ref"] = target
    data["tag_name"] = resource_id
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "post",
        success_codes=[201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/projects/{project_id}/repository/tags",
        data=data,
    )
    if ret.result:
        ret.ret["project_id"] = project_id
        ret.ret = hub.tool.gitlab.project.tag.raw_to_present(ret.ret)
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
              gitlab.project.tag.present:
                - resource_id: value
                - project_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.tag.update
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

    # If the message or branch id didn't change, then we don't want to recreate a tag
    if (
        all(ctx.old_state.get(key) == kwargs.get(key) for key in kwargs)
        and before_branch_id == new_branch_id
    ):
        return dict(result=True, ret=None, comment=[])

    # There is no update for tags, so we delete and recreate it
    get_ret = await hub.exec.gitlab.project.tag.get(
        ctx, resource_id=resource_id, project_id=project_id
    )
    if get_ret.result:
        delete_ret = await hub.exec.gitlab.project.tag.delete(
            ctx, resource_id=resource_id, project_id=project_id, **kwargs
        )
        if not delete_ret.result:
            return delete_ret

    create_ret = await hub.exec.gitlab.project.tag.create(
        ctx, resource_id=resource_id, project_id=project_id, **kwargs
    )
    return create_ret


async def delete(
    hub, ctx, resource_id: str, project_id: int, **kwargs
) -> dict[str, Any]:
    """
    Parameters:


    Args:
        resource_id(str):
            The name of a tag.

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
              gitlab.project.tag.absent:
                - resource_id: value
                - project_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.tag.delete resource_id=value, project_id=value
    """
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "delete",
        url=f"{ctx.acct.endpoint_url}/projects/{project_id}/repository/tags/{resource_id}",
        success_codes=[202, 204, 404],
    )
    return ret
