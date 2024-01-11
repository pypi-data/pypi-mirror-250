import copy
import pathlib

import tqdm


HEADER_TEMPLATE = "Tests for validating {}."


def run(hub, ctx, root_directory: pathlib.Path or str):
    if isinstance(root_directory, str):
        root_directory = pathlib.Path(root_directory)
    cloud_spec = copy.deepcopy(ctx.cloud_spec)

    for ref, plugin in tqdm.tqdm(
        cloud_spec.plugins.items(), desc=f"Generating test functions"
    ):
        resource_ref = hub.cloudspec.parse.plugin.resource_ref(ctx, ref)
        resource_header = HEADER_TEMPLATE.format(
            hub.tool.format.inflect.ENGINE.plural_noun(resource_ref)
        )

        plugin["imports"] = [
            "import pytest",
            "import tempfile",
            "import yaml",
            "from tests.integration.conftest import TestFlag",
        ]

        test_dir = root_directory / "tests" / "integration" / "states"

        mod_file = hub.cloudspec.parse.plugin.touch(
            root=test_dir, ref=ref, is_test=True
        )

        to_write = hub.cloudspec.parse.plugin.header(
            plugin=plugin, resource_header=resource_header
        )

        for function_name in (
            "resource_init",
            "test_present",
            "test_get",
            "test_list",
            "test_describe",
            "test_update",
            "test_absent",
        ):
            if function_name == "resource_init":
                t = hub.pop_create.gitlab.template.TEST_RESOURCE_INIT
            elif function_name == "test_present":
                t = hub.pop_create.gitlab.template.TEST_PRESENT
            elif function_name == "test_get":
                t = hub.pop_create.gitlab.template.TEST_GET
            elif function_name == "test_list":
                t = hub.pop_create.gitlab.template.TEST_LIST
            elif function_name == "test_describe":
                t = hub.pop_create.gitlab.template.TEST_DESCRIBE
            elif function_name == "test_update":
                t = hub.pop_create.gitlab.template.TEST_UPDATE
            elif function_name == "test_absent":
                t = hub.pop_create.gitlab.template.TEST_ABSENT
            else:
                continue

            template = hub.tool.jinja.template(t)

            try:
                to_write += template.render(
                    function={
                        "name": function_name,
                        "service_name": cloud_spec.service_name,
                        "ref": f"gitlab.{ref}",
                    },
                )
            except Exception as err:
                hub.log.error(
                    f"Failed to generate resource {resource_ref} function's action definitions for {function_name}: {err.__class__.__name__}: {err}"
                )

        mod_file.write_text(to_write)
