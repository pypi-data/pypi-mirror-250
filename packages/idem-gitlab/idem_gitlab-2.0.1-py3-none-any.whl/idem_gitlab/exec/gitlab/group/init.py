def __init__(hub):
    """
    Patch the group sub onto the group module
    """
    # Get the group module
    mod = hub.exec.gitlab._loaded["group"]
    # Get the group sub
    sub = hub.exec.gitlab._subs["group"]
    # Load all the modules in the group sub
    sub._load_all()
    # Add the modules on the group sub to the group module
    mod._attrs.update(sub._loaded)
    # This is so that "describe" can find the group sub modules
    mod._subs = sub._loaded
