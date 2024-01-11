async def get(hub, ctx, email: str, size: int = None, **kwargs) -> dict[str, any]:
    """
    Test the credentials by doing the most basic authenticated call

    Examples:
        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.avatar.get email="email@example.com"
    """
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "get",
        url=f"{ctx.acct.endpoint_url}/avatar",
        params={"email": email, "size": size},
        success_codes=[200],
    )
    ret.result = ret.result and "avatar_url" in ret.ret

    return ret
