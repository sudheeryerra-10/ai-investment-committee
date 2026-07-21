import yfinance as yf
import requests

def get_stock_data(ticker_symbol: str) -> dict:
    """
    Fetches fundamental data for a given US stock ticker using yfinance.
    Includes custom session headers to avoid cloud IP rate-limiting.
    """
    ticker_symbol = ticker_symbol.upper().strip()
    
    # Create a custom requests session with a browser user-agent
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    })
    
    # Initialize yfinance Ticker with custom session
    ticker = yf.Ticker(ticker_symbol, session=session)
    info = ticker.info
    
    if not info or 'financialData' not in str(info):
        # Fallback check if info dictionary returned empty
        info = ticker.fast_info
        
    revenue_growth = info.get('revenueGrowth', 0.0)
    profit_margins = info.get('profitMargins', 0.0)
    
    # Convert growth and margins to percentages
    rev_growth_pct = revenue_growth * 100 if revenue_growth else 0.0
    profit_margin_pct = profit_margins * 100 if profit_margins else 0.0
    
    # Calculate Rule of 40
    rule_of_40 = rev_growth_pct + profit_margin_pct
    
    # Extract valuation and cash flow metrics
    fcf = info.get('freeCashflow', 0)
    market_cap = info.get('marketCap', 1)
    fcf_yield = (fcf / market_cap * 100) if fcf and market_cap else 0.0
    
    pe_ratio = info.get('trailingPE', 0.0)
    ps_ratio = info.get('priceToSalesTrailing12Months', 0.0)
    
    return {
        "ticker": ticker_symbol,
        "rule_of_40": round(rule_of_40, 2),
        "fcf_yield_pct": round(fcf_yield, 2),
        "pe_ratio": round(pe_ratio, 2) if pe_ratio else "N/A",
        "ps_ratio": round(ps_ratio, 2) if ps_ratio else "N/A",
        "raw_info": info
    }