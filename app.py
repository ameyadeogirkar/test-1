import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from data.fetch_data import fetch_stock_data

from analysis.fundamentals import (
    calculate_fundamental_score,
    get_company_overview
)

from analysis.valuation import (
    graham_intrinsic_value,
    dcf_valuation,
    valuation_status
)

from analysis.technicals import (
    calculate_indicators,
    technical_score
)

from analysis.risk import (
    calculate_risk_metrics
)

from forecast.prophet_model import (
    run_prophet_forecast
)

from forecast.arima_model import (
    run_arima_forecast
)

from forecast.montecarlo import (
    monte_carlo_forecast
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AlphaQuant Pro",
    layout="wide"
)

st.title("📈 AlphaQuant Pro")
st.caption(
    "Institutional Equity Research Terminal"
)

# --------------------------------------------------
# SEARCH SECTION
# --------------------------------------------------

ticker = st.text_input(
    "Enter Stock Symbol",
    value="RELIANCE.NS"
)

analyze = st.button(
    "🚀 Analyze Stock",
    use_container_width=True
)

if not analyze:
    st.info(
        "Enter a ticker and click Analyze."
    )
    st.stop()

# --------------------------------------------------
# FETCH DATA
# --------------------------------------------------

try:

    df, info = fetch_stock_data(
        ticker
    )

except Exception as e:

    st.error(
        f"Error fetching stock data: {e}"
    )

    st.stop()

# --------------------------------------------------
# BASIC VARIABLES
# --------------------------------------------------

st.write("DF Columns:", df.columns)

close = df["Close"]

st.write("Close Type:", type(close))
st.write("Close Last Value:", close.iloc[-1])

st.stop()
overview = get_company_overview(
    info
)

# --------------------------------------------------
# SCORES
# --------------------------------------------------

fund_score = calculate_fundamental_score(
    info
)

indicators = calculate_indicators(
    close
)

tech_score = technical_score(
    current_price,
    indicators
)

risk_metrics = calculate_risk_metrics(
    close
)

# --------------------------------------------------
# VALUATION
# --------------------------------------------------

eps = info.get("trailingEps")

growth = info.get(
    "earningsGrowth",
    0
)

intrinsic_value = graham_intrinsic_value(
    eps,
    growth
)

valuation_verdict = valuation_status(
    intrinsic_value,
    current_price
)

fcf = info.get("freeCashflow")

dcf_value = dcf_valuation(
    fcf
)

# --------------------------------------------------
# TABS
# --------------------------------------------------

tabs = st.tabs([
    "Overview",
    "Fundamentals",
    "Valuation",
    "Technicals",
    "Forecast",
    "Risk",
    "Recommendation"
])

# ==================================================
# OVERVIEW
# ==================================================

with tabs[0]:

    st.subheader(
        overview["company"]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Current Price",
        f"{current_price:.2f}"
    )

    col2.metric(
        "Sector",
        overview["sector"]
    )

    col3.metric(
        "Industry",
        overview["industry"]
    )

    st.write(
        f"Country: {overview['country']}"
    )

    st.write(
        f"Employees: {overview['employees']}"
    )

    st.write(
        f"Website: {overview['website']}"
    )

# ==================================================
# FUNDAMENTALS
# ==================================================

with tabs[1]:

    st.subheader(
        "Fundamental Analysis"
    )

    st.metric(
        "Financial Health Score",
        f"{fund_score}/10"
    )

    metrics = {
        "Market Cap":
            info.get("marketCap"),

        "PE Ratio":
            info.get("trailingPE"),

        "EPS":
            info.get("trailingEps"),

        "Revenue Growth":
            info.get("revenueGrowth"),

        "Profit Margin":
            info.get("profitMargins"),

        "Debt To Equity":
            info.get("debtToEquity")
    }

    st.dataframe(
        pd.DataFrame(
            metrics.items(),
            columns=["Metric","Value"]
        )
    )

# ==================================================
# VALUATION
# ==================================================

with tabs[2]:

    st.subheader(
        "Intrinsic Valuation"
    )

    st.metric(
        "Current Price",
        round(current_price,2)
    )

    st.metric(
        "Graham Value",
        round(intrinsic_value,2)
        if intrinsic_value
        else "N/A"
    )

    st.metric(
        "DCF Value",
        round(dcf_value,2)
        if dcf_value
        else "N/A"
    )

    st.success(
        valuation_verdict
    )

# ==================================================
# TECHNICALS
# ==================================================

with tabs[3]:

    st.subheader(
        "Technical Dashboard"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=close,
            name="Close"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=indicators["sma50"],
            name="SMA50"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=indicators["sma200"],
            name="SMA200"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.metric(
        "Technical Score",
        tech_score
    )

    st.metric(
        "RSI",
        round(
            indicators["rsi"].iloc[-1],
            2
        )
    )

# ==================================================
# FORECAST
# ==================================================

with tabs[4]:

    st.subheader(
        "Forecast Models"
    )

    with st.spinner(
        "Running Prophet..."
    ):

        prophet = run_prophet_forecast(
            df
        )

    prophet_target = float(
        prophet["yhat"].iloc[-1]
    )

    st.metric(
        "Prophet Forecast",
        round(
            prophet_target,
            2
        )
    )

    arima = run_arima_forecast(
        close
    )

    arima_target = float(
        arima.iloc[-1]
    )

    st.metric(
        "ARIMA Forecast",
        round(
            arima_target,
            2
        )
    )

    mc = monte_carlo_forecast(
        close
    )

    st.metric(
        "Monte Carlo Median",
        round(
            np.median(
                mc[-1]
            ),
            2
        )
    )

# ==================================================
# RISK
# ==================================================

with tabs[5]:

    st.subheader(
        "Risk Metrics"
    )

    st.metric(
        "Sharpe Ratio",
        round(
            risk_metrics["sharpe"],
            2
        )
    )

    st.metric(
        "Max Drawdown",
        f"{risk_metrics['max_drawdown']:.2%}"
    )

    st.metric(
        "VaR (95%)",
        f"{risk_metrics['var95']:.2%}"
    )

# ==================================================
# RECOMMENDATION
# ==================================================

with tabs[6]:

    total_score = (
        fund_score +
        tech_score
    )

    if total_score >= 10:

        verdict = "🟢 BUY"

    elif total_score >= 6:

        verdict = "🟡 HOLD"

    else:

        verdict = "🔴 SELL"

    st.header(
        verdict
    )

    st.metric(
        "Total Score",
        total_score
    )

    st.metric(
        "Current Price",
        round(
            current_price,
            2
        )
    )

    if intrinsic_value:

        upside = (
            (
                intrinsic_value -
                current_price
            )
            /
            current_price
        ) * 100

        st.metric(
            "Potential Upside",
            f"{upside:.2f}%"
        )
