import yfinance as yf
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from tools.fa import replace_nan_with_none

def get_portfolio_analysis(portfolio: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Performs scientific portfolio analysis including Correlation Matrix, 
    Weights, and Concentration Risk (HHI).
    
    Args:
        portfolio: List of dicts with 'ticker' and 'market_value'.
        
    Returns:
        Dict: Analysis results.
    """
    try:
        if not portfolio:
            return {"error": "Portfolio is empty."}

        tickers = [item['ticker'] for item in portfolio]
        market_values = {item['ticker']: item['market_value'] for item in portfolio}
        total_value = sum(market_values.values())
        
        # 1. Weights Calculation
        weights = {ticker: val / total_value for ticker, val in market_values.items()}
        
        # 2. HHI (Herfindahl-Hirschman Index)
        # HHI = sum(weight^2) * 10000. 
        # < 1500: Unconcentrated, 1500-2500: Moderate, > 2500: Highly Concentrated.
        hhi = sum((w * 100)**2 for w in weights.values())
        
        # 3. Correlation Matrix
        # Fetch 1-year daily returns
        if len(tickers) > 1:
            data = yf.download(tickers, period="1y", interval="1d", auto_adjust=True)['Close']
            
            # Handle Single Ticker if yfinance returns Series instead of DataFrame
            if isinstance(data, pd.Series):
                data = data.to_frame()
                
            returns = data.pct_change().dropna()
            corr_matrix = returns.corr()
            
            # Find highly correlated pairs (> 0.7)
            high_corr_pairs = []
            cols = corr_matrix.columns
            for i in range(len(cols)):
                for j in range(i + 1, len(cols)):
                    val = corr_matrix.iloc[i, j]
                    if val > 0.7:
                        high_corr_pairs.append({
                            "pair": [cols[i], cols[j]],
                            "correlation": round(val, 4),
                            "risk": "High"
                        })
                    elif val < 0:
                        high_corr_pairs.append({
                            "pair": [cols[i], cols[j]],
                            "correlation": round(val, 4),
                            "risk": "Hedge/Negative"
                        })
            
            corr_dict = corr_matrix.to_dict()
        else:
            corr_dict = {}
            high_corr_pairs = []

        return replace_nan_with_none({
            "weights": {t: round(w, 4) for t, w in weights.items()},
            "hhi": round(hhi, 2),
            "concentration_level": "High" if hhi > 2500 else "Moderate" if hhi > 1500 else "Low",
            "correlation_matrix": corr_dict,
            "significant_pairs": high_corr_pairs,
            "total_market_value": total_value
        })

    except Exception as e:
        return {"error": f"Failed to analyze portfolio: {str(e)}"}
