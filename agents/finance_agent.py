from agents.base_agent import BaseAgent
from tools.finance_data import FinanceDataTool

class FinanceAgent(BaseAgent):
    def __init__(self):
        super().__init__("FinanceAgent")
        self.tool = FinanceDataTool()

    def run(self, ticker: str):
        """
        Very basic test function.
        Fetch price data and key metrics.
        """
        result = {
            "price_history": self.tool.get_price_history(ticker),
            "summary": self.tool.get_summary(ticker),
            "financials": self.tool.get_financials(ticker)
        }

        return result
