from urllib.parse import urlparse


DEFAULT_API_VERSION = "v4"
DEFAULT_ENDPOINT_URL = "https://gitlab.com"


async def profile(hub, ctx: dict[str, any], headers: dict[str, any]):
    """
    Each acct plugin creates the appropriate header.
    This function standardizes some other options that can be added to the headers
    """
    if "sudo" in ctx:
        headers["Sudo"] = ctx["sudo"]

    # Default to only showing owned items
    ctx["owned"] = str(ctx.get("owned", True)).lower()
    ctx["headers"] = headers


def endpoint_url(hub, ctx):
    """
    Ensure that the ctx contains an endpoint_url
    """
    # Break the url up into the base, which can be used for oauth tokens, and the full endpoint based on api version
    parsed_url = urlparse(ctx.get("endpoint_url", DEFAULT_ENDPOINT_URL))
    ctx["base_url"] = parsed_url.scheme + "://" + parsed_url.netloc

    api_version = ctx.get("api_version", DEFAULT_API_VERSION)
    ctx["endpoint_url"] = f"{ctx['base_url']}/api/{api_version}"
