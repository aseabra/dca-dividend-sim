from __future__ import annotations

from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

def plot_results(df: pd.DataFrame, title: str, output_html: str | Path | None = None) -> go.Figure:
  """
  Plot contributed vs portfolio value with dividends paid out vs reinvested.
  If output_html is provided, saves a self-contained HTML file.
  """
  required = {"contributed", "value_no_drip_total", "value_drip"}
  missing = required - set(df.columns)
  if missing:
    raise ValueError(f"Missing required columns for plotting: {sorted(missing)}")
  
  fig = go.Figure()

  fig.add_trace(go.Scatter(x=df.index, y=df["contributed"], name="Total contributed"))
  fig.add_trace(go.Scatter(x=df.index, y=df["value_no_drip_total"], name="Value (dividends paid out)"))
  fig.add_trace(go.Scatter(x=df.index, y=df["value_drip"], name="Value (dividends reinvested)"))
  fig.add_trace(go.Scatter(x=df.index, y=df["Shares_no_drip"] * ["price"], name="Value (price only, no DRIP)"))

  fig.update_layout(
    title=title,
    xaxis_title="Date",
    yaxis_title="Value",
    hovermode="x unified",
    legend_title_text="",
  )

  if output_html is not None:
    output_html = Path(output_html)
    output_html.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(str(output_html), include_plotlyjs="cdn")

  return fig
