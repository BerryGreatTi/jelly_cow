import pandas_ta as ta
from pandas import DataFrame
import yfinance as yf


def get_ohlcv(ticker: str, period: str = "1y") -> DataFrame:
    """
    Get historical market data (OHLCV) for a given ticker.

    Args:
        ticker (str): The stock ticker symbol.
        period (str): The period for which to download data (e.g., "1y", "6mo").

    Returns:
        DataFrame: A pandas DataFrame containing the OHLCV data.
    """
    return yf.download(ticker, period=period)


def get_current_rsi(ticker: str, length: int = 14):
    """
    Calculate the current Relative Strength Index (RSI) for a given ticker.

    Args:
        ticker (str): The stock ticker symbol.
        length (int): The time period for RSI calculation.

    Returns:
        float: The current RSI value.
    """
    df = get_ohlcv(ticker)
    rsi = df.ta.rsi(length=length)
    return rsi.iloc[-1]


def get_current_macd(ticker: str, fast: int = 12, slow: int = 26, signal: int = 9):
    """
    Calculate the current Moving Average Convergence Divergence (MACD) for a given ticker.

    Args:
        ticker (str): The stock ticker symbol.
        fast (int): The fast period for MACD calculation.
        slow (int): The slow period for MACD calculation.
        signal (int): The signal period for MACD calculation.

    Returns:
        dict: A dictionary containing the current MACD, histogram, and signal values.
    """
    df = get_ohlcv(ticker)
    macd = df.ta.macd(fast=fast, slow=slow, signal=signal)
    return macd.iloc[-1].to_dict()


def get_current_moving_average(ticker: str, length: int = 20):
    """
    Calculate the current Simple Moving Average (SMA) for a given ticker.

    Args:
        ticker (str): The stock ticker symbol.
        length (int): The time period for SMA calculation.

    Returns:
        float: The current SMA value.
    """
    df = get_ohlcv(ticker)
    sma = df.ta.sma(length=length)
    return sma.iloc[-1]


def get_current_bbands(ticker: str, length: int = 20, std: int = 2):
    """
    Calculate the current Bollinger Bands for a given ticker.

    Args:
        ticker (str): The stock ticker symbol.
        length (int): The time period for the moving average.
        std (int): The number of standard deviations.

    Returns:
        dict: A dictionary with the current upper, middle, and lower bands.
    """
    df = get_ohlcv(ticker)
    bbands = df.ta.bbands(length=length, std=std)
    return bbands.iloc[-1].to_dict()


def get_current_obv(ticker: str):
    """
    Calculate the current On-Balance Volume (OBV) for a given ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        float: The current OBV value.
    """
    df = get_ohlcv(ticker)
    obv = df.ta.obv()
    return obv.iloc[-1]


def get_current_stoch(ticker: str, k: int = 14, d: int = 3, smooth_k: int = 3):
    """
    Calculate the current Stochastic Oscillator for a given ticker.

    Args:
        ticker (str): The stock ticker symbol.
        k (int): The time period for the %K line.
        d (int): The time period for the %D line (moving average of %K).
        smooth_k (int): The smoothing period for the %K line.

    Returns:
        dict: A dictionary with the current Stochastic %K and %D values.
    """
    df = get_ohlcv(ticker)
    stoch = df.ta.stoch(k=k, d=d, smooth_k=smooth_k)
    return stoch.iloc[-1].to_dict()
