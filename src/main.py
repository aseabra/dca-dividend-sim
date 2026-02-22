from __future__ import annotations

from src.data import fetch_market_data

def main() -> None:
  ticker = "AAPL"
  start = "2021-01-01"
  end = "2026-01-01"

  md = fetch_market_data(ticker, start, end)

  print(f"Ticker: {md.ticker}")
  print(f"Prices: {md.prices.index.min().date()} -> {md.prices.index.max().date()} | rows={len(md.prices)}")
  print(f"Dividends: count={len(md.dividends)} | total={md.dividends.sum():.4f}")

  print("\nLast 5 prices:")
  print(md.prices.tail())

  print("\nLast 5 dividends:")
  print(md.dividends.tail())

if __name__ == "__main__":
  main()