from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

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
    instruction=INSTRUCTIONS,
    tools=[
        AgentTool(agent=sub_agents.fundamental_analyzer.agent),
        AgentTool(agent=sub_agents.technical_analyzer.agent),
        AgentTool(agent=sub_agents.news_analyzer.agent),
    ],
)