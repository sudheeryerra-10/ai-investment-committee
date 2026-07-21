import os
import json
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

from schemas import QuantReport, RiskReport, InvestmentMemo
from agent_quant import run_quant_agent
from agent_risk import run_risk_agent

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

PM_SYSTEM_PROMPT = """
You are the Chief Investment Officer (CIO) and Portfolio Manager of an institutional technology growth fund.
You do not analyze raw data directly; your sole function is to adjudicate the structural debate between Agent A (The Quant Analyst) and Agent B (The Macro Risk Officer).

Your Core Objectives:
1. Evaluate the tension between Agent A's fundamental growth math and Agent B's macro risk critique.
2. Determine a consensus conviction_score (0.0 to 100.0).
3. Assign a recommended_allocation_pct (0.0% to 10.0% of portfolio). 
   - Rule: If macro_headwind_score > 80.0 and P/E > 100, allocation MUST be capped below 3.0%.
4. Set human_in_the_loop_flag = True if valuation is extreme (P/E > 100 or P/S > 50) or if conviction is below 50.0.
5. Provide a final_decision rating: STRONG BUY, BUY, HOLD, or AVOID.

Output a structured InvestmentMemo adhering strictly to the Pydantic schema.
"""

def run_portfolio_manager(ticker_symbol: str, quant_report: QuantReport, risk_report: RiskReport) -> InvestmentMemo:
    """
    Executes Agent C (The Portfolio Manager): Adjudicates Agent A & Agent B outputs to produce a final InvestmentMemo.
    """
    print(f"\n[Agent C: Portfolio Manager (Gemini)] Adjudicating committee debate for {ticker_symbol.upper()}...")
    
    user_prompt = f"""
    Target Ticker: {ticker_symbol.upper()}
    
    === AGENT A (QUANT ANALYST) REPORT ===
    - Fundamental Score: {quant_report.fundamental_score}/100
    - Rule of 40 Score: {quant_report.rule_of_40_score}%
    - FCF Yield: {quant_report.fcf_yield_pct}%
    - Trailing P/E: {quant_report.pe_ratio}
    - Trailing P/S: {quant_report.ps_ratio}
    - Summary: {quant_report.quant_summary}
    
    === AGENT B (MACRO RISK OFFICER) REPORT ===
    - Macro Headwind Score: {risk_report.macro_headwind_score}/100
    - Identified Risks: {json.dumps([r.model_dump() for r in risk_report.identified_risks], indent=2)}
    - Bear Case Thesis: {risk_report.bear_case_thesis}
    
    Synthesize these opposing viewpoints and deliver the final InvestmentMemo.
    """
    
    # Call Gemini 2.5 Flash enforcing structured Pydantic output
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=PM_SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=InvestmentMemo,
            temperature=0.2,
        ),
    )
    
    report_dict = json.loads(response.text)
    return InvestmentMemo(**report_dict)

if __name__ == "__main__":
    # Test Full End-to-End Multi-Agent Loop
    ticker = "PLTR"
    
    quant_res = run_quant_agent(ticker)
    risk_res = run_risk_agent(ticker, quant_res)
    memo_res = run_portfolio_manager(ticker, quant_res, risk_res)
    
    print("\n==========================================")
    print(f"   FINAL INVESTMENT MEMO: ${ticker.upper()}")
    print("==========================================")
    print(json.dumps(memo_res.model_dump(), indent=2))