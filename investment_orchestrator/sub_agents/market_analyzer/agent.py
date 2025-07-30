import os
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from dotenv import load_dotenv

from .sub_agents import *
from .prompt import get_instruction


load_dotenv()

GOOGLE_GENAI_USE_VERTEXAI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", False)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
AGENT_MODEL = os.getenv("MODEL", "gemini-2.0-flash")
MARKET_ANALYZER_PROMPT_VERSION = os.getenv("MARKET_ANALYZER_PROMPT_VERSION", "latest")


agent = Agent(
    name="market_analyzer",
    model=AGENT_MODEL,
    description="A specialized agent for creating comprehensive investment reports by delegating to specialist analyzers.",
    instruction=get_instruction(version=MARKET_ANALYZER_PROMPT_VERSION),
    tools=[
        AgentTool(agent=fundamental_analyzer.agent.agent),
        AgentTool(agent=technical_analyzer.agent.agent),
        AgentTool(agent=news_analyzer.agent.agent),
    ],
)