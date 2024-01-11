"""Exec module for managing Project Commits. Commits"""
from typing import Any

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    resource_id: str = None,
    *,
    project_id: int,
) -> dict[str, Any]:
    """
    Returns information about the merge request that originally introduced a specific commit.

    Args:
        resource_id(str):
            The commit hash or name of a repository branch or tag

        project_id(int):
            The ID or URL-encoded path of the project owned by the authenticated user.

    Returns:
        dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            unmanaged_resource:
              exec.run:
                - path: gitlab.project.commit.get
                - kwargs:
                  resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.commit.get resource_id=value
    """
    if not resource_id:
        # get the default branch for this project
        project_ret = await hub.exec.gitlab.project.get(ctx, project_id)
        resource_id = project_ret.ret.default_branch

    ret = await hub.tool.gitlab.request.json(
        ctx,
        "get",
        success_codes=[200, 201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/projects/{project_id}/repository/commits/{resource_id}",
    )
    if ret.result:
        ret.ret = hub.tool.gitlab.project.commit.raw_to_present(ret.ret)
        ret.ret["project_id"] = project_id
    return ret


async def list_(hub, ctx, project_id: int = None, **kwargs) -> dict[str, Any]:
    """
    Get a list of repository commits in a project.

    Returns:
        dict[str, Any]

    Examples:

        Resource State:

        .. code-block:: sls

            unmanaged_resources:
              exec.run:
                - path: gitlab.project.commit.list
                - kwargs:


        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.commit.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe gitlab.project.commit

    """
    result = dict(ret=[], result=True, comment=[])

    if project_id:
        # Parse the commits for a single project id
        async for ret in hub.tool.gitlab.request.paginate(
            ctx,
            url=f"{ctx.acct.endpoint_url}/projects/{project_id}/repository/commits",
            **kwargs,
        ):
            resource = hub.tool.gitlab.project.commit.raw_to_present(ret)
            resource["project_id"] = project_id
            result["ret"].append(resource)
    else:
        # Get the commits for every project
        async for project in hub.tool.gitlab.request.paginate(
            ctx, url=f"{ctx.acct.endpoint_url}/projects", **kwargs
        ):
            project_id = project.id
            async for ret in hub.tool.gitlab.request.paginate(
                ctx,
                url=f"{ctx.acct.endpoint_url}/projects/{project_id}/repository/commits",
                **kwargs,
            ):
                resource = hub.tool.gitlab.project.commit.raw_to_present(ret)
                resource["project_id"] = project_id
                result["ret"].append(resource)

    return result
