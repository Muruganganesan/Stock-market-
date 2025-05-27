import streamlit as st

# Import your functions (you may need to refactor scripts into importable functions)
from gainers_losers import show_top10_gainers_losers
from volatility import show_volatility_analysis
from cumulative_return import show_cumulative_return
from sector_performance import show_sectorwise_performance
from correlation import show_stock_price_correlation
from top5_gainers_losers import show_top5_gainers_losers

st.set_page_config(page_title="Stock Market Dashboard", layout="wide")

st.title("📊 Stock Market Analysis Dashboard")

# Sidebar navigation
page = st.sidebar.selectbox(
    "Select Analysis",
    [
        "Top 10 Gainers and Losers",
        "Top 5 Gainers and Losers",
        "Volatility Analysis",
        "Cumulative Return",
        "Sector-wise Performance",
        "Stock Price Correlation"
    ]
)

# Route to the correct function based on selection
if page == "Top 10 Gainers and Losers":
    show_top10_gainers_losers()
elif page == "Top 5 Gainers and Losers":
    show_top5_gainers_losers()
elif page == "Volatility Analysis":
    show_volatility_analysis()
elif page == "Cumulative Return":
    show_cumulative_return()
elif page == "Sector-wise Performance":
    show_sectorwise_performance()
elif page == "Stock Price Correlation":
    show_stock_price_correlation()
