import os
from google.adk.agents import Agent
from dotenv import load_dotenv

from .prompt import get_instruction


load_dotenv()

GOOGLE_GENAI_USE_VERTEXAI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", False)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
AGENT_MODEL = os.getenv("MODEL", "gemini-2.0-flash")
PUBLISHER_PROMPT_VERSION = os.getenv("PUBLISHER_PROMPT_VERSION", "latest")


def publish_content(content: str, channel: str) -> str:
    """Publishes the given content to the specified channel (e.g., 'email', 'slack')."""
    print(f"--- Publishing to {channel} ---\n{content}\n--- End of Publication ---")
    return f"Successfully published content to {channel}."

agent = Agent(
    name="publisher",
    model=AGENT_MODEL,
    description="A specialized agent for publishing the given content to specified channel.",
    instruction=get_instruction(version=PUBLISHER_PROMPT_VERSION),
    tools=[publish_content],
)