import json
from typing import Any

from dict_tools.data import NamespaceDict


async def gather(hub, profiles) -> dict[str, Any]:
    """
    Get a temporary access token based on a username and password.

    Example:
    .. code-block:: yaml

        gitlab.login:
          profile_name:
            endpoint_url: https://gitlab.com
            username: user@example.com
            password: secret
            # Optional Parameters
            sudo: <username or id>
            api_version: v4
            owned: True
    """
    sub_profiles = {}

    for profile, ctx in profiles.get("gitlab.login", {}).items():
        hub.tool.gitlab.acct.endpoint_url(ctx)

        # Create a temporary ctx just to be used to get an oauth token
        temp_ctx = NamespaceDict(acct={})

        try:
            ret = await hub.exec.request.raw.post(
                temp_ctx,
                url=f"{ctx['base_url']}/oauth/token",
                data={
                    "username": ctx["username"],
                    "password": ctx["password"],
                    "grant_type": "password",
                },
            )
        except Exception as e:
            hub.log.error(f"{e.__class__.__name__}: {e}")
            continue

        if not ret["result"]:
            hub.log.error(f"Unable to authenticate gitlab user: {ctx['username']}")
            continue

        ret_data = json.loads(ret.ret)
        token = ret_data["access_token"]

        headers = {"Authorization": f"Bearer {token}"}
        await hub.tool.gitlab.acct.profile(ctx, headers)
        sub_profiles[profile] = ctx
    return sub_profiles
