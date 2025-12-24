# Verification & Test Plan (Next_test.md)

This document defines the test cases required to verify that `jelly_cow` has successfully attained the capabilities outlined in `Next_spec.md`.

## 1. Unit Tests (Tool Level)
*Goal: Verify that the new calculation functions in `tools/` return accurate and sane values.*

### Test Suite A: Advanced Fundamental Metrics (`tools/fa.py`)
*Target Function*: `get_advanced_financial_metrics(ticker)`

| Case ID | Test Case | Expected Outcome / Acceptance Criteria |
| :--- | :--- | :--- |
| **FA-01** | **Healthy Company (e.g., AAPL)** | • **ROIC**: Should be > 15% (High quality).<br>• **Altman Z-Score**: Should be > 3.0 (Safe zone).<br>• **FCF**: Should be positive and close to reported values from external sites. |
| **FA-02** | **Distressed/Risk Company** | • **Altman Z-Score**: Should be low (e.g., < 1.8 or close to it).<br>• **Piotroski F-Score**: Should be relatively low (0-4). |
| **FA-03** | **Growth Company** | • **PEG Ratio**: Should be calculated. If P/E is high but Growth is high, PEG should be reasonable (< 2.0).<br>• **EV/EBITDA**: Should be positive (for profitable firms) and comparable to sector peers. |
| **FA-04** | **Missing Data Handling** | If a ticker lacks some data (e.g., negative earnings preventing P/E), the function should return `None` or a clear "N/A" for that metric, not crash. |

### Test Suite B: Risk & Quant Metrics (`tools/ta.py`)
*Target Function*: `get_risk_metrics(ticker)`

| Case ID | Test Case | Expected Outcome / Acceptance Criteria |
| :--- | :--- | :--- |
| **TA-01** | **Standard Volatility** | • **Volatility**: Calculate annualized std dev. Compare with a known value (e.g., VIX or Yahoo Finance). |
| **TA-02** | **Drawdown Check** | • **MDD**: Should be a negative percentage (e.g., -0.15). Must accurately reflect the worst drop in the fetched period. |
| **TA-03** | **Risk-Adjusted Return** | • **Sharpe Ratio**: Should be calculated correctly.<br>• **Sortino Ratio**: Should be calculated. Typically higher than Sharpe if downside volatility is low. |
| **TA-04** | **Beta Calculation** | • **Beta**: Compare against S&P 500 (SPY). High beta stock (e.g., TSLA) should supply > 1.0, Low beta (e.g., KO) < 1.0. |

---

## 2. Integration Tests (Agent Level)
*Goal: Verify that Agents correctly choose and utilize the new tools.*

### Test Suite C: FundamentalAnalyzer Agent
*Prompt*: "Analyze the financial health of Tesla (TSLA)."

| Case ID | Checkpoint | Acceptance Criteria |
| :--- | :--- | :--- |
| **INT-FA-01** | **Tool Selection** | The agent **MUST** call `get_advanced_financial_metrics` in its execution trace. |
| **INT-FA-02** | **Report Content** | The final response must mention terms like **"ROIC"**, **"Free Cash Flow"**, or **"Z-Score"**. |
| **INT-FA-03** | **Interpretation** | The agent should not just list the number but interpret it (e.g., "Tesla's Z-Score of X suggests it is financially stable"). |

### Test Suite D: TechnicalAnalyzer Agent
*Prompt*: "How is the technical trend of NVDA?"

| Case ID | Checkpoint | Acceptance Criteria |
| :--- | :--- | :--- |
| **INT-TA-01** | **Tool Selection** | The agent **MUST** call `get_risk_metrics` in its execution trace. |
| **INT-TA-02** | **Report Content** | The final response must include a "Risk Profile" section mentioning **Sharpe Ratio**, **MDD**, or **Volatility**. |
| **INT-TA-03** | **Risk Warning** | If MDD is high, the agent should explicitly warn the user about potential downside risk. |

---

## 3. Scenario Tests (End-to-End)
*Goal: Verify the "Professional Analyst" experience.*

### Test Suite E: Portfolio Rebalancing
*Context*: User has a portfolio with High Correlation assets (e.g., GOOGL, MSFT, NVDA).
*Prompt*: "Analyze my portfolio and suggest rebalancing."

| Case ID | Checkpoint | Acceptance Criteria |
| :--- | :--- | :--- |
| **E2E-01** | **Correlation & Concentration** | The `PortfolioAnalyzer` should identify highly correlated assets AND mention **Concentration Risk** (via HHI or weights). |
| **E2E-02** | **Actionable Advice** | The suggestion should be to diversify into a different sector or asset class to improve the portfolio's Sharpe Ratio. |

---

## 4. Test Execution Strategy
1.  **Manual Script**: Create `tests/manual_verification.py` to run Unit Tests (Suite A & B) quickly without spinning up the whole agent system.
2.  **Interactive Session**: Use the CLI to chat with the agent for Integration Tests (Suite C & D).
3.  **Log Review**: Check the agent's "Thought" process in the logs to ensure it is reasoning based on the new metrics, not hallucinating.
