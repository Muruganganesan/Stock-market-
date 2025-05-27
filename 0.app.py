import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Page Config ---
st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")
plt.style.use("seaborn-v0_8")


df = pd.read_csv("merged_and_sorted.csv")
sector_df = pd.read_csv("Sector_data.csv")

# --- Sidebar Navigation ---
#st.sidebar.title("Navigation")
tabs = [
    "Top 10 Gainers & Losers",
    "Volatility Analysis",
    "Cumulative Return (Top 5)",
    "Sector-wise Performance",
    "Stock Correlation Heatmap",
    "Monthly Top 5 Gainers & Losers"
]
choice = st.sidebar.radio("Select Analysis", tabs)

# --- 1. Top 10 Gainers & Losers ---
if choice == tabs[0]:
    st.header("Top 10 Gainers & Losers (Yearly)")

    def compute_yearly_return(group):
        group = group.sort_values(by='date')
        first_open = group.iloc[0]['open']
        last_close = group.iloc[-1]['close']
        yearly_return = (last_close - first_open) / first_open
        return pd.Series({'first_open': first_open, 'last_close': last_close, 'yearly_return': yearly_return})

    returns_df = df.groupby(['Ticker', 'year']).apply(compute_yearly_return).reset_index()
    latest_year = returns_df['year'].max()
    latest_returns = returns_df[returns_df['year'] == latest_year]

    top_10_green = latest_returns.sort_values(by='yearly_return', ascending=False).head(10)
    top_10_loss = latest_returns.sort_values(by='yearly_return').head(10)

    st.subheader(f"Top 10 Gainers ({latest_year})")
    st.dataframe(top_10_green[['Ticker', 'yearly_return', 'first_open', 'last_close']])

    st.subheader(f"Top 10 Losers ({latest_year})")
    st.dataframe(top_10_loss[['Ticker', 'yearly_return', 'first_open', 'last_close']])

    green_stocks = (latest_returns['yearly_return'] > 0).sum()
    red_stocks = (latest_returns['yearly_return'] < 0).sum()
    avg_price = df['close'].mean()
    avg_volume = df['volume'].mean()

    st.markdown(f"**Market Summary:**  \n✅ Green Stocks: `{green_stocks}`  \n❌ Red Stocks: `{red_stocks}`  \n💰 Average Price: `{avg_price:.2f}`  \n📈 Average Volume: `{avg_volume:.0f}`")

# --- 2. Volatility Analysis ---
elif choice == tabs[1]:
    st.header("Top 10 Most Volatile Stocks (Yearly)")
    df = df.sort_values(by=['Ticker', 'date'])
    df['daily_return'] = df.groupby('Ticker')['close'].pct_change()
    latest_year = df['year'].max()
    latest_year_df = df[df['year'] == latest_year]

    volatility = latest_year_df.groupby('Ticker')['daily_return'].std().dropna()
    top_10_volatility = volatility.sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(12, 6))
    top_10_volatility.plot(kind='bar', color='orange', ax=ax)
    ax.set_title(f"Top 10 Most Volatile Stocks ({latest_year})")
    ax.set_xlabel("Ticker")
    ax.set_ylabel("Volatility (Std Dev of Daily Returns)")
    ax.grid(axis='y')
    st.pyplot(fig)

# --- 3. Cumulative Return (Top 5) ---
elif choice == tabs[2]:
    st.header("Cumulative Return Over Time - Top 5 Performing Stocks")
    df = df.sort_values(by=['Ticker', 'date'])
    df['daily_return'] = df.groupby('Ticker')['close'].pct_change()
    latest_year = df['year'].max()
    latest_year_df = df[df['year'] == latest_year].copy()
    latest_year_df['daily_return'] = latest_year_df['daily_return'].fillna(0)
    latest_year_df['cumulative_return'] = latest_year_df.groupby('Ticker')['daily_return'].transform(lambda x: (1 + x).cumprod() - 1)

    final_returns = latest_year_df.groupby('Ticker')['cumulative_return'].last().sort_values(ascending=False)
    top_5_tickers = final_returns.head(5).index
    top_5_data = latest_year_df[latest_year_df['Ticker'].isin(top_5_tickers)]

    fig, ax = plt.subplots(figsize=(14, 7))
    for ticker in top_5_tickers:
        ticker_data = top_5_data[top_5_data['Ticker'] == ticker]
        ax.plot(ticker_data['date'], ticker_data['cumulative_return'], label=ticker)

    ax.set_title(f"Cumulative Return Over Time - Top 5 Performing Stocks ({latest_year})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Return")
    ax.legend(title="Ticker")
    ax.grid(True)
    st.pyplot(fig)

# --- 4. Sector-wise Performance ---
elif choice == tabs[3]:
    st.header("Average Yearly Return by Sector")
    latest_year = df['year'].max()
    yearly_df = df[df['year'] == latest_year].copy()
    yearly_df = yearly_df.sort_values(by=['Ticker', 'date'])
    yearly_df['daily_return'] = yearly_df.groupby('Ticker')['close'].pct_change().fillna(0)
    yearly_df['yearly_return'] = yearly_df.groupby('Ticker')['daily_return'].transform(lambda x: (1 + x).cumprod() - 1)
    final_returns = yearly_df.groupby('Ticker')['yearly_return'].last().reset_index()
    final_with_sector = pd.merge(final_returns, sector_df, on='Ticker', how='left')

    sector_performance = final_with_sector.groupby('sector')['yearly_return'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(12, 6))
    sector_performance.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title(f"Average Yearly Return by Sector ({latest_year})")
    ax.set_xlabel("Sector")
    ax.set_ylabel("Average Yearly Return")
    ax.grid(axis='y')
    st.pyplot(fig)

# --- 5. Stock Correlation Heatmap ---
elif choice == tabs[4]:
    st.header("Stock Price Correlation Heatmap")
    price_pivot = df.pivot(index='date', columns='Ticker', values='close')
    returns = price_pivot.pct_change().dropna()
    correlation_matrix = returns.corr()

    fig, ax = plt.subplots(figsize=(14, 10))
    sns.heatmap(correlation_matrix, cmap='coolwarm', annot=False, center=0, linewidths=0.5, ax=ax)
    ax.set_title("Stock Price Correlation Heatmap")
    st.pyplot(fig)

# --- 6. Monthly Top 5 Gainers & Losers ---
elif choice == tabs[5]:
    st.header("Monthly Top 5 Gainers & Losers")
    monthly_data = df.sort_values(by=['Ticker', 'date'])
    monthly_return = monthly_data.groupby(['Ticker', 'month'])['close'].agg(['first', 'last'])
    monthly_return['monthly_return'] = (monthly_return['last'] - monthly_return['first']) / monthly_return['first']
    monthly_return.reset_index(inplace=True)

    unique_months = monthly_return['month'].unique()
    month_selected = st.selectbox("Select Month", sorted(unique_months))
    month_df = monthly_return[monthly_return['month'] == month_selected].copy()

    top_gainers = month_df.sort_values(by='monthly_return', ascending=False).head(5)
    top_losers = month_df.sort_values(by='monthly_return', ascending=True).head(5)
    combined = pd.concat([top_gainers, top_losers])
    colors = ['green'] * 5 + ['red'] * 5

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(range(len(combined['Ticker'])), combined['monthly_return'] * 100, color=colors)
    ax.set_title(f"Top 5 Gainers & Losers - {month_selected}")
    ax.set_ylabel("Monthly Return (%)")
    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_xticks(range(len(combined['Ticker'])))
    ax.set_xticklabels(combined['Ticker'], rotation=45)
    st.pyplot(fig)

# --- Footer ---
st.markdown("---")
st.caption("📊 Stock Analysis Dashboard | Powered by Streamlit")
