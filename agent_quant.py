import os
import json
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

from schemas import QuantReport

load_dotenv()

# Safe API key lookup for local & Streamlit Cloud
api_key = os.getenv("AQ.Ab8RN6LucwU076eFsdgbY65KniyOBG9Y9qQJx8phFdCoO5wbmg") or st.secrets.get("AQ.Ab8RN6LucwU076eFsdgbY65KniyOBG9Y9qQJx8phFdCoO5wbmg")
client = genai.Client(api_key=api_key)

QUANT_SYSTEM_PROMPT = """
You are Agent A: Institutional Lead Quantitative Fundamental Analyst.
Your task is to analyze the given US stock ticker using real-time financial search.

You must search for and evaluate:
1. Trailing 12-Month (TTM) Revenue Growth (%) & Profit Margin (%)
2. Rule of 40 Score (Revenue Growth % + Profit Margin %)
3. Free Cash Flow (FCF) Yield (%)
4. Trailing P/E and P/S Ratios

Produce a structured QuantReport adhering strictly to the required output schema.
"""

def run_quant_agent(ticker_symbol: str) -> QuantReport:
    """
    Executes Agent A (Quant Analyst): Grounded with Google Search to evaluate stock fundamentals.
    """
    print(f"\n[Agent A: Quant Analyst (Gemini Grounded)] Analyzing {ticker_symbol.upper()}...")

    user_prompt = f"""
    Target Ticker: {ticker_symbol.upper()}
    
    Search for live financial data for {ticker_symbol.upper()}:
    - Find current Revenue Growth (TTM), Net Profit Margin, Free Cash Flow, Market Cap, P/E ratio, and P/S ratio.
    - Calculate the Rule of 40 score and FCF yield.
    - Analyze operational quality and valuation discipline.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=QUANT_SYSTEM_PROMPT,
            tools=[{"google_search": {}}],  # Enables live search grounding
            response_mime_type="application/json",
            response_schema=QuantReport,
            temperature=0.2,
        ),
    )
    
    report_dict = json.loads(response.text)
    return QuantReport(**report_dict)