from google.adk.agents import Agent
from google.adk.tools import google_search

# from tools.lookup import fmp_symbol_search

agent = Agent(
    name="TickerLookupAgent",
    model="gemini-2.0-flash",
    description="A specialist agent that finds a stock ticker for a given company name.",
    instruction=(
        "You are a specialist agent that finds a stock ticker for a given company name. "
        "Your goal is to return a single, accurate ticker symbol that is compatible with `yfinance`.\n"
        "\n"
        "**Workflow:**\n"
        "1.  **Search:** Use the `google_search` tool to find the stock ticker. Use a query like '[Company Name] yfinance ticker' or '[Company Name] stock ticker yfinance'. The company name may be in Korean. For Korean stocks, ensure the ticker includes the appropriate suffix (e.g., '.KS' for KOSPI, '.KQ' for KOSDAQ).\n"
        "2.  **Analyze Google Results:** Examine the search results text to find the `yfinance`-compatible ticker. The ticker is often a short string of capital letters or numbers followed by a market code (e.g., AAPL, 005930.KS, 035420.KQ). If you find a clear ticker, return only that ticker string and stop.\n"
        "3.  **Failure:** If you cannot find a ticker after all steps, return an error message: 'Could not find a ticker for the given company name.'"
    ),
    tools=[
        # fmp_symbol_search,
        google_search,
    ],
)
