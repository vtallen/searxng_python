from typing import List
import requests
import json


class SearchResult:
    """
    A storage class that holds the information for a singal search result from the SearXNG API
    """

    def __init__(
        self, url: str, title: str, thumbnail: str, positions: List[str], score: float
    ) -> None:
        """
        Takes the arguments and stores them in the class

        Args:
            url             (str): The url of the search result
            title           (str): The title of the page referenced by this search result
            thumbnail       (str): The url for the thumbnail of the result (if exists)
            positions (List[str]): The position of this result in the search results from each engine that returned this url
            score         (float): The search engine ranking for how close of a match to the query this result is
        """
        self.url = url
        self.title = title
        self.thumbnail = thumbnail
        self.positions = positions
        self.score = score

    def __str__(self) -> str:
        """
        Returns the string representation of all class members

        Returns:
            str: The string representation of this class
        """
        return f"url:{self.url}\ntitle:{self.title}\nthumbnail:{self.thumbnail}\npositions:{self.positions}\nscore:{self.score}\n"


class SearchParameters:
    """
    A storage class that holds most of the parameters needed to do a search

    This class does not include the "q" (query) parameter, it must be added by the code using this class before the parameters are
    set into the http request
    """

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
        """
        Sets the internal members of the class to the constructor arguments

        see https://docs.searxng.org/dev/search_api.html for information on allowed values for each argument

        Args:
            categories       (List[str]): Specifies the active search categories
            engines          (List[str]): Specifies which engines should be active for this search
            language               (str): Specifies the language to get search results from
            pageno                 (int): Specifies which page of the search results to return
            time_range             (str): Specifies the time range from which to pull results (if the search engine supports this)
            image_proxy           (bool): Whether or not to proxy images through the SearXNG instance
            safe_search            (str): Whether or not to enable safe search on the engines that support it (allowed vals: 0, 1, 2)
            enabled_plugins  (List[str]): A list of the server's plugins that should be enabled for the search
            disabled_plugins (List[str]): A list of the server's plugins that should be disabled for the search
            enabled_engines  (List[str]): A list of engines that should be enabled for the search
            disabled_engines (List[str]): A list of engines that should be disabled for the search
        """
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
        """
        Updates the internal members to the value provided, if an argument is passed in as None it will be ignored

        Args:
            categories       (List[str]): Specifies the active search categories
            engines          (List[str]): Specifies which engines should be active for this search
            language               (str): Specifies the language to get search results from
            pageno                 (int): Specifies which page of the search results to return
            time_range             (str): Specifies the time range from which to pull results (if the search engine supports this)
            image_proxy           (bool): Whether or not to proxy images through the SearXNG instance
            safe_search            (str): Whether or not to enable safe search on the engines that support it (allowed vals: 0, 1, 2)
            enabled_plugins  (List[str]): A list of the server's plugins that should be enabled for the search
            disabled_plugins (List[str]): A list of the server's plugins that should be disabled for the search
            enabled_engines  (List[str]): A list of engines that should be enabled for the search
            disabled_engines (List[str]): A list of engines that should be disabled for the search

        """
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
        """
        Converts the members of this class into a dictionary that can be passed to a requests object for a request to the
        SearXNG API.

        Returns:
            dict - the params dictionary representation of this class
        """
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
        """
        Sets the api endpoint and default search parameters

        Args:
            base_url                   (str): The url of the SearXNG instance. This should be the base URL, not the api endpoint
            search_params (SearchParameters): The SearchParameters object contining the default parameters to be used in searches from this object
                                              if not provided, the defaults will be used
        """
        self.endpoint = base_url + "/search"
        self.search_params = search_params

    def parse_api_json(self, json: dict) -> List[SearchResult]:
        """
        Takes the json output from the SearXNG api and parses it into a list of SearchResult objects

        Args:
            json (dict): The json returned from an api request

        Returns:
            List[SearchResult] - The list of search results represented by the json
        """
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
        """
        Preforms a search on the API. If more than 1 page of results has been requested, then a seperate request will be made
        for each page.

        If no SearchParameters object is provided in the argument search_params, then this class's set defaults will be used instead

        Args:
            query                      (str): The serch to preform
            n_pages                    (int): The number of search results pages to request
            search_params (SearchParameters): The parameters to use for the search

        Returns:
            List[SearchResult] - A list of the search results of query

        """
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

    def search_from_sites(
        self, query: str, sites: List[str], search_params=None, n_pages: int = 1
    ):
        """
        Preforms a search with query, only returns results from the domains specified in the sites list.

        This is done by appending site:<domain 1> OR site:<domain 2> ... OR site:<domain n> to the query string before it is sent
        """
        pass

    def search_from_sites_combined(
        self, query: str, sites: List[str], search_params=None
    ):
        """
        Preforms a search with query only on the domains specified in sites. A seperate api call is made to get results from each domain.

        Ex. sites = ["amazon.com", "walmart.com"]

        2 requests would be made. One with "<query> site:amazon.com" and one with "<query> site:walmart.com" as the query string

        Results are combined into a single results list following the order of the domains in sites
        """
        pass
