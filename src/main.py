from __future__ import annotations

from src.data import fetch_market_data
from src.simulate import simulate_dca_dividends

def main() -> None:
  ticker = "AAPL"
  start = "2021-01-01"
  end = "2026-01-01"
  monthly = 200.0

  md = fetch_market_data(ticker, start, end)
  df = simulate_dca_dividends(md.prices, md.dividends, monthly)

  print(f"Ticker: {md.ticker}")
  print(f"Monthly contribution: {monthly}")
  print(df.tail(3)[["contributed", "value_no_drip_total", "value_drip", "cash_dividends"]])

  last = df.iloc[-1]
  print("\n---End Summary---")
  print(f"Contributed: {last['contributed']:.2f}")
  print(f"Paid-out total: {last['value_no_drip_total']:.2f} (cash dividends: {last['cash_dividends']:.2f})")
  print(f"DRIP total: {last['value_drip']:.2f}")

if __name__ == "__main__":
  main()