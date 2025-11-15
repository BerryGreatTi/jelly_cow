"""
This tool file is for stock screening.
It requires an FMP_API_KEY in the environment variables.
"""
import os
import requests

API_KEY = os.environ.get("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com/api/v3"


def run_screener_query(
    market_cap_more_than: int = None,
    market_cap_lower_than: int = None,
    price_more_than: int = None,
    price_lower_than: int = None,
    beta_more_than: float = None,
    beta_lower_than: float = None,
    volume_more_than: int = None,
    volume_lower_than: int = None,
    dividend_more_than: float = None,
    dividend_lower_than: float = None,
    is_etf: bool = None,
    is_actively_trading: bool = True,
    sector: str = None,
    industry: str = None,
    country: str = "US",
    exchange: str = None,
    limit: int = 100,
) -> list[dict]:
    """
    Filters stocks based on fundamental and market data using the FMP Stock Screener API.
    
    Args:
        market_cap_more_than: Minimum market capitalization.
        market_cap_lower_than: Maximum market capitalization.
        price_more_than: Minimum stock price.
        price_lower_than: Maximum stock price.
        beta_more_than: Minimum beta.
        beta_lower_than: Maximum beta.
        volume_more_than: Minimum trading volume.
        volume_lower_than: Maximum trading volume.
        dividend_more_than: Minimum dividend yield.
        dividend_lower_than: Maximum dividend yield.
        is_etf: Set to True to include ETFs.
        is_actively_trading: Set to True to only include actively trading stocks.
        sector: The stock sector (e.g., "Technology").
        industry: The stock industry (e.g., "Software").
        country: The country of the stocks (e.g., "US").
        exchange: The stock exchange (e.g., "NASDAQ").
        limit: The maximum number of results to return.
        
    Returns:
        A list of dictionaries, where each dictionary represents a stock matching the criteria.
    """
    if not API_KEY:
        return {"error": "FMP_API_KEY is not set in environment variables."}

    params = {
        "marketCapMoreThan": market_cap_more_than,
        "marketCapLowerThan": market_cap_lower_than,
        "priceMoreThan": price_more_than,
        "priceLowerThan": price_lower_than,
        "betaMoreThan": beta_more_than,
        "betaLowerThan": beta_lower_than,
        "volumeMoreThan": volume_more_than,
        "volumeLowerThan": volume_lower_than,
        "dividendMoreThan": dividend_more_than,
        "dividendLowerThan": dividend_lower_than,
        "isEtf": is_etf,
        "isActivelyTrading": is_actively_trading,
        "sector": sector,
        "industry": industry,
        "country": country,
        "exchange": exchange,
        "limit": limit,
        "apikey": API_KEY,
    }
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}
    
    response = requests.get(f"{BASE_URL}/stock-screener", params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"API request failed with status code {response.status_code}", "details": response.text}


def get_technical_indicator(
    symbol: str,
    period: int,
    indicator_type: str,
    from_date: str = None,
    to_date: str = None,
) -> list[dict]:
    """
    Fetches daily technical indicator data for a given stock symbol from the FMP API.
    
    Args:
        symbol: The stock symbol (e.g., "AAPL").
        period: The time period for the indicator (e.g., 10 for 10-day SMA).
        indicator_type: The type of indicator. Supported values include 'sma', 'ema', 'rsi', 'standardDeviation', etc.
        from_date: The start date in YYYY-MM-DD format.
        to_date: The end date in YYYY-MM-DD format.
        
    Returns:
        A list of dictionaries containing the technical indicator data over time.
    """
    if not API_KEY:
        return {"error": "FMP_API_KEY is not set in environment variables."}

    params = {
        "period": period,
        "apikey": API_KEY,
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    url = f"{BASE_URL}/technical_indicator/daily/{symbol}?type={indicator_type}"
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"API request failed with status code {response.status_code}", "details": response.text}
