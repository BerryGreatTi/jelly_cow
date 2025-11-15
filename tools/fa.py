import yfinance as yf
from typing import Dict, Any

def get_company_info(ticker: str) -> Dict[str, Any]:
    """
    Retrieves general information about a company for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        Dict[str, Any]: A dictionary containing the company's name, sector, industry, and summary.
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "longName": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "longBusinessSummary": info.get("longBusinessSummary"),
    }

def get_financial_summary(ticker: str) -> Dict[str, Any]:
    """
    Retrieves a summary of key financial metrics for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        Dict[str, Any]: A dictionary of key financial ratios and metrics.
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "marketCap": info.get("marketCap"),
        "trailingPE": info.get("trailingPE"),
        "forwardPE": info.get("forwardPE"),
        "priceToBook": info.get("priceToBook"),
        "priceToSales": info.get("priceToSalesTrailing12Months"),
        "evToEbitda": info.get("enterpriseToEbitda"),
        "dividendYield": info.get("dividendYield"),
        "payoutRatio": info.get("payoutRatio"),
        "debtToEquity": info.get("debtToEquity"),
        "revenueGrowth": info.get("revenueGrowth"),
        "earningsGrowth": info.get("earningsGrowth"),
    }

def get_analyst_recommendations(ticker: str) -> Any:
    """
    Retrieves the latest analyst recommendations for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        Any: A summary of the latest analyst recommendations, usually a DataFrame.
    """
    stock = yf.Ticker(ticker)
    recommendations = stock.recommendations
    # Return the most recent recommendations if the table is large
    if recommendations is not None and not recommendations.empty:
        return recommendations.tail(5).to_dict('records')
    return "No analyst recommendations found."

def get_income_statement(ticker: str) -> Any:
    """
    Retrieves the income statement for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        Any: The income statement, usually a DataFrame.
    """
    stock = yf.Ticker(ticker)
    income_stmt = stock.income_stmt
    if income_stmt is not None and not income_stmt.empty:
        return income_stmt.to_dict()
    return "No income statement found."

def get_balance_sheet(ticker: str) -> Any:
    """
    Retrieves the balance sheet for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        Any: The balance sheet, usually a DataFrame.
    """
    stock = yf.Ticker(ticker)
    balance_sheet = stock.balance_sheet
    if balance_sheet is not None and not balance_sheet.empty:
        return balance_sheet.to_dict()
    return "No balance sheet found."

def get_cash_flow(ticker: str) -> Any:
    """
    Retrieves the cash flow statement for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        Any: The cash flow statement, usually a DataFrame.
    """
    stock = yf.Ticker(ticker)
    cash_flow = stock.cashflow
    if cash_flow is not None and not cash_flow.empty:
        return cash_flow.to_dict()
    return "No cash flow statement found."

def get_major_shareholders(ticker: str) -> Any:
    """
    Retrieves major institutional shareholders for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        Any: Major shareholders data, usually a DataFrame.
    """
    stock = yf.Ticker(ticker)
    major_holders = stock.major_holders
    if major_holders is not None and not major_holders.empty:
        return major_holders.to_dict()
    return "No major shareholders found."

def get_insider_transactions(ticker: str) -> Any:
    """
    Retrieves insider transactions for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        Any: Insider transactions data, usually a DataFrame.
    """
    stock = yf.Ticker(ticker)
    insider_transactions = stock.insider_transactions
    if insider_transactions is not None and not insider_transactions.empty:
        return insider_transactions.to_dict()
    return "No insider transactions found."
