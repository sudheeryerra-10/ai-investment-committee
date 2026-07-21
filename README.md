# 🤖 Multi-Agent AI Investment Committee

An institutional-grade equity analysis engine powered by **Gemini 2.5 Flash**, **Pydantic**, and **Streamlit**. 

This system uses a three-agent debate architecture to evaluate high-growth US equities by balancing quantitative financial metrics against real-time macroeconomic news and geopolitical risk factors.

---

## 🏛️ Architecture Overview

1. **Agent A (Quant Fundamental Analyst):** Evaluates live fundamental metrics via `yfinance` (Rule of 40 score, FCF Yield, P/E, P/S) and scores operational health.

2. **Agent B (Macro Risk Officer):** Scans real-time RSS news feeds for the target ticker to identify valuation risks, regulatory hurdles, and supply chain exposure.

3. **Agent C (Portfolio Manager / CIO):** Adjudicates the structural debate between Agent A and Agent B, determines portfolio allocation %, and enforces human-in-the-loop risk gating for extreme valuations.

---

## 🚀 Quickstart

1. **Clone the repository:**

   ```bash

   git clone [[https://github.com/sudheeryerra-10/ai-investment-committee.git](https://github.com/sudheeryerra-10/ai-investment-committee.git)](https://github.com/sudheeryerra-10/ai-investment-committee.git](https://github.com/sudheeryerra-10/ai-investment-committee.git))

   cd ai-investment-committee