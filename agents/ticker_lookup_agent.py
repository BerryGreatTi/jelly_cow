from google.adk.agents import Agent
from google.adk.tools import google_search

# from tools.lookup import fmp_symbol_search

agent = Agent(
    name="TickerLookupAgent",
    model="gemini-2.5-flash",
    description="A specialist agent that finds a stock ticker for a given company name.",
    instruction=(
        "You are a specialist agent that finds a stock ticker for a given company name. "
        "Your goal is to return a single, accurate ticker symbol that is compatible with `yfinance`.\n"
        "\n"
        "**Workflow:**\n"
        "1.  **Identify Stock Exchange:** First, use the `google_search` tool to determine the primary stock exchange where the company is listed (e.g., NASDAQ, NYSE, KOSPI, KOSDAQ). Use queries like '[Company Name] stock exchange' or '[Company Name] 상장 거래소'.\n"
        "2.  **Determine `yfinance` Suffix:** Based on the exchange, find the correct ticker suffix for `yfinance`. Common suffixes are '.KS' for KOSPI and '.KQ' for KOSDAQ. Most US stocks (NASDAQ, NYSE) do not have a suffix. Search for '[Stock Exchange name] yfinance ticker suffix' if unsure.\n"
        "3.  **Find Base Ticker:** Search for the company's base ticker symbol using queries like '[Company Name] stock symbol' or '[Company Name] 티커'.\n"
        "4.  **Combine and Verify:** Combine the base ticker and the suffix (e.g., '005930' + '.KS' -> '005930.KS'). Verify the final ticker is correct by searching for it on `yfinance` (e.g., '005930.KS yfinance').\n"
        "5.  **Return Ticker:** If you find a clear, verified ticker, return *only* that ticker string and stop.\n"
        "6.  **Failure:** If you cannot find a ticker after all steps, return an error message: 'Could not find a ticker for the given company name.'"
    ),
    tools=[
        # fmp_symbol_search,
        google_search,
    ],
)
