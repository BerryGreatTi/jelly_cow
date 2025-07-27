from adk.agent import Agent
from adk.tools import import_agent_as_tool

from . import tools


INSTRUCTIONS = """
You are a master investment orchestrator agent.
Your primary role is to understand the user's high-level goals and delegate tasks to specialized sub-agents.
You have the following agents available as tools:
- market_analyzer: Analyzes assets and generates investment reports.
- publisher: Publishes content to specified channels.
- qa_agent: Answers user questions based on generated reports.
- trading_agent: Executes trades based on user requests.

Based on the user's request, determine the correct sequence of sub-agents to call to accomplish the goal.
"""

agent = Agent(
    name="investment_orchestrator",
    instructions=INSTRUCTIONS,
    tools=[
        import_agent_as_tool(tools.market_analyzer.agent),
        import_agent_as_tool(tools.publisher.agent),
        import_agent_as_tool(tools.qa_agent.agent),
        import_agent_as_tool(tools.trading_agent.agent),
    ],
)