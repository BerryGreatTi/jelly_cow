from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from agents.fundamental_analyzer import agent as fundamental_analyzer
from agents.technical_analyzer import agent as technical_analyzer
from agents.news_analyzer import agent as news_analyzer


agent = Agent(
    name="JellyMonsterRootAgent",
    model="gemini-2.5-flash",
    
    description="A specialized agent for creating comprehensive investment reports by delegating to specialist analyzers.",
    
    instruction=(
"You are a senior investment analyst agent. "
"Your goal is to create a comprehensive investment report in Korean on a given asset. "
"To do this, you must delegate analysis tasks to your team of specialist agents:\n"
"- fundamental_analyzer: For financial statements and valuation.\n"
"- technical_analyzer: For chart patterns and market indicators.\n"
"- news_analyzer: For recent news, sentiment, and market issues.\n"
"\n"
"First, call all three specialist agents to gather insights. "
"Then, synthesize their findings into a single, well-structured final report."
    ),
    
    tools=[
        AgentTool(agent=fundamental_analyzer),
        AgentTool(agent=technical_analyzer),
        AgentTool(agent=news_analyzer),
    ],
)