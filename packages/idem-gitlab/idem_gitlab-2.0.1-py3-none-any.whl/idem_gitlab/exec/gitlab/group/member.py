"""Exec module for managing Group Members. Members"""
from typing import Any

__contracts__ = ["auto_state"]

__func_alias__ = {"list_": "list"}


async def get(
    hub, ctx, resource_id: str, *, group_id: int = None, user_id: int = None, **kwargs
) -> dict[str, Any]:
    """
    This function takes pagination parameters page and per_page to restrict the list of users.

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
                - path: gitlab.group.member.get
                - kwargs:
                  resource_id: value
                  group_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.group.member.get resource_id=value group_id=value
    """
    if not user_id and not group_id:
        group_id, user_id = resource_id.split("::", maxsplit=1)
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "get",
        success_codes=[200, 201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/groups/{group_id}/members/{user_id}",
    )
    if ret.result:
        ret.ret["group_id"] = group_id
        ret.ret = hub.tool.gitlab.group.member.raw_to_present(ret.ret)
    return ret


async def list_(
    hub,
    ctx,
    **kwargs,
) -> dict[str, Any]:
    """
    This function takes pagination parameters page and per_page to restrict the list of users.

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
                - path: gitlab.group.member.list
                - kwargs:

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.group.member.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe gitlab.group.member
    """
    result = dict(ret=[], result=True, comment=[])

    async for group in hub.tool.gitlab.request.paginate(
        ctx, url=f"{ctx.acct.endpoint_url}/groups", **kwargs
    ):
        group_id = group.id
        async for ret in hub.tool.gitlab.request.paginate(
            ctx, url=f"{ctx.acct.endpoint_url}/groups/{group_id}/members", **kwargs
        ):
            ret["group_id"] = group_id
            resource = hub.tool.gitlab.group.member.raw_to_present(ret)
            result["ret"].append(resource)

    return result


async def create(
    hub,
    ctx,
    resource_id: str = None,
    *,
    name: str = None,
    user_id: int = None,
    group_id: int = None,
    access_level: int,
    expires_at: str = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Adds a member to a group or project.

    Args:
        resource_id(str):
            The user ID of the new member or multiple IDs separated by commas.

        group_id(int):
            The ID or URL-encoded path of the group owned by the authenticated user.

        access_level(int):
            A valid access level.

        name(str, Optional):
            Full name of the user

        expires_at(str, Optional):
            A date string in the format YEAR-MONTH-DAY. Defaults to None.

        kwargs(dict, Optional):
            Any keyword arguments to be passed as data to the resource. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              gitlab.group.member.present:
                - resource_id: value
                - group_id: value
                - access_level: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.group.member.create resource_id=value group_id=value access_level=value
    """
    if not user_id and not group_id:
        group_id, user_id = resource_id.split("::", maxsplit=1)
    data = {k: v for k, v in locals().items() if k not in ("hub", "ctx", "resource_id")}
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "post",
        success_codes=[201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/groups/{group_id}/members",
        data=data,
    )
    ret.ret["group_id"] = group_id
    ret.ret = hub.tool.gitlab.group.member.raw_to_present(ret.ret)
    return ret


async def update(
    hub,
    ctx,
    resource_id: str,
    *,
    group_id: int = None,
    user_id: int = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Changes the membership state of a user in a group. The state is applied to
    all subgroups and projects.

    Args:
        kwargs(dict, Optional):
            Any keyword arguments to be passed as data to the resource. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              gitlab.group.member.present:
                - resource_id: value
                - project_id: value
                - state: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.group.member.update resource_id=value project_id=value state=value
    """
    if not user_id and not group_id:
        group_id, user_id = resource_id.split("::", maxsplit=1)
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "put",
        url=f"{ctx.acct.endpoint_url}/groups/{group_id}/members/{user_id}",
        success_codes=[200, 204, 304],
        params={"owned": ctx.acct.owned},
        data=kwargs,
    )
    return ret


async def delete(
    hub,
    ctx,
    resource_id: str,
    *,
    group_id: int = None,
    user_id: int = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Sets the override flag to false and allows LDAP Group Sync to reset the access
    level to the LDAP-prescribed value.


    Args:
        resource_id(str):
            The user ID of the member.
            A unique identifier for the resource.

        group_id(int):
            The ID or URL-encoded path of the group owned by the authenticated user.

        kwargs(dict, Optional):
            Any keyword arguments to be passed as data to the resource. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              gitlab.group.member.absent:
                - resource_id: value
                - group_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.group.member.delete resource_id=value group_id=value
    """
    if not user_id and not group_id:
        group_id, user_id = resource_id.split("::", maxsplit=1)

    ret = await hub.tool.gitlab.request.json(
        ctx,
        "delete",
        url=f"{ctx.acct.endpoint_url}/groups/{group_id}/members/{user_id}",
        success_codes=[202, 204, 404],
        data={},
    )

    return ret
