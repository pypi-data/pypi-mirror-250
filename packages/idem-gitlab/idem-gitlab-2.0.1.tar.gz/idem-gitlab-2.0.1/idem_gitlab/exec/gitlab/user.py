"""Exec module for managing Users."""
import uuid
from typing import Any

__contracts__ = ["auto_state"]

__func_alias__ = {"list_": "list"}


async def get(hub, ctx, resource_id: str, **kwargs) -> dict[str, Any]:
    """
    You can use all parameters available for everyone plus these additional parameters available only for administrators.

    If no resource_id is given, return the details of the currently authenticated user.

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
                - path: gitlab.user.get
                - kwargs:
                  resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.user.get resource_id=value
    """
    if resource_id:
        ret = await hub.tool.gitlab.request.json(
            ctx,
            "get",
            success_codes=[200, 201, 304, 204],
            url=f"{ctx.acct.endpoint_url}/users/{resource_id}",
            data=kwargs,
        )
    else:
        ret = await hub.tool.gitlab.request.json(
            ctx,
            "get",
            success_codes=[200, 201, 304, 204],
            url=f"{ctx.acct.endpoint_url}/user",
            data=kwargs,
        )

    if ret.ret["state"] == "blocked":
        ret.result = False
        ret.ret = None
    else:
        ret.ret = hub.tool.gitlab.standalone.user.raw_to_present(ret.ret)

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
                - path: gitlab.user.list

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.user.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe gitlab.user

    """
    result = dict(ret=[], result=True, comment=[])

    async for ret in hub.tool.gitlab.request.paginate(
        ctx, url=f"{ctx.acct.endpoint_url}/users", **kwargs
    ):
        resource = hub.tool.gitlab.standalone.user.raw_to_present(ret)
        result["ret"].append(resource)

    return result


async def create(
    hub,
    ctx,
    resource_id: str = None,
    *,
    name: str = None,
    email: str,
    username: str = None,
    admin: bool = None,
    auditor: bool = None,
    bio: str = None,
    can_create_group: bool = None,
    color_scheme_id: int = None,
    extern_uid: str = None,
    external: bool = None,
    extra_shared_runners_minutes_limit: int = None,
    group_id_for_saml: int = None,
    linkedin: bool = None,
    location: str = None,
    note: str = None,
    organization: str = None,
    password: str = None,
    private_profile: bool = None,
    project_limit: int = None,
    provider: str = None,
    shared_runners_minutes_limit: bool = None,
    skip_confirmation: bool = None,
    skype: str = None,
    theme_id: int = None,
    discord: str = None,
    view_diffs_file_by_file: bool = None,
    website_url: str = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Args:
        resource_id(str):
            A unique identifier for the resource.

        name(str):
            The user's name

        email(str):
            The user's email address

        username(str):
            The user's username

        admin(bool, Optional):
            User is an administrator. Valid values are true or false. Defaults to false.

        auditor(bool, Optional):
            User is an auditor. Valid values are true or false. Defaults to false.

        bio (str, Optional)
            User’s biography

        can_create_group(bool, Optional):
            User can create top-level groups - true or false

        color_scheme_id(int, Optional):
            User’s color scheme for the file viewer.

        extern_uid(str, Optional):
            External UID

        external(bool, Optional):
            Flags the user as external - true or false (default)

        extra_shared_runners_minutes_limit(int):
            Can be set by administrators only. Additional compute minutes for this user.

        group_id_for_saml(int):
                ID of group where SAML has been configured

        linkedin(bool):
            LinkedIn

        location(str):
            User’s location

        note(str):
            Administrator notes for this user

        organization(str):
            Organization name

        password(str):
            Password

        private_profile(bool):
            User’s profile is private - true or false. The default value is determined by this setting.

        project_limit(int):
            Number of projects user can create

        provider(str):
            External provider name

        shared_runners_minutes_limit(bool):
            Can be set by administrators only.
            Maximum number of monthly compute minutes for this user.
            Can be nil (default; inherit system default), 0 (unlimited), or > 0.

        skip_confirmation(bool):
                Skip confirmation - true or false (default)

        skype(str):
            Skype ID

        theme_id(int):
            GitLab theme for the user

        discord(str):
            Discord account

        view_diffs_file_by_file(bool):
            Flag indicating the user sees only one file diff per page

        website_url(str):
            Website URL

        kwargs(dict, Optional):
            Any keyword arguments to be passed as data to the resource. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              gitlab.user.present:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.user.create resource_id=value
    """
    if not password:
        force_random_password = True  # noqa
        reset_password = True  # noqa

    if not name:
        name = email.split("@")[0].title().replace("_", " ")

    if not username:
        username = (
            name.lower().replace(" ", "_") + "_" + str(uuid.uuid4()).split("-")[0]
        )

    data = {k: v for k, v in locals().items() if k not in ("hub", "ctx", "resource_id")}

    ret = await hub.tool.gitlab.request.json(
        ctx,
        "post",
        success_codes=[201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/users",
        data=data,
    )

    if ret.result:
        ret.ret = hub.tool.gitlab.standalone.user.raw_to_present(ret.ret)
    else:
        ret.ret = {}
    return ret


async def update(hub, ctx, resource_id: str, **kwargs) -> dict[str, Any]:
    """
    Args:
        resource_id(str):
            A unique identifier for the resource.

        kwargs(dict, Optional):
            Any keyword arguments to be passed as data to the resource. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              gitlab.user.present:
                - resource_id: value
                - _: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.user.update resource_id=value, _=value
    """

    ret = await hub.tool.gitlab.request.json(
        ctx,
        "put",
        url=f"{ctx.acct.endpoint_url}/users/{resource_id}",
        success_codes=[200, 204, 304],
        data=dict(id=resource_id, **kwargs),
    )
    return ret


async def delete(
    hub,
    ctx,
    resource_id: str,
    hard_delete: bool = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Args:
        resource_id(str):
            ID of a user.

        kwargs(dict, Optional):
            Any keyword arguments to be passed as data to the resource. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              gitlab.user.absent:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.user.delete resource_id=value
    """

    ret = await hub.tool.gitlab.request.json(
        ctx,
        "delete",
        url=f"{ctx.acct.endpoint_url}/users/{resource_id}",
        success_codes=[202, 204, 404],
        data={"hard_delete": hard_delete},
    )
    return ret
