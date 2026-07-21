import feedparser

def fetch_financial_news(ticker_symbol: str) -> list[str]:
    """
    Fetches breaking financial headlines for a given ticker via Yahoo Finance RSS feed.
    """
    ticker_symbol = ticker_symbol.upper().strip()
    rss_url = f"https://finance.yahoo.com/rss/headline?s={ticker_symbol}"
    
    feed = feedparser.parse(rss_url)
    headlines = []
    
    for entry in feed.entries[:5]:
        headlines.append(f"- {entry.title} ({entry.published})")
        
    return headlines if headlines else [f"No recent news headlines found for {ticker_symbol}."]