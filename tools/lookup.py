"""
This tool file is for lookup functionalities like finding tickers.
It requires an FMP_API_KEY in the environment variables.
"""
import os
import requests

API_KEY = os.environ.get("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com/api/v3"


def fmp_symbol_search(query: str) -> list[dict]:
    """
    Searches for stock symbols using a company name via the FMP Search API.
    
    Args:
        query: The company name to search for (preferably in English).
        
    Returns:
        A list of dictionaries with potential matches, including symbol, name, and exchange.
    """
    if not API_KEY:
        return {"error": "FMP_API_KEY is not set in environment variables."}

    params = {
        "query": query,
        "limit": 10,
        "apikey": API_KEY,
    }
    
    response = requests.get(f"{BASE_URL}/search-name", params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"API request failed with status code {response.status_code}", "details": response.text}
