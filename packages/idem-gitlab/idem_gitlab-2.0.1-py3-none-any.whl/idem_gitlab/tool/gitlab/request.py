import asyncio
import json
import re
from collections.abc import AsyncGenerator
from typing import Any
from typing import Literal

__func_alias__ = {"json_": "json"}

NEXT_RESOURCE_URL = re.compile(r'<([^>]+)>; rel="next"')


async def paginate(hub, ctx, url: str, **kwargs) -> AsyncGenerator:
    """
    Paginate items from the given gitlab url when running list commands
    """
    params = kwargs.copy()

    params.update({"per_page": 20, "owned": ctx.acct.owned})

    # Recursively perform list operations until we have collected all of them.
    while url:
        ret = await hub.exec.request.json.get(
            ctx,
            url=url,
            params=params,
            success_codes=[200],
        )
        if not ret["result"]:
            if "RateLimit-Remaining" in ret["headers"]:
                rate_limit = int(ret["headers"].get("RateLimit-Remaining", 0))
                if not rate_limit:
                    # try again, the failure was because of rate limits
                    delay = int(ret["headers"].get("Retry-After", 0))
                    hub.log.debug(f"Waiting for rate limit to expire: {delay}")
                    await asyncio.sleep(delay)
                    continue
            # It was a plain failure
            return
        for result in ret["ret"]:
            yield result

        # Extract the URL for the next page of resources
        link = ret["headers"].get("Link", "")
        match = NEXT_RESOURCE_URL.search(link)
        if match:
            url = match.group(1)
        else:
            # No more "next" pages, end iteration
            return


async def first_owned(hub, ctx, url: str, **kwargs) -> dict[str, any]:
    """
    Run a list operation but return only the first owned item.
    This is how we get user defaults
    """
    params = kwargs.copy()

    params.update({"per_page": 1, "owned": "true"})

    ret = await hub.exec.request.json.get(
        ctx,
        url=url,
        params=params,
        success_codes=[200],
    )
    return ret


async def json_(
    hub,
    ctx,
    request_type: Literal["get", "post", "put", "delete"],
    data: dict[str, Any] = None,
    params: dict[str, Any] = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Perform a request and assume that the result is json and decode it
    since gitlab doesn't return a proper content-type header.

    Args:
        hub (_type_):
        ctx (_type_):
        request_type (str): "get", "post", "put", "delete"

    Returns:
        dict[str, Any]: The raw output of the command from idem-aiohttp as parsed JSON
    """
    new_params = {}
    if params:
        for key, value in params.items():
            if value is None:
                continue
            else:
                new_params[key] = value
        kwargs["params"] = new_params

    new_data = {}

    # Perform some sanitization on
    if data:
        for key, value in data.items():
            # Remove "None" values from data
            if value is None:
                continue
            # Cast boolean values as strings
            if isinstance(value, bool):
                new_data[key] = str(value).lower()
            else:
                new_data[key] = value
        kwargs["json"] = new_data

    # Pass the request on to idem-aiohttp
    ret = await hub.exec.request.raw[request_type](ctx, **kwargs)
    # Remove unserializable headers
    ret.pop("headers", None)

    # Make sure that the comment is a list per idem convention
    if isinstance(ret.comment, str):
        ret.comment = [ret.comment]

    # Decode the return of the request
    if isinstance(ret.ret, bytes):
        ret.ret = ret.ret.decode()

    if not ret.ret:
        ret.ret = "{}"
    try:
        ret.ret = json.loads(ret.ret)

        # Usually the JSON return contains attributes of a resource
        # If there were other things like errors or a message, add it to the comments
        if "error" in ret.ret:
            error_message = ret.ret.pop("error")
            hub.tool.idem.comment.append(ret["comment"], error_message)
        if "message" in ret.ret:
            message = ret.ret.pop("message")
            hub.tool.idem.comment.append(ret["comment"], message)

    except json.JSONDecodeError as e:
        ret.result = False

        # If idem was run with the "--hard-fail" flag then provide a traceback here
        if hub.OPT.idem.get("hard_fail"):
            raise

    return ret
