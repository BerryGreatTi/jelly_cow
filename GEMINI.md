# Project Context: jelly_cow

## Tech Stack
- Python 3.12
- Agent Development Kit

## Agent Architecture
The project follows a hierarchical agent structure:

- `multi_tool_agent/`: The root orchestrator agent (`investment_orchestrator`). It delegates high-level tasks to the appropriate sub-agents.
    - `tools/market_analyzer/`: A sub-agent responsible for creating comprehensive investment reports by delegating to specialist analyzers.
        - `sub_agents/fundamental_analyzer.py`: Specialist agent for fundamental analysis.
        - `sub_agents/technical_analyzer.py`: Specialist agent for technical analysis.
        - `sub_agents/news_analyzer.py`: Specialist agent for news and sentiment analysis.
    - `tools/publisher/`: A sub-agent for publishing content.
    - `tools/qa_agent/`: A sub-agent for answering questions based on reports.
    - `tools/trading_agent/`: A sub-agent for executing trades (with safety guards).

## Development Guidelines

### Agent & Tool Design
- **Docstrings**: Clear, detailed, in English. Explain purpose, parameters, and returns for LLM.
- **Root Agent Role (`multi_tool_agent`)**: Planner & delegator. Receives a user's query, creates a plan, and assigns tasks to sub-agents. **Must not** use tools directly, only other agents.
- **Sub-agent Role**: Can be either a delegator (like `market_analyzer`) or an executor. Executors run tasks using tools (e.g., calculation, data retrieval).

### Tool Implementation
- **Technical Indicator Library Priority**:
    1. Use `pandas_ta`.
    2. If not available, use `TA-Lib`.
    3. If not available, implement custom calculation.
- **Custom Calculations**: Isolate pure calculation logic into a separate function.

### General
- **Language**: English for all code, docstrings, and comments.

## Prohibitions
- Do not generate code without any explicit request.
- Do not commit directly to the `main` branch.