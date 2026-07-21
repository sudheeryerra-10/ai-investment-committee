import os
import json
import re
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

from schemas import QuantReport

load_dotenv()

# Safe API key lookup for local dev & Streamlit Cloud Secrets
api_key = os.getenv("AQ.Ab8RN6LucwU076eFsdgbY65KniyOBG9Y9qQJx8phFdCoO5wbmg") or st.secrets.get("AQ.Ab8RN6LucwU076eFsdgbY65KniyOBG9Y9qQJx8phFdCoO5wbmg")
client = genai.Client(api_key=api_key)

QUANT_SYSTEM_PROMPT = """
You are Agent A: Institutional Lead Quantitative Fundamental Analyst.
Analyze the target US stock ticker using real-time search grounding.

Search for and evaluate:
1. Trailing 12-Month (TTM) Revenue Growth (%) & Profit Margin (%)
2. Rule of 40 Score (Revenue Growth % + Profit Margin %)
3. Free Cash Flow (FCF) Yield (%)
4. Trailing P/E and P/S Ratios

CRITICAL OUTPUT REQUIREMENT:
You MUST return ONLY a raw JSON object adhering strictly to this format (no markdown fences, no extra text):
{
    "ticker": "TICKER",
    "valuation_verdict": "UNDERVALUED" | "FAIRLY_VALUED" | "OVERVALUED",
    "rule_of_40_score": 45.2,
    "fcf_yield_pct": 3.1,
    "pe_ratio": "32.5",
    "ps_ratio": "10.2",
    "key_positives": ["Point 1", "Point 2"],
    "key_risks": ["Risk 1", "Risk 2"],
    "quantitative_summary": "Detailed institutional analysis text..."
}
"""

def run_quant_agent(ticker_symbol: str) -> QuantReport:
    """
    Executes Agent A (Quant Analyst): Grounded with Google Search to evaluate stock fundamentals.
    """
    print(f"\n[Agent A: Quant Analyst (Gemini Grounded)] Analyzing {ticker_symbol.upper()}...")

    user_prompt = f"""
    Target Ticker: {ticker_symbol.upper()}
    
    Search for live financial metrics for {ticker_symbol.upper()} and output the results as a raw JSON object.
    """
    
    # Notice: response_mime_type and response_schema are omitted to allow Google Search Grounding
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=QUANT_SYSTEM_PROMPT,
            tools=[{"google_search": {}}],  # Live web grounding enabled
            temperature=0.1,
        ),
    )
    
    # Extract JSON cleanly from response text
    raw_text = response.text.strip()
    # Strip markdown block formatting if present
    if "```" in raw_text:
        raw_text = re.sub(r"^```(?:json)?\n|\n```$", "", raw_text, flags=re.MULTILINE).strip()
        
    report_dict = json.loads(raw_text)
    return QuantReport(**report_dict)