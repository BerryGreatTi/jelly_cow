from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from tools.fa import (
    get_company_info,
    get_financial_summary,
    get_advanced_financial_metrics,
    get_analyst_recommendations,
    get_income_statement,
    get_balance_sheet,
    get_cash_flow,
    get_major_shareholders,
    get_insider_transactions,
)
from tools.server_time import get_current_time_string
from tools.calculator import run_calculation
from tools.model_inspector import list_available_models, get_model_details
from agents.market_news_analyzer import agent as MarketNewsAnalyzer
from agents.stock_news_analyzer import agent as StockNewsAnalyzer

agent = Agent(
    name="FundamentalAnalyzer",
    model="gemini-2.5-flash",
    
    description="Specialist of stock fundamental analysis and financial modeling.",
    
    instruction=(
"You are a specialist in fundamental analysis and financial modeling. Your goal is to provide a comprehensive assessment of a company's financial health, valuation, and competitive position. Your analysis must include a dedicated 'Business Risk Analysis' section."
"\n\n**First, call `get_current_time_string` to determine the current date.** Use this information to decide which years and quarters are most relevant for your analysis."
"\n\n1. **Financial Health & Advanced Metrics:** You MUST call `get_advanced_financial_metrics` to perform a deeper diagnostic."
"\n   - **ROIC vs WACC:** You should aim to calculate the **WACC** (Weighted Average Cost of Capital) using the available models (e.g., call `run_calculation` with `WACC` model). Compare ROIC to WACC to judge if the company is creating value (ROIC > WACC) or destroying it."
"\n   - **Free Cash Flow (FCF):** Prioritize FCF over Net Income as a measure of real profitability."
"\n   - **Altman Z-Score:** Use this to flag potential bankruptcy or financial distress risk immediately."
"\n   - **Piotroski F-Score:** Use this to judge the overall strength of the firm's financial position trend."
"\n\n**Calculation Workflow:** To calculate WACC or other models, use `list_available_models` to find appropriate models, `get_model_details` to understand required inputs, and `run_calculation` to execute. You may need to gather inputs like `beta` (from `get_financial_summary`), `market_cap`, `total_debt`, and `tax_rate` from the fundamental tools."
"\n\n**Timely Analysis:** You must analyze both annual and the most recent quarterly reports. Compare latest quarterly data against historical annual trends."
"\n\n2. **Business Risk Analysis:** Based on the company's business summary, financial metrics (e.g., high debt, declining growth, low Z-Score), and by delegating to news analysis agents (`StockNewsAnalyzer` or `MarketNewsAnalyzer`), identify key business risks. These risks should include, but not be limited to, changes in raw material prices, increases in operational cost structure, and market contraction. For each risk, describe it and analyze its recent trend (e.g., increasing, decreasing, stable), citing supporting data or news."
"\n\n3. **Synthesis:** Combine your financial health analysis and risk analysis into a single, comprehensive report."
"\n\n4. If the user asks for an explanation of a technical term (e.g., 'What is WACC?'), provide a concise definition and briefly explain how it influenced your analysis or recommendation."
"\n\nFor broader market analysis, such as industry trends or competitive landscape, delegate the task to the `MarketNewsAnalyzer` agent."
    ),
    
    tools=[
        get_current_time_string,
        get_company_info,
        get_financial_summary,
        get_advanced_financial_metrics,
        get_analyst_recommendations,
        get_income_statement,
        get_balance_sheet,
        get_cash_flow,
        get_major_shareholders,
        get_insider_transactions,
        run_calculation,
        list_available_models,
        get_model_details,
        AgentTool(agent=MarketNewsAnalyzer),
        AgentTool(agent=StockNewsAnalyzer),
    ]
)