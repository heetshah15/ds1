"""
Crypto Price Ticker (15-minute refresh, full chart)
--------------------------------------------------
- Beginner-friendly, resume-ready Dash app
- Fetches full history from CoinGecko every 15 minutes (cached)
- pandas for data shaping, Plotly for visualization, Dash for UI
- CSV export of the currently displayed dataset
"""

from __future__ import annotations
import time
from datetime import datetime, timezone

import dash
from dash import Dash, dcc, html, Input, Output, State, no_update
import plotly.graph_objects as go
import pandas as pd

from utils import (
    fetch_market_chart_df_cached,
    COIN_OPTIONS,
    CG_IDS_TO_SYMBOL,
)

# ---- Dash app ----
app: Dash = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Crypto Ticker • 15-min Refresh"

FALLBACK_FIG = go.Figure().update_layout(
    template="plotly_dark",
    margin=dict(l=40, r=40, t=50, b=40),
    xaxis_title="Time",
    yaxis_title="Price (USD)",
    font=dict(size=12),
)

app.layout = html.Div(
    style={
        "fontFamily": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif",
        "backgroundColor": "#0f1419",
        "minHeight": "100vh",
        "color": "#e7e9ea",
        "padding": "20px",
    },
    children=[
        # Header
        html.Div(
            style={
                "maxWidth": "1400px",
                "margin": "0 auto",
                "marginBottom": "30px",
            },
            children=[
                html.Div(
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "gap": "15px",
                        "marginBottom": "20px",
                    },
                    children=[
                        html.Span(
                            "◉",
                            style={
                                "fontSize": "32px",
                                "color": "#1d9bf0",
                            }
                        ),
                        html.H1(
                            "Crypto Live Ticker",
                            style={
                                "margin": "0",
                                "fontSize": "28px",
                                "fontWeight": "700",
                            }
                        ),
                    ],
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "gap": "15px",
                        "flexWrap": "wrap",
                        "alignItems": "center",
                    },
                    children=[
                        dcc.Dropdown(
                            id="coin-select",
                            options=COIN_OPTIONS,
                            value="bitcoin",
                            clearable=False,
                            style={
                                "width": "200px",
                                "color": "#0f1419",
                            }
                        ),
                        dcc.RadioItems(
                            id="range-select",
                            options=[
                                {"label": "24H", "value": 1},
                                {"label": "7D", "value": 7},
                                {"label": "30D", "value": 30},
                            ],
                            value=1,
                            style={
                                "display": "flex",
                                "gap": "15px",
                            },
                            inputStyle={"marginRight": "6px"},
                        ),
                        html.Button(
                            "Export CSV",
                            id="export-btn",
                            style={
                                "padding": "8px 16px",
                                "backgroundColor": "#1d9bf0",
                                "color": "white",
                                "border": "none",
                                "borderRadius": "6px",
                                "cursor": "pointer",
                                "fontWeight": "600",
                                "fontSize": "14px",
                            }
                        ),
                        dcc.Download(id="download-data"),
                    ],
                ),
            ],
        ),

        # KPI row
        html.Div(
            style={
                "maxWidth": "1400px",
                "margin": "0 auto 30px",
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))",
                "gap": "20px",
            },
            children=[
                html.Div(
                    style={
                        "backgroundColor": "#16181c",
                        "padding": "20px",
                        "borderRadius": "12px",
                        "border": "1px solid #2f3336",
                    },
                    children=[
                        html.Label(
                            "Price (USD)",
                            style={
                                "fontSize": "13px",
                                "color": "#71767b",
                                "marginBottom": "8px",
                                "display": "block",
                            }
                        ),
                        html.Div(
                            id="live-price",
                            style={
                                "fontSize": "24px",
                                "fontWeight": "700",
                                "color": "#e7e9ea",
                            },
                            children="—"
                        ),
                    ]
                ),
                html.Div(
                    style={
                        "backgroundColor": "#16181c",
                        "padding": "20px",
                        "borderRadius": "12px",
                        "border": "1px solid #2f3336",
                    },
                    children=[
                        html.Label(
                            "Change",
                            style={
                                "fontSize": "13px",
                                "color": "#71767b",
                                "marginBottom": "8px",
                                "display": "block",
                            }
                        ),
                        html.Div(
                            id="live-change",
                            style={
                                "fontSize": "24px",
                                "fontWeight": "700",
                            },
                            children="—"
                        ),
                    ]
                ),
                html.Div(
                    style={
                        "backgroundColor": "#16181c",
                        "padding": "20px",
                        "borderRadius": "12px",
                        "border": "1px solid #2f3336",
                    },
                    children=[
                        html.Label(
                            "Last Updated",
                            style={
                                "fontSize": "13px",
                                "color": "#71767b",
                                "marginBottom": "8px",
                                "display": "block",
                            }
                        ),
                        html.Div(
                            id="last-updated",
                            style={
                                "fontSize": "16px",
                                "fontWeight": "600",
                                "color": "#e7e9ea",
                            },
                            children="—"
                        ),
                    ]
                ),
            ],
        ),

        # Chart
        html.Div(
            style={
                "maxWidth": "1400px",
                "margin": "0 auto",
                "backgroundColor": "#16181c",
                "padding": "20px",
                "borderRadius": "12px",
                "border": "1px solid #2f3336",
            },
            children=[
                dcc.Graph(
                    id="price-graph",
                    figure=FALLBACK_FIG,
                    config={"displayModeBar": False},
                    style={"height": "500px"},
                ),
                html.Div(
                    id="error-banner",
                    style={
                        "marginTop": "10px",
                        "padding": "12px",
                        "backgroundColor": "#3a1919",
                        "color": "#f4212e",
                        "borderRadius": "8px",
                        "display": "none",
                    }
                ),
            ],
        ),

        # 15-minute refresh timer (900,000 ms)
        dcc.Interval(id="refresh-interval", interval=900_000, n_intervals=0),

        # Store the latest dataframe for export
        dcc.Store(id="data-store", data=None),
    ],
)


# ---- Helper to create figure ----
def make_price_figure(df: pd.DataFrame, coin_id: str) -> go.Figure:
    """Create a styled price chart with the given data."""
    symbol = CG_IDS_TO_SYMBOL.get(coin_id, coin_id.upper()[:4])
    
    fig = go.Figure()
    
    # Main line
    fig.add_scatter(
        x=df["time"],
        y=df["price"],
        mode="lines",
        name=f"{symbol}/USD",
        line=dict(color="#1d9bf0", width=2),
        hovertemplate="<b>%{y:,.2f} USD</b><br>%{x|%Y-%m-%d %H:%M UTC}<extra></extra>",
    )
    
    # Current price marker
    fig.add_scatter(
        x=[df["time"].iloc[-1]],
        y=[df["price"].iloc[-1]],
        mode="markers",
        name="Current",
        marker=dict(size=10, color="#1d9bf0", line=dict(width=2, color="#e7e9ea")),
        hovertemplate="<b>Current: %{y:,.2f} USD</b><extra></extra>",
    )
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#16181c",
        plot_bgcolor="#16181c",
        margin=dict(l=60, r=40, t=60, b=60),
        xaxis_title="Time (UTC)",
        yaxis_title="Price (USD)",
        hovermode="x unified",
        title=dict(
            text=f"{symbol}/USD • {len(df):,} data points",
            x=0.02,
            xanchor="left",
            font=dict(size=18, color="#e7e9ea"),
        ),
        font=dict(color="#e7e9ea", size=12),
        showlegend=False,
    )
    
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="#2f3336",
        color="#71767b",
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="#2f3336",
        color="#71767b",
    )
    
    return fig


# ---- Main callback: fetch + render ----
@app.callback(
    Output("price-graph", "figure"),
    Output("live-price", "children"),
    Output("live-change", "children"),
    Output("live-change", "style"),
    Output("last-updated", "children"),
    Output("error-banner", "children"),
    Output("error-banner", "style"),
    Output("data-store", "data"),
    Input("refresh-interval", "n_intervals"),
    Input("coin-select", "value"),
    Input("range-select", "value"),
    prevent_initial_call=False,
)
def update_view(_tick, coin_id, days):
    """
    Triggers on:
      - Initial page load
      - Every 15 minutes (auto-refresh)
      - User changes coin or time range
    
    Uses 15-min cache to avoid redundant API calls.
    """
    # 15-min cache bucket: floor(now / 900 seconds)
    bucket = int(time.time() // 900)
    df, err = fetch_market_chart_df_cached(coin_id, int(days), bucket)

    # Error state
    if err or df is None or df.empty:
        error_style = {
            "marginTop": "10px",
            "padding": "12px",
            "backgroundColor": "#3a1919",
            "color": "#f4212e",
            "borderRadius": "8px",
            "display": "block",
        }
        change_style = {"fontSize": "24px", "fontWeight": "700", "color": "#e7e9ea"}
        return (
            FALLBACK_FIG,
            "—",
            "—",
            change_style,
            "—",
            f"⚠ API Error: {err or 'No data available'}",
            error_style,
            None
        )

    # Calculate KPIs
    last_price = float(df["price"].iloc[-1])
    
    # Format price based on value
    if last_price >= 1:
        price_text = f"${last_price:,.2f}"
    else:
        price_text = f"${last_price:.6f}"

    # Calculate change
    change_text = "—"
    change_style = {"fontSize": "24px", "fontWeight": "700", "color": "#71767b"}
    
    if len(df) > 1:
        first_price = float(df["price"].iloc[0])
        if first_price > 0:
            pct = ((last_price - first_price) / first_price) * 100
            arrow = "▲" if pct >= 0 else "▼"
            change_text = f"{arrow} {abs(pct):.2f}%"
            change_style["color"] = "#00ba7c" if pct >= 0 else "#f4212e"

    # Last updated timestamp
    now_utc = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")

    # Create figure
    fig = make_price_figure(df, coin_id)
    
    # Hide error banner
    error_style = {
        "marginTop": "10px",
        "padding": "12px",
        "backgroundColor": "#3a1919",
        "color": "#f4212e",
        "borderRadius": "8px",
        "display": "none",
    }

    return (
        fig,
        price_text,
        change_text,
        change_style,
        now_utc,
        "",
        error_style,
        df.to_dict(orient="list")
    )


# ---- CSV Export ----
@app.callback(
    Output("download-data", "data"),
    Input("export-btn", "n_clicks"),
    State("data-store", "data"),
    State("coin-select", "value"),
    State("range-select", "value"),
    prevent_initial_call=True,
)
def export_csv(n, data, coin_id, days):
    """Export the currently displayed chart data as CSV."""
    if not n or not data:
        return no_update

    df = pd.DataFrame(data)
    symbol = CG_IDS_TO_SYMBOL.get(coin_id, coin_id.upper()[:4])
    range_label = {1: "24h", 7: "7d", 30: "30d"}.get(int(days), f"{days}d")
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"{symbol}_{range_label}_{ts}.csv"

    return dcc.send_data_frame(df.to_csv, filename, index=False)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)