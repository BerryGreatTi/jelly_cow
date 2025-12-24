# Professional Analyst Specification (Next_spec.md)

## 1. Overview
The goal is to elevate `jelly_cow` from a "Research Assistant" to a **"Professional Quantitative & Fundamental Analyst"**. The system must shift from **descriptive analysis** (what happened?) to **diagnostic and predictive analysis** (why it happened and what are the risks?).

## 2. Key Competency Pillars

### Pillar A: Deep Fundamental Analysis (The "Quality" & "Value" Engine)
*Objective: Assess the true health and intrinsic value of a business beyond reported earnings.*

| Category | Metric / Model | Purpose | Implementation Target |
| :--- | :--- | :--- | :--- |
| **Profitability Quality** | **ROIC (Return on Invested Capital)** | Measures true return on capital, comparing it to WACC. | `tools/fa.py` |
| | **FCF (Free Cash Flow)** | The actual cash available to shareholders (Operating Cash Flow - CapEx). | `tools/fa.py` |
| **Financial Health** | **Altman Z-Score** | Predicts bankruptcy risk. Essential for screening "value traps". | `tools/fa.py` |
| | **Piotroski F-Score** | A 0-9 scale to determine the strength of a firm's financial position. | `tools/fa.py` |
| **Valuation** | **PEG Ratio** | P/E adjusted for growth. Crucial for judging if a growth stock is overpriced. | `tools/fa.py` |
| | **EV/EBITDA** | Capital-structure neutral valuation metric. | `tools/fa.py` |

### Pillar B: Quantitative Risk Management (The "Risk" Engine)
*Objective: Quantify uncertainty and downside potential using statistical methods.*

| Category | Metric / Model | Purpose | Implementation Target |
| :--- | :--- | :--- | :--- |
| **Risk-Adjusted Return** | **Sharpe Ratio** | Excess return per unit of total risk. | `tools/ta.py` |
| | **Sortino Ratio** | Excess return per unit of *downside* risk (penalizes only losses). | `tools/ta.py` |
| **Downside Risk** | **MDD (Maximum Drawdown)** | The worst historical loss from peak to trough. "How much can I lose?" | `tools/ta.py` |
| | **VaR (Value at Risk)** | (Optional) Estimate of potential loss over a specific period. | `tools/ta.py` |
| **Market Sensitivity** | **Beta** | Sensitivity to market movements (Systematic Risk). | `models/cost_of_equity/capm.py` |

### Pillar C: Portfolio Science (The "Allocation" Engine)
*Objective: Optimize asset mix based on mathematical correlation, not just qualitative diversity.*

| Category | Metric / Model | Purpose | Implementation Target |
| :--- | :--- | :--- | :--- |
| **Diversification** | **Correlation Matrix** | Identify assets that move together. Avoid "diworsification". | `agents/portfolio_analyzer_agent.py` |
| **Rebalancing** | **Drift Analysis** | Detect how far the current portfolio has deviated from target weights. | `agents/portfolio_analyzer_agent.py` |

---

## 3. Agent Persona Updates

### Fundamental Analyzer Agent
*   **Current**: Reads Income Statement -> Summarizes Revenue/Net Income.
*   **Next Spec**:
    *   Calculates **ROIC** and compares it to the industry average.
    *   Checks **Altman Z-Score** to flag distress risk immediately.
    *   Prioritizes **FCF** over Net Income.

### Technical Analyzer Agent
*   **Current**: Looks at RSI/MACD charts -> "Bullish/Bearish".
*   **Next Spec**:
    *   Calculates **Volatility (Annualized std dev)**.
    *   Reports **Sharpe/Sortino Ratios** to justify if the trend is worth the risk.
    *   Identifies **MDD** levels to set realistic stop-loss expectations.

### Portfolio Analyzer Agent
*   **Current**: "You have Apple and Tesla. Buy more Microsoft."
*   **Next Spec**: "Apple and Tesla have a correlation of 0.7 (High). Adding Microsoft (Correlation 0.6) increases concentration risk. Consider adding a defensive asset or a non-correlated sector."
