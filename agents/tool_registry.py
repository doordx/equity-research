from tools.finance_data import FinanceDataTool
from tools.web_search import WebSearchTool
from tools.financial_analysis import FinancialAnalysisTool
from tools.news_sentiment import NewsSentimentTool

class ToolRegistry:
    """
    Holds tool instances and exposes a callable interface.
    """

    def __init__(self):
        self.tools = {
            "finance_data": FinanceDataTool(),
            "web_search": WebSearchTool(),
            "financial_analysis": FinancialAnalysisTool(),
            "news_sentiment": NewsSentimentTool()
        }

    def call(self, tool_name: str, **kwargs):
        # --- Finance Data ---
        if tool_name == "finance_data":
            ticker = kwargs.get("ticker")
            return {
                "summary": self.tools["finance_data"].get_summary(ticker),
                "financials": self.tools["finance_data"].get_financials(ticker),
            }

        if tool_name == "price_history":
            return self.tools["finance_data"].get_price_history(kwargs["ticker"])


        # --- Web Search Tools ---
        if tool_name == "search":
            return self.tools["web_search"].search(kwargs["query"], max_results=5)

        if tool_name == "news":
            return self.tools["web_search"].news(kwargs["query"], max_results=5)


        # --- Financial Analysis Tool ---
        if tool_name == "financial_ratios":
            summary = kwargs.get("summary")
            financials = kwargs.get("financials")
            return self.tools["financial_analysis"].compute_ratios(summary, financials)

        if tool_name == "score_company":
            ratios = kwargs.get("ratios")
            return self.tools["financial_analysis"].score_company(ratios)

        if tool_name == "news_sentiment":
            return self.tools["news_sentiment"].analyze(kwargs["news_items"])

        raise ValueError(f"Unknown tool: {tool_name}")
