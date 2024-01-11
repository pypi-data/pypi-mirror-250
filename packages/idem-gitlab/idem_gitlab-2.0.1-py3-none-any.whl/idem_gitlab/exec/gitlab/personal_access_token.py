"""Exec module for managing Personal Access Tokens."""
from typing import Any

__contracts__ = ["auto_state"]

__func_alias__ = {"list_": "list"}


async def get(hub, ctx, resource_id: str, **kwargs) -> dict[str, Any]:
    """
    You can use all parameters available for everyone plus these additional parameters available only for administrators.

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
                - path: gitlab.personal_access_token.get
                - kwargs:
                  resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.personal_access_token.get resource_id=value
    """
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "get",
        success_codes=[200, 201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/personal_access_tokens/{resource_id}",
        data=kwargs,
    )
    if ret.result:
        if ret.ret["revoked"] is True:
            ret.result = False
            ret.ret = None
        else:
            ret.ret = hub.tool.gitlab.standalone.personal_access_token.raw_to_present(
                ret.ret
            )
    return ret


async def list_(
    hub,
    ctx,
    **kwargs,
) -> dict[str, Any]:
    """
    This function takes pagination parameters page and per_page to restrict the list of personal access tokens.

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
                - path: gitlab.personal_access_token.list

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.personal_access_token.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe gitlab.personal_access_token

    """
    result = dict(ret=[], result=True, comment=[])

    async for ret in hub.tool.gitlab.request.paginate(
        ctx, url=f"{ctx.acct.endpoint_url}/personal_access_tokens", **kwargs
    ):
        resource = hub.tool.gitlab.standalone.personal_access_token.raw_to_present(ret)
        result["ret"].append(resource)

    return result


async def create(
    hub,
    ctx,
    resource_id: str = None,
    *,
    name: str,
    scopes: list[str],
    expires_at: str = None,
    user_id: str = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Args:
        resource_id(str):
            A unique identifier for the resource.

        name(str):
            The personal_access_token's name

        expires_at(str):
            Expiration date of the access token in ISO format(YYY-MM-DD).
            If no date is set, the expiration is set to the maximum allowable lifetime of an access token.

        scopes(list[str]):
            Array of scopes of the personal access token.

        kwargs(dict, Optional):
            Any keyword arguments to be passed as data to the resource. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              gitlab.personal_access_token.present:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.personal_access_token.create name="my_token" scopes=api
    """
    data = {k: v for k, v in locals().items() if k not in ("hub", "ctx", "resource_id")}

    # Get the currently authenticated user
    if user_id is None:
        user_ret = await hub.exec.gitlab.user.get(ctx, None)
        if not user_ret.result:
            return user_ret
        user_id = user_ret.ret.resource_id

    ret = await hub.tool.gitlab.request.json(
        ctx,
        "post",
        success_codes=[201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/users/{user_id}/personal_access_tokens",
        data=data,
    )

    if ret.result:
        ret.ret = hub.tool.gitlab.standalone.personal_access_token.raw_to_present(
            ret.ret
        )
    else:
        ret.ret = {}

    return ret


async def update(hub, ctx, resource_id: str, **kwargs) -> dict[str, Any]:
    """
    This is a no-op operation, you cannot update a personal_access_token
    """
    comments = []
    for key, value in kwargs.items():
        if ctx.old_state[key] != value:
            comments.append(
                f"Unable to update {key} of personal_access_token: {resource_id}"
            )
    return dict(result=True, ret={}, comment=comments)


async def delete(
    hub,
    ctx,
    resource_id: str,
    **kwargs,
) -> dict[str, Any]:
    """
    Revoke a personal access token

    Args:
        resource_id(str):
            ID of a personal_access_token.

        kwargs(dict, Optional):
            Any keyword arguments to be passed as data to the resource. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              gitlab.personal_access_token.absent:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.personal_access_token.delete resource_id=value
    """

    ret = await hub.tool.gitlab.request.json(
        ctx,
        "delete",
        url=f"{ctx.acct.endpoint_url}/personal_access_tokens/{resource_id}",
        success_codes=[200, 202, 204, 404],
    )
    return ret
