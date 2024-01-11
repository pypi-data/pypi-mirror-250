"""Utility functions for Project Protected Branches. Protected branches"""
from typing import Any


def raw_to_present(hub, resource: dict[str, Any]) -> dict[str, Any]:
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

    # There exists a unique integer id, but it is not useful
    resource.pop("id", None)

    clean_resource = {
        "resource_id": resource.pop("name"),
    }

    # Remove empty values
    clean_resource.update(
        {
            k: v
            for k, v in resource.items()
            if v is not None and not isinstance(v, dict) and not isinstance(v, list)
        }
    )
    return clean_resource
