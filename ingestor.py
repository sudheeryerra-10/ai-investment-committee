import yfinance as yf
from typing import Dict, Any

def fetch_financial_metrics(ticker_symbol: str) -> Dict[str, Any]:
    """
    Fetches raw financial data via yfinance and derives core quantitative metrics:
    - Rule of 40 (YoY Revenue Growth % + FCF Margin %)
    - FCF Yield %
    - Key Multiples (P/E, P/S)
    """
    print(f"[Ingestor] Fetching live data for {ticker_symbol.upper()}...")
    stock = yf.Ticker(ticker_symbol)
    
    info = stock.info
    
    # 1. Market Cap & Basic Info
    market_cap = info.get("marketCap", 0) or 0
    current_price = info.get("currentPrice") or info.get("regularMarketPrice", 0) or 0
    company_name = info.get("longName", ticker_symbol)
    
    # 2. Revenue Growth (YoY)
    rev_growth = (info.get("revenueGrowth") or 0.0) * 100  # Convert fraction to %
    
    # 3. Free Cash Flow & FCF Margin
    free_cash_flow = info.get("freeCashflow") or 0
    total_revenue = info.get("totalRevenue") or 0
    
    if total_revenue and total_revenue > 0:
        fcf_margin = (free_cash_flow / total_revenue) * 100
    else:
        fcf_margin = 0.0
        
    if market_cap and market_cap > 0:
        fcf_yield = (free_cash_flow / market_cap) * 100
    else:
        fcf_yield = 0.0
        
    # 4. Rule of 40 Calculation
    rule_of_40 = rev_growth + fcf_margin
    
    # 5. Key Valuation Multiples
    pe_ratio = info.get("trailingPE")
    ps_ratio = info.get("priceToSalesTrailing12Months")
    
    payload = {
        "ticker": ticker_symbol.upper(),
        "company_name": company_name,
        "current_price": current_price,
        "market_cap": market_cap,
        "revenue_growth_pct": round(rev_growth, 2),
        "fcf_margin_pct": round(fcf_margin, 2),
        "fcf_yield_pct": round(fcf_yield, 2),
        "rule_of_40_score": round(rule_of_40, 2),
        "pe_ratio": round(pe_ratio, 2) if pe_ratio else None,
        "ps_ratio": round(ps_ratio, 2) if ps_ratio else None,
        "sector": info.get("sector", "Unknown"),
        "industry": info.get("industry", "Unknown")
    }
    
    print(f"[Ingestor] Data successfully processed for {ticker_symbol.upper()}. Rule of 40: {payload['rule_of_40_score']}%")
    return payload

if __name__ == "__main__":
    # Test script with a high-growth ticker (e.g., PLTR or NVDA)
    test_data = fetch_financial_metrics("PLTR")
    import json
    print(json.dumps(test_data, indent=2))