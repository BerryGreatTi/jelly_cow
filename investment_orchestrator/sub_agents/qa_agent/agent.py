import os
from google.adk.agents import Agent
from dotenv import load_dotenv

from .prompt import get_instruction


load_dotenv()

GOOGLE_GENAI_USE_VERTEXAI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", False)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
AGENT_MODEL = os.getenv("MODEL", "gemini-2.0-flash")
QA_PROMPT_VERSION = os.getenv("QA_PROMPT_VERSION", "latest")


agent = Agent(
    name="qa_agent",
    model=AGENT_MODEL,
    description="A specialized agent for answering questions based on investment reports.",
    instruction=get_instruction(version=QA_PROMPT_VERSION),
)