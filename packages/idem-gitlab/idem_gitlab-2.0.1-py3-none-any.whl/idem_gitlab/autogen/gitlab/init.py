import json
import pathlib

from dict_tools.data import NamespaceDict

try:
    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


def context(hub, ctx, directory: pathlib.Path):
    ctx = hub.pop_create.idem_cloud.init.context(ctx, directory)

    ctx.servers = ["https://gitlab.com/api/v4/"]

    # We already have an acct plugin
    ctx.has_acct_plugin = False
    ctx.service_name = ctx.service_name or "gitlab_auto"
    version = "v4"
    docs_api = "https://docs.gitlab.com/ee/api/"
    cloud_spec = None

    cloud_spec_cache = pathlib.Path(ctx.cloud_spec_cache)
    if cloud_spec_cache.exists():
        try:
            cache = json.loads(cloud_spec_cache.read_text())
            cloud_spec = NamespaceDict(**cache)
        except:
            ...

    if not cloud_spec:
        plugins = hub.pop_create.gitlab.resource.parse(docs_api)

        # Initialize cloud spec
        cloud_spec = NamespaceDict(
            api_version=version,
            project_name=ctx.project_name,
            service_name=ctx.service_name,
            request_format={
                "create": hub.pop_create.gitlab.template.CREATE,
                "get": hub.pop_create.gitlab.template.CREATE,
                "list": hub.pop_create.gitlab.template.LIST,
                "update": hub.pop_create.gitlab.template.UPDATE,
                "delete": hub.pop_create.gitlab.template.DELETE,
                "raw_to_present": hub.pop_create.gitlab.template.RAW_TO_PRESENT,
            },
            plugins=plugins,
        )

        with cloud_spec_cache.open("w+") as fh:
            json.dump(cloud_spec, fh)

    ctx.cloud_spec = cloud_spec

    if ctx.create_plugin in ["auto_states", "exec_modules", "state_modules"]:
        create_plugins = ["auto_state", "tool"]
    else:
        create_plugins = [ctx.create_plugin]

    hub.cloudspec.init.run(
        ctx,
        directory,
        create_plugins=create_plugins,
    )
    hub.pop_create.init.run(
        directory=directory,
        subparsers=["cicd"],
        **ctx,
    )

    ctx.cloud_spec.plugins = {}
    return ctx
