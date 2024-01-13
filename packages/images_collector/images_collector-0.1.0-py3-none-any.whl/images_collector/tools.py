from typing import Any, Dict, List, Optional
import requests
from typing_extensions import Literal



class GoogleSerperTool:
    k: int = 10
    gl: str = "us"
    hl: str = "en"
    page : int = 0
    type: Literal["news", "search", "places", "images"] = "images"
    result_key_for_type = {
        "news": "news",
        "places": "places",
        "images": "images",
        "search": "organic",
    }
    serper_api_key: Optional[str] = None

    def results(self, query: str, **kwargs: Any) -> Dict:
        """Run query thourgh Google search"""
        return self._google_serper_api_results(
            query,
            gl=self.gl,
            hl=self.hl,
            num=self.k,
            page = self.page,
            search_type=self.type,
            
            **kwargs,
        )

    def _google_serper_api_results(
        self, search_term: str, search_type: str = "images", **kwargs: Any
    ) -> Dict:
        headers = {
            "X-API-KEY": self.serper_api_key or "",
            "Content-Type": "application/json",
        }
        params = {
            "q": search_term,
            **{key: value for key, value in kwargs.items() if value is not None},
        }
        response = requests.post(
            f"https://google.serper.dev/{search_type}", headers=headers, params=params
        )
        response.raise_for_status()
        search_results = response.json()
        return search_results