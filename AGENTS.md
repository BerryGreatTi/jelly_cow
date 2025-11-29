# Project Context: jelly_cow

## Tech Stack
- Python 3.12
- Google Agent Development Kit (ADK)
- **yfinance**: Primary source for fundamental data (financial statements), technical indicators, company news, and historical price data.
- **Financial Modeling Prep (FMP) API**: Secondary source used for stock screening (`run_screener_query`) and advanced technical indicators (`get_technical_indicator`).
- FastAPI
- Slack Bolt
- Docker

## Agent Architecture
The project follows a hierarchical, orchestrated agent structure. A `root_agent` acts as a master controller, routing user requests to the appropriate specialist agent. This design promotes modularity, scalability, and maintainability.

```
[root_agent] (Orchestrator)
    |
    |--- (pre-processes) ---> [get_current_time_string]
    |
    |--- [TickerLookupAgent] (Utility: Name -> Ticker)
    |
    |--- (delegates to specialist tools) ---> [portfolio_analyzer_agent], [recommender_agent], etc.
    |
    |--- (delegates final content to) ---> [FormatterAgent] (Sub-Agent for UI)
    |
    L--- [single_asset_analyzer_agent] (Task: Comprehensive Analysis)
           |
           |--- [fundamental_analyzer]
           |      |
           |      |--- (pre-processes) ---> [get_current_time_string]
           |      |
           |      L--- (delegates to) ---> [market_news_analyzer]
           |
           |--- [technical_analyzer]
           |
           L--- [stock_news_analyzer]
                  L--- (uses tools) ---> [get_company_news, load_web_page]
```

- `agents/root_agent.py`: The root orchestrator agent (`JellyMonster`). This file now defines two main agent instances:
    - The **full-featured agent** (`agent`): Used in Direct Messages (DMs), it has access to all specialist tools, including those for personal account analysis.
    - The **restricted agent** (`restricted_agent`): Used in public and private channels, it excludes tools that access sensitive personal account information (e.g., `portfolio_analyzer_agent`). Its instruction set also includes a notice informing users about these restrictions and directing them to DMs for sensitive requests.
    Its responsibility is to understand the user's intent, delegate tasks to specialist agents to gather information, synthesize the content into a markdown draft, and then delegate the final UI generation to its `FormatterAgent` sub-agent.

- `agents/formatter_agent.py`: A specialist sub-agent whose sole purpose is to convert a raw markdown string into a well-structured and highly readable Slack Block Kit JSON. This promotes a separation of concerns between content generation and presentation. This file now defines two instances, `formatter_agent` and `formatter_agent_public`, to avoid validation errors when used by two different parent agents.

- `agents/recommender_agent.py`: A high-level agent that handles stock recommendation workflows. It uses `run_screener_query` and `get_technical_indicator` to find candidates, then calls the `single_asset_analyzer_agent` to perform in-depth analysis before making a final recommendation.

- `agents/portfolio_analyzer_agent.py`: A high-level agent dedicated to analyzing a user's investment portfolio. It calls the `get_current_portfolio` tool (which implicitly receives the user's context) and then calls the `single_asset_analyzer_agent` for each asset to form a holistic rebalancing plan.

- `agents/single_asset_analyzer_agent.py`: A mid-level agent that performs a comprehensive analysis of a single stock. It encapsulates the process of calling the three low-level analyzers (`fundamental`, `technical`, `stock_news`) and synthesizing their findings into one report. This is a reusable component called by `recommender_agent` and `portfolio_analyzer_agent`.

- `agents/ticker_lookup_agent.py`: A utility agent responsible for converting a company name (in English or Korean) into a valid `yfinance` stock ticker. It now exclusively uses `google_search` to find the company's primary exchange and combine the base symbol with the correct suffix (e.g., `.KS` for KOSPI, `.KQ` for KOSDAQ).

- `agents/fundamental_analyzer.py`: A low-level specialist that performs deep fundamental analysis. It first calls `get_current_time_string` to determine the current date. Based on the date, it analyzes both **annual and the most recent quarterly** financial statements (`income_statement`, `balance_sheet`, `cash_flow`) to ensure a timely analysis. It also analyzes key metrics, analyst ratings, and insider transactions. It can delegate to the `MarketNewsAnalyzer` for qualitative, market-based research.

- `agents/technical_analyzer.py`: A low-level specialist for technical analysis of a stock's price and volume data using tools from `tools/ta.py`.

- `agents/stock_news_analyzer.py`: A low-level specialist for stock-specific news analysis. It uses `get_company_news` to find recent articles and `load_web_page` to read their full content, analyzing them for sentiment and key events.

- `agents/market_news_analyzer.py`: A low-level specialist for qualitative market research. It uses `google_search` to analyze the broader market context, including identifying peer companies for comparative analysis, researching industry trends, and assessing the impact of macroeconomic indicators.

### Foundation Model Strategy
All agents use `gemini-2.5-flash` by default, providing a strong balance of performance and cost.

- **`root_agent`**: For smart routing, content synthesis, and delegation.
- **`FormatterAgent`**: **(Recommended)** Should be upgraded to a high-performance model (e.g., latest Gemini flagship) to ensure maximum reliability and quality in generating complex UI (Slack Block Kit JSON).
- **`recommender_agent` & `portfolio_analyzer_agent`**: For orchestrating complex, multi-step analysis workflows.
- **`single_asset_analyzer_agent`**: For synthesizing reports from multiple sub-agents.
- **`ticker_lookup_agent`**: For translating and parsing search results to find tickers.
- **`fundamental_analyzer`, `technical_analyzer`, `stock_news_analyzer`, `market_news_analyzer`**: For interpreting structured and unstructured data to provide insights.

### Output Generation and UI
The system uses a robust, two-tiered approach to generate final outputs for Slack, ensuring both high quality and stability.

1.  **Ideal Path: `FormatterAgent`**: The `root_agent` generates content as markdown and delegates it to the `FormatterAgent`. This specialist agent, ideally powered by a high-performance model, converts the markdown into a rich, readable Slack Block Kit JSON structure.

2.  **Safety Net: Intelligent Adaptive Rendering**: The `apis/slack.py` handler acts as a safety net. If the agent layer fails to produce valid Block Kit JSON for any reason, this handler will not crash. Instead, it will treat the raw output as markdown and intelligently split it into paragraph-based sections, ensuring a readable, structured message is still delivered. This makes the entire system resilient to failures in the agent-based formatting step.

## Multi-User Support & Context Passing

To support multiple users with distinct API credentials for portfolio analysis, the system uses the ADK's session state to pass user context implicitly.

- **`apis/slack.py`**: The `user_id` is retrieved from the incoming Slack event (`message` or `app_mention`).
- **`apis/agent_handler.py`**: This `user_id` is injected into the session state when the session is created or retrieved, by calling `session_service.create_session(..., state={"user_id": user_id})`.
- **`tools/account.py`**: The `get_current_portfolio` tool is designed to receive the `ToolContext` object from the ADK framework. It accesses the `user_id` via `tool_context.state.get("user_id")`.
- **`apis/user_api_manager.py`**: A new `UserApiHandler` class in this file uses the retrieved `user_id` to load the correct user profile from `profiles/<user_id>.json`. Crucially, this handler also caches the initialized `KoreaInvestmentAPI` instance for each user, reusing it until its access token expires to prevent excessive token requests and potential rate-limiting.

This architecture ensures that portfolio analysis is always performed for the correct user without needing the agent to explicitly handle the `user_id` in its prompts.

## Core Tools
The agents rely on a set of specialized tools to gather information.

- **`tools/fa.py`**: Contains tools based on `yfinance` for fetching fundamental data. Used by `FundamentalAnalyzer`.
    - Includes: `get_company_info`, `get_financial_summary`, `get_analyst_recommendations`, `get_major_shareholders`, `get_insider_transactions`.
    - The financial statement tools (`get_income_statement`, `get_balance_sheet`, `get_cash_flow`) accept a `period` argument to fetch 'annual' or 'quarterly' data.

- **`tools/ta.py`**: Contains tools based on `yfinance` and `pandas-ta` for technical analysis. Used by `TechnicalAnalyzer`.
    - Includes: `get_rsi`, `get_macd`, `get_moving_average`, `get_bbands`, `get_obv`, `get_stoch`.

- **`tools/na.py`**: Contains tools based on `yfinance` for fetching company-specific news articles. Used by `StockNewsAnalyzer`.
    - Includes: `get_company_news`.

- **`tools/screener.py`**: Contains tools that use the FMP API for screening and filtering stocks. Used by `RecommenderAgent`.
    - `run_screener_query()`: Filters stocks based on a wide range of criteria (market cap, sector, etc.).
    - `get_technical_indicator()`: Fetches specific technical indicator data (e.g., SMA, Standard Deviation).

- **`tools/account.py`**:
    - `get_current_portfolio()`: Retrieves the user's current investment portfolio. It automatically receives the user's context via the ADK's `ToolContext` and uses the `user_id` from the session state to load the correct profile and fetch the corresponding account data. Used by `PortfolioAnalyzerAgent`.

- **`tools/server_time.py`**:
    - `get_current_time_string()`: Returns the current server time. Used by `RootAgent` and `FundamentalAnalyzer` to provide temporal context for analysis.

- **`tools/lookup.py`**:
    - `fmp_symbol_search()`: (Currently disabled) Previously used for ticker lookups but has been replaced by a `google_search`-based workflow in `TickerLookupAgent`.

- **`google.adk.tools`**:
    - `google_search`: A built-in tool used by `MarketNewsAnalyzer` for market research and by `TickerLookupAgent` for finding tickers.
    - `load_web_page`: A built-in tool used by `StockNewsAnalyzer` to read the content of news articles from URLs.

## Other APIs
- **Slack**: The primary user interface. The bot connects to Slack via **Socket Mode**, listening for direct messages and mentions.
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

### Interactive Q&A
To improve user interaction, all specialist agents are instructed to handle follow-up questions regarding concepts they introduce in their analysis. If a user asks for clarification on a technical analysis term (e.g., "What is RSI?") or a company-specific technology (e.g., "What is CUDA?"), the agent that mentioned it will provide a concise definition and explain its relevance to the analysis. This allows for a more interactive and educational experience.

For standalone questions about market concepts or technologies not directly tied to an ongoing analysis, the `root_agent` will delegate the query to the `MarketNewsAnalyzer`, which will use its web search capabilities to provide an answer.

### General
- **Language**: English for all code, docstrings, and comments.

## Long-term Researches
- **DCF Modeling Agent**: Implement an advanced agent capable of performing Discounted Cash Flow (DCF) analysis. This would be a significant, research-level task involving:
    - Projecting a company's future cash flows based on historical data and growth assumptions.
    - Determining an appropriate discount rate (WACC).
    - Calculating the intrinsic value of the stock and comparing it to the current market price.
    - This would likely require a dedicated set of tools for financial modeling calculations and a sophisticated instruction set for making reasonable assumptions.
- **Macroeconomic Forecasting Agent**: Develop a dedicated agent for in-depth macroeconomic analysis and forecasting. This is a complex, research-level endeavor that would involve:
    - Accessing vast datasets of historical economic data.
    - Utilizing specialized tools for time-series analysis and econometric modeling (e.g., ARIMA, VAR models).
    - Building a sophisticated instruction set to enable the agent to generate its own macroeconomic forecasts, rather than just synthesizing existing reports.
