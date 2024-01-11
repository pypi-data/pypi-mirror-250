import re
from typing import Any

__func_alias__ = {"type_": "type"}


def parse(hub, name: str, path: str, link: str, ref: str):
    clean_path = re.sub(
        r":(\w+)", lambda m: f"{{{hub.tool.format.keyword.unclash(m.group(1))}}}", path
    )
    # Gitlab defines path parameters as ":param", transform that into "{param}"
    functions: dict[str, Any] = hub.pop_create.gitlab.functions.parse(
        link, path, clean_path
    )
    if not functions:
        return {}

    match = re.match(r"(.+)/{(.+)}", clean_path)
    if match:
        short_list_path = match.group(1)
    else:
        short_list_path = ""

    shared_func_data = {
        "hardcoded": {
            "path": clean_path,
            "ref": ref,
            "short_list_path": short_list_path,
            "create_parameter": functions["create"].get("params", {}),
        },
    }

    # Fully define the plugin
    plugin = {
        "doc": name,
        "imports": [
            "from typing import *",
            "from dataclasses import make_dataclass",
        ],
        "func_alias": {"list_": "list"},
        "contracts": ["auto_state"],
        "functions": {
            "get": dict(
                doc=functions["get"].get("doc"),
                params=functions["get"].get("params", {}),
                **shared_func_data,
            ),
            "list": dict(
                doc=functions["list"].get("doc"),
                params=functions["delete"].get("params", {}),
                **shared_func_data,
            ),
            "create": dict(
                doc=functions["create"].get("doc"),
                params=functions["create"].get("params", {}),
                **shared_func_data,
            ),
            "update": dict(
                doc=functions["update"].get("doc"),
                params=functions["update"].get("params", {}),
                **shared_func_data,
            ),
            "delete": dict(
                doc=functions["delete"].get("doc"),
                params=functions["delete"].get("params", {}),
                **shared_func_data,
            ),
            "raw_to_present": dict(
                doc="Convert the raw output from the GitLab API to a version that conforms to idem conventions and can be used in present states.",
                params={"resource": hub.pop_create.gitlab.param.RESOURCE},
                **shared_func_data,
            ),
        },
    }
    return plugin
