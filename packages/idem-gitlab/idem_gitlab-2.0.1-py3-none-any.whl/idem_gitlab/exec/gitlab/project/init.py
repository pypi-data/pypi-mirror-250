def __init__(hub):
    """
    Patch the project sub onto the project module
    """
    # Get the project module
    mod = hub.exec.gitlab._loaded["project"]
    # Get the project sub
    sub = hub.exec.gitlab._subs["project"]
    # Load all the modules in the project sub
    sub._load_all()
    # Add the modules on the project sub to the project module
    mod._attrs.update(sub._loaded)
    # This is so that "describe" can find the project sub modules
    mod._subs = sub._loaded
