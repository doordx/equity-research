from agents.base_agent import BaseAgent
from tools.web_search import WebSearchTool

class WebSearchAgent(BaseAgent):
    def __init__(self):
        super().__init__("WebSearchAgent")
        self.tool = WebSearchTool()

    def run(self, query: str, fetch_content=False):
        """
        Perform DuckDuckGo news + web search.
        """

        news_results = self.tool.news(query, max_results=5)
        web_results = self.tool.search(query, max_results=5)

        enriched = []

        for item in news_results:
            url = item.get("url")
            if fetch_content and url:
                item["content"] = self.tool.fetch_page_text(url)
            enriched.append(item)

        return {
            "news": enriched,
            "web": web_results
        }
