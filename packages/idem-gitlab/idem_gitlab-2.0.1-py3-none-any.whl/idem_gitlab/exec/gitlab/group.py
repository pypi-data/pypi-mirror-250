"""Exec module for managing Groups."""
from typing import Any
from typing import Literal

from dict_tools.typing import Computed

__contracts__ = ["auto_state"]

__func_alias__ = {"list_": "list"}

TREQ = {
    "present": {"require": ["gitlab.group.subscription.present"]},
}


async def get(hub, ctx, resource_id: str, **kwargs) -> dict[str, Any]:
    """
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
                - path: gitlab.group.get
                - kwargs:
                  resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.group.get resource_id=value
    """
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "get",
        success_codes=[200, 201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/groups/{resource_id}",
    )

    if ret.status == 404:
        ret.ret = {}
    else:
        ret.ret = hub.tool.gitlab.group.group.raw_to_present(ret.ret)

    return ret


async def list_(hub, ctx, **kwargs) -> dict[str, Any]:
    """
    Parameters:

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
                - path: gitlab.group.list
                - kwargs:

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.group.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe gitlab.group

    """
    result = dict(ret=[], result=True, comment=[])

    async for ret in hub.tool.gitlab.request.paginate(
        ctx, url=f"{ctx.acct.endpoint_url}/groups", **kwargs
    ):
        resource = hub.tool.gitlab.group.group.raw_to_present(ret)
        result["ret"].append(resource)

        # Find all sub_groups recursively under this one
        async for ret in hub.tool.gitlab.request.paginate(
            ctx,
            url=f"{ctx.acct.endpoint_url}/groups/{resource['resource_id']}/subgroups",
            **kwargs,
        ):
            resource = hub.tool.gitlab.group.group.raw_to_present(ret)
            result["ret"].append(resource)

    return result


async def create(
    hub,
    ctx,
    resource_id: str = None,
    *,
    name: str = None,
    path: str = None,
    auto_devops_enabled: bool = None,
    avatar: str = None,
    default_branch_protection: int = None,
    description: str = None,
    emails_enabled: bool = None,
    lfs_enabled: bool = None,
    mentions_disabled: bool = None,
    parent_id: int = None,
    project_creation_level: Literal["noone", "maintainer", "developer"] = None,
    request_access_enabled: bool = None,
    require_two_factor_authentication: bool = None,
    share_with_group_lock: bool = None,
    subgroup_creation_level: Literal["owner", "maintainer"] = None,
    two_factor_grace_period: int = None,
    visibility: Literal["private", "internal", "public"] = None,
    membership_lock: bool = None,
    extra_shared_runners_minutes_limit: int = None,
    shared_runners_minutes_limit: int = None,
    wiki_access_level: Literal["disabled", "private", "enabled"] = None,
    full_path: Computed[str] = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Args:
        resource_id(str):
            A unique identifier for the resource.

        name(str):
            The name of the group.

        path(str):
            The path of the group.

        auto_devops_enabled(bool, Optional):
            Default to Auto DevOps pipeline for all projects within this group. Defaults to None.

        avatar(str, Optional):
            Image file for avatar of the group. Introduced in GitLab 12.9. Defaults to None.

        default_branch_protection(int, Optional):
            See Options for default_branch_protection. Default to the global level default branch protection setting. Defaults to None.

        description(str, Optional):
            The group’s description. Defaults to None.

        emails_enabled(bool, Optional):
            Enable email notifications. Defaults to None.

        lfs_enabled(bool, Optional):
            Enable/disable Large File Storage (LFS) for the projects in this group. Defaults to None.

        mentions_disabled(bool, Optional):
            Disable the capability of a group from getting mentioned. Defaults to None.

        parent_id(int, Optional):
            The parent group ID for creating nested group. Defaults to None.

        project_creation_level(str, Optional):
            Determine if developers can create projects in the group.
            Can be noone (No one), maintainer (users with the Maintainer role), or developer (users with the Developer or Maintainer role). Defaults to None.

        request_access_enabled(bool, Optional):
            Allow users to request member access. Defaults to None.

        require_two_factor_authentication(bool, Optional):
            Require all users in this group to setup Two-factor authentication. Defaults to None.

        share_with_group_lock(bool, Optional):
            Prevent sharing a project with another group within this group. Defaults to None.

        subgroup_creation_level(str, Optional):
            Allowed to create subgroups. Can be owner (Owners), or maintainer (users with the Maintainer role). Defaults to None.

        two_factor_grace_period(int, Optional):
            Time before Two-factor authentication is enforced (in hours). Defaults to None.

        visibility(str, Optional):
            The group’s visibility. Can be private, internal, or public. Defaults to None.

        membership_lock(bool, Optional):
            Users cannot be added to projects in this group. Defaults to None.

        extra_shared_runners_minutes_limit(int, Optional):
            Can be set by administrators only. Additional compute minutes for this group. Defaults to None.

        shared_runners_minutes_limit(int, Optional):
            Can be set by administrators only. Maximum number of monthly compute minutes for this group. Can be nil (default; inherit system default), 0 (unlimited), or > 0. Defaults to None.

        wiki_access_level(str, Optional):
            The wiki access level. Can be disabled, private, or enabled. Defaults to None.

        kwargs(dict, Optional):
            Arguments that are ignored

    Returns:
        dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              gitlab.group.present:
                - resource_id: value
                - name: value
                - path: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.group.create name=value path=value
    """
    if name and not path:
        path = name
    elif path and not name:
        name = path
    data = {k: v for k, v in locals().items() if k not in ("hub", "ctx", "resource_id")}
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "post",
        success_codes=[201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/groups",
        data=data,
    )
    ret.ret = hub.tool.gitlab.group.group.raw_to_present(ret.ret)
    return ret


async def update(
    hub,
    ctx,
    resource_id: str,
    *,
    parent_id: str = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Updates the project group. Only available to group owners and administrators.


    Args:
        resource_id(str):
            A unique identifier for the resource.

    Returns:
        dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              gitlab.group.present:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.group.update resource_id=value
    """
    if parent_id != ctx.old_state.get("parent_id"):
        old_parent_id = ctx.old_state.get("parent_id")
        ret = await hub.tool.gitlab.request.json(
            ctx,
            "put",
            url=f"{ctx.acct.endpoint_url}/groups/{resource_id}/transfer",
            success_codes=[200, 204, 304],
            data=dict(group_id=parent_id),
        )
        if ret.result:
            if parent_id and old_parent_id:
                # This was a group transfer
                ret.comment.append(
                    f"Group {resource_id} transferd from subgroup {old_parent_id} to {parent_id}"
                )
            elif old_parent_id:
                # The sub_group was converted to top-level
                ret.comment.append(
                    f"Group {resource_id} moved from {old_parent_id} to top-level"
                )
            else:
                # The sub_group was moved from top-level to a new sub group
                ret.comment.append(
                    f"Group {resource_id} moved from top-level to {parent_id}"
                )
        return ret

    ret = await hub.tool.gitlab.request.json(
        ctx,
        "put",
        url=f"{ctx.acct.endpoint_url}/groups/{resource_id}",
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
    name: str = None,
    permanently_remove: str = None,
    full_path: str = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Parameters:

    Args:
        resource_id(str):
            A unique identifier for the resource.

        name(str):
            Idem's identifier for the resource

        permanently_remove(str, Optional):
            Immediately deletes a subgroup if it is marked for deletion. Introduced in GitLab 15.4. Defaults to None.

        full_path(str, Optional):
            Full path of subgroup to use with permanently_remove. Introduced in GitLab 15.4. To find the subgroup path, see the group details. Defaults to None.

        kwargs(dict, Optional):
            Arguments that are ignored

    Returns:
        dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              gitlab.group.absent:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.group.delete resource_id=value, project_id=value, _=value
    """
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "delete",
        url=f"{ctx.acct.endpoint_url}/groups/{resource_id}",
        success_codes=[202, 204, 404],
        data={
            "id": resource_id,
            "permanently_remove": permanently_remove,
            "full_path": full_path,
        },
    )
    return ret
