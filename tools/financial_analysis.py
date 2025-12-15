import pandas as pd
import numpy as np

class FinancialAnalysisTool:
    """
    Computes financial ratios and growth metrics
    using Yahoo Finance data.
    """

    def compute_ratios(self, summary: dict, financials: dict):
        ratios = {}

        try:
            # Valuation ratios
            ratios["PE_ratio"] = summary.get("trailingPE")
            ratios["PEG_ratio"] = summary.get("pegRatio")
            ratios["Price_to_Book"] = summary.get("priceToBook")
            ratios["Price_to_Sales"] = summary.get("priceToSalesTrailing12Months")

            # Enterprise value ratios
            ev = summary.get("enterpriseValue")
            revenue = summary.get("totalRevenue")
            ebitda = summary.get("ebitda")

            if ev and revenue:
                ratios["EV_to_Revenue"] = ev / revenue

            if ev and ebitda:
                ratios["EV_to_EBITDA"] = ev / ebitda

            # Profitability margins
            income = financials["income_statement"]
            revenue_row = income.loc["Total Revenue"].iloc[0] if "Total Revenue" in income.index else None
            gross_profit = income.loc["Gross Profit"].iloc[0] if "Gross Profit" in income.index else None
            net_income = income.loc["Net Income"].iloc[0] if "Net Income" in income.index else None

            if revenue_row and gross_profit:
                ratios["Gross_Margin"] = gross_profit / revenue_row

            if revenue_row and net_income:
                ratios["Net_Margin"] = net_income / revenue_row

            # Growth (YoY revenue)
            if "Total Revenue" in income.index and len(income.columns) >= 2:
                curr = income.loc["Total Revenue"].iloc[0]
                prev = income.loc["Total Revenue"].iloc[1]
                ratios["Revenue_YoY_Growth"] = (curr - prev) / prev if prev else None

            # Balance sheet metrics
            balance = financials["balance_sheet"]
            if "Total Debt" in balance.index and "Total Stockholder Equity" in balance.index:
                debt = balance.loc["Total Debt"].iloc[0]
                equity = balance.loc["Total Stockholder Equity"].iloc[0]
                ratios["Debt_to_Equity"] = debt / equity if equity else None

            # Cashflow ratios
            cashflow = financials["cashflow"]
            if "Free Cash Flow" in cashflow.index:
                ratios["Free_Cash_Flow"] = cashflow.loc["Free Cash Flow"].iloc[0]

        except Exception as e:
            ratios["error"] = str(e)

        return ratios

    def score_company(self, ratios):
        """
        Basic heuristic scoring system.
        """
        score = 0

        if ratios.get("PE_ratio") and ratios["PE_ratio"] < 20:
            score += 1
        if ratios.get("Revenue_YoY_Growth") and ratios["Revenue_YoY_Growth"] > 0.10:
            score += 1
        if ratios.get("Net_Margin") and ratios["Net_Margin"] > 0.10:
            score += 1
        if ratios.get("Debt_to_Equity") and ratios["Debt_to_Equity"] < 1:
            score += 1

        if score >= 3:
            return "Strong"
        elif score == 2:
            return "Mixed"
        else:
            return "Weak"
