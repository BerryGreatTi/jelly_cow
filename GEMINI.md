# Project Context: jelly_cow

## Tech Stack
- Python 3.12
- Google Agent Development Kit (ADK)
- FastAPI
- Slack Bolt
- Pandas, yfinance, pandas-ta for financial analysis

## Agent Architecture
The project follows a hierarchical agent structure orchestrated by a root agent.

- `agents/root_agent.py`: The root orchestrator agent (`JellyMonsterRootAgent`). It receives a user's query from Slack, delegates analysis tasks to the appropriate sub-agents, and synthesizes their findings into a final report.
- `agents/fundamental_analyzer.py`: A sub-agent specializing in fundamental analysis of a company's financial health.
- `agents/technical_analyzer.py`: A sub-agent specializing in technical analysis of stock charts and indicators.
- `agents/news_analyzer.py`: A sub-agent specializing in analyzing news and market sentiment.

## Integrations
- **Slack**: The primary user interface. The bot listens for direct messages and mentions in channels, processes the request, and replies in a thread. This is handled by `app.py` (FastAPI) and `apis/slack.py` (Slack Bolt).
- **Korea Investment API**: `apis/koreainvestment.py` contains a client for interacting with the Korea Investment & Securities API.
- **Notion**: `apis/notion.py` is a placeholder for a future integration to publish reports to Notion.

## Development Guidelines

### Agent & Tool Design
- **Docstrings**: All agents and tools should have clear, detailed English docstrings explaining their purpose, parameters, and returns for the LLM.
- **Root Agent Role (`root_agent`)**: Acts as a planner and delegator. It receives a user query, creates a plan, and assigns tasks to sub-agents. It should not use tools directly, only other agents.
- **Sub-agent Role**: Executor agents that perform specific analysis tasks using tools (e.g., data retrieval, calculation). Note: The tools for the analyzer agents are not yet implemented.

### General
- **Language**: English for all code, docstrings, and comments.

## Prohibitions
- Do not generate code without an explicit request.
- Do not commit directly to the `main` branch.
