from typing import List
import requests
import json


class SearchResult:
    def __init__(
        self, url: str, title: str, thumbnail: str, positions: List[str], score: float
    ) -> None:
        self.url = url
        self.title = title
        self.thumbnail = thumbnail
        self.positions = positions
        self.score = score

    def __str__(self) -> str:
        return f"url:{self.url}\ntitle:{self.title}\nthumbnail:{self.thumbnail}\npositions:{self.positions}\nscore:{self.score}\n"


class SearchParameters:
    def __init__(
        self,
        categories: List[str] = [],
        engines: List[str] = [],
        language: str = "",
        pageno: int = 1,
        time_range: str = "",
        image_proxy: bool = True,
        safe_search: str = "",
        enabled_plugins: List[str] = [],
        disabled_plugins: List[str] = [],
        enabled_engines: List[str] = [],
        disabled_engines: List[str] = [],
    ):
        self.categories = categories
        self.engines = engines
        self.language = language
        self.pageno = pageno
        self.time_range = time_range
        self.image_proxy = image_proxy
        self.safe_search = safe_search
        self.enabled_plugins = enabled_plugins
        self.disabled_plugins = disabled_plugins
        self.enabled_engines = enabled_engines
        self.disabled_engines = disabled_engines

        self.format = "json"

    def update(
        self,
        categories=None,
        engines=None,
        language=None,
        pageno=None,
        time_range=None,
        image_proxy=None,
        safe_search=None,
        enabled_plugins=None,
        disabled_plugins=None,
        enabled_engines=None,
        disabled_engines=None,
    ):
        if categories != None:
            self.categories = categories

        if engines != None:
            self.engines = engines

        if language != None:
            self.language = language

        if pageno != None:
            self.pageno = pageno

        if time_range != None:
            self.time_range = time_range

        if image_proxy != None:
            self.image_proxy = image_proxy

        if safe_search != None:
            self.safe_search = safe_search

        if enabled_plugins != None:
            self.enabled_plugins = enabled_plugins

        if disabled_plugins != None:
            self.disabled_plugins = disabled_plugins

        if enabled_engines != None:
            self.enabled_engines = enabled_engines

        if disabled_engines != None:
            self.disabled_engines = disabled_engines

    def as_dict(self):
        param_dict = {
            "pageno": str(self.pageno),
            "format": self.format,
            "image_proxy": str(self.image_proxy),
        }

        if self.categories:
            param_dict.update({"categories": ",".join(self.categories)})

        if self.engines:
            param_dict.update({"engines": ",".join(self.engines)})

        if self.language != "":
            param_dict.update({"language": self.language})

        if self.safe_search != "":
            param_dict.update({"safe_search": self.safe_search})

        if self.enabled_plugins:
            param_dict.update({"enabled_plugins": ",".join(self.enabled_plugins)})

        if self.disabled_plugins:
            param_dict.update({"disabled_plugins": ",".join(self.disabled_plugins)})

        if self.enabled_engines:
            param_dict.update({"enabled_engines": ",".join(self.enabled_engines)})

        if self.disabled_engines:
            param_dict.update({"disabled_engines": ",".join(self.disabled_engines)})

        return param_dict


class SearXNG:
    def __init__(
        self, base_url: str, search_params: SearchParameters = SearchParameters()
    ) -> None:
        self.endpoint = base_url + "/search"
        self.search_params = search_params

    def parse_api_json(self, json: dict) -> List[SearchResult]:
        assembled_list = []
        for current_dict in json["results"]:
            assembled_list.append(
                SearchResult(
                    url=current_dict.get("url", ""),
                    title=current_dict.get("title", ""),
                    thumbnail=current_dict.get("thumbnail", ""),
                    positions=current_dict.get("positions", ""),
                    score=float(current_dict.get("score", 0)),
                )
            )

        return assembled_list

    def search(self, query: str, n_pages: int = 1, search_params=None):
        if search_params == None:
            search_params = self.search_params.as_dict()
        else:
            search_params = search_params.as_dict()

        search_params.update({"q": query})

        results = []
        for idx in range(1, n_pages + 1):
            search_params["pageno"] = str(idx)

            response = requests.get(self.endpoint, params=search_params)

            if response.status_code != 200:
                raise ValueError(
                    f"searxng endpoint={self.endpoint} status code was not 200, got={response.status_code}"
                )

            results.extend(self.parse_api_json(response.json()))

        return results

    def search_from_sites(self, query: str, sites: List[str], search_params=None):
        pass

    def search_from_sites_combined(
        self, query: str, sites: List[str], search_params=None
    ):
        pass
