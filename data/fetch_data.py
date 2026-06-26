import yfinance as yf
from datetime import datetime, timedelta

def fetch_stock_data(ticker):


end = datetime.today()
start = end - timedelta(days=5*365)

stock = yf.Ticker(ticker)

df = yf.download(
    ticker,
    start=start,
    end=end,
    progress=False,
    auto_adjust=True
)

info = stock.info

return df, info
