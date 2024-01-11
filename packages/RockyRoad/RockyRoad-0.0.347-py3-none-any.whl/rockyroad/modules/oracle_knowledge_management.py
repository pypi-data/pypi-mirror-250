from .module_imports import *


@headers({"Ocp-Apim-Subscription-Key": key})
class _Oracle_Knowledge_Management(Consumer):
    """Inteface to Oracle knowledge management resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    @returns.json
    @http_get("oracle/content/articles/{id}")
    def get_article(
        self,
        id: Query(type=str)
    ):
        """This call will return the Oracle knowledge base article for the specified answer id."""

    @returns.json
    @http_get("oracle/search/question/")
    def get_search_results(
        self,
        question: str,
    ):
        """This call will return the Oracle user for the specified email."""
