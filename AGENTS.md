# Project Context: jelly_cow

## Tech Stack
- Python 3.12
- Google Agent Development Kit (ADK)
- FastAPI
- Slack Bolt
- Pandas, yfinance, pandas-ta for financial analysis
- Docker

## Agent Architecture
The project follows a hierarchical agent structure orchestrated by a root agent.

- `agents/root_agent.py`: The root orchestrator agent (`JellyMonsterRootAgent`). It receives a user's query from Slack and can perform two main tasks:
    1.  **Single Asset Analysis**: Delegates analysis to sub-agents and synthesizes their findings into a report.
    2.  **Portfolio Analysis**: Analyzes the user's current portfolio, including cash, and provides a holistic rebalancing plan.

- `agents/fundamental_analyzer.py`: A sub-agent that uses tools in `tools/fa.py` to analyze a company's profile, key financial metrics (P/E, P/B, debt-to-equity), and analyst recommendations.

- `agents/technical_analyzer.py`: A sub-agent that uses tools in `tools/ta.py` to analyze a stock's performance based on key technical indicators like RSI, MACD, Bollinger Bands, OBV, and Stochastic Oscillator.

- `agents/news_analyzer.py`: A sub-agent that uses tools in `tools/na.py` to fetch recent news articles and `load_web_page` to analyze their content for market sentiment and key issues.

### Foundation Model Strategy
The choice of foundation model for each agent is based on a balance of performance, cost, and speed for its specific task.

- **`root_agent` (`JellyMonster`)**: `gemini-2.5-flash`
  - **Reason**: As the orchestrator, this agent requires strong reasoning and synthesis capabilities to combine outputs from sub-agents into a coherent and detailed final report. `gemini-2.5-flash` provides a strong balance of high performance for this complex task while remaining efficient in terms of cost and latency.

- **`news_analyzer`**: `gemini-2.5-flash`
  - **Reason**: This agent needs to process unstructured text from web pages, which can be lengthy. `gemini-2.5-flash` is chosen for its strong natural language understanding and larger context window, ensuring it can analyze articles for sentiment and key issues effectively.

- **`fundamental_analyzer` & `technical_analyzer`**: `gemini-2.5-flash`
  - **Reason**: These agents interpret relatively structured data from their tools. `gemini-2.5-flash` has sufficient capability to interpret financial and technical indicators and provide meaningful analysis beyond simply reporting raw data.

## Core Tools
The sub-agents rely on a set of specialized tools to gather information. All tools are based on the `yfinance` library.

- `tools/account.py`:
    - `get_current_portfolio()`: Retrieves the user's mock portfolio, including stock holdings and cash balances in multiple currencies.

- `tools/market.py`:
    - `get_exchange_rate()`: Fetches the exchange rate between two currencies.
    - `get_current_prices()`: Gets the current market price for a list of stocks and currencies, converting them to a single output currency.
    - `evaluate_portfolio()`: Calculates the total value of the portfolio in a specified currency.

- `tools/fa.py` (Fundamental Analysis):
    - `get_company_info()`: Retrieves general company information (name, sector, summary).
    - `get_financial_summary()`: Gets key financial ratios and metrics.
    - `get_analyst_recommendations()`: Fetches the latest analyst recommendations.

- `tools/ta.py` (Technical Analysis):
    - `get_ohlcv()`: Fetches historical OHLCV data.
    - `get_current_rsi()`, `get_current_macd()`, etc.: Calculate current values for various technical indicators.

- `tools/na.py` (News Analysis):
    - `get_company_news()`: Retrieves recent news articles for a given ticker.

## Other APIs
- **Slack**: The primary user interface. The bot connects to Slack via **Socket Mode**, listening for direct messages and mentions. This is handled by `app.py` and `apis/slack.py` (Slack Bolt).
- **Korea Investment API**: `apis/koreainvestment.py` contains a client for the Korea Investment & Securities API. (Currently not used by the main agent logic).
- **Notion**: `apis/notion.py` is a placeholder for a future integration to publish reports to Notion. (Currently not used).

## DevOps

### Environment Management with Docker
The project uses Docker and Docker Compose to manage `development` and `production` environments.

- **`Dockerfile`**: Defines the Python 3.12 container for the application, installs dependencies from `requirements.txt`, and copies the application code.

- **`docker-compose.yml`**: Defines two services:
    - **`prod`**: Runs the application based on the code copied into the Docker image at build time. This is the stable, production environment.
    - **`dev`**: Mounts the local source code directory into the container. This allows for live testing of code changes without rebuilding the image.

### Development Workflow
1.  **Start Development Environment**:
    ```bash
    docker-compose up dev -d
    ```
    (Code changes on the local machine are reflected instantly in the container.)

2.  **Update and Deploy to Production**:
    Once development is complete, build a new image and start the `prod` service.
    ```bash
    docker-compose up prod -d --build
    ```

3.  **Stop Services**:
    ```bash
    docker-compose down
    ```

4.  **View Logs**:
    ```bash
    docker-compose logs -f <service_name>
    ```
    (e.g., `docker-compose logs -f dev`)


## Development Guidelines

### Agent & Tool Design
- **Docstrings**: All agents and tools should have clear, detailed English docstrings explaining their purpose, parameters, and returns for the LLM.
- **Root Agent Role (`root_agent`)**: Acts as a planner and delegator. It receives a user query, creates a plan, and assigns tasks to sub-agents.
- **Sub-agent Role**: Executor agents that perform specific analysis tasks using the provided tools.

### General
- **Language**: English for all code, docstrings, and comments.

## Prohibitions
- Do not generate code without an explicit request.
- Do not commit directly to the `main` branch.
