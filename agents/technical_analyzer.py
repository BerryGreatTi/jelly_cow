from google.adk.agents import Agent
from tools.ta import (
    get_current_rsi,
    get_current_macd,
    get_current_moving_average,
    get_current_bbands,
    get_current_obv,
    get_current_stoch,
)

agent = Agent(
    name="TechnicalAnalyzer",
    model="gemini-2.5-flash",

    description="Specialist of stock technical analysis.",
    
    instruction=(
"You are a specialist in technical analysis. "
"Analyze the given asset's price charts, volume, and key indicators (MA, RSI, MACD, Bollinger Bands, OBV, Stochastic Oscillator)."
    ),
    
    tools=[
        get_current_rsi,
        get_current_macd,
        get_current_moving_average,
        get_current_bbands,
        get_current_obv,
        get_current_stoch,
    ],
)