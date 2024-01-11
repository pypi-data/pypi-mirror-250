async def get(hub, ctx, **kwargs) -> dict[str, any]:
    """
    Test the credentials by doing the most basic authenticated call

    Examples:
        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.version.get
    """
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "get",
        url=f"{ctx.acct.endpoint_url}/version",
        success_codes=[200],
    )
    ret.result = ret.result and "version" in ret.ret

    return ret
