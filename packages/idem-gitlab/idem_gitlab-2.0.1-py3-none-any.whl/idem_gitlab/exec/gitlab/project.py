"""Exec module for managing Gitlab Projects."""
from dataclasses import make_dataclass
from typing import Any
from typing import Literal

__contracts__ = ["auto_state"]

__func_alias__ = {"list_": "list"}


async def get(hub, ctx, resource_id: str, **kwargs) -> dict[str, Any]:
    """
    This endpoint supports keyset pagination
    for selected order_by options.

    Args:
        resource_id(str):
            The ID or URL-encoded path of the project. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            unmanaged_resource:
              exec.run:
                - path: gitlab.project.get
                - kwargs:
                  resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.get resource_id=value
    """
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "get",
        url=f"{ctx.acct.endpoint_url}/projects/{resource_id}",
        params={"owned": ctx.acct.owned},
        success_codes=[200],
    )
    if not ret.result:
        ret.ret = {}
    else:
        ret.ret = hub.tool.gitlab.project.project.raw_to_present(ret.ret)
    return ret


async def list_(
    hub,
    ctx,
    **kwargs,
) -> dict[str, Any]:
    """
    Get a list of all visible projects across GitLab for the authenticated user.
    When accessed without authentication, only public projects with simple fields
    are returned.

    Returns:
        dict[str, Any]

    Examples:

        Resource State:

        .. code-block:: sls

            unmanaged_resources:
              exec.run:
                - path: gitlab.project.list


        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe gitlab.project

    """
    result = dict(ret=[], result=True, comment=[])

    async for ret in hub.tool.gitlab.request.paginate(
        ctx, url=f"{ctx.acct.endpoint_url}/projects", **kwargs
    ):
        resource = hub.tool.gitlab.project.project.raw_to_present(ret)
        result["ret"].append(resource)

    return result


async def create(
    hub,
    ctx,
    resource_id: str = None,
    *,
    path: str,
    allow_merge_on_skipped_pipeline: bool = None,
    only_allow_merge_if_all_status_checks_passed: bool = None,
    analytics_access_level: Literal["disabled", "private", "enabled"] = None,
    auto_cancel_pending_pipelines: bool = None,
    auto_devops_deploy_strategy: Literal[
        "continuous", "manual", "timed_incremental"
    ] = None,
    auto_devops_enabled: bool = None,
    autoclose_referenced_issues: bool = None,
    avatar: str = None,
    build_git_strategy: str = None,
    build_timeout: int = None,
    builds_access_level: Literal["disabled", "private", "enabled"] = None,
    ci_config_path: str = None,
    container_expiration_policy_attributes: make_dataclass(
        "container_expiration_policy_attributes",
        [
            ("cadence", str),
            ("keep_n", int),
            ("older_than", str),
            ("name_regex", str),
            ("name_regex_delete", str),
            ("name_regex_keep", str),
            ("enabled", bool),
        ],
    ) = None,
    container_registry_access_level: Literal["disabled", "private", "enabled"] = None,
    default_branch: str = None,
    description: str = None,
    emails_enabled: bool = None,
    external_authorization_classification_label: str = None,
    forking_access_level: str = None,
    group_runners_enabled: bool = None,
    group_with_project_templates_id: int = None,
    import_url: str = None,
    initialize_with_readme: bool = None,
    issues_access_level: Literal["disabled", "private", "enabled"] = None,
    lfs_enabled: bool = None,
    merge_method: str = None,
    merge_pipelines_enabled: bool = None,
    merge_requests_access_level: Literal["disabled", "private", "enabled"] = None,
    merge_trains_enabled: bool = None,
    mirror_trigger_builds: bool = None,
    mirror: bool = None,
    namespace_id: int = None,
    only_allow_merge_if_all_discussions_are_resolved: bool = None,
    only_allow_merge_if_pipeline_succeeds: bool = None,
    packages_enabled: bool = None,
    pages_access_level: str = None,
    printing_merge_request_link_enabled: bool = None,
    public_builds: bool = None,
    releases_access_level: Literal["disabled", "private", "enabled"] = None,
    environments_access_level: Literal["disabled", "private", "enabled"] = None,
    feature_flags_access_level: Literal["disabled", "private", "enabled"] = None,
    infrastructure_access_level: Literal["disabled", "private", "enabled"] = None,
    monitor_access_level: Literal["disabled", "private", "enabled"] = None,
    model_experiments_access_level: Literal["disabled", "private", "enabled"] = None,
    remove_source_branch_after_merge: bool = None,
    repository_access_level: Literal["disabled", "private", "enabled"] = None,
    repository_storage: str = None,
    request_access_enabled: bool = None,
    requirements_access_level: Literal["disabled", "private", "enabled"] = None,
    resolve_outdated_diff_discussions: bool = None,
    security_and_compliance_access_level: Literal[
        "disabled", "private", "enabled"
    ] = None,
    shared_runners_enabled: bool = None,
    show_default_award_emojis: bool = None,
    snippets_access_level: Literal["disabled", "private", "enabled"] = None,
    squash_option: Literal["never", "always", "default_on", "default_off"] = None,
    template_name: str = None,
    template_project_id: int = None,
    topics: list[str] = None,
    use_custom_template: bool = None,
    visibility: str = None,
    wiki_access_level: str = None,
    **kwargs,
) -> dict[str, Any]:
    """
    Example request:

    Args:
        resource_id(str, Optional):
            The ID or URL-encoded path of the project. Defaults to None.

        path(str, Optional):
            Repository name for new project. Generated based on name if not provided (generated as lowercase with dashes). Starting with GitLab 14.9, path must not start or end with a special character and must not contain consecutive special characters. Defaults to None.

        allow_merge_on_skipped_pipeline(bool, Optional):
            Set whether or not merge requests can be merged with skipped jobs. Defaults to None.

        only_allow_merge_if_all_status_checks_passed(bool, Optional):
            Indicates that merges of merge requests should be blocked unless all status checks have passed. Defaults to false. Introduced in GitLab 15.5 with feature flag only_allow_merge_if_all_status_checks_passed disabled by default. Defaults to None.

        analytics_access_level(str, Optional):
            One of disabled, private or enabled. Defaults to None.

        auto_cancel_pending_pipelines(bool, Optional):
            Auto-cancel pending pipelines. This action toggles between an enabled state and a disabled state; it is not a boolean. Defaults to None.

        auto_devops_deploy_strategy(str, Optional):
            Auto Deploy strategy (continuous, manual or timed_incremental). Defaults to None.

        auto_devops_enabled(bool, Optional):
            Enable Auto DevOps for this project. Defaults to None.

        autoclose_referenced_issues(bool, Optional):
            Set whether auto-closing referenced issues on default branch. Defaults to None.

        avatar(str, Optional):
            Image file for avatar of the project. Defaults to None.

        build_git_strategy(str, Optional):
            The Git strategy. Defaults to fetch. Defaults to None.

        build_timeout(int, Optional):
            The maximum amount of time, in seconds, that a job can run. Defaults to None.

        builds_access_level(str, Optional):
            One of disabled, private, or enabled. Defaults to None.

        ci_config_path(str, Optional):
            The path to CI configuration file. Defaults to None.

        container_expiration_policy_attributes:
            Update the image cleanup policy for this project. Accepts: cadence (string), keep_n (integer), older_than (string), name_regex (string), name_regex_delete (string), name_regex_keep (string), enabled (boolean). See the Container Registry documentation for more information on cadence, keep_n and older_than values. Defaults to None.

        container_registry_access_level(str, Optional):
            Set visibility of container registry, for this project, to one of disabled, private or enabled. Defaults to None.

        default_branch(str, Optional):
            The default branch name. Requires initialize_with_readme to be true. Defaults to None.

        description(str, Optional):
            Short project description. Defaults to None.

        emails_enabled(bool, Optional):
            Enable email notifications. Defaults to None.

        external_authorization_classification_label(str, Optional):
            The classification label for the project. Defaults to None.

        forking_access_level(str, Optional):
            One of disabled, private, or enabled. Defaults to None.

        group_runners_enabled(bool, Optional):
            Enable group runners for this project. Defaults to None.

        group_with_project_templates_id(int, Optional):
            For group-level custom templates, specifies ID of group from which all the custom project templates are sourced. Leave empty for instance-level templates. Requires use_custom_template to be true. Defaults to None.

        import_url(str, Optional):
            URL to import repository from. When the URL value isn’t empty, you must not set initialize_with_readme to true. Doing so might result in the following error: not a git repository. Defaults to None.

        initialize_with_readme(bool, Optional):
            Whether to create a Git repository with just a README.md file. Default is false. When this boolean is true, you must not pass import_url or other attributes of this endpoint which specify alternative contents for the repository. Doing so might result in the following error: not a git repository. Defaults to None.

        issues_access_level(str, Optional):
            One of disabled, private, or enabled. Defaults to None.

        lfs_enabled(bool, Optional):
            Enable LFS. Defaults to None.

        merge_method(str, Optional):
            Set the merge method used. Defaults to None.

        merge_pipelines_enabled(bool, Optional):
            Enable or disable merge pipelines. Defaults to None.

        merge_requests_access_level(str, Optional):
            One of disabled, private, or enabled. Defaults to None.

        merge_trains_enabled(bool, Optional):
            Enable or disable merge trains. Defaults to None.

        mirror_trigger_builds(bool, Optional):
            Pull mirroring triggers builds. Defaults to None.

        mirror(bool, Optional):
            Enables pull mirroring in a project. Defaults to None.

        namespace_id(int, Optional):
            Namespace for the new project (defaults to the current user’s namespace). Defaults to None.

        only_allow_merge_if_all_discussions_are_resolved(bool, Optional):
            Set whether merge requests can only be merged when all the discussions are resolved. Defaults to None.

        only_allow_merge_if_pipeline_succeeds(bool, Optional):
            Set whether merge requests can only be merged with successful pipelines. This setting is named Pipelines must succeed in the project settings. Defaults to None.

        packages_enabled(bool, Optional):
            Enable or disable packages repository feature. Defaults to None.

        pages_access_level(str, Optional):
            One of disabled, private, enabled, or public. Defaults to None.

        printing_merge_request_link_enabled(bool, Optional):
            Show link to create/view merge request when pushing from the command line. Defaults to None.

        public_builds(bool, Optional):
            If true, jobs can be viewed by non-project members. Defaults to None.

        releases_access_level(str, Optional):
            One of disabled, private, or enabled. Defaults to None.

        environments_access_level(str, Optional):
            One of disabled, private, or enabled. Defaults to None.

        feature_flags_access_level(str, Optional):
            One of disabled, private, or enabled. Defaults to None.

        infrastructure_access_level(str, Optional):
            One of disabled, private, or enabled. Defaults to None.

        monitor_access_level(str, Optional):
            One of disabled, private, or enabled. Defaults to None.

        model_experiments_access_level(str, Optional):
            One of disabled, private, or enabled. Defaults to None.

        remove_source_branch_after_merge(bool, Optional):
            Enable Delete source branch option by default for all new merge requests. Defaults to None.

        repository_access_level(str, Optional):
            One of disabled, private, or enabled. Defaults to None.

        repository_storage(str, Optional):
            Which storage shard the repository is on. (administrator only). Defaults to None.

        request_access_enabled(bool, Optional):
            Allow users to request member access. Defaults to None.

        requirements_access_level(str, Optional):
            One of disabled, private or enabled. Defaults to None.

        resolve_outdated_diff_discussions(bool, Optional):
            Automatically resolve merge request diffs discussions on lines changed with a push. Defaults to None.

        security_and_compliance_access_level(str, Optional):
            (GitLab 14.9 and later) Security and compliance access level. One of disabled, private, or enabled. Defaults to None.

        shared_runners_enabled(bool, Optional):
            Enable shared runners for this project. Defaults to None.

        show_default_award_emojis(bool, Optional):
            Show default emoji reactions. Defaults to None.

        snippets_access_level(str, Optional):
            One of disabled, private, or enabled. Defaults to None.

        squash_option(str, Optional):
            One of never, always, default_on, or default_off. Defaults to None.

        template_name(str, Optional):
            When used without use_custom_template, name of a built-in project template. When used with use_custom_template, name of a custom project template. Defaults to None.

        template_project_id(int, Optional):
            When used with use_custom_template, project ID of a custom project template. Using a project ID is preferable to using template_name since template_name may be ambiguous. Defaults to None.

        topics(list[str], Optional):
            The list of topics for a project; put array of topics, that should be finally assigned to a project. (Introduced in GitLab 14.0.). Defaults to None.

        use_custom_template(bool, Optional):
            Use either custom instance or group (with group_with_project_templates_id) project template. Defaults to None.

        visibility(str, Optional):
            See project visibility level. Defaults to None.

        wiki_access_level(str, Optional):
            One of disabled, private, or enabled. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              gitlab.project.present:
                - path: string

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.create
    """
    data = {k: v for k, v in locals().items() if k not in ("hub", "ctx", "resource_id")}
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "post",
        success_codes=[201, 304, 204],
        url=f"{ctx.acct.endpoint_url}/projects",
        data=data,
    )
    ret.ret = hub.tool.gitlab.project.project.raw_to_present(ret.ret)
    return ret


async def update(
    hub,
    ctx,
    resource_id: str,
    **kwargs,
) -> dict[str, Any]:
    """
    Supported attributes:

    Args:
        resource_id(str):
            The ID or URL-encoded path of the project. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              gitlab.project.present:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.update resource_id=value
    """
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "put",
        url=f"{ctx.acct.endpoint_url}/projects/{resource_id}",
        success_codes=[200, 204, 304],
        params={"owned": ctx.acct.owned},
        data=dict(id=resource_id, **kwargs),
    )
    return ret


async def delete(
    hub,
    ctx,
    resource_id: str,
    *,
    permanently_remove: bool = None,
    full_path: str = None,
    **kwargs,
) -> dict[str, Any]:
    """
    This endpoint:

    Args:
        resource_id(str):
            The ID or URL-encoded path of the project. Defaults to None.

        permanently_remove(bool, Optional):
            Immediately deletes a project if it is marked for deletion. Introduced in GitLab 15.11. Defaults to None.

        full_path(str, Optional):
            Full path of project to use with permanently_remove. Introduced in GitLab 15.11. To find the project path, use path_with_namespace from get single project. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              gitlab.project.absent:
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec gitlab.project.delete resource_id=value
    """
    ret = await hub.tool.gitlab.request.json(
        ctx,
        "delete",
        url=f"{ctx.acct.endpoint_url}/projects/{resource_id}",
        success_codes=[202, 204, 404],
        data={
            "id": resource_id,
            "permanently_remove": permanently_remove,
            "full_path": full_path,
        },
    )
    return ret
