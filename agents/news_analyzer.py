from google.adk.agents import Agent

agent = Agent(
    name="NewsAnalyzer",
    model="gemini-2.5-flash",
    
    description="Specialist of news and sentiment analysis about economy, market, industry, sector and company.",
    
    instruction=(
"You are a specialist in news and sentiment analysis. "
"Find recent news, analyze market sentiment, and identify key issues related to the given asset. "
"The tools for this are not yet implemented."
    ),
    
    tools=[],
)