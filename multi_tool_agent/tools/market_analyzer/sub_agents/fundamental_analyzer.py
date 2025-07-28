from google.adk.agents import Agent

agent = Agent(
    name="fundamental_analyzer",
    instruction="You are a specialist in fundamental analysis. Analyze the given company's financial health, valuation, and competitive advantages. The tools for this are not yet implemented.",
    # tools=[] # Tools to be added later
)