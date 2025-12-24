import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.fa import get_advanced_financial_metrics
from tools.ta import get_risk_metrics
from tools.portfolio_math import get_portfolio_analysis
import json

def test_fundamental_metrics():
    print("=== Testing Fundamental Metrics (AAPL) ===")
    res = get_advanced_financial_metrics("AAPL")
    print(json.dumps(res, indent=2))
    assert "ROIC" in res
    assert "FCF" in res
    assert "Altman_Z_Score" in res
    assert "EV_EBITDA" in res
    print("SUCCESS\n")

def test_risk_metrics():
    print("=== Testing Risk Metrics (NVDA) ===")
    res = get_risk_metrics("NVDA")
    print(json.dumps(res, indent=2))
    assert "sharpe_ratio" in res
    assert "beta" in res
    assert "max_drawdown" in res
    print("SUCCESS\n")

def test_portfolio_analysis():
    print("=== Testing Portfolio Analysis ===")
    portfolio = [
        {"ticker": "AAPL", "market_value": 10000},
        {"ticker": "MSFT", "market_value": 10000},
        {"ticker": "KO", "market_value": 5000}
    ]
    res = get_portfolio_analysis(portfolio)
    print(json.dumps(res, indent=2))
    assert "hhi" in res
    assert "correlation_matrix" in res
    assert len(res["significant_pairs"]) > 0
    print("SUCCESS\n")

if __name__ == "__main__":
    try:
        test_fundamental_metrics()
        test_risk_metrics()
        test_portfolio_analysis()
        print("All Manual Verification Passed!")
    except Exception as e:
        print(f"VERIFICATION FAILED: {e}")
