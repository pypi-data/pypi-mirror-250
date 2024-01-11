import requests

try:
    import bs4
    import tqdm

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


__func_alias__ = {"type_": "type"}


def parse(hub, api_url: str):
    plugins = {}

    with requests.get(f"{api_url}/api_resources.html") as response:
        html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")
    main = soup.find("div", {"role": "main"})
    tables: list[bs4.Tag] = main.find_all("table")

    for table in tables:
        resource = table.find_previous("h2").get("id").rsplit("-", maxsplit=1)[0]
        body = table.find("tbody")
        rows = body.find_all("tr")
        for row in tqdm.tqdm(rows, desc=resource):
            cells: list[bs4.Tag] = row.find_all("td")
            name = cells[0].find("a").text
            clean_name = hub.tool.format.inflect.ENGINE.singular_noun(
                hub.tool.format.case.snake(name)
            )
            ref = f"{resource}.{clean_name}"
            plugin = hub.pop_create.gitlab.plugin.parse(
                name=name,
                path=cells[0].find("code").text,
                link=api_url + cells[0].find("a").get("href"),
                ref=ref,
            )
            if plugin:
                plugins[ref] = plugin

    return plugins
