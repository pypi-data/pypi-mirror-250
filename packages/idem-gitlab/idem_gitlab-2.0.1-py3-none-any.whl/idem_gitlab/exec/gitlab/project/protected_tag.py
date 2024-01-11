"""Exec module for managing Project Protected Tags. Protected tags"""
from typing import Any

__contracts__ = ["auto_state"]

__func_alias__ = {"list_": "list"}


async def get(
    hub, ctx, resource_id: str, *, project_id: int, **kwargs
) -> dict[str, Any]:
    """
    Gets a list of protected tags from a project.
    This function takes pagination parameters page and per_page to restrict the list of protected tags.

    Args:
        resource_id(str):
            The name of the tag or wildcard

        project_id(int):
            The ID or URL-encoded path of the project owned by the authenticated user.

    Returns:
        dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            unmanaged_resource:
              exec.run:
                - path: gitlab.project.protected_tag.get
                - kwargs:
                  resource_id: value
                  project_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.protected_tag.get resource_id=value, project_id=value
    """
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "get",
        success_codes=[200, 201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/projects/{project_id}/protected_tags/{resource_id}",
    )
    if ret.result:
        ret.ret["project_id"] = project_id
        ret.ret = hub.tool.gitlab.project.protected_tag.raw_to_present(ret.ret)
    return ret


async def list_(hub, ctx, **kwargs) -> dict[str, Any]:
    """
    Gets a list of protected tags from a project.
    This function takes pagination parameters page and per_page to restrict the list of protected tags.

    Returns:
        dict[str, Any]

    Examples:

        Resource State:

        .. code-block:: sls

            unmanaged_resources:
              exec.run:
                - path: gitlab.project.protected_tag.list
                - kwargs:

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.protected_tag.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe gitlab.project.protected_tag
    """
    result = dict(ret=[], result=True, comment=[])

    async for project in hub.tool.gitlab.request.paginate(
        ctx, url=f"{ctx.acct.endpoint_url}/projects", **kwargs
    ):
        project_id = project.id
        async for ret in hub.tool.gitlab.request.paginate(
            ctx,
            url=f"{ctx.acct.endpoint_url}/projects/{project_id}/protected_tags",
            **kwargs,
        ):
            resource = hub.tool.gitlab.project.protected_tag.raw_to_present(ret)
            resource["project_id"] = project_id
            result["ret"].append(resource)

    return result


async def create(
    hub, ctx, resource_id: str, *, project_id: bool, create_access_level: int = None
) -> dict[str, Any]:
    """

    Returns:
        dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              gitlab.project.protected_tag.present:
                - resource_id: v*
                - create_access_level: 40
                - project_id: 1231234

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.protected_tag.create "v*" project_id=1234
    """
    data = dict(
        name=resource_id,
        create_access_level=create_access_level,
    )
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "post",
        success_codes=[201, 304, 204, 422],
        url=f"{ctx.acct.endpoint_url}/projects/{project_id}/protected_tags",
        data=data,
    )
    if ret.result:
        ret.ret = hub.tool.gitlab.project.protected_tag.raw_to_present(ret.ret)
        ret.ret["project_id"] = project_id
        ret.ret["resource_id"] = resource_id
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
              gitlab.project.protected_tag.present:
                -

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.protected_tag.update
    """
    # Only perform an update if anything changed
    if all(ctx.old_state.get(key) == kwargs.get(key) for key in kwargs):
        return dict(result=True, ret=None, comment=[])

    # There is no update for protected tags, so we delete and recreate it
    get_ret = await hub.exec.gitlab.project.protected_tag.get(
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
    hub, ctx, resource_id: str, *, project_id: int, **kwargs
) -> dict[str, Any]:
    """

    Returns:
        dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              gitlab.project.protected_tag.absent:
                -

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.protected_tag.delete
    """
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "delete",
        url=f"{ctx.acct.endpoint_url}/projects/{project_id}/protected_tags/{resource_id}",
        success_codes=[202, 204, 404],
    )
    return ret
