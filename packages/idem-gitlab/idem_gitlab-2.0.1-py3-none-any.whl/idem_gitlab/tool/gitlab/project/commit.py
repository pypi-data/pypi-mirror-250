"""Utility functions for Project Commits. Commits"""
from typing import Any


def raw_to_present(hub, resource: dict[str, Any]) -> dict[str, Any]:
    r"""
    Convert the raw output from the GitLab API to a version that conforms to idem conventions and can be used in present states.

    Returns:
        dict[str, Any]

    """
    if not isinstance(resource, dict):
        raise TypeError(resource)

    clean_resource = {
        "resource_id": resource.pop("id"),
    }

    # Remove empty values
    clean_resource.update(
        {k: v for k, v in resource.items() if v is not None and not isinstance(v, dict)}
    )
    return clean_resource
