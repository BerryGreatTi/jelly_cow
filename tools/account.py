import os
from apis.koreainvestment import KoreaInvestmentAPI_mockup


account = KoreaInvestmentAPI_mockup(os.environ.get('KIS_PROFILE_PATH'))

def get_current_portfolio():
    """
    Retrieves the current investment portfolio, including stocks and cash balances.

    Returns:
        dict: A dictionary with two keys:
              'stocks': A dict where keys are tickers and values are share counts.
              'cash': A dict where keys are currency codes (e.g., "KRW", "USD")
                      and values are the cash amounts.
    """
    # This is a mock implementation.
    # In a real scenario, this would fetch data from a brokerage account.
    return account.inquire_account_balance()['message']

