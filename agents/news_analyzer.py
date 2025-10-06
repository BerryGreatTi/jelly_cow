from google.adk.agents import Agent
from google.adk.tools.load_web_page import load_web_page
from tools.na import get_company_news

agent = Agent(
    name="NewsAnalyzer",
    model="gemini-2.5-flash",
    
    description="Specialist of news and sentiment analysis about economy, market, industry, sector and company.",
    
    instruction=(
"You are a specialist in news and sentiment analysis. "
"Your workflow is to first use the `get_company_news` tool to find recent articles for a given ticker. "
"Then, use the `load_web_page` tool with the URLs from the news articles to read their full content. "
"Finally, analyze the content to determine market sentiment and identify key issues related to the asset."
    ),
    
    tools=[
        get_company_news,
        load_web_page,
    ],
)