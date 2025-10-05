import yfinance as yf
from typing import List, Dict, Any

def get_company_news(ticker: str) -> List[Dict[str, Any]]:
    """
    Retrieves recent news articles for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        List[Dict[str, Any]]: A list of news articles, where each article is a dictionary
                                containing title, publisher, link, and publish time.
    """
    stock = yf.Ticker(ticker)
    news = stock.news
    if news:
        # Return a curated list of dictionaries for easier processing
        return [
            {
                "title": article.get("content").get("title"),
                "publisher": article.get("content").get("provider").get("displayName"),
                "link": article.get("content").get("link"),
                "summary": article.get("content").get("summary"),
                "publishTime": article.get("content").get("pubDate"),
                "url": article.get("content").get("canonicalUrl").get("url"),
            }
            for article in news
        ]
    return "No news found for this ticker."
