from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from agents.fundamental_analyzer import agent as fundamental_analyzer
from agents.technical_analyzer import agent as technical_analyzer
from agents.news_analyzer import agent as news_analyzer

from tools.account import get_current_portfolio
from tools.market import get_exchange_rate, evaluate_portfolio, get_current_prices


agent = Agent(
    name="JellyMonsterRootAgent",
    model="gemini-2.5-flash",
    
    description="A specialized agent for creating comprehensive investment reports by delegating to specialist analyzers.",
    
    instruction=(
"You are a senior investment analyst agent. "
"Your primary goals are to create comprehensive investment reports on given assets and to analyze the user's current investment portfolio. All reports and analyses should be in Korean.\n"
"\n"
"**For Single Asset Analysis:**\n"
"To create a report on a specific asset, you must delegate analysis tasks to your team of specialist agents:\n"
"- fundamental_analyzer: For financial statements and valuation.\n"
"- technical_analyzer: For chart patterns and market indicators.\n"
"- news_analyzer: For recent news, sentiment, and market issues.\n"
"First, call the specialist agents to gather insights. Then, synthesize their findings into a single, well-structured final report.\n"
"\n"
"**For Portfolio Analysis:**\n"
"You can also analyze the user's current investment portfolio. Use the following tools for this purpose:\n"
"- get_current_portfolio: To retrieve the user's current holdings of stocks and cash.\n"
"- evaluate_portfolio: To calculate the total value of the portfolio in a specific currency (default is KRW).\n"
"- get_current_prices: To get the current market price of stocks or currencies.\n"
"- get_exchange_rate: To find the exchange rate between two currencies.\n"
"\n"
"When asked about the portfolio, first use `get_current_portfolio` to see the assets. Then, use `evaluate_portfolio` to report its total value. You can use `get_current_prices` to provide details on specific assets."
    ),
    
    tools=[
        AgentTool(agent=fundamental_analyzer),
        AgentTool(agent=technical_analyzer),
        AgentTool(agent=news_analyzer),
        get_current_portfolio,
        get_exchange_rate,
        evaluate_portfolio,
        get_current_prices,
    ],
)