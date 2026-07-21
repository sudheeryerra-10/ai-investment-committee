import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from google import genai
from google.genai import types
from dotenv import load_dotenv

from schemas import QuantReport, RiskReport
from agent_quant import run_quant_agent

# Load environment variables
load_dotenv()

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("AQ.Ab8RN6IXgBuWZhoW4nJcy2YQMThiWFdIl6HnsorCB-xUwq4YlA"))

def fetch_ticker_news_rss(ticker_symbol: str, max_items: int = 5) -> str:
    """
    Fetches real-time stock news headlines and summaries via Yahoo Finance RSS.
    100% Free, no API key required, no anti-bot blocks.
    """
    rss_url = f"https://finance.yahoo.com/rss/headline?s={ticker_symbol.upper()}"
    print(f"[Risk Data Engine] Fetching live news feed for {ticker_symbol.upper()}...")
    
    try:
        req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        news_items = []
        
        for item in root.findall('./channel/item')[:max_items]:
            title = item.find('title').text if item.find('title') is not None else ""
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
            description = item.find('description').text if item.find('description') is not None else ""
            
            news_items.append(f"- [{pub_date}] {title}: {description}")
            
        if not news_items:
            return "No recent news items found via RSS feed."
            
        return "\n".join(news_items)
    except Exception as e:
        print(f"[Risk Data Engine Warning] RSS News fetch failed: {e}")
        return "Unable to fetch news feed. Proceeding with fundamental risk analysis."

RISK_SYSTEM_PROMPT = """
You are a cynical institutional macroeconomic risk officer. Your sole job is to protect capital by finding hidden traps, margin pressures, competitive threats, and geopolitical/regulatory vulnerabilities in an investment thesis.

You will receive:
1. A Quantitative Fundamental Report from Agent A (The Quant Analyst).
2. Live Real-Time News & Headlines for the company.

Your objective is to critique and stress-test Agent A's optimism using both corporate fundamentals and recent market news.

Perform a targeted assessment covering:
1. Geopolitical & Supply Chain Exposure (e.g., contract dependencies, export restrictions).
2. Regulatory & Legal Cross-winds / Short-seller & Analyst headwinds.
3. Macro/Interest Rate Sensitivities & Multiple Compression Risks.

Output a structured RiskReport:
- List specific identified_risks with category, severity (LOW, MEDIUM, HIGH), and description.
- Calculate a macro_headwind_score from 0.0 (no risk) to 100.0 (extreme risk).
- Write a compelling bear_case_thesis directly challenging Agent A's fundamental score.
"""

def run_risk_agent(ticker_symbol: str, quant_report: QuantReport) -> RiskReport:
    """
    Executes Agent B: Audits Agent A's report against live macro news using Gemini 2.5.
    """
    print(f"\n[Agent B: Risk Officer (Gemini)] Auditing macro & news risks for {ticker_symbol.upper()}...")
    
    # Fetch live stock-specific news
    live_news = fetch_ticker_news_rss(ticker_symbol)
    
    user_prompt = f"""
    Target Ticker: {ticker_symbol.upper()}
    
    Quant Analyst Report (Agent A):
    - Fundamental Score: {quant_report.fundamental_score}/100
    - Rule of 40 Score: {quant_report.rule_of_40_score}%
    - FCF Yield: {quant_report.fcf_yield_pct}%
    - P/E Ratio: {quant_report.pe_ratio}
    - Quant Summary: {quant_report.quant_summary}
    
    Recent Company News & Press Releases:
    {live_news}
    
    Evaluate the financial math alongside the recent headlines to generate the structured RiskReport.
    """
    
    # Call Gemini 2.5 Flash enforcing structured Pydantic output
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=RISK_SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=RiskReport,
            temperature=0.3,
        ),
    )
    
    report_dict = json.loads(response.text)
    return RiskReport(**report_dict)

if __name__ == "__main__":
    # Test pipeline up to Agent B
    quant_res = run_quant_agent("PLTR")
    risk_res = run_risk_agent("PLTR", quant_res)
    
    print("\n--- AGENT B OUTPUT (RISK REPORT) ---")
    print(json.dumps(risk_res.model_dump(), indent=2))