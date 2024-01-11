"""Utility functions for Project Runners. Runners"""
from typing import Any


async def raw_to_present(hub, ctx, resource: dict[str, Any]) -> dict[str, Any]:
    r"""

    Convert the raw output from the GitLab API to a version that conforms to idem conventions and can be used in present states.

    Args:
        resource(dict[str, Any]):
            None.

    Returns:
        dict[str, Any]

    """

    if not isinstance(resource, dict):
        raise TypeError(resource)

    clean_resource = {
        "resource_id": str(resource.pop("id")),
        "tags": resource.pop("tag_list", []),
        "type": resource.pop("runner_type").split("_type")[0],
        "shared": resource.pop("is_shared"),
        "projects": [project["id"] for project in resource.pop("projects", {})],
        "groups": [group["id"] for group in resource.pop("groups", {})],
    }

    # Remove empty values
    clean_resource.update(
        {k: v for k, v in resource.items() if v is not None and not isinstance(v, dict)}
    )
    return clean_resource
