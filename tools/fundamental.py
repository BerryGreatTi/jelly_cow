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
