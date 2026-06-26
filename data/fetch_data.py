import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def fetch_stock_data(ticker):

    end = datetime.today()
    start = end - timedelta(days=5 * 365)

    stock = yf.Ticker(ticker)

    df = yf.download(
        ticker,
        start=start,
        end=end,
        progress=False,
        auto_adjust=True,
        group_by="column"
    )

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    info = stock.info

    return df, info
