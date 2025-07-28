from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

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

root_agent = Agent(
    name="investment_orchestrator",
    instruction=INSTRUCTIONS,
    tools=[
        AgentTool(agent=tools.market_analyzer.agent.agent),
        AgentTool(agent=tools.publisher.agent.agent),
        AgentTool(agent=tools.qa_agent.agent.agent),
        AgentTool(agent=tools.trading_agent.agent.agent),
    ],
)