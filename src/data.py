from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import pandas as pd
import yfinance as yf

@dataclass(frozen=True)
class MarketData:
  ticker: str
  prices: pd.Series # index: DatetimeIndex (daily trading days), values: close price
  dividends: pd.Series  # index: DatetimeIndex (dividend event dates), values: dividend per share

def fetch_market_data(
    ticker: str, 
    start: str,
    end: str,
    *,
    auto_adjust: bool = False,
) -> MarketData:
  """
  Fetch daily close prices and dividend events for a ticker.
  
  Notes:
    - prices are daily Close from yfinance history()
    - dividends are a Series (dividend per share) indexed by date
    - start/end are ISO string: "YYYY-MM-DD
  """

  yt = yf.Ticker(ticker)

  hist = yt.history(start=start, end=end, auto_adjust=auto_adjust)
  if hist is None or hist.empty:
    raise ValueError(f"No price history returned for ticker={ticker}, start={start}, end={end}")
  
  # Daily close price series
  prices = hist["Close"].copy()
  prices.name = "price"
  prices.index = pd.to_datetime(prices.index).tz_localize(None)

  # Dividend events (per share)
  divs = yt.dividends
  divs = divs.loc[start:end].copy() if not divs.empty else divs
  divs.index = pd.to_datetime(divs.index).tz_localize(None)
  divs.name = "dividend"

  # Keep only positive dividens (defensive)
  if not divs.empty:
    divs = divs[divs > 0]

  return MarketData(ticker=ticker, prices=prices, dividends=divs)