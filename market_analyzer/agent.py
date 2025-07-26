import yfinance as yf
import numpy as np
import pykrx
from google.adk.agents import Agent

def get_momentum_data(code: str) -> dict:
    """Retrieves recent momentum values recent days.

    Args:
        code (str): The ticker of the asset for which to retrieve the momentum data.

    Returns:
        dict: status and result or error msg.
    """
    
    short_term_length = 5
    long_term_length = 10

    try:
        # data = yf.Ticker(code).history('1y')
        data = pykrx.stock.get_market_ohlcv("20240711","20250711",code)
        data["Close"] = data["종가"]
        
        data["short-day"] = data["Close"].rolling(short_term_length).mean().shift()
        data["long-day"] = data["Close"].rolling(long_term_length).mean().shift()
        data.iloc[long_term_length:long_term_length+5]
        data["signal"] = np.where(data["short-day"] > data["long-day"], 1, 0)
        data["signal"] = np.where(data["short-day"] < data["long-day"], -1, data["signal"])
        data["momentum"] = data["short-day"] - data["long-day"]
        data = data["momentum"].iloc[-90:]
        data.index = data.index.map(lambda x: x.strftime("%Y-%m-%d"))
        data = data.to_json()

        return {
            "status": "success",
            "report": data,
        }
    except:
        return {
            "status": "error",
            "error_message": f"Tha momemtum data for '{code}' is not available.",
        }


root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.5-pro",
    description=(
        "Agent to perform ."
    ),
    instruction=(
        "You are an helpful analyst to perform the quantitative analysis of stock prices. "
        "Your job is to perform analysis from the retrieve momentum data. "
        "You provide the detail analysis report to user. "
        "But DON'T PROVIDE A MENTION DIRECTLY TO BUY OR SELL OF THE ASSET."
    ),
    tools=[get_momentum_data,],
)