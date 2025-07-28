from google.adk.agents import Agent

agent = Agent(
    name="technical_analyzer",
    instruction="You are a specialist in technical analysis. Analyze the given asset's price charts, volume, and key indicators (MA, RSI, MACD). The tools for this are not yet implemented.",
    # tools=[] # Tools to be added later
)