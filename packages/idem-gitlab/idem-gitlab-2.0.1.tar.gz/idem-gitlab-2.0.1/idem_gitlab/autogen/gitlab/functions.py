import requests

try:
    import bs4

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


def parse(hub, link: str, path: str, clean_path: str):
    result = {"create": {}, "delete": {}, "get": {}, "list": {}, "update": {}}
    # Parse the path
    with requests.get(link) as response:
        html = response.text

    soup = bs4.BeautifulSoup(html, "lxml")
    main = soup.find("div", {"role": "main"})
    try:
        main.find_all("table", {"thead": {}})
    except AttributeError:
        hub.log.debug(f"Something went wrong generating {link}")
    else:
        for table in main.find_all("table", {"thead": {}}):
            body: bs4.Tag = table.tbody

            try:
                example = table.find_previous_sibling("div").find("code").text
                if path not in example:
                    continue
            except AttributeError:
                example = ""
            function_doc = table.find_previous_sibling("p").text

            params = {}
            for row in body.find_all("tr"):
                cells: list[bs4.Tag] = row.find_all("td")
                if len(cells) < 4:
                    continue
                name = cells[0].text.strip()
                target = "kwargs"
                if f":{name}" in path:
                    target = "hardcoded"
                    if name == "id":
                        name = "project_id"

                required = cells[2].text.startswith("yes")

                # Skip deprecated parameters
                if "deprecated" in str(cells[3]).lower():
                    continue

                # Identify the default value and default type requested by gitlab APIs
                param_type = hub.pop_create.gitlab.param.type(
                    value=cells[1].text.strip(), name=name, description=cells[3]
                )

                params[name] = {
                    "required": required,
                    "default": None,
                    "target_type": "mapping",
                    "target": target,
                    "param_type": param_type,
                    "doc": cells[3].text.strip(),
                }

            function_data = {
                "doc": function_doc,
                "params": params,
            }
            if "POST" in example and not result["create"]:
                params["resource_id"] = hub.pop_create.gitlab.param.RESOURCE_ID
                params["*"] = hub.pop_create.gitlab.param.POS_ARG
                params["kwargs"] = hub.pop_create.gitlab.param.KWARGS
                result["create"] = function_data
            elif "PUT" in example and not result["update"]:
                params["resource_id"] = hub.pop_create.gitlab.param.RESOURCE_ID
                params["*"] = hub.pop_create.gitlab.param.POS_ARG
                params["kwargs"] = hub.pop_create.gitlab.param.KWARGS
                result["update"] = function_data
            elif "DELETE" in example and not result["delete"]:
                params["resource_id"] = hub.pop_create.gitlab.param.RESOURCE_ID
                params["*"] = hub.pop_create.gitlab.param.POS_ARG
                params["kwargs"] = hub.pop_create.gitlab.param.KWARGS
                result["delete"] = function_data
            elif "GET" in example:
                try:
                    head = table.find_previous_sibling("h2").text
                except:
                    head = ""
                if "list" in head.lower():
                    get_params = {}
                    for name, param_data in function_data.get("params", {}).items():
                        if name in clean_path:
                            continue
                        get_params[name] = param_data
                    function_data["params"] = get_params
                    if not result["list"]:
                        params["resource_id"] = hub.pop_create.gitlab.param.RESOURCE_ID
                        params["*"] = hub.pop_create.gitlab.param.POS_ARG
                        params["kwargs"] = hub.pop_create.gitlab.param.KWARGS
                        result["list"] = function_data
                    elif not result["get"]:
                        params["resource_id"] = hub.pop_create.gitlab.param.RESOURCE_ID
                        params["*"] = hub.pop_create.gitlab.param.POS_ARG
                        params["kwargs"] = hub.pop_create.gitlab.param.KWARGS
                        result["get"] = function_data

            elif "PATCH" in example and not result["update"]:
                params["resource_id"] = hub.pop_create.gitlab.param.RESOURCE_ID
                params["*"] = hub.pop_create.gitlab.param.POS_ARG
                params["kwargs"] = hub.pop_create.gitlab.param.KWARGS
                result["update"] = function_data

        # This will usually work
        if not result["get"]:
            result["get"] = result["list"]

    return result
