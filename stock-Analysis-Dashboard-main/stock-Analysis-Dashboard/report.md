# Stock Analysis Dashboard — Project Report

---

## 1. Introduction

Stock market analysis is essential for investors and traders to make informed decisions. Technical analysis, which involves studying historical price data and computed indicators, is one of the most widely used approaches. This project presents an **interactive Stock Analysis Dashboard** that fetches real-time market data, computes key technical indicators, and visualizes trends through modern, interactive charts — all within a user-friendly web interface.

## 2. Abstract

The Stock Analysis Dashboard is a web-based application built using **Python**, **Streamlit**, **yfinance**, and **Plotly**. It enables users to enter any publicly traded stock ticker, select a custom date range, and analyze the stock's performance through five technical indicators: Simple Moving Average (SMA), Exponential Moving Average (EMA), Relative Strength Index (RSI), Moving Average Convergence Divergence (MACD), and Bollinger Bands. The dashboard presents candlestick charts with indicator overlays, dedicated RSI and MACD panels, a comprehensive performance summary, and data export functionality. It supports both US and Indian stock markets.

## 3. Tools Used

| Tool / Library | Version | Purpose |
|---|---|---|
| **Python** | 3.9+ | Core programming language |
| **Streamlit** | 1.45.x | Web application framework for the dashboard UI |
| **yfinance** | 0.2.x | Fetching historical stock data from Yahoo Finance |
| **Plotly** | 6.1.x | Interactive charting (candlestick, line, bar charts) |
| **Pandas** | 2.2.x | Data manipulation, indicator calculations, CSV export |
| **NumPy** | 2.2.x | Numerical computations (volatility, returns) |

## 4. Steps Involved in Building the Project

**Step 1 — Project Setup:** Initialized the project structure with `requirements.txt` for dependency management and `.streamlit/config.toml` for a dark-themed UI configuration.

**Step 2 — Sidebar & User Input:** Built a Streamlit sidebar allowing users to enter a stock ticker symbol, select start/end dates, choose a data interval (daily, weekly, monthly), and toggle individual technical indicators on or off.

**Step 3 — Data Fetching:** Used the `yfinance` library to fetch historical OHLCV (Open, High, Low, Close, Volume) data based on user inputs. Implemented error handling for invalid tickers and empty results.

**Step 4 — Technical Indicator Calculations:** Implemented five indicators using Pandas and NumPy:
- **SMA (20, 50):** Rolling mean of closing prices.
- **EMA (12, 26):** Exponentially weighted mean of closing prices.
- **RSI (14):** Computed from average gains and losses over a 14-period window.
- **MACD (12/26/9):** Difference between fast and slow EMAs, with a signal line.
- **Bollinger Bands (20, 2σ):** Middle band (SMA-20) ± 2 standard deviations.

**Step 5 — Interactive Charts:** Created three Plotly chart panels:
- *Candlestick Chart* with SMA, EMA, and Bollinger Band overlays, plus a volume subplot.
- *RSI Chart* with overbought (70) and oversold (30) reference lines and colored zones.
- *MACD Chart* with MACD line, signal line, and colored histogram bars.

**Step 6 — Performance Summary:** Computed and displayed key performance metrics: current price, period high/low, total and annualized returns, annualized volatility, average daily volume, 52-week high/low, and trading days in the selected range.

**Step 7 — CSV Export:** Added two download buttons — one for the full OHLCV + indicators dataset and one for a condensed performance summary, both exported as CSV files.

**Step 8 — Styling & Polish:** Applied custom CSS for a premium dark-themed interface with gradient headers, styled metric cards, and smooth hover effects.

## 5. Conclusion

The Stock Analysis Dashboard successfully delivers an end-to-end stock analysis workflow in a single, interactive web application. It demonstrates practical skills in **data fetching** (APIs), **data processing** (Pandas/NumPy), **data visualization** (Plotly), and **web development** (Streamlit). The modular design makes it easy to extend with additional indicators, multiple stock comparisons, or predictive models. This project is well-suited for showcasing in data science and analytics interviews, as it covers the complete pipeline from raw data ingestion to actionable visual insights.

---

*Report prepared as part of the Python Data Analytics project assignment.*
