import os
from google.adk.agents import Agent
from dotenv import load_dotenv

from . import prompt as prompt


load_dotenv()

GOOGLE_GENAI_USE_VERTEXAI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", False)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
AGENT_MODEL = os.getenv("MODEL", "gemini-2.0-flash")
TECHNICAL_ANALYZER_PROMPT_VERSION = os.getenv("TECHNICAL_ANALYZER_PROMPT_VERSION", "latest")


agent = Agent(
    name="technical_analyzer",
    model=AGENT_MODEL,
    description="Specialist agent for technical analysis.",
    instruction=prompt.get_instruction(version=TECHNICAL_ANALYZER_PROMPT_VERSION),
    # tools=[] # Tools to be added later
)