import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

from schemas import QuantReport
from ingestor import fetch_financial_metrics

# Load environment variables from .env
load_dotenv()

# Initialize Gemini Client using the GEMINI_API_KEY from .env
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

QUANT_SYSTEM_PROMPT = """
You are an institutional growth equity analyst focusing strictly on maximum-return US equities. 
Your role is to look past corporate narrative and isolate the raw financial math.

You must evaluate the target stock using three quantitative pillars:
1. The Rule of 40 (YoY Revenue Growth % + Free Cash Flow Margin %): Scores > 40% indicate hyper-efficient growth.
2. Free Cash Flow Yield vs Sector Expectations.
3. Valuation Multiples (P/E and P/S relative to growth rates).

Output a structured QuantReport:
- Calculate an overall fundamental_score (0.0 to 100.0) reflecting business efficiency and valuation balance.
- Provide a razor-sharp quant_summary highlighting financial strengths and valuation risks.
- Restrict your focus purely to corporate fundamentals. Do not evaluate external macro news.
"""

def run_quant_agent(ticker_symbol: str) -> QuantReport:
    """
    Executes Agent A: Ingests financial data and returns a structured QuantReport Pydantic object using Gemini.
    """
    print(f"\n[Agent A: Quant Analyst (Gemini)] Analyzing {ticker_symbol.upper()}...")
    
    # 1. Fetch raw financial metrics
    metrics = fetch_financial_metrics(ticker_symbol)
    
    # 2. Call Gemini enforcing the QuantReport Pydantic schema
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Analyze the following financial metrics for {ticker_symbol.upper()}:\n{json.dumps(metrics, indent=2)}",
        config=types.GenerateContentConfig(
            system_instruction=QUANT_SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=QuantReport,
            temperature=0.2,
        ),
    )
    
    # 3. Parse and return Pydantic object
    report_dict = json.loads(response.text)
    return QuantReport(**report_dict)

if __name__ == "__main__":
    # Test Agent A with Palantir
    result = run_quant_agent("PLTR")
    print("\n--- AGENT A OUTPUT (GEMINI) ---")
    print(json.dumps(result.model_dump(), indent=2))