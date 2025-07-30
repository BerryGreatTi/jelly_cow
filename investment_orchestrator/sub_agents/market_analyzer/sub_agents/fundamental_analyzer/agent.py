import os
from google.adk.agents import Agent
from dotenv import load_dotenv

from .prompt import get_instruction


load_dotenv()

GOOGLE_GENAI_USE_VERTEXAI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", False)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
AGENT_MODEL = os.getenv("MODEL", "gemini-2.0-flash")
FUNDAMENTAL_ANALYZER_PROMPT_VERSION = os.getenv("FUNDAMENTAL_ANALYZER_PROMPT_VERSION", "latest")


agent = Agent(
    name="fundamental_analyzer",
    model=AGENT_MODEL,
    description="Specialist agent for fundamental analysis.",
    instruction=get_instruction(version=FUNDAMENTAL_ANALYZER_PROMPT_VERSION),
    # tools=[] # Tools to be added later
)