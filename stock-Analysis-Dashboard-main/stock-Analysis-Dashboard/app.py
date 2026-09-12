"""
Stock Analysis Dashboard
========================
Interactive Streamlit dashboard for analyzing stock trends with technical indicators.
Uses yfinance for data, Plotly for charts, and Pandas for computation.
"""

import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io

# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Custom CSS for premium styling
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #0d1b2a 0%, #1b2838 50%, #0d2137 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(0, 212, 170, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    .main-header h1 {
        background: linear-gradient(90deg, #00D4AA, #00B4D8, #00D4AA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
    }
    .main-header p {
        color: #8899AA;
        font-size: 1rem;
        margin: 0.3rem 0 0 0;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1A1F2E 0%, #1E2536 100%);
        border: 1px solid rgba(0, 212, 170, 0.15);
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    div[data-testid="stMetric"] label {
        color: #8899AA !important;
        font-size: 0.85rem;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #E0E0E0 !important;
        font-weight: 700;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0E1117 0%, #151B28 100%);
        border-right: 1px solid rgba(0, 212, 170, 0.1);
    }
    section[data-testid="stSidebar"] .stMarkdown h2 {
        color: #00D4AA;
        font-size: 1.1rem;
        border-bottom: 1px solid rgba(0, 212, 170, 0.2);
        padding-bottom: 0.5rem;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: #1A1F2E;
        border-radius: 8px;
        border: 1px solid rgba(0, 212, 170, 0.15);
        padding: 0.5rem 1rem;
        color: #8899AA;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00D4AA22, #00B4D822) !important;
        border-color: #00D4AA !important;
        color: #00D4AA !important;
    }

    /* Download button */
    .stDownloadButton button {
        background: linear-gradient(135deg, #00D4AA, #00B4D8) !important;
        color: #0E1117 !important;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
    }
    .stDownloadButton button:hover {
        box-shadow: 0 4px 15px rgba(0, 212, 170, 0.4);
        transform: translateY(-1px);
    }

    /* Section dividers */
    .section-header {
        color: #00D4AA;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 1.5rem 0 0.8rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid rgba(0, 212, 170, 0.3);
    }

    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #1A1F2E, #1E2536);
        border: 1px solid rgba(0, 212, 170, 0.2);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Technical Indicator Calculations
# ──────────────────────────────────────────────

def calculate_sma(data: pd.DataFrame, period: int) -> pd.Series:
    """Calculate Simple Moving Average."""
    return data["Close"].rolling(window=period).mean()


def calculate_ema(data: pd.DataFrame, period: int) -> pd.Series:
    """Calculate Exponential Moving Average."""
    return data["Close"].ewm(span=period, adjust=False).mean()


def calculate_rsi(data: pd.DataFrame, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index."""
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(data: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9):
    """Calculate MACD, Signal Line, and Histogram."""
    ema_fast = data["Close"].ewm(span=fast, adjust=False).mean()
    ema_slow = data["Close"].ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def calculate_bollinger_bands(data: pd.DataFrame, period: int = 20, std_dev: int = 2):
    """Calculate Bollinger Bands (Upper, Middle, Lower)."""
    middle = data["Close"].rolling(window=period).mean()
    std = data["Close"].rolling(window=period).std()
    upper = middle + (std * std_dev)
    lower = middle - (std * std_dev)
    return upper, middle, lower


# ──────────────────────────────────────────────
# Chart Builders
# ──────────────────────────────────────────────

CHART_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(14, 17, 23, 0)",
    plot_bgcolor="rgba(26, 31, 46, 0.5)",
    font=dict(family="Inter, sans-serif", color="#E0E0E0"),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        showgrid=True,
        zeroline=False,
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        showgrid=True,
        zeroline=False,
    ),
    margin=dict(l=50, r=30, t=50, b=40),
    legend=dict(
        bgcolor="rgba(0,0,0,0.3)",
        bordercolor="rgba(0,212,170,0.2)",
        borderwidth=1,
        font=dict(size=11),
    ),
    hovermode="x unified",
)


def build_candlestick_chart(data, indicators, ticker):
    """Build the main candlestick chart with volume subplot and indicator overlays."""

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.75, 0.25],
        subplot_titles=("", "Volume"),
    )

    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="OHLC",
            increasing_line_color="#00D4AA",
            decreasing_line_color="#FF6B6B",
            increasing_fillcolor="#00D4AA",
            decreasing_fillcolor="#FF6B6B",
        ),
        row=1, col=1,
    )

    # SMA overlays
    if indicators.get("sma_20"):
        fig.add_trace(
            go.Scatter(x=data.index, y=data["SMA_20"], name="SMA 20",
                       line=dict(color="#FFD93D", width=1.5, dash="dot")),
            row=1, col=1,
        )
    if indicators.get("sma_50"):
        fig.add_trace(
            go.Scatter(x=data.index, y=data["SMA_50"], name="SMA 50",
                       line=dict(color="#FF8C42", width=1.5, dash="dot")),
            row=1, col=1,
        )

    # EMA overlays
    if indicators.get("ema_12"):
        fig.add_trace(
            go.Scatter(x=data.index, y=data["EMA_12"], name="EMA 12",
                       line=dict(color="#6C63FF", width=1.5)),
            row=1, col=1,
        )
    if indicators.get("ema_26"):
        fig.add_trace(
            go.Scatter(x=data.index, y=data["EMA_26"], name="EMA 26",
                       line=dict(color="#A855F7", width=1.5)),
            row=1, col=1,
        )

    # Bollinger Bands
    if indicators.get("bollinger"):
        fig.add_trace(
            go.Scatter(x=data.index, y=data["BB_Upper"], name="BB Upper",
                       line=dict(color="rgba(0,180,216,0.4)", width=1)),
            row=1, col=1,
        )
        fig.add_trace(
            go.Scatter(x=data.index, y=data["BB_Lower"], name="BB Lower",
                       line=dict(color="rgba(0,180,216,0.4)", width=1),
                       fill="tonexty", fillcolor="rgba(0,180,216,0.06)"),
            row=1, col=1,
        )

    # Volume bars
    colors = ["#00D4AA" if c >= o else "#FF6B6B"
              for c, o in zip(data["Close"], data["Open"])]
    fig.add_trace(
        go.Bar(x=data.index, y=data["Volume"], name="Volume",
               marker_color=colors, opacity=0.6, showlegend=False),
        row=2, col=1,
    )

    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text=f"{ticker} — Price & Volume", font=dict(size=18, color="#00D4AA")),
        xaxis_rangeslider_visible=False,
        height=600,
    )
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    return fig


def build_rsi_chart(data):
    """Build the RSI chart with overbought/oversold zones."""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=data.index, y=data["RSI"], name="RSI (14)",
                   line=dict(color="#00D4AA", width=2))
    )

    # Overbought / Oversold zones
    fig.add_hline(y=70, line_dash="dash", line_color="#FF6B6B",
                  annotation_text="Overbought (70)", annotation_position="right")
    fig.add_hline(y=30, line_dash="dash", line_color="#4ADE80",
                  annotation_text="Oversold (30)", annotation_position="right")
    fig.add_hline(y=50, line_dash="dot", line_color="rgba(255,255,255,0.15)")

    # Zone fill
    fig.add_hrect(y0=70, y1=100, fillcolor="rgba(255,107,107,0.08)", line_width=0)
    fig.add_hrect(y0=0, y1=30, fillcolor="rgba(74,222,128,0.08)", line_width=0)

    rsi_layout = {k: v for k, v in CHART_LAYOUT.items() if k != "yaxis"}
    rsi_yaxis = {**CHART_LAYOUT["yaxis"], "range": [0, 100]}
    fig.update_layout(
        **rsi_layout,
        title=dict(text="Relative Strength Index (RSI)", font=dict(size=16, color="#00D4AA")),
        yaxis=rsi_yaxis,
        height=300,
    )
    return fig


def build_macd_chart(data):
    """Build the MACD chart with signal line and histogram."""
    fig = go.Figure()

    # Histogram
    colors = ["#00D4AA" if v >= 0 else "#FF6B6B" for v in data["MACD_Hist"]]
    fig.add_trace(
        go.Bar(x=data.index, y=data["MACD_Hist"], name="Histogram",
               marker_color=colors, opacity=0.5)
    )

    # MACD Line
    fig.add_trace(
        go.Scatter(x=data.index, y=data["MACD"], name="MACD",
                   line=dict(color="#6C63FF", width=2))
    )

    # Signal Line
    fig.add_trace(
        go.Scatter(x=data.index, y=data["MACD_Signal"], name="Signal",
                   line=dict(color="#FF8C42", width=2, dash="dot"))
    )

    fig.add_hline(y=0, line_color="rgba(255,255,255,0.15)", line_width=1)

    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text="MACD (12, 26, 9)", font=dict(size=16, color="#00D4AA")),
        height=300,
    )
    return fig


# ──────────────────────────────────────────────
# Performance Summary
# ──────────────────────────────────────────────

def compute_performance(data: pd.DataFrame, ticker_info: dict):
    """Compute key performance metrics from historical data."""
    current_price = data["Close"].iloc[-1]
    start_price = data["Close"].iloc[0]
    period_high = data["High"].max()
    period_low = data["Low"].min()

    total_return = ((current_price - start_price) / start_price) * 100
    trading_days = len(data)
    years = trading_days / 252
    annualized_return = ((current_price / start_price) ** (1 / max(years, 0.01)) - 1) * 100 if years > 0 else 0

    daily_returns = data["Close"].pct_change().dropna()
    volatility = daily_returns.std() * np.sqrt(252) * 100  # Annualized
    avg_volume = data["Volume"].mean()

    # Attempt 52-week data from ticker info
    week_52_high = ticker_info.get("fiftyTwoWeekHigh", period_high)
    week_52_low = ticker_info.get("fiftyTwoWeekLow", period_low)
    company_name = ticker_info.get("shortName", ticker_info.get("longName", "N/A"))
    sector = ticker_info.get("sector", "N/A")
    market_cap = ticker_info.get("marketCap", None)

    return {
        "company_name": company_name,
        "sector": sector,
        "market_cap": market_cap,
        "current_price": current_price,
        "start_price": start_price,
        "period_high": period_high,
        "period_low": period_low,
        "total_return": total_return,
        "annualized_return": annualized_return,
        "volatility": volatility,
        "avg_volume": avg_volume,
        "week_52_high": week_52_high,
        "week_52_low": week_52_low,
        "trading_days": trading_days,
    }


def format_large_number(num):
    """Format large numbers for readability."""
    if num is None:
        return "N/A"
    if num >= 1e12:
        return f"${num / 1e12:.2f}T"
    if num >= 1e9:
        return f"${num / 1e9:.2f}B"
    if num >= 1e6:
        return f"${num / 1e6:.2f}M"
    return f"${num:,.0f}"


# ──────────────────────────────────────────────
# Main Application
# ──────────────────────────────────────────────

def main():
    # ── Header ──
    st.markdown("""
    <div class="main-header">
        <h1>📈 Stock Analysis Dashboard</h1>
        <p>Real-time technical analysis with interactive charts and key indicators</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar ──
    with st.sidebar:
        st.markdown("## 🔍 Stock Selection")

        ticker = st.text_input(
            "Ticker Symbol",
            value="AAPL",
            help="Enter a stock ticker (e.g., AAPL, MSFT, GOOGL). For Indian stocks use .NS or .BO suffix.",
        ).upper().strip()

        st.markdown("## 📅 Date Range")
        col_start, col_end = st.columns(2)
        with col_start:
            start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=365))
        with col_end:
            end_date = st.date_input("End Date", value=datetime.now())

        interval = st.selectbox(
            "Interval",
            options=["1d", "1wk", "1mo"],
            index=0,
            help="Data granularity: daily, weekly, or monthly.",
        )

        st.markdown("## 📊 Indicators")
        sma_20 = st.checkbox("SMA (20-day)", value=True)
        sma_50 = st.checkbox("SMA (50-day)", value=True)
        ema_12 = st.checkbox("EMA (12-day)", value=True)
        ema_26 = st.checkbox("EMA (26-day)", value=False)
        show_rsi = st.checkbox("RSI (14-period)", value=True)
        show_macd = st.checkbox("MACD (12/26/9)", value=True)
        show_bollinger = st.checkbox("Bollinger Bands (20, 2σ)", value=False)

        st.markdown("---")
        analyze_btn = st.button("🚀 Analyze", use_container_width=True, type="primary")

    # ── Session state for persistence ──
    if "data" not in st.session_state:
        st.session_state.data = None
        st.session_state.perf = None
        st.session_state.ticker_info = {}
        st.session_state.last_ticker = ""

    # ── Fetch & Compute ──
    if analyze_btn:
        if not ticker:
            st.error("⚠️ Please enter a valid ticker symbol.")
            return

        with st.spinner(f"Fetching data for **{ticker}**..."):
            try:
                stock = yf.Ticker(ticker)
                data = stock.history(start=start_date, end=end_date, interval=interval)

                if data.empty:
                    st.error(f"❌ No data found for **{ticker}**. Please check the ticker symbol and date range.")
                    return

                # Flatten multi-level columns if present
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)

                # Compute indicators
                data["SMA_20"] = calculate_sma(data, 20)
                data["SMA_50"] = calculate_sma(data, 50)
                data["EMA_12"] = calculate_ema(data, 12)
                data["EMA_26"] = calculate_ema(data, 26)
                data["RSI"] = calculate_rsi(data)
                data["MACD"], data["MACD_Signal"], data["MACD_Hist"] = calculate_macd(data)
                data["BB_Upper"], data["BB_Middle"], data["BB_Lower"] = calculate_bollinger_bands(data)

                try:
                    ticker_info = stock.info
                except Exception:
                    ticker_info = {}

                st.session_state.data = data
                st.session_state.perf = compute_performance(data, ticker_info)
                st.session_state.ticker_info = ticker_info
                st.session_state.last_ticker = ticker

            except Exception as e:
                st.error(f"❌ Error fetching data: {e}")
                return

    # ── Display Dashboard ──
    data = st.session_state.data
    perf = st.session_state.perf
    display_ticker = st.session_state.last_ticker or ticker

    if data is None or data.empty:
        # Welcome state
        st.markdown("""
        <div class="info-box">
            <h3 style="color: #00D4AA; margin-top: 0;">👋 Welcome!</h3>
            <p>Enter a stock ticker in the sidebar and click <strong>Analyze</strong> to get started.</p>
            <p style="color: #8899AA; font-size: 0.9rem;">
                <strong>Popular tickers:</strong> AAPL · MSFT · GOOGL · AMZN · TSLA · META · NVDA<br>
                <strong>Indian stocks:</strong> RELIANCE.NS · TCS.NS · INFY.NS · HDFCBANK.NS
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Company Info Bar ──
    st.markdown(f"""
    <div class="info-box" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <span style="font-size: 1.4rem; font-weight: 700; color: #E0E0E0;">{perf['company_name']}</span>
            <span style="color: #00D4AA; font-weight: 600; margin-left: 0.8rem;">{display_ticker}</span>
        </div>
        <div style="color: #8899AA; font-size: 0.9rem;">
            Sector: <strong style="color:#E0E0E0;">{perf['sector']}</strong> &nbsp;|&nbsp;
            Market Cap: <strong style="color:#E0E0E0;">{format_large_number(perf['market_cap'])}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Performance Metrics ──
    st.markdown('<p class="section-header">📊 Performance Summary</p>', unsafe_allow_html=True)

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Current Price", f"${perf['current_price']:.2f}",
              delta=f"{perf['total_return']:.2f}%")
    m2.metric("Period High", f"${perf['period_high']:.2f}")
    m3.metric("Period Low", f"${perf['period_low']:.2f}")
    m4.metric("Total Return", f"{perf['total_return']:.2f}%")
    m5.metric("Annualized Return", f"{perf['annualized_return']:.2f}%")
    m6.metric("Volatility", f"{perf['volatility']:.2f}%")

    m7, m8, m9, m10 = st.columns(4)
    m7.metric("52-Week High", f"${perf['week_52_high']:.2f}")
    m8.metric("52-Week Low", f"${perf['week_52_low']:.2f}")
    m9.metric("Avg Daily Volume", f"{perf['avg_volume']:,.0f}")
    m10.metric("Trading Days", f"{perf['trading_days']}")

    # ── Charts ──
    st.markdown('<p class="section-header">📈 Technical Charts</p>', unsafe_allow_html=True)

    indicators = {
        "sma_20": sma_20,
        "sma_50": sma_50,
        "ema_12": ema_12,
        "ema_26": ema_26,
        "bollinger": show_bollinger,
    }

    tab1, tab2, tab3, tab4 = st.tabs(["🕯️ Candlestick", "📉 RSI", "📊 MACD", "📋 Raw Data"])

    with tab1:
        fig_candle = build_candlestick_chart(data, indicators, display_ticker)
        st.plotly_chart(fig_candle, use_container_width=True)

    with tab2:
        if show_rsi:
            fig_rsi = build_rsi_chart(data)
            st.plotly_chart(fig_rsi, use_container_width=True)

            # RSI interpretation
            latest_rsi = data["RSI"].dropna().iloc[-1] if not data["RSI"].dropna().empty else None
            if latest_rsi is not None:
                if latest_rsi > 70:
                    st.warning(f"⚠️ RSI is at **{latest_rsi:.1f}** — the stock may be **overbought**.")
                elif latest_rsi < 30:
                    st.success(f"✅ RSI is at **{latest_rsi:.1f}** — the stock may be **oversold**.")
                else:
                    st.info(f"ℹ️ RSI is at **{latest_rsi:.1f}** — within normal range.")
        else:
            st.info("Enable the **RSI** indicator in the sidebar to view this chart.")

    with tab3:
        if show_macd:
            fig_macd = build_macd_chart(data)
            st.plotly_chart(fig_macd, use_container_width=True)

            # MACD interpretation
            latest_macd = data["MACD"].dropna().iloc[-1] if not data["MACD"].dropna().empty else None
            latest_signal = data["MACD_Signal"].dropna().iloc[-1] if not data["MACD_Signal"].dropna().empty else None
            if latest_macd is not None and latest_signal is not None:
                if latest_macd > latest_signal:
                    st.success("📈 **Bullish signal** — MACD is above the Signal line.")
                else:
                    st.warning("📉 **Bearish signal** — MACD is below the Signal line.")
        else:
            st.info("Enable the **MACD** indicator in the sidebar to view this chart.")

    with tab4:
        st.dataframe(
            data.style.format({
                "Open": "${:.2f}", "High": "${:.2f}", "Low": "${:.2f}", "Close": "${:.2f}",
                "SMA_20": "${:.2f}", "SMA_50": "${:.2f}", "EMA_12": "${:.2f}", "EMA_26": "${:.2f}",
                "RSI": "{:.2f}", "MACD": "{:.4f}", "MACD_Signal": "{:.4f}", "MACD_Hist": "{:.4f}",
                "BB_Upper": "${:.2f}", "BB_Middle": "${:.2f}", "BB_Lower": "${:.2f}",
                "Volume": "{:,.0f}",
            }),
            use_container_width=True,
            height=400,
        )

    # ── CSV Export ──
    st.markdown('<p class="section-header">💾 Export Data</p>', unsafe_allow_html=True)

    csv_buffer = io.StringIO()
    data.to_csv(csv_buffer)
    csv_data = csv_buffer.getvalue()

    col_dl1, col_dl2, _ = st.columns([1, 1, 3])
    with col_dl1:
        st.download_button(
            label="⬇️ Download Full CSV",
            data=csv_data,
            file_name=f"{display_ticker}_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )
    with col_dl2:
        # Summary report CSV
        summary_data = pd.DataFrame([perf])
        summary_csv = summary_data.to_csv(index=False)
        st.download_button(
            label="📄 Download Summary",
            data=summary_csv,
            file_name=f"{display_ticker}_summary_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

    # ── Footer ──
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #556677; font-size: 0.8rem;">'
        'Stock Analysis Dashboard • Built with Streamlit, yfinance & Plotly • Data from Yahoo Finance'
        '</p>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
