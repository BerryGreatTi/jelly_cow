from google.adk.agents import Agent
from google.adk.tools import google_search

agent = Agent(
    name="MarketNewsAnalyzer",
    model="gemini-2.5-flash",
    
    description="Provides analysis of market conditions, raw materials, and cost factors for a company's products and services.",
    
    instruction=(
"You are a market research analyst. "
"Your role is to analyze the overall market situation for a company's products or services, including the status of raw materials and other cost factors. "
"Use the available web search tool to find and synthesize information from news articles, industry reports, and other web sources. "
"Specifically, identify peer companies for comparative analysis and research relevant broad economic indicators (e.g., GDP growth, inflation, interest rates) that could impact the company or industry. "
"Provide a comprehensive overview of the market landscape, including competitive analysis and economic context."
    ),
    
    tools=[
        google_search,
    ]
)
