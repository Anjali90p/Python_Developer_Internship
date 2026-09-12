# 📈 Stock Analysis Dashboard

An interactive stock analysis dashboard built with **Streamlit**, **yfinance**, and **Plotly**. Analyze any stock with real-time data, technical indicators, and beautiful interactive charts.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-6.1-3F4F75?logo=plotly&logoColor=white)

---

## ✨ Features

- **Real-time stock data** fetched via Yahoo Finance (yfinance)
- **5 Technical Indicators**: SMA (20/50), EMA (12/26), RSI (14), MACD (12/26/9), Bollinger Bands (20, 2σ)
- **Interactive Plotly charts**: Candlestick with overlays, RSI, MACD
- **Performance summary**: Return %, volatility, 52-week high/low, and more
- **CSV export**: Download full analysis data or summary report
- **Dark-themed UI** with premium styling
- **Supports US & Indian stocks** (e.g., AAPL, RELIANCE.NS)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Installation

```bash
# Clone or navigate to the project directory
cd stockAnalysis

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`.

---

## 🎯 How to Use

1. **Enter a stock ticker** in the sidebar (e.g., `AAPL`, `MSFT`, `RELIANCE.NS`)
2. **Select date range** and data interval (daily/weekly/monthly)
3. **Toggle indicators** — SMA, EMA, RSI, MACD, Bollinger Bands
4. **Click "Analyze"** to fetch data and generate charts
5. **Explore tabs** — Candlestick, RSI, MACD, and Raw Data
6. **Export data** as CSV using the download buttons

---

## 📊 Technical Indicators

| Indicator | Parameters | Description |
|---|---|---|
| SMA | 20-day, 50-day | Simple Moving Average — smooths price data |
| EMA | 12-day, 26-day | Exponential Moving Average — weights recent prices more |
| RSI | 14-period | Relative Strength Index — measures momentum (0–100) |
| MACD | 12/26/9 | Moving Average Convergence Divergence — trend following |
| Bollinger Bands | 20-period, 2σ | Volatility bands around moving average |

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Frontend / UI | Streamlit |
| Data Source | yfinance (Yahoo Finance) |
| Charting | Plotly |
| Data Processing | Pandas, NumPy |

---

## 📁 Project Structure

```
stockAnalysis/
├── app.py                  # Main Streamlit dashboard
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── report.md               # Project report (1-2 pages)
└── .streamlit/
    └── config.toml         # Streamlit theme configuration
```

---

## 📄 License

This project is for educational purposes.
