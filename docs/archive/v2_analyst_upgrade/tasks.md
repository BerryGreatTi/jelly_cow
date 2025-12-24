# Development Tasks: Professional Analyst Upgrade

This checklist is derived from `Next_plan.md` and `Next_spec.md`.

## Phase 1: Tooling Upgrade (The Foundation)
- [x] **1.1. Advanced Fundamental Metrics (`tools/fa.py`)**
    - [x] Import necessary libraries and defined constants.
    - [x] Implement `get_advanced_financial_metrics(ticker)`:
        - [x] Fetch Income, Balance, Cash Flow via `yfinance`.
        - [x] Calculate `ROIC` (NOPAT / Invested Capital).
        - [x] Calculate `FCF` (OCF - CapEx).
        - [x] Calculate `Altman Z-Score` (1.2A + 1.4B + 3.3C + 0.6D + 1.0E).
        - [x] Calculate `Piotroski F-Score`.
        - [x] Calculate `PEG Ratio` & `EV/EBITDA`.
        - [x] Calculate `Cost of Debt (Est.)`.
        - [x] Handle missing data/exceptions (return `None` for specific metrics if failed).

- [x] **1.2. Risk & Quant Metrics (`tools/ta.py`)**
    - [x] Implement `get_risk_metrics(ticker)`:
        - [x] **Market Detection**: Identify correct benchmark (`^GSPC` vs `^KS11`).
        - [x] **Data Fetching**: Fetch 1-year daily adjusted close for Stock & Benchmark.
        - [x] **Risk-Free Rate**: Fetch `^TNX` or use constant for KR.
        - [x] Calculate `Annualized Volatility`.
        - [x] Calculate `MDD` (Max Drawdown).
        - [x] Calculate `Beta` (Covariance/Variance).
        - [x] Calculate `Sharpe Ratio` & `Sortino Ratio`.

- [x] **1.3. Portfolio Science (`tools/portfolio_math.py`)**
    - [x] Create `tools/portfolio_math.py`.
    - [x] Implement `get_portfolio_analysis(portfolio_data)`:
        - [x] Fetch historical prices for all tickers in the portfolio.
        - [x] Calculate **Correlation Matrix**.
        - [x] Calculate **Portfolio Weights**.
        - [x] Calculate **HHI (Herfindahl-Hirschman Index)** for concentration risk.
        - [x] Return structured dictionary.

## Phase 2: Model Activation (The Logic)
- [x] **2.1. CAPM Update (`models/cost_of_equity/capm.py`)**
    - [x] Ensure `CAPM` model correctly uses inputs (Risk-Free, Beta, Market Return).
    - [x] Verify `calculate` method logic.

- [x] **2.2. WACC Implementation (`models/wacc.py`)**
    - [x] Create `models/wacc.py`.
    - [x] Define `WACC` class with `get_metadata`.
    - [x] Implement `calculate` method: `(E/V * Re) + (D/V * Rd * (1 - T))`.

## Phase 3: Agent Intelligence (The Brain)
- [x] **3.1. Fundamental Analyzer (`agents/fundamental_analyzer.py`)**
    - [x] Update system prompt:
        - [x] Mandate usage of `get_advanced_financial_metrics`.
        - [x] Add instructions for interpreting ROIC, Z-Score, FCF.

- [x] **3.2. Technical Analyzer (`agents/technical_analyzer.py`)**
    - [x] Update system prompt:
        - [x] Mandate usage of `get_risk_metrics`.
        - [x] Add instructions for interpreting Sharpe, Sortino, Beta, MDD.

- [x] **3.3. Portfolio Analyzer (`agents/portfolio_analyzer_agent.py`)**
    - [x] Update system prompt:
        - [x] Mandate usage of `get_portfolio_analysis`.
        - [x] Add instructions for checking Correlation, HHI, and Beta exposure.

## Phase 4: Verification & UI
- [x] **4.1. Unit Testing**
    - [x] Create `tests/manual_verification.py`.
    - [x] Implement `Test Suite A` (Fundamental Metrics) checks.
    - [x] Implement `Test Suite B` (Risk Metrics) checks.
    - [x] Run script and fix bugs.

- [x] **4.2. Formatter Agent**
    - [x] Verify `FormatterAgent` handles the new JSON output structures (especially Correlation Matrix) gracefully.
    - [x] (Optional) Update `agents/formatter_agent.py` if custom rendering is needed.
