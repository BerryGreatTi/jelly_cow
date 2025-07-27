from adk.agent import Agent
from adk.tools import import_agent_as_tool

from . import sub_agents

INSTRUCTIONS = """
You are a senior investment analyst agent.
Your goal is to create a comprehensive investment report on a given asset.
To do this, you must delegate analysis tasks to your team of specialist agents:
- fundamental_analyzer: For financial statements and valuation.
- technical_analyzer: For chart patterns and market indicators.
- news_analyzer: For recent news, sentiment, and market issues.

First, call all three specialist agents to gather insights.
Then, synthesize their findings into a single, well-structured final report.
"""

agent = Agent(
    name="market_analyzer",
    instructions=INSTRUCTIONS,
    tools=[
        import_agent_as_tool(sub_agents.fundamental_analyzer.agent),
        import_agent_as_tool(sub_agents.technical_analyzer.agent),
        import_agent_as_tool(sub_agents.news_analyzer.agent),
    ],
)