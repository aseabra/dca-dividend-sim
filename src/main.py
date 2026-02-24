from __future__ import annotations

from pathlib import Path

from src.data import fetch_market_data
from src.simulate import simulate_dca_dividends
from src.plotting import plot_results

def main() -> None:
  ticker = "AAPL" # change me
  start = "2025-01-01"  # change me
  end = "2026-01-01"  # change me
  monthly = 200.0 # change me

  md = fetch_market_data(ticker, start, end)
  df = simulate_dca_dividends(md.prices, md.dividends, monthly)

  # Summary
  last = df.iloc[-1]
  print("\n---End summary---")
  print(f"Ticker: {md.ticker}")
  print(f"Period: {df.index.min().date()} -> {df.index.max().date()}")
  print(f"Monthly contribution: {monthly}")
  print(f"Contributed: {last['contributed']:.2f}")
  print(f"Paid-out total: {last['value_no_drip_total']:.2f} (cash dividends: {last['cash_dividends']:.2f})")
  print(f"DRIP total: {last['value_drip']:.2f}")

  # Plot
  out = Path("outputs") / f"{ticker}_{start}_{end}_{int(monthly)}permonth.html"
  title = f"{ticker}: DCA {monthly:.0f}/month - dividends paid out vs reinvested"
  plot_results(df, title=title, output_html=out)

  print(f"\nChart saved to: {out.resolve()}")
  
if __name__ == "__main__":
  main()