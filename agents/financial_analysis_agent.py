from agents.base_agent import BaseAgent
from tools.finance_data import FinanceDataTool
from tools.financial_analysis import FinancialAnalysisTool

class FinancialAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__("FinancialAnalysisAgent")
        self.finance_tool = FinanceDataTool()
        self.analysis_tool = FinancialAnalysisTool()

    def run(self, ticker: str):
        """
        Fetches financial data then computes ratios & scores.
        """
        summary = self.finance_tool.get_summary(ticker)
        financials = self.finance_tool.get_financials(ticker)

        ratios = self.analysis_tool.compute_ratios(summary, financials)
        score = self.analysis_tool.score_company(ratios)

        return {
            "ticker": ticker,
            "valuation_ratios": ratios,
            "score": score
        }
