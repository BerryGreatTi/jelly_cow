from google.adk.agents import Agent
from google.adk.tools.load_web_page import load_web_page
from tools.na import get_company_news

agent = Agent(
    name="StockNewsAnalyzer",
    model="gemini-2.5-flash",
    
    description="Specialist of stock-specific news and sentiment analysis.",
    
    instruction=(
"You are a specialist in stock-specific news and sentiment analysis. "
"Your workflow is to first use the `get_company_news` tool to find recent articles for a given ticker. "
"Then, use the `load_web_page` tool with the URLs from the news articles to read their full content. "
"Finally, analyze the content to determine market sentiment and identify key issues related to the asset.\n"
"If the user asks for an explanation of a technical term or concept you used in your analysis (e.g., 'What is a P/E ratio?') or a company-specific technology (e.g., 'What is CUDA?'), provide a concise definition and briefly explain how it influenced your analysis or recommendation."
    ),
    
    tools=[
        get_company_news,
        load_web_page,
    ],
)