from __future__ import annotations

import pandas as pd

def _month_end_invest_dates(prices: pd.Series) -> pd.DatetimeIndex:
  """
  Return month_end invest dates aligned to actual trading days in 'prices'
  Strategy: for each calendar month, invest on the last available trading day.
  """
  idx = pd.to_datetime(prices.index).tz_localize(None)
  last_by_month = idx.to_series().groupby(idx.to_period("M")).max()
  monthly_last = prices.resample("ME").last()
  return pd.DatetimeIndex(last_by_month.values)

def simulate_dca_dividends(
    prices: pd.Series,
    dividends: pd.Series,
    monthly_amount: float,
) -> pd.DataFrame:
  """
  Simulate monthly DCA into a single asset, comparing:
  - dividends paid out (tracked as cash)
  - dividends reinvested (DRIP)
  
  Assumptions (v1):
  - invest monthly on the last trading day of each month at that day's close price
  - Dividends are applied on the dividend event date (as indexed in 'dividends')
  - Reinvestment buys shares at that day's close price
  - No FX, fees or taxes
  """
  if prices.empty:
    raise ValueError("prices is empty")
  if monthly_amount <= 0:
    raise ValueError("monthly_amount must be > 0")
  
  # Normalize indexes (defensive)
  prices = prices.copy()
  prices.index = pd.to_datetime(prices.index).tz_localize(None)
  prices = prices.sort_index()

  dividends = dividends.copy() if dividends is not None else pd.Series(dtype=float)
  if not dividends.empty:
    dividends.index = pd.to_datetime(dividends.index).tz_localize(None)
    dividends = dividends.sort_index()
    dividends = dividends[dividends > 0]

  invest_dates = set(_month_end_invest_dates(prices))

  # Align dividends to trading days (0 on non-dividend days)
  div_daily = dividends.reindex(prices.index).fillna(0.0)

  # State
  shares_no_drip = 0.0
  cash_dividends = 0.0

  shares_drip = 0.0

  contributed = 0.0

  rows = []
  for day, price in prices.items():
    price = float(price)
    div_per_share = float(div_daily.loc[day])

    # Monthly buy
    if day in invest_dates:
      buy_shares = monthly_amount / price
      shares_no_drip += buy_shares
      shares_drip += buy_shares
      contributed += monthly_amount

    # Dividend event
    if div_per_share > 0:
      # paid-out: add to cash
      cash_dividends += shares_no_drip + div_per_share

      # DRIP: reinvest immediately
      drip_cash = shares_drip * div_per_share
      shares_drip += drip_cash / price

    value_no_drip_total = shares_no_drip * price + cash_dividends
    value_drip = shares_drip * price

    rows.append(
      {
        "date": day,
        "price": price,
        "contributed": contributed,
        "shares_no_drip": shares_no_drip,
        "cash_dividends": cash_dividends,
        "value_no_drip_total": value_no_drip_total,
        "shares_drip": shares_drip,
        "value_drip": value_drip,
      }
    )
  
  df = pd.DataFrame(rows).set_index("date")
  return df
