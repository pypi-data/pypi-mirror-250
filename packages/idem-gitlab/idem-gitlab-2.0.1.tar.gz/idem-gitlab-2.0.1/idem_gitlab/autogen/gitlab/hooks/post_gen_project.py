import pathlib

import pop.hub
from dict_tools.data import NamespaceDict

if __name__ == "__main__":
    root_directory = pathlib.Path.cwd()
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="tool")
    hub.pop.sub.load_subdirs(hub.tool, recurse=True)
    ctx = NamespaceDict({{cookiecutter}})

    for file in (root_directory / ctx.clean_name / "exec" / ctx.service_name).glob(
        "*/*.py"
    ):
        lines = []
        with file.open("r") as fh:
            for line in fh.readlines():
                lines.append(
                    line.replace("id_", "project_id")
                    .replace("kwargs: dict = None", "**kwargs")
                    .replace("_: None", "*")
                )
        with file.open("w") as fh:
            fh.writelines(lines)
