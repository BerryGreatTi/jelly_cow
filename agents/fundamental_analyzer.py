from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from tools.fa import (
    get_company_info,
    get_financial_summary,
    get_analyst_recommendations,
    get_income_statement,
    get_balance_sheet,
    get_cash_flow,
    get_major_shareholders,
    get_insider_transactions,
)
from agents.market_news_analyzer import agent as MarketNewsAnalyzer

agent = Agent(
    name="FundamentalAnalyzer",
    model="gemini-2.5-flash",
    
    description="Specialist of stock fundamental analysis.",
    
    instruction=(
"You are a specialist in fundamental analysis. Your goal is to provide a comprehensive assessment of a company's financial health, valuation, and competitive position. "
"Use the available tools to analyze the given company's financial statements (income statement, balance sheet, cash flow) over multiple periods to identify trends, "
"key financial metrics, analyst recommendations, major shareholders, and insider transactions. "
"For broader market analysis, such as industry trends, competitive landscape, or raw material costs, delegate the task to the MarketNewsAnalyzer agent."
    ),
    
    tools=[
        get_company_info,
        get_financial_summary,
        get_analyst_recommendations,
        get_income_statement,
        get_balance_sheet,
        get_cash_flow,
        get_major_shareholders,
        get_insider_transactions,
        AgentTool(agent=MarketNewsAnalyzer),
    ]
)