import yfinance as yf
from datetime import datetime, timedelta

def get_exchange_rate(from_currency: str, to_currency: str) -> float | None:
    """
    Retrieves the exchange rate between two currencies using yfinance.

    Args:
        from_currency (str): The currency to convert from (e.g., "USD").
        to_currency (str): The currency to convert to (e.g., "KRW").

    Returns:
        float | None: The exchange rate, or None if it cannot be fetched.
    """
    if from_currency.upper() == to_currency.upper():
        return 1.0
    try:
        ticker_symbol = f"{from_currency.upper()}{to_currency.upper()}=X"
        ticker = yf.Ticker(ticker_symbol)
        # Use a recent period to get the latest rate
        data = ticker.history(period="5d")
        if not data.empty:
            return float(data['Close'].iloc[-1])
        else:
            print(f"Warning: No data for exchange rate {ticker_symbol}")
            return None
    except Exception as e:
        print(f"Error fetching exchange rate for {from_currency} to {to_currency}: {e}")
        return None

def get_current_prices(items: list[str], output_currency: str = "KRW") -> dict[str, float | None]:
    """
    Retrieves the current market price for a list of stock tickers and currency symbols.

    Args:
        items (list[str]): A list of stock tickers (e.g., "005930.KS", "AAPL") or
                             currency symbols (e.g., "USD", "EUR").
        output_currency (str): The desired output currency for the prices (e.g., "KRW", "USD").
                             Defaults to "KRW".

    Returns:
        dict[str, float | None]: A dictionary where keys are items and values are their current
                                 prices in the specified currency. A value is None if the price
                                 or exchange rate could not be fetched.
    """
    prices = {}
    for item in items:
        # Heuristic: If item is a 3-letter uppercase string, try treating it as a currency first.
        if len(item) == 3 and item.isupper():
            rate = get_exchange_rate(item, output_currency)
            # If a rate is found, we assume it's a currency and move to the next item.
            if rate is not None:
                prices[item] = rate
                continue

        # If not treated as a currency, process as a stock ticker.
        try:
            stock = yf.Ticker(item)
            hist = stock.history(period="2d")
            if hist.empty:
                print(f"Warning: No history found for ticker {item}")
                prices[item] = None
                continue
            
            last_price = hist['Close'].iloc[-1]
            
            stock_currency = stock.info.get('currency')
            if not stock_currency:
                print(f"Warning: Could not determine currency for {item}.")
                prices[item] = None
                continue

            if stock_currency.upper() == output_currency.upper():
                prices[item] = last_price
            else:
                exchange_rate = get_exchange_rate(stock_currency, output_currency)
                if exchange_rate is not None:
                    prices[item] = last_price * exchange_rate
                else:
                    prices[item] = None
        
        except Exception as e:
            print(f"Error fetching price for {item}: {e}")
            prices[item] = None
            
    return prices

def evaluate_portfolio(portfolio: dict, output_currency: str = "KRW") -> float | None:
    """
    Evaluates the total value of a given portfolio in a specified currency.

    The portfolio dictionary should have 'stocks' and 'cash' keys.
    - 'stocks': A dictionary of {ticker: shares}.
    - 'cash': A dictionary of {currency_code: amount}.

    Args:
        portfolio (dict): The portfolio dictionary from get_current_portfolio().
        output_currency (str): The currency to evaluate the portfolio in. Defaults to "KRW".

    Returns:
        float | None: The total portfolio value in the specified currency. Returns None
                      if the price for any item could not be determined, to avoid
                      returning a misleading partial value.
    """
    stock_tickers = list(portfolio.get('stocks', {}).keys())
    cash_currencies = list(portfolio.get('cash', {}).keys())
    
    all_items = stock_tickers + cash_currencies
    if not all_items:
        return 0.0
        
    item_prices = get_current_prices(all_items, output_currency)

    total_value = 0.0
    all_prices_found = True

    # Calculate value of stocks
    for ticker, shares in portfolio.get('stocks', {}).items():
        price = item_prices.get(ticker)
        if price is None:
            print(f"Warning: Could not determine price for stock {ticker}. Total value will be incomplete.")
            all_prices_found = False
            continue
        total_value += price * shares

    # Calculate value of cash
    for currency, amount in portfolio.get('cash', {}).items():
        rate = item_prices.get(currency)
        if rate is None:
            print(f"Warning: Could not determine exchange rate for cash {currency}. Total value will be incomplete.")
            all_prices_found = False
            continue
        total_value += rate * amount
        
    return float(total_value) if all_prices_found else None