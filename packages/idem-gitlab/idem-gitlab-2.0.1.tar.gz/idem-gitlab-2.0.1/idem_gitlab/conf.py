import pathlib

DEFAULT_CLOUDSPEC_PATH = str(pathlib.Path(".").absolute() / "cloud_spec_cache.json")
CONFIG = {
    "cloud_spec_cache": {
        "help": "To save time parsing the gitlab REST API, save it to this location",
        "default": DEFAULT_CLOUDSPEC_PATH,
        "dyne": "pop_create",
    },
}

CLI_CONFIG = {
    "cloud_spec_cache": {
        "subcommands": ["gitlab"],
        "dyne": "pop_create",
    },
}

SUBCOMMANDS = {
    "gitlab": {
        "help": "Create idem_aws state modules by parsing the reset api",
        "dyne": "pop_create",
    },
}

DYNE = {
    "pop_create": ["autogen"],
    "exec": ["exec"],
    "acct": ["acct"],
    "tool": ["tool"],
    "cloudspec": ["cloudspec"],
}
