import os
import json
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

from ingestor import get_stock_data
from schemas import QuantReport

load_dotenv()

# Safe API key lookup for both local environment and Streamlit Cloud Secrets
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("AQ.Ab8RN6LucwU076eFsdgbY65KniyOBG9Y9qQJx8phFdCoO5wbmg")
client = genai.Client(api_key=api_key)

QUANT_SYSTEM_PROMPT = """
You are Agent A: Institutional Lead Quantitative Fundamental Analyst.
Analyze the provided target ticker and fundamental quantitative metrics (Rule of 40, Free Cash Flow Yield, P/E, P/S).
Evaluate corporate operational performance and market valuation discipline.
Produce a structured QuantReport adhering strictly to the required output schema.
"""

def run_quant_agent(ticker_symbol: str) -> QuantReport:
    """
    Executes Agent A (Quant Analyst): Evaluates financial data and outputs structured QuantReport.
    """
    print(f"\n[Agent A: Quant Analyst (Gemini)] Analyzing {ticker_symbol.upper()}...")
    
    # Fetch live data strictly
    raw_data = get_stock_data(ticker_symbol)

    user_prompt = f"""
    Target Ticker: {ticker_symbol.upper()}
    
    Fundamental Quantitative Data:
    - Rule of 40 Score: {raw_data['rule_of_40']}%
    - Free Cash Flow Yield: {raw_data['fcf_yield_pct']}%
    - Trailing P/E Ratio: {raw_data['pe_ratio']}
    - Trailing P/S Ratio: {raw_data['ps_ratio']}
    
    Evaluate these fundamental metrics and produce a structured QuantReport.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=QUANT_SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=QuantReport,
            temperature=0.2,
        ),
    )
    
    report_dict = json.loads(response.text)
    return QuantReport(**report_dict)