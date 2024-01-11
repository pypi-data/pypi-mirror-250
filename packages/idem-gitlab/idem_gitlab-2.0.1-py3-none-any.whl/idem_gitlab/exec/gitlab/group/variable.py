"""Exec module for managing Group Group Level Variables. Group-level variables"""
import re
from typing import Any
from typing import Literal

VALID_KEY = re.compile(r"^\w{1,255}$")

__contracts__ = ["auto_state"]

__func_alias__ = {"list_": "list"}


async def get(
    hub, ctx, resource_id: str, *, name: str = None, group_id: int, **kwargs
) -> dict[str, Any]:
    """
    Get list of a group’s variables.

    Args:
        resource_id(str):

        group_id(int):
            The ID of a group or URL-encoded path of the group. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            unmanaged_resource:
              exec.run:
                - path: gitlab.group.variable.get
                - kwargs:
                  resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.group.variable.get resource_id=value
    """

    data = {k: v for k, v in locals().items() if k not in ("hub", "ctx", "resource_id")}
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "get",
        success_codes=[200, 201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/groups/{group_id}/variables/{resource_id}",
        data=data,
    )
    if ret.result:
        ret.ret["name"] = name
        ret.ret["group_id"] = group_id
        ret.ret = hub.tool.gitlab.group.variable.raw_to_present(ret.ret)
    return ret


async def list_(hub, ctx, **kwargs) -> dict[str, Any]:
    """
    Get list of a group’s variables.

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
                - path: gitlab.group.variable.list
                - kwargs:

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.group.variable.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe gitlab.group.variable
    """

    result = dict(ret=[], result=True, comment=[])

    async for group in hub.tool.gitlab.request.paginate(
        ctx, url=f"{ctx.acct.endpoint_url}/groups", **kwargs
    ):
        group_id = group.id
        async for ret in hub.tool.gitlab.request.paginate(
            ctx, url=f"{ctx.acct.endpoint_url}/groups/{group_id}/variables", **kwargs
        ):
            ret["group_id"] = group_id
            resource = hub.tool.gitlab.group.variable.raw_to_present(ret)
            result["ret"].append(resource)

    return result


async def create(
    hub,
    ctx,
    resource_id: str,
    *,
    name: str = None,
    group_id: int,
    value: str,
    variable_type: Literal["env_var", "file"] = None,
    protected: bool = None,
    masked: bool = None,
    raw: bool = None,
    environment_scope: str = None,
    description: str = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Create a new variable.

    Args:
        resource_id(str):
            The key of a variable; must have no more than 255 characters; only A-Z, a-z, 0-9, and _ are allowed. Defaults to None.

        group_id(int, Optional):
            The ID of a group or URL-encoded path of the group. Defaults to None.

        value(str, Optional):
            The value of a variable. Defaults to None.

        variable_type(str, Optional):
            The type of a variable. Available types are: env_var (default) and file. Defaults to None.

        protected(bool, Optional):
            Whether the variable is protected. Defaults to None.

        masked(bool, Optional):
            Whether the variable is masked. Defaults to None.

        raw(bool, Optional):
            Whether the variable is treated as a raw string. Default: false. When true, variables in the value are not expanded. Defaults to None.

        environment_scope(str, Optional):
            The environment scope of a variable. Defaults to None.

        description(str, Optional):
            The description of the variable. Default: null. Defaults to None.

        kwargs(dict, Optional):
            Any keyword arguments to be passed as data to the resource. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              gitlab.group.variable.present:
                - resource_id: value
                - group_id: value
                - value: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.group.variable.create resource_id=value group_id=value
    """
    data = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "resource_id", "name", "group_id")
    }
    data["key"] = resource_id or name
    if not VALID_KEY.fullmatch(data["key"]):
        raise ValueError(
            "The key of a variable; must have no more than 255 characters; only A-Z, a-z, 0-9, and _ are allowed"
        )

    ret = await hub.tool.gitlab.request.json(
        ctx,
        "post",
        success_codes=[201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/groups/{group_id}/variables",
        data=data,
    )
    if ret.result:
        ret.ret["group_id"] = group_id
        ret.ret = hub.tool.gitlab.group.variable.raw_to_present(ret.ret)
    return ret


async def update(
    hub, ctx, resource_id: str, *, group_id: int, **kwargs
) -> dict[str, Any]:
    """
    Update a group’s variable.

    Args:
        resource_id(str):
            A unique identifier for the resource.

        group_id(int, Optional):
            The ID of a group or URL-encoded path of the group. Defaults to None.

        kwargs(dict, Optional):
            Any keyword arguments to be passed as data to the resource. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              gitlab.group.variable.present:
                - resource_id: value
                - group_id: value
                - value: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.group.variable.update resource_id=value
    """
    kwargs.pop("name", None)
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "put",
        url=f"{ctx.acct.endpoint_url}/groups/{group_id}/variables/{resource_id}",
        success_codes=[200, 204, 304],
        data=kwargs,
    )
    return ret


async def delete(
    hub, ctx, resource_id: str, *, group_id: int = None, **kwargs
) -> dict[str, Any]:
    """
    Remove a group’s variable.


    Args:
        resource_id(str):
            The key of a variable. Defaults to None.

        group_id(int, Optional):
            The ID of a group or URL-encoded path of the group. Defaults to None.

        kwargs(dict, Optional):
            Any keyword arguments to be passed as data to the resource. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              gitlab.group.variable.absent:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.group.variable.delete resource_id=value
    """

    ret = await hub.tool.gitlab.request.json(
        ctx,
        "delete",
        url=f"{ctx.acct.endpoint_url}/groups/{group_id}/variables/{resource_id}",
        success_codes=[202, 204, 404],
    )
    return ret
