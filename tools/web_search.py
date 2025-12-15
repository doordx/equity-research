from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup

class WebSearchTool:
    """
    Wrapper around DuckDuckGo Search.
    Supports:
    - General web search
    - News search
    - Fetching page content
    """

    def search(self, query: str, max_results: int = 5):
        """
        Basic web search.
        """
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return results

    def news(self, query: str, max_results: int = 5):
        """
        News search (great for equity research).
        """
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=max_results))
        return results

    def fetch_page_text(self, url: str):
        """
        Fetch the raw text from a webpage.
        """
        try:
            response = requests.get(url, timeout=8)
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract only readable text
            text = " ".join(t.strip() for t in soup.stripped_strings)
            return text

        except Exception as e:
            return f"Error fetching page: {e}"
