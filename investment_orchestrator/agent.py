import os
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from dotenv import load_dotenv

from .tools import market_analyzer, publisher, qa_agent, trading_agent
from .prompt import get_instruction


load_dotenv()

GOOGLE_GENAI_USE_VERTEXAI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", False)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
AGENT_MODEL = os.getenv("MODEL", "gemini-2.0-flash")
ROOT_PROMPT_VERSION = os.getenv("ROOT_PROMPT_VERSION", "latest")


root_agent = Agent(
    name="investment_orchestrator",
    model=AGENT_MODEL,
    description="",
    instruction=get_instruction(version=ROOT_PROMPT_VERSION),
    tools=[
        AgentTool(agent=market_analyzer.agent.agent),
        AgentTool(agent=publisher.agent.agent),
        AgentTool(agent=qa_agent.agent.agent),
        AgentTool(agent=trading_agent.agent.agent),
    ],
)