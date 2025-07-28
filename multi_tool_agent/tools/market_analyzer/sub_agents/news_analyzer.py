from google.adk.agents import Agent

agent = Agent(
    name="news_analyzer",
    instruction="You are a specialist in news and sentiment analysis. Find recent news, analyze market sentiment, and identify key issues related to the given asset. The tools for this are not yet implemented.",
    # tools=[] # Tools to be added later
)