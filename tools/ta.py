import pandas_ta as ta
from pandas import DataFrame
import yfinance as yf
import pandas as pd


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


def get_rsi(ticker: str, length: int = 14, limit: int = 30):
    """
    Calculate the Relative Strength Index (RSI) for a given ticker for a recent period.

    Args:
        ticker (str): The stock ticker symbol.
        length (int): The time period for RSI calculation.
        limit (int): The number of recent data points to return.

    Returns:
        list[float]: A list of RSI values, ordered from oldest to newest.
    """
    df = get_ohlcv(ticker)
    rsi = df.ta.rsi(length=length)
    return rsi.tail(limit).tolist()


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
        list[float]: A list of SMA values, ordered from oldest to newest.
    """
    df = get_ohlcv(ticker)
    sma = df.ta.sma(length=length)
    return sma.tail(limit).tolist()


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
        list[float]: A list of OBV values, ordered from oldest to newest.
    """
    df = get_ohlcv(ticker)
    obv = df.ta.obv()
    return obv.tail(limit).tolist()


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