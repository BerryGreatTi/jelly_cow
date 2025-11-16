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
from agents.stock_news_analyzer import agent as StockNewsAnalyzer

agent = Agent(
    name="FundamentalAnalyzer",
    model="gemini-2.5-flash",
    
    description="Specialist of stock fundamental analysis.",
    
    instruction=(
"You are a specialist in fundamental analysis. Your goal is to provide a comprehensive assessment of a company's financial health, valuation, and competitive position. Your analysis must include a dedicated 'Business Risk Analysis' section."
"\n\n1. **Financial Health Analysis:** Use the available tools to analyze the company's financial statements (income statement, balance sheet, cash flow) over multiple periods to identify trends, key financial metrics, analyst recommendations, major shareholders, and insider transactions."
"\n\n2. **Business Risk Analysis:** Based on the company's business summary, financial metrics (e.g., high debt, declining growth), and by delegating to news analysis agents (`StockNewsAnalyzer` or `MarketNewsAnalyzer`), identify key business risks. These risks should include, but not be limited to, changes in raw material prices, increases in operational cost structure, and market contraction. For each risk, describe it and analyze its recent trend (e.g., increasing, decreasing, stable), citing supporting data or news."
"\n\n3. **Synthesis:** Combine your financial health analysis and risk analysis into a single, comprehensive report."
"\n\nFor broader market analysis, such as industry trends or competitive landscape, delegate the task to the `MarketNewsAnalyzer` agent."
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
        AgentTool(agent=StockNewsAnalyzer),
    ]
)