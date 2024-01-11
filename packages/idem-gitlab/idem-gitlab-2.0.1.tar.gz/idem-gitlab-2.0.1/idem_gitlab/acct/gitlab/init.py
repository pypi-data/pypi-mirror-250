from typing import Any


async def gather(hub, profiles) -> dict[str, Any]:
    """
    Authenticate to gitlab using a personal access token or oauth token

    https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html

    Grant access to at least "api" for the access token

    Example:
    .. code-block:: yaml

        gitlab:
          profile_name:
            token: <personal_access_token>
            # Optional Parameters
            endpoint_url: https://gitlab.com
            sudo: <username or id>
            api_version: v4
            owned: True
    """
    sub_profiles = {}

    for profile, ctx in profiles.get("gitlab", {}).items():
        hub.tool.gitlab.acct.endpoint_url(ctx)
        # If the user already created headers, then work with that
        if "headers" in ctx:
            headers = ctx["headers"]
        else:
            headers = {"PRIVATE-TOKEN": ctx["token"]}
        await hub.tool.gitlab.acct.profile(ctx, headers)
        sub_profiles[profile] = ctx

    return sub_profiles
