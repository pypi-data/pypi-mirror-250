"""
Manipulate variables from gitlab API to keep them as such.
"""
try:
    pass

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


__func_alias__ = {"type_": "type", "value_": "value"}


RESOURCE_ID = {
    "required": True,
    "default": None,
    "target_type": "arg",
    "target": "resource_id",
    "param_type": "str",
    "doc": "A unique identifier for the resource",
}
KWARGS = {
    "required": False,
    "default": None,
    "target_type": "kwargs",
    "target": "**kwargs",
    "param_type": "dict",
    "doc": "Any keyword arguments to be passed as data to the resource",
    "exclude_from_example": True,
}

POS_ARG = {
    "required": True,
    "default": None,
    "target_type": "arg",
    "target": "*",
    "param_type": "None",
    "doc": None,
    "exclude_from_example": True,
}
RESOURCE = {
    "required": True,
    "default": None,
    "target_type": "arg",
    "target": "resource",
    "param_type": "dict[str, Any]",
    "doc": None,
    "exclude_from_example": True,
}


def type_(hub, value: str, name: str = None, description: str = None):
    """
    Convert the type from gitlab API docs into their base equivalent.
    :param hub:
    :param value:
    :return: Type
    """
    value = value.lower()

    # Handle resources that should be a Literal type
    if hasattr(description, "text") and "One of " in description.text:
        literals = []
        for code in description.contents:
            if not hasattr(code, "contents"):
                continue
            literals.append(f'"{code.text}"')
        return f"Literal[{', '.join(literals)}]"
    elif "hash" in value:
        member_params = []
        # Iterate over this 2 at a time skipping the first line
        for member_param_name, member_param_type in zip(
            description.contents[1::2], description.contents[2::2]
        ):
            if "), " not in member_param_type:
                continue
            else:
                member_param_type = hub.pop_create.gitlab.param.type(member_param_type)

            member_params.append(f'("{member_param_name.text}", {member_param_type})')
        return f'make_dataclass("{name}", [{", ".join(member_params)}])'

    elif "integer" in value or "number" in value:
        return "int"
    elif "float" in value:
        return "float"
    elif "str" in value:
        return "str"
    elif "bool" in value:
        return "bool"
    elif "date" in value:
        return "str"
    elif "array" in value:
        return "list[str]"
    elif "json" in value:
        return "dict[str, Any]"
    else:
        return "str"
