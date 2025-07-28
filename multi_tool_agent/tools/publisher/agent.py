from google.adk.agents import Agent

def publish_content(content: str, channel: str) -> str:
    """Publishes the given content to the specified channel (e.g., 'email', 'slack')."""
    print(f"--- Publishing to {channel} ---\n{content}\n--- End of Publication ---")
    return f"Successfully published content to {channel}."

agent = Agent(
    name="publisher",
    instruction="You are a publisher agent. Your job is to take content and publish it to a user-specified channel using the available tools.",
    tools=[publish_content],
)