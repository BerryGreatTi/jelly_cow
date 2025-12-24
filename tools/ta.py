import pandas_ta as ta
from pandas import DataFrame
import yfinance as yf
import pandas as pd
import numpy as np
from tools.fa import replace_nan_with_none

def get_ohlcv(ticker: str, period: str = "4mo") -> DataFrame:
    """
    Get historical market data (OHLCV) for a given ticker.

    Args:
        ticker (str): The stock ticker symbol.
        period (str): The period for which to download data (e.g., "1y", "6mo").

    Returns:
        DataFrame: A pandas DataFrame containing the OHLCV data. The data is ordered from oldest to newest.
    """
    df = yf.download(ticker, period=period, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    return df


def get_ohlcv_dict(ticker: str, limit: str = 30) -> DataFrame:
    """
    Get historical market data (OHLCV) for a given ticker.

    Args:
        ticker (str): The stock ticker symbol.
        limit (int): The number of recent data points to return.

    Returns:
        list[dict]: A list of dictionaries containing the OHLCV value, ordered from oldest to newest.
    """
    df = get_ohlcv(ticker)
    return df.tail(limit).to_dict("records")


def get_rsi(ticker: str, length: int = 14, limit: int = 30):
    """
    Calculate the Relative Strength Index (RSI) for a given ticker for a recent period.

    Args:
        ticker (str): The stock ticker symbol.
        length (int): The time period for RSI calculation.
        limit (int): The number of recent data points to return.

    Returns:
        list[dict]: A list of dictionaries containing the RSI value, ordered from oldest to newest.
    """
    df = get_ohlcv(ticker)
    indicator_data = df.ta.rsi(length=length)
    if isinstance(indicator_data, pd.DataFrame):
        indicator_series = indicator_data[f"RSI_{length}"]
    else:
        indicator_series = indicator_data

    rsi = indicator_series.to_frame("RSI")
    return rsi.tail(limit).to_dict("records")


def get_macd(ticker: str, fast: int = 12, slow: int = 26, signal: int = 9, limit: int = 30):
    """
    Calculate the Moving Average Convergence Divergence (MACD) for a given ticker for a recent period.

    Args:
        ticker (str): The stock ticker symbol.
        fast (int): The fast period for MACD calculation.
        slow (int): The slow period for MACD calculation.
        signal (int): The signal period for MACD calculation.
        limit (int): The number of recent data points to return.

    Returns:
        list[dict]: A list of dictionaries containing the MACD, histogram, and signal values, ordered from oldest to newest.
    """
    df = get_ohlcv(ticker)
    macd = df.ta.macd(fast=fast, slow=slow, signal=signal)
    macd.columns = ['MACD', 'Histogram', 'Signal']
    return macd.tail(limit).to_dict('records')


def get_moving_average(ticker: str, length: int = 20, limit: int = 30):
    """
    Calculate the Simple Moving Average (SMA) for a given ticker for a recent period.

    Args:
        ticker (str): The stock ticker symbol.
        length (int): The time period for SMA calculation.
        limit (int): The number of recent data points to return.

    Returns:
        list[dict]: A list of dictionaries containing the SMA value, ordered from oldest to newest.
    """
    # Adjust period if length is large (e.g., 200-day SMA requires > 4mo data)
    period = "4mo"
    if length > 50:
        period = "2y"
        
    df = get_ohlcv(ticker, period=period)
    # df.ta.sma might return a DataFrame with SMAs for O,H,L,C,V
    # We select the one for the close price, which is the default.
    indicator_data = df.ta.sma(length=length)
    
    if indicator_data is None: # Handle case where ta fails due to insufficient data
         return [{"SMA": None}] * limit

    if isinstance(indicator_data, pd.DataFrame):
        # Column name usually SMA_length
        col_name = f"SMA_{length}"
        if col_name in indicator_data.columns:
            indicator_series = indicator_data[col_name]
        else:
             # Fallback or error handling
             return [{"SMA": None}] * limit
    else:  # It's already a series
        indicator_series = indicator_data

    sma = indicator_series.to_frame("SMA")
    return sma.tail(limit).to_dict("records")


def get_bbands(ticker: str, length: int = 20, std: int = 2, limit: int = 30):
    """
    Calculate the Bollinger Bands for a given ticker for a recent period.

    Args:
        ticker (str): The stock ticker symbol.
        length (int): The time period for the moving average.
        std (int): The number of standard deviations.
        limit (int): The number of recent data points to return.

    Returns:
        list[dict]: A list of dictionaries with the upper, middle, and lower bands, band width and band percentage, ordered from oldest to newest.
    """
    df = get_ohlcv(ticker)
    bbands = df.ta.bbands(length=length, std=std)
    bbands.columns = ['BBL', 'BBM', 'BBU', 'BBB', 'BBP']
    return bbands.tail(limit).to_dict('records')


def get_obv(ticker: str, limit: int = 30):
    """
    Calculate the On-Balance Volume (OBV) for a given ticker for a recent period.

    Args:
        ticker (str): The stock ticker symbol.
        limit (int): The number of recent data points to return.

    Returns:
        list[dict]: A list of dictionaries containing the OBV value, ordered from oldest to newest.
    """
    df = get_ohlcv(ticker)
    indicator_data = df.ta.obv()
    if isinstance(indicator_data, pd.DataFrame):
        # Default OBV column name in pandas-ta is just 'OBV'
        indicator_series = indicator_data["OBV"]
    else:
        indicator_series = indicator_data

    obv = indicator_series.to_frame("OBV")
    return obv.tail(limit).to_dict("records")


def get_stoch(ticker: str, k: int = 14, d: int = 3, smooth_k: int = 3, limit: int = 30):
    """
    Calculate the Stochastic Oscillator for a given ticker for a recent period.

    Args:
        ticker (str): The stock ticker symbol.
        k (int): The time period for the %K line.
        d (int): The time period for the %D line (moving average of %K).
        smooth_k (int): The smoothing period for the %K line.
        limit (int): The number of recent data points to return.

    Returns:
        list[dict]: A list of dictionaries with the Stochastic %K, %D and %H values, ordered from oldest to newest.
    """
    df = get_ohlcv(ticker)
    stoch = df.ta.stoch(k=k, d=d, smooth_k=smooth_k)
    stoch.columns = ['STOCH_K', 'STOCH_D', 'STOCH_H']
    return stoch.tail(limit).to_dict('records')


def get_risk_metrics(ticker: str) -> dict:
    """
    Calculates key risk and quantitative metrics for a given ticker.
    Includes Volatility, MDD, Beta, Sharpe Ratio, and Sortino Ratio.
    """
    try:
        # 1. Market Detection & Benchmark Selection
        is_kr = ticker.endswith(('.KS', '.KQ'))
        benchmark_ticker = "^KS11" if is_kr else "^GSPC"
        
        # 2. Risk-Free Rate Fetching
        # Default fallback values
        risk_free_rate = 0.035 if is_kr else 0.045
        try:
            tnx = yf.Ticker("^TNX")
            tnx_info = tnx.info
            current_tnx = tnx_info.get('regularMarketPrice') or tnx_info.get('previousClose')
            if current_tnx:
                risk_free_rate = current_tnx / 100.0
        except:
            pass # Keep defaults

        # 3. Fetch 1-year history
        prices = yf.download([ticker, benchmark_ticker], period="1y", interval="1d", auto_adjust=True)['Close']
        if prices.empty or ticker not in prices.columns or benchmark_ticker not in prices.columns:
            return {"error": "Insufficient data to calculate risk metrics."}
        
        # 4. Return Calculations
        returns = prices.pct_change().dropna()
        stock_ret = returns[ticker]
        mkt_ret = returns[benchmark_ticker]
        
        # Annualized metrics
        ann_factor = 252
        annual_vol = stock_ret.std() * np.sqrt(ann_factor)
        
        # CAGR (Cumulative Annual Growth Rate)
        total_return = (prices[ticker].iloc[-1] / prices[ticker].iloc[0]) - 1
        days = (prices.index[-1] - prices.index[0]).days
        cagr = (1 + total_return)**(365.25/days) - 1 if days > 0 else total_return

        # 5. Beta Calculation
        covariance = stock_ret.cov(mkt_ret)
        market_variance = mkt_ret.var()
        beta = covariance / market_variance if market_variance != 0 else 1.0
        
        # 6. Risk-Adjusted Returns
        sharpe = (cagr - risk_free_rate) / annual_vol if annual_vol != 0 else 0
        
        # Sortino (Downside Deviation)
        downside_rets = stock_ret[stock_ret < 0]
        downside_std = downside_rets.std() * np.sqrt(ann_factor)
        sortino = (cagr - risk_free_rate) / downside_std if downside_std != 0 else 0
        
        # 7. Max Drawdown (MDD)
        cum_returns = (1 + stock_ret).cumprod()
        running_max = cum_returns.cummax()
        drawdown = (cum_returns - running_max) / running_max
        mdd = drawdown.min()

        return replace_nan_with_none({
            "ticker": ticker,
            "benchmark": benchmark_ticker,
            "risk_free_rate": round(risk_free_rate, 4),
            "annualized_volatility": round(annual_vol, 4),
            "cagr": round(cagr, 4),
            "beta": round(beta, 4),
            "sharpe_ratio": round(sharpe, 4),
            "sortino_ratio": round(sortino, 4),
            "max_drawdown": round(mdd, 4)
        })
    except Exception as e:
        return {"error": f"Failed to calculate risk metrics: {str(e)}"}