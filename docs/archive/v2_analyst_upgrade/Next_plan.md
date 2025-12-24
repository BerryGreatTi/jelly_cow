# Implementation Plan (Next_plan.md)

This plan outlines the steps to implement the specifications defined in `Next_spec.md`, incorporating robust quantitative methods and market-aware logic.

## Phase 1: Tooling Upgrade (The Foundation)
*Goal: Equip the agents with calculators for advanced metrics and raw data processing.*

### 1.1. Upgrade `tools/fa.py` (Fundamental Analysis Tools)
*   **Action**: Implement `get_advanced_financial_metrics(ticker)` function.
*   **Details**:
    *   Fetch raw financial data (Income, Balance, Cash Flow) using `yfinance`.
    *   **Calculate**:
        *   `ROIC`: NOPAT / Invested Capital (Use effective tax rate).
        *   `FCF`: Operating Cash Flow - CapEx.
        *   `Altman Z-Score`: 1.2A + 1.4B + 3.3C + 0.6D + 1.0E (Standard formula for manufacturing, adapt for non-manufacturing if possible, or stick to general).
        *   `Piotroski F-Score`: 9-point scoring system based on y-o-y changes.
        *   `PEG`: P/E / Earnings Growth Rate (Handle cases with negative earnings/growth).
        *   `EV/EBITDA`: Enterprise Value / EBITDA.
        *   `Cost of Debt (Est.)`: Interest Expense / Total Debt (Required for future WACC model).

### 1.2. Upgrade `tools/ta.py` (Technical & Quant Tools)
*   **Action**: Implement `get_risk_metrics(ticker)` function with **Benchmark Awareness**.
*   **Details**:
    *   **Market Detection**: Determine if ticker is KR (ends in .KS, .KQ) or US/Other.
    *   **Benchmark Selection**: Use `^GSPC` (S&P 500) for US, `^KS11` (KOSPI) for KR.
    *   **Risk-Free Rate**: Fetch `^TNX` (US 10Y Treasury) for US. For KR, use a fixed estimate (e.g., 3.5%) or fetch KR 10Y if available, otherwise default to a conservative 4%.
    *   **Data Fetching**: Get 1-year daily adjusted close prices for **both** the stock and the benchmark.
    *   **Calculate**:
        *   `Annualized Volatility`: Std Dev of daily returns * sqrt(252).
        *   `MDD (Max Drawdown)`: Worst peak-to-trough decline.
        *   `Beta`: Covariance(Stock_Ret, Market_Ret) / Variance(Market_Ret).
        *   `Sharpe Ratio`: (CAGR - RiskFree) / Volatility.
        *   `Sortino Ratio`: (CAGR - RiskFree) / Downside Deviation.

### 1.3. **NEW** - Create `tools/portfolio_math.py` (Portfolio Science)
*   **Action**: Implement `get_portfolio_analysis(portfolio_data)` function.
*   **Rationale**: Agents need to calculate correlations and concentration risks mathematically.
*   **Details**:
    *   **Correlation Matrix**:
        *   Input: List of tickers.
        *   Output: Matrix highlighting high correlation (>0.7) and negative correlation (<0.0) pairs.
    *   **Concentration & Drift**:
        *   Calculate current **Weights** (Value / Total Portfolio Value).
        *   Calculate **HHI (Herfindahl-Hirschman Index)** to quantify concentration risk.
        *   (Future) Compare against target weights if defined in user profile to report 'Drift'.

---

## Phase 2: Model Activation (The Logic)
*Goal: Activate the dormant `models/` directory for theory-based calculations.*

### 2.1. Implement CAPM & WACC
*   **Action**: Update `models/cost_of_equity/capm.py` and create `models/wacc.py`.
*   **Details**:
    *   `CAPM`: Requires `risk_free_rate`, `beta` (from Phase 1.2), and `market_return`.
    *   `WACC`: Requires `cost_of_equity` (from CAPM), `cost_of_debt` (from Phase 1.1), `tax_rate`, and `equity/debt weights`.

---

## Phase 3: Agent Intelligence (The Brain)
*Goal: Teach agents to request and interpret the new metrics.*

### 3.1. Update `FundamentalAnalyzer` Instruction
*   **Action**: Modify `agents/fundamental_analyzer.py`.
*   **Instruction Changes**:
    *   Mandate calling `get_advanced_financial_metrics`.
    *   Explicitly ask to interpret `ROIC` vs `WACC` (if available) to judge value creation.
    *   Use `Altman Z-Score` to flag distress.

### 3.2. Update `TechnicalAnalyzer` Instruction
*   **Action**: Modify `agents/technical_analyzer.py`.
*   **Instruction Changes**:
    *   Mandate calling `get_risk_metrics`.
    *   Focus on **Risk-Adjusted Returns** (Sharpe) rather than just raw direction.
    *   Use `Beta` to explain market sensitivity (e.g., "High beta means aggressive...").

### 3.3. Update `PortfolioAnalyzerAgent` Instruction
*   **Action**: Modify `agents/portfolio_analyzer_agent.py`.
*   **Instruction Changes**:
    *   **Mandate**: Call `get_portfolio_analysis` for the user's holdings.
    *   **Logic**: "If Correlation(A, B) > 0.7, warn about concentration risk."
    *   **Logic**: "Use HHI or Weights to identify if the portfolio is 'Drifting' towards excessive concentration in one stock or sector."
    *   **Logic**: "Check if the portfolio is overweight in High Beta stocks without hedging."

---

## Phase 4: Verification & UI
*Goal: Ensure the output is readable and accurate.*

### 4.1. Unit Testing
*   Create `tests/manual_verification.py` to run Phase 1 tools.
*   **Key Check**: Verify `Beta` calculation for a known stock (e.g., AAPL) matches public sources (approx. 1.2) to ensure Benchmark logic is working.

### 4.2. Formatter Agent Update
*   Ensure `FormatterAgent` can handle the `Correlation Matrix` data (e.g., presenting it as a list of "Highly Correlated Pairs").

---

## Execution Order
1.  **Phase 1.1**: `tools/fa.py` (Advanced Fundamentals)
2.  **Phase 1.2**: `tools/ta.py` (Risk Metrics with Benchmarking)
3.  **Phase 1.3**: `tools/portfolio_math.py` (Correlation Matrix)
4.  **Phase 3.1 & 3.2**: Agent Instructions (Single Asset)
5.  **Phase 3.3**: Agent Instruction (Portfolio)
6.  **Verification**: Test scripts and End-to-End query.
