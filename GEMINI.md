# Project Context: jelly_cow

## Tech Stack
- Python 3.12
- Agent Development Kit

## File Structure
- `market_analyzer/agent.py`: Main agent. Plans and delegates tasks. Does not use tools directly.

## Development Guidelines

### Agent & Tool Design
- **Docstrings**: Clear, detailed, in English. Explain purpose, parameters, and returns for LLM.
- **Main Agent Role**: Planner & delegator. Receives query, creates plan, assigns tasks to sub-agents. **Must not** use tools directly.
- **Sub-agent Role**: Executor. Runs tasks from the main agent using tools (e.g., calculation, data retrieval).

### Tool Implementation
- **Technical Indicator Library Priority**:
    1. Use `pandas_ta`.
    2. If not available, use `TA-Lib`.
    3. If not available, implement custom calculation.
- **Custom Calculations**: Isolate pure calculation logic into a separate function.

### General
- **Language**: English for all code, docstrings, and comments.

## Prohibitions
- Do not commit directly to the `main` branch.