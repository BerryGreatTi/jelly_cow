from google.adk.agents import Agent
from tools.fa import (
    get_company_info,
    get_financial_summary,
    get_analyst_recommendations,
)

agent = Agent(
    name="FundamentalAnalyzer",
    model="gemini-2.5-flash",
    
    description="Specialist of stock fundamental analysis.",
    
    instruction=(
"You are a specialist in fundamental analysis. "
"Use the available tools to analyze the given company's financial health, valuation, and competitive advantages."
    ),
    
    tools=[
        get_company_info,
        get_financial_summary,
        get_analyst_recommendations,
    ]
)