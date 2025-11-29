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
from agents.formatter_agent import agent as formatter_agent, formatter_agent_public

# Other tools
from apis.notion import create_notion_page
from tools.server_time import get_current_time_string


# Define the primary agent with a full toolset for use in DMs
agent = Agent(
    name="JellyMonster",
    model="gemini-2.5-flash",
    description="A master financial agent that orchestrates tasks by delegating to a team of specialist agents.",
    instruction=(
        "You are a master financial agent, an orchestrator. Your primary goal is to follow established workflows, "
        "generate content, and delegate the final formatting to a sub-agent. All responses should be in Korean.\n"
        "\n"
        "**--- Core Output Workflow ---**\n"
        "Your final step is ALWAYS to delegate the content you've prepared (as a markdown string) to the `FormatterAgent`. "
        "The `FormatterAgent` handles the final response. Your job is done after delegating.\n"
        "**NEVER generate Slack Block Kit JSON yourself.**\n"
        "\n"
        "**--- Workflow based on User Intent ---**\n"
        "You must first determine the user's goal. There are two main paths:\n"
        "\n"
        "**Path 1: Standard Analysis Request (Default)**\n"
        "- If the user asks for an analysis (e.g., '삼성전자 분석해줘'), your process is:\n"
        "  1. Delegate to the appropriate specialist agent (e.g., `SingleAssetAnalyzer`) to get a **full, detailed analysis report**.\n"
        "  2. Once you receive the detailed report, create a **concise summary (under 2500 characters) as a markdown string**.\n"
        "  3. **Delegate this markdown summary to the `FormatterAgent`.** (Your job is done).\n"
        "  **Do NOT create a Notion page in this case.**\n"
        "\n"
        "**Path 2: Explicit Notion Report Request**\n"
        "- If the user explicitly asks for a report on Notion (e.g., '자세한 리포트를 노션에 만들어줘'), your process is:\n"
        "  1. Delegate to the appropriate specialist agent to get the **full, detailed analysis report**.\n"
        "  2. Use the `create_notion_page` tool to publish the **entire detailed report** to Notion. The title should be descriptive.\n"
        "  3. Create a **simple confirmation message as a markdown string**, including the link to the new Notion page.\n"
        "  4. **Delegate this confirmation message to the `FormatterAgent`.** (Your job is done).\n"
        "\n"
        "**--- General Rules ---**\n"
        "- **Time Context:** Before starting any analysis, you MUST call the `get_current_time_string` tool.\n"
        "- **Ticker Lookup:** Before delegating to an analysis agent, you MUST use the `TickerLookupAgent`.\n"
        "\n"
        "**--- Routing Rules ---**\n"
        "- For a **portfolio analysis**, delegate to `PortfolioAnalyzer`.\n"
        "- For a **stock recommendation**, delegate to `Recommender`.\n"
        "- For a **comprehensive analysis of a single stock**, delegate to `SingleAssetAnalyzer`.\n"
        "- For specific **fundamental, technical, stock news, or market news analysis**, delegate to the respective specialist agents."
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
    sub_agents=[formatter_agent],
)

# --- Define the restricted agent based on the primary agent ---

# Create a restricted list of tools by filtering the main agent's tools
restricted_tools = [
    tool for tool in agent.tools
    if not (isinstance(tool, AgentTool) and tool.agent.name == portfolio_analyzer_agent.name)
]

# Define the restriction notice
RESTRICTION_NOTICE = (
    "You are currently in a public channel, so tools that access personal information (like portfolio analysis) are disabled for security reasons. "
    "If a user asks for a portfolio analysis, you MUST inform them that this function is only available in a Direct Message (DM) and politely decline the request."
)

# Create the restricted instruction by prepending the notice to the full agent's instruction
restricted_description = f"{agent.description}\nSome tools requiring personal information are disabled in public channels."
restricted_instruction = f"{RESTRICTION_NOTICE}\n\n{agent.instruction}"

# A restricted agent for use in public channels, with sensitive tools removed
restricted_agent = Agent(
    name=agent.name + "_public",
    model=agent.model,
    description=restricted_description,
    instruction=restricted_instruction,
    tools=restricted_tools,
    sub_agents=[formatter_agent_public],
)