"""Utility functions for Standalone Namespaces."""
from typing import Any


def raw_to_present(hub, resource: dict[str, Any]) -> dict[str, Any]:
    """
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
    }
    clean_resource.update(resource)

    # Remove empty values
    clean_resource = {k: v for k, v in clean_resource.items() if v is not None}
    return clean_resource
