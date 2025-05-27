import pandas as pd
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv(r"C:\Users\admin\Music\Guvi\Driven Stock Analysis\Data\data\merged_and_sorted.csv")

# Convert date and extract year
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
latest_year = df['year'].max()

# Sort and calculate daily returns
df = df.sort_values(by=['Ticker', 'date'])
df['daily_return'] = df.groupby('Ticker')['close'].pct_change()

# Filter data for the latest year
latest_year_df = df[df['year'] == latest_year].copy()
latest_year_df['daily_return'] = latest_year_df['daily_return'].fillna(0)

# ✅ Calculate cumulative return using transform to preserve index
latest_year_df['cumulative_return'] = (
    latest_year_df.groupby('Ticker')['daily_return']
    .transform(lambda x: (1 + x).cumprod() - 1)
)

# Get final cumulative return per stock
final_returns = latest_year_df.groupby('Ticker')['cumulative_return'].last().sort_values(ascending=False)
top_5_tickers = final_returns.head(5).index

# Filter data for top 5 performing stocks
top_5_data = latest_year_df[latest_year_df['Ticker'].isin(top_5_tickers)]

# Plot cumulative returns
plt.figure(figsize=(14, 7))
for ticker in top_5_tickers:
    ticker_data = top_5_data[top_5_data['Ticker'] == ticker]
    plt.plot(ticker_data['date'], ticker_data['cumulative_return'], label=ticker)

plt.title(f"Cumulative Return Over Time - Top 5 Performing Stocks ({latest_year})")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend(title="Ticker")
plt.grid(True)
plt.tight_layout()
plt.show()
