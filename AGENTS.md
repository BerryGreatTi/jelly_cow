# Project Context: jelly_cow

## Tech Stack
- Python 3.12
- Google Agent Development Kit (ADK)
- Financial Modeling Prep (FMP) API for market data and screening
- FastAPI
- Slack Bolt
- Docker

## Agent Architecture
The project follows a hierarchical, orchestrated agent structure. A `root_agent` acts as a master controller, routing user requests to the appropriate specialist agent. This design promotes modularity, scalability, and maintainability.

```
[root_agent] (Orchestrator)
    |
    |--- [TickerLookupAgent] (Utility: Name -> Ticker)
    |
    |--- [portfolio_analyzer_agent] (Workflow: Portfolio Analysis)
    |      |
    |      L--- (calls) ---> [single_asset_analyzer_agent]
    |
    |--- [recommender_agent] (Workflow: Stock Recommendation)
    |      |
    |      |--- (uses tools from) ---> tools/screener.py
    |      |
    |      L--- (calls) ---> [single_asset_analyzer_agent]
    |
    L--- [single_asset_analyzer_agent] (Task: Comprehensive Analysis)
           |
           |--- [fundamental_analyzer]
           |      L--- (delegates to) ---> [market_news_analyzer]
           |
           |--- [technical_analyzer]
           L--- [stock_news_analyzer]
```

- `agents/root_agent.py`: The root orchestrator agent (`JellyMonster`). Its sole responsibility is to understand the user's intent and delegate the task to the most appropriate specialist agent. It handles routing and pre-processing tasks like ticker lookups.

- `agents/recommender_agent.py`: A high-level agent that handles stock recommendation workflows. It uses screener tools to find candidates, then calls the `single_asset_analyzer_agent` to perform in-depth analysis before making a final recommendation.

- `agents/portfolio_analyzer_agent.py`: A high-level agent dedicated to analyzing a user's investment portfolio. It retrieves the user's holdings and calls the `single_asset_analyzer_agent` for each asset to form a holistic rebalancing plan.

- `agents/single_asset_analyzer_agent.py`: A mid-level agent that performs a comprehensive analysis of a single stock. It encapsulates the process of calling the three low-level analyzers (`fundamental`, `technical`, `stock_news`) and synthesizing their findings into one report. This is a reusable component called by `recommender_agent` and `portfolio_analyzer_agent`.

- `agents/ticker_lookup_agent.py`: A utility agent responsible for converting a company name (in English or Korean) into a valid stock ticker. It uses a hybrid approach: first querying the FMP Symbol Search API, and falling back to `google_search` if needed.

- `agents/fundamental_analyzer.py`: A low-level specialist that performs deep fundamental analysis. It is equipped with tools to analyze a company's financial statements (income, balance sheet, cash flow), key metrics, analyst ratings, major shareholders, and insider transactions. It is instructed to analyze trends over time and can delegate to the `MarketNewsAnalyzer` for qualitative, market-based research.

- `agents/technical_analyzer.py`: A low-level specialist for technical analysis of a stock's price and volume data.

- `agents/stock_news_analyzer.py`: A low-level specialist for stock-specific news analysis. It finds recent news articles for a ticker, reads their content, and analyzes them for sentiment and key events.

- `agents/market_news_analyzer.py`: A low-level specialist for qualitative market research. It uses `google_search` to analyze the broader market context, including identifying peer companies for comparative analysis, researching industry trends, and assessing the impact of macroeconomic indicators.

### Foundation Model Strategy
All agents now use `gemini-2.5-flash`, providing a strong balance of performance, cost, and reasoning capabilities for all tasks, from simple routing to complex analysis and synthesis. The one exception is the `MarketNewsAnalyzer`.

- **`root_agent`**: For smart routing and pre-processing.
- **`recommender_agent` & `portfolio_analyzer_agent`**: For orchestrating complex, multi-step analysis workflows.
- **`single_asset_analyzer_agent`**: For synthesizing reports from multiple sub-agents.
- **`ticker_lookup_agent`**: For translating and parsing search results to find tickers.
- **`fundamental_analyzer`, `technical_analyzer`, `stock_news_analyzer`**: For interpreting structured and unstructured data to provide insights.
- **`market_news_analyzer`**: Uses `gemini-2.0-flash` as required by the `google_search` tool to perform web-based market research.

## Core Tools
The agents rely on a set of specialized tools to gather information.

- **`tools/lookup.py`**:
    - `fmp_symbol_search()`: Searches for a ticker using a company name via the FMP API. Used by `TickerLookupAgent`.

- **`tools/screener.py`**:
    - `run_screener_query()`: Filters stocks based on a wide range of criteria (market cap, sector, etc.) using the FMP Screener API.
    - `get_technical_indicator()`: Fetches specific technical indicator data (e.g., SMA, Standard Deviation) for a stock from the FMP API.

- **`google.adk.tools.google_search`**: A built-in tool used by `MarketNewsAnalyzer` for market research and by `TickerLookupAgent` as a fallback.

- `tools/account.py`:
    - `get_current_portfolio()`: Retrieves the user's mock portfolio.

- `tools/fa.py`: Contains tools based on `yfinance` for fetching fundamental data. Used by `FundamentalAnalyzer`.
    - Includes: `get_company_info`, `get_financial_summary`, `get_analyst_recommendations`, `get_income_statement`, `get_balance_sheet`, `get_cash_flow`, `get_major_shareholders`, `get_insider_transactions`.

- `tools/ta.py`: Contains tools for technical analysis.

- `tools/na.py`: Contains tools for fetching company-specific news articles. Used by `StockNewsAnalyzer`.

## Other APIs
- **Slack**: The primary user interface. The bot connects to Slack via **Socket Mode**, listening for direct messages and mentions.
- **Financial Modeling Prep (FMP) API**: The primary source for market data, used for stock screening, symbol lookups, and fetching technical indicators.
- **Notion**: The `create_notion_page` tool is available to the `root_agent` for publishing reports.

## DevOps

### Environment Management with Docker
The project uses Docker and Docker Compose to manage `development` and `production` environments.

- **`Dockerfile`**: Defines the Python 3.12 container for the application.
- **`docker-compose.yml`**: Defines `prod` and `dev` services.

### Development Workflow
1.  **Start Development Environment**:
    ```bash
    docker-compose up dev -d
    ```
2.  **Update and Deploy to Production**:
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

## Development Guidelines

### Agent & Tool Design
- **Docstrings**: All agents and tools should have clear, detailed English docstrings.
- **`root_agent` Role**: Acts as a smart orchestrator/router. It understands user intent and delegates to the most appropriate specialist agent. It should not perform complex analysis itself.
- **Specialist Agent Role**: High-level agents (`Recommender`, `PortfolioAnalyzer`) define complex workflows, while low-level agents perform specific, granular tasks.
- **Modularity**: Common, repeated tasks (like single-asset analysis or ticker lookup) should be encapsulated into their own reusable agents.

### General
- **Language**: English for all code, docstrings, and comments.

## Future Work / Long-term Tasks
- **DCF Modeling Agent**: Implement an advanced agent capable of performing Discounted Cash Flow (DCF) analysis. This would be a significant, research-level task involving:
    - Projecting a company's future cash flows based on historical data and growth assumptions.
    - Determining an appropriate discount rate (WACC).
    - Calculating the intrinsic value of the stock and comparing it to the current market price.
    - This would likely require a dedicated set of tools for financial modeling calculations and a sophisticated instruction set for making reasonable assumptions.
- **Macroeconomic Forecasting Agent**: Develop a dedicated agent for in-depth macroeconomic analysis and forecasting. This is a complex, research-level endeavor that would involve:
    - Accessing vast datasets of historical economic data.
    - Utilizing specialized tools for time-series analysis and econometric modeling (e.g., ARIMA, VAR models).
    - Building a sophisticated instruction set to enable the agent to generate its own macroeconomic forecasts, rather than just synthesizing existing reports.
