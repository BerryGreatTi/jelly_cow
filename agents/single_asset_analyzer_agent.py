from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from agents.fundamental_analyzer import agent as fundamental_analyzer
from agents.technical_analyzer import agent as technical_analyzer
from agents.stock_news_analyzer import agent as stock_news_analyzer

agent = Agent(
    name="SingleAssetAnalyzer",
    model="gemini-2.5-flash",
    description="A specialist agent that creates a comprehensive report on a single stock.",
    instruction=(
        "You are a specialist agent that creates a comprehensive report on a single stock. "
        "Your input will be a stock symbol. "
        "You must delegate the analysis to `fundamental_analyzer`, `technical_analyzer`, and `stock_news_analyzer` to gather insights. "
        "Then, synthesize their findings into a single, well-structured final report in Korean for the given stock. "
        "The report should have a clear summary, followed by the detailed analysis from each specialist.\n"
        "If the user asks for an explanation of a technical term or concept you used in your analysis (e.g., 'What is a P/E ratio?') or a company-specific technology (e.g., 'What is CUDA?'), provide a concise definition and briefly explain how it influenced your analysis or recommendation."
    ),
    tools=[
        AgentTool(agent=fundamental_analyzer),
        AgentTool(agent=technical_analyzer),
        AgentTool(agent=stock_news_analyzer),
    ],
)
