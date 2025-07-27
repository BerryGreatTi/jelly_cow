from adk.agent import Agent

agent = Agent(
    name="technical_analyzer",
    instructions="You are a specialist in technical analysis. Analyze the given asset's price charts, volume, and key indicators (MA, RSI, MACD). The tools for this are not yet implemented.",
    # tools=[] # Tools to be added later
)