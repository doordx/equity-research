import yfinance as yf
import pandas as pd

class FinanceDataTool:
    """
    Simple wrapper around Yahoo Finance (yfinance).
    Fetches price data, financial statements, and key metrics.
    """

    def get_price_history(self, ticker: str, period="1y", interval="1d"):
        """
        Fetch historical price data.
        """
        stock = yf.Ticker(ticker)
        data = stock.history(period=period, interval=interval)

        return data.reset_index()

    def get_summary(self, ticker: str):
        """
        Fetch general company info & key metrics.
        """
        stock = yf.Ticker(ticker)
        info = stock.info   # returns dict
        return info

    def get_financials(self, ticker: str):
        """
        Fetch financial statements (income, balance sheet, cashflow)
        """
        stock = yf.Ticker(ticker)
        return {
            "income_statement": stock.financials,
            "balance_sheet": stock.balance_sheet,
            "cashflow": stock.cashflow
        }
