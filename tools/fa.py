import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, Any, Union

def replace_nan_with_none(data: Any) -> Any:
    """
    Recursively replaces NaN values with None in dictionaries, lists, or single values.
    """
    if isinstance(data, dict):
        return {k: replace_nan_with_none(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_nan_with_none(i) for i in data]
    elif isinstance(data, float) and np.isnan(data):
        return None
    elif pd.isna(data) if hasattr(pd, 'isna') else False:
        if isinstance(data, (pd.Series, pd.DataFrame)):
             return data.where(pd.notnull(data), None).to_dict()
        return None
    return data

def get_company_info(ticker: str) -> Dict[str, Any]:
    """
    Retrieves company information and business summary.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "symbol": info.get("symbol"),
            "longName": info.get("longName"),
            "industry": info.get("industry"),
            "sector": info.get("sector"),
            "summary": info.get("longBusinessSummary"),
            "website": info.get("website"),
            "marketCap": info.get("marketCap"),
            "currency": info.get("currency"),
        }
    except Exception as e:
        return {"error": str(e)}

def get_financial_summary(ticker: str) -> Dict[str, Any]:
    """
    Retrieves key financial summary data (P/E, EPS, etc.).
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "marketCap": info.get("marketCap"),
            "enterpriseValue": info.get("enterpriseValue"),
            "trailingPE": info.get("trailingPE"),
            "forwardPE": info.get("forwardPE"),
            "pegRatio": info.get("pegRatio"),
            "priceToBook": info.get("priceToBook"),
            "trailingEps": info.get("trailingEps"),
            "forwardEps": info.get("forwardEps"),
            "dividendYield": info.get("dividendYield"),
            "profitMargins": info.get("profitMargins"),
            "operatingMargins": info.get("operatingMargins"),
            "returnOnAssets": info.get("returnOnAssets"),
            "returnOnEquity": info.get("returnOnEquity"),
            "revenueGrowth": info.get("revenueGrowth"),
            "earningsGrowth": info.get("earningsGrowth"),
            "currentRatio": info.get("currentRatio"),
            "debtToEquity": info.get("debtToEquity"),
            "totalCash": info.get("totalCash"),
            "totalDebt": info.get("totalDebt"),
        }
    except Exception as e:
        return {"error": str(e)}

def get_advanced_financial_metrics(ticker: str) -> Dict[str, Any]:
    """
    Calculates advanced financial metrics: ROIC, FCF, Altman Z-Score, Piotroski F-Score, PEG, and Cost of Debt.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Helper to get safe float
        def get_val(df, key, idx=0, default=0.0):
            try:
                if key in df.index:
                    return float(df.loc[key].iloc[idx])
                return default
            except:
                return default

        # Fetch Financials
        balance_sheet = stock.balance_sheet
        income_stmt = stock.income_stmt
        cash_flow = stock.cash_flow
        
        if balance_sheet.empty or income_stmt.empty or cash_flow.empty:
            return {"error": "Insufficient financial data for advanced metrics."}

        # 1. Free Cash Flow (FCF)
        # FCF = Operating Cash Flow - Capital Expenditure
        ocf = get_val(cash_flow, "Total Cash From Operating Activities") # Newer yfinance key
        if ocf == 0.0:
            ocf = get_val(cash_flow, "Operating Cash Flow") # Fallback
            
        capex = get_val(cash_flow, "Capital Expenditure")
        if capex == 0.0: # Sometimes CapEx is negative in CF statement, sometimes positive.
             # Look for "Purchase Of PPE"
             capex = get_val(cash_flow, "Purchase Of PPE")
        
        # Ensure CapEx is treated as outflow (negative) for calculation if it comes as positive
        # But usually in yf, Purchase of PPE is negative. FCF = OCF + CapEx (if CapEx is negative)
        # Let's trust yfinance sign convention but be careful.
        # Standard: FCF = OCF - (-CapEx) = OCF + CapEx (if CapEx is negative number)
        # Let's just sum them if they have correct signs.
        fcf = ocf + capex 

        # 2. ROIC (Return on Invested Capital)
        # NOPAT / Invested Capital
        # NOPAT = EBIT * (1 - Tax Rate)
        ebit = get_val(income_stmt, "EBIT")
        if ebit == 0.0:
            ebit = get_val(income_stmt, "Operating Income")
            
        tax_provision = get_val(income_stmt, "Tax Provision")
        pretax_income = get_val(income_stmt, "Pretax Income")
        
        effective_tax_rate = 0.21 # Default
        if pretax_income > 0:
            effective_tax_rate = tax_provision / pretax_income
            effective_tax_rate = max(0.0, min(effective_tax_rate, 0.5)) # Clamp 0~50%

        nopat = ebit * (1 - effective_tax_rate)
        
        # Invested Capital = Total Debt + Total Equity - Cash
        total_debt = get_val(balance_sheet, "Total Debt")
        total_equity = get_val(balance_sheet, "Stockholders Equity")
        if total_equity == 0.0:
             total_equity = get_val(balance_sheet, "Total Stockholder Equity")
             
        cash_and_equivalents = get_val(balance_sheet, "Cash And Cash Equivalents")
        
        invested_capital = total_debt + total_equity - cash_and_equivalents
        
        roic = (nopat / invested_capital) if invested_capital > 0 else 0.0

        # 3. Altman Z-Score (Manufacturing Formula - General Approximation)
        # Z = 1.2A + 1.4B + 3.3C + 0.6D + 1.0E
        # A = Working Capital / Total Assets
        # B = Retained Earnings / Total Assets
        # C = EBIT / Total Assets
        # D = Market Value of Equity / Total Liabilities
        # E = Sales / Total Assets
        
        total_assets = get_val(balance_sheet, "Total Assets")
        total_liab = get_val(balance_sheet, "Total Liabilities Net Minority Interest")
        current_assets = get_val(balance_sheet, "Current Assets")
        current_liab = get_val(balance_sheet, "Current Liabilities")
        working_capital = current_assets - current_liab
        retained_earnings = get_val(balance_sheet, "Retained Earnings")
        market_cap = info.get("marketCap", 0)
        sales = get_val(income_stmt, "Total Revenue")

        z_score = 0.0
        if total_assets > 0 and total_liab > 0:
            A = working_capital / total_assets
            B = retained_earnings / total_assets
            C = ebit / total_assets
            D = market_cap / total_liab
            E = sales / total_assets
            z_score = 1.2*A + 1.4*B + 3.3*C + 0.6*D + 1.0*E

        # 4. Piotroski F-Score (0-9)
        # Requires current and previous year data
        f_score = 0
        try:
            # Current (t) and Previous (t-1)
            net_income_t = get_val(income_stmt, "Net Income", 0)
            net_income_prev = get_val(income_stmt, "Net Income", 1)
            roa_t = net_income_t / total_assets if total_assets else 0
            ocf_t = ocf
            
            # 1. Profitability
            if net_income_t > 0: f_score += 1
            if ocf_t > 0: f_score += 1
            if roa_t > (net_income_prev / get_val(balance_sheet, "Total Assets", 1) if get_val(balance_sheet, "Total Assets", 1) else 0): f_score += 1
            if ocf_t > net_income_t: f_score += 1
            
            # 2. Leverage/Liquidity
            # Long term debt ratio check? (Simplified: check if LTD decreased)
            ltd_t = get_val(balance_sheet, "Long Term Debt", 0)
            ltd_prev = get_val(balance_sheet, "Long Term Debt", 1)
            if ltd_t <= ltd_prev: f_score += 1
            
            curr_ratio_t = current_assets / current_liab if current_liab else 0
            curr_ratio_prev = get_val(balance_sheet, "Current Assets", 1) / get_val(balance_sheet, "Current Liabilities", 1) if get_val(balance_sheet, "Current Liabilities", 1) else 0
            if curr_ratio_t > curr_ratio_prev: f_score += 1
            
            # Shares outstanding (Did it not increase?)
            shares_t = get_val(balance_sheet, "Share Issued", 0) # Approximation
            shares_prev = get_val(balance_sheet, "Share Issued", 1)
            if shares_t <= shares_prev: f_score += 1
            
            # 3. Operating Efficiency
            # Gross Margin
            gm_t = (sales - get_val(income_stmt, "Cost Of Revenue", 0)) / sales if sales else 0
            sales_prev = get_val(income_stmt, "Total Revenue", 1)
            gm_prev = (sales_prev - get_val(income_stmt, "Cost Of Revenue", 1)) / sales_prev if sales_prev else 0
            if gm_t > gm_prev: f_score += 1
            
            # Asset Turnover
            at_t = sales / total_assets if total_assets else 0
            at_prev = sales_prev / get_val(balance_sheet, "Total Assets", 1) if get_val(balance_sheet, "Total Assets", 1) else 0
            if at_t > at_prev: f_score += 1
            
        except Exception:
            pass # F-score calculation can fail if history is missing, keep partial score or 0

        # 5. Cost of Debt (Est.)
        # Interest Expense / Total Debt
        interest_expense = get_val(income_stmt, "Interest Expense") # Often negative
        interest_expense = abs(interest_expense)
        cost_of_debt = (interest_expense / total_debt) if total_debt > 0 else 0.0

        # 6. EV/EBITDA
        enterprise_value = info.get("enterpriseValue")
        if not enterprise_value:
            enterprise_value = market_cap + total_debt - cash_and_equivalents
        
        ebitda = get_val(income_stmt, "EBITDA")
        if ebitda == 0.0:
            depreciation = get_val(cash_flow, "Depreciation And Amortization")
            if depreciation == 0.0:
                depreciation = get_val(cash_flow, "Depreciation")
            ebitda = ebit + depreciation

        ev_ebitda = (enterprise_value / ebitda) if ebitda != 0 else None

        return replace_nan_with_none({
            "ROIC": round(roic, 4),
            "FCF": fcf,
            "Altman_Z_Score": round(z_score, 2),
            "Piotroski_F_Score": f_score,
            "PEG_Ratio": info.get("pegRatio"),
            "EV_EBITDA": round(ev_ebitda, 2) if ev_ebitda is not None else None,
            "Cost_of_Debt": round(cost_of_debt, 4),
            "Invested_Capital": invested_capital,
            "Tax_Rate_Est": round(effective_tax_rate, 2)
        })

    except Exception as e:
        return {"error": f"Failed to calculate advanced metrics: {str(e)}"}

def get_analyst_recommendations(ticker: str) -> Dict[str, Any]:
    """
    Retrieves the latest analyst recommendations for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        Any: A summary of the latest analyst recommendations, usually a DataFrame.
    """
    stock = yf.Ticker(ticker)
    recommendations = stock.recommendations
    if recommendations is not None and not recommendations.empty:
        return replace_nan_with_none(recommendations.tail(5).to_dict('records'))
    return "No analyst recommendations found."

def get_income_statement(ticker: str, period: str = 'annual') -> Any:
    """
    Retrieves the income statement for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.
        period (str): 'annual' or 'quarterly'. Defaults to 'annual'.

    Returns:
        Any: The income statement, usually a DataFrame.
    """
    stock = yf.Ticker(ticker)
    if period == 'quarterly':
        income_stmt = stock.quarterly_income_stmt
    else:
        income_stmt = stock.income_stmt
    
    if income_stmt is not None and not income_stmt.empty:
        income_stmt.columns = income_stmt.columns.astype(str)
        return replace_nan_with_none(income_stmt.to_dict())
    return "No income statement found."

def get_balance_sheet(ticker: str, period: str = 'annual') -> Any:
    """
    Retrieves the balance sheet for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.
        period (str): 'annual' or 'quarterly'. Defaults to 'annual'.

    Returns:
        Any: The balance sheet, usually a DataFrame.
    """
    stock = yf.Ticker(ticker)
    if period == 'quarterly':
        balance_sheet = stock.quarterly_balance_sheet
    else:
        balance_sheet = stock.balance_sheet
    
    if balance_sheet is not None and not balance_sheet.empty:
        balance_sheet.columns = balance_sheet.columns.astype(str)
        return replace_nan_with_none(balance_sheet.to_dict())
    return "No balance sheet found."

def get_cash_flow(ticker: str, period: str = 'annual') -> Any:
    """
    Retrieves the cash flow statement for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.
        period (str): 'annual' or 'quarterly'. Defaults to 'annual'.

    Returns:
        Any: The cash flow statement, usually a DataFrame.
    """
    stock = yf.Ticker(ticker)
    if period == 'quarterly':
        cash_flow = stock.quarterly_cashflow
    else:
        cash_flow = stock.cashflow
    
    if cash_flow is not None and not cash_flow.empty:
        cash_flow.columns = cash_flow.columns.astype(str)
        return replace_nan_with_none(cash_flow.to_dict())
    return "No cash flow statement found."

def get_major_shareholders(ticker: str) -> Any:
    """
    Retrieves major institutional shareholders for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        Any: Major shareholders data, usually a DataFrame.
    """
    stock = yf.Ticker(ticker)
    major_holders = stock.major_holders
    if major_holders is not None and not major_holders.empty:
        return replace_nan_with_none(major_holders.to_dict())
    return "No major shareholders found."

def get_insider_transactions(ticker: str) -> Any:
    """
    Retrieves insider transactions for a given stock ticker.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        Any: Insider transactions data, usually a DataFrame.
    """

    stock = yf.Ticker(ticker)
    insider_transactions = stock.insider_transactions
    if insider_transactions is not None and not insider_transactions.empty:
        return replace_nan_with_none(insider_transactions.to_dict())
    return "No insider transactions found."

def get_beta(ticker: str) -> float:
    """
    Retrieves the beta value for a given stock ticker.
    Beta is a measure of a stock's volatility in relation to the overall market.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        float: The beta value of the stock. Returns None if not available.
    """

    stock = yf.Ticker(ticker)
    beta = stock.info.get("beta")
    return replace_nan_with_none(beta)