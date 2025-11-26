from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

# Low-level specialist agents
from agents.fundamental_analyzer import agent as fundamental_analyzer
from agents.technical_analyzer import agent as technical_analyzer
from agents.stock_news_analyzer import agent as stock_news_analyzer
from agents.market_news_analyzer import agent as market_news_analyzer

# Mid-level comprehensive analyzer agent
from agents.single_asset_analyzer_agent import agent as single_asset_analyzer_agent

# High-level workflow agents
from agents.portfolio_analyzer_agent import agent as portfolio_analyzer_agent
from agents.recommender_agent import agent as recommender_agent

# Utility agents
from agents.ticker_lookup_agent import agent as ticker_lookup_agent

# Other tools
from apis.notion import create_notion_page
from tools.server_time import get_current_time_string


agent = Agent(
    name="JellyMonster",
    model="gemini-2.5-flash",
    description="A master financial agent that orchestrates tasks by delegating to a team of specialist agents.",
    instruction=(
        "You are a master financial agent, an orchestrator that delegates tasks to specialist agents. "
        "Your primary goal is to understand the user's intent and route the request. All responses should be in Korean.\n"
        "\n"
        "**Workflow based on User Intent**\n"
        "You must first determine the user's goal. There are two main paths:\n"
        "\n"
        "**Path 1: Standard Analysis Request (Default)**\n"
        "- If the user asks for an analysis (e.g., '삼성전자 분석해줘', 'AAPL 전망이 어때?'), your process is:\n"
        "  1. Delegate to the appropriate specialist agent (e.g., `SingleAssetAnalyzer`) to get a **full, detailed analysis report**.\n"
        "  2. Once you receive the detailed report, your next task is to **create a concise summary** of that report. The summary must be **under 2500 characters**.\n"
        "  3. Format this summary using Slack Block Kit JSON and send it as the final response. **Do NOT create a Notion page in this case.**\n"
        "\n"
        "**Path 2: Explicit Notion Report Request**\n"
        "- If the user explicitly asks to create a report on Notion (e.g., '자세한 리포트를 노션에 만들어줘', '노션에 포스팅해줘'), your process is:\n"
        "  1. Delegate to the appropriate specialist agent to get the **full, detailed analysis report**. The detailed report content (for Notion) should be written in Korean, unless the user explicitly requests otherwise.\n"
        "  2. Use the `create_notion_page` tool to publish the **entire detailed report** to Notion. The title should be descriptive, like '[Company Name] 상세 분석 리포트'.\n"
        "  3. Send a confirmation message to Slack, including the link to the new Notion page, formatted in Slack Block Kit JSON.\n"
        "\n"
        "**General Rules:**\n"
        "- **Time Context:** Before starting any analysis, you MUST call the `get_current_time_string` tool to ascertain the current time.\n"
        "- **Ticker Lookup:** Before delegating to an analysis agent, you MUST use the `TickerLookupAgent` to resolve company names to tickers.\n"
        "- **Output Formatting:** All final outputs must be valid Slack Block Kit JSON wrapped in a ```json code block.\n"
        "\n"
        "**Routing Rules:**\n"
        "- For a **portfolio analysis**, delegate to `PortfolioAnalyzer`.\n"
        "- For a **stock recommendation**, delegate to `Recommender`.\n"
        "- For a **comprehensive analysis of a single stock**, delegate to `SingleAssetAnalyzer`.\n"
        "- For specific **fundamental, technical, stock news, or market news analysis**, delegate to the respective specialist agents (`FundamentalAnalyzer`, `TechnicalAnalyzer`, etc.)."
    ),
    tools=[
        # High-level workflow agents
        AgentTool(agent=portfolio_analyzer_agent),
        AgentTool(agent=recommender_agent),
        
        # Mid-level comprehensive analyzer
        AgentTool(agent=single_asset_analyzer_agent),
        
        # Low-level specialist agents
        AgentTool(agent=fundamental_analyzer),
        AgentTool(agent=technical_analyzer),
        AgentTool(agent=stock_news_analyzer),
        AgentTool(agent=market_news_analyzer),
        
        # Utility Agents
        AgentTool(agent=ticker_lookup_agent),
        
        # Standalone tools
        create_notion_page,
        get_current_time_string,
    ],
)
