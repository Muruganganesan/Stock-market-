import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("merged_and_sorted.csv")

# Convert date to datetime and extract year
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

# Sort data by Ticker and Date
df = df.sort_values(by=['Ticker', 'date'])

# Calculate daily returns
df['daily_return'] = df.groupby('Ticker')['close'].pct_change()

# Filter for the latest year
latest_year = df['year'].max()
latest_year_df = df[df['year'] == latest_year]

# Calculate volatility (standard deviation of daily returns) for each stock
volatility = latest_year_df.groupby('Ticker')['daily_return'].std().dropna()

# Get the top 10 most volatile stocks
top_10_volatility = volatility.sort_values(ascending=False).head(10)

# Plot bar chart of volatility
plt.figure(figsize=(12, 6))
top_10_volatility.plot(kind='bar', color='orange')
plt.title("Top 10 Most Volatile Stocks ({})".format(latest_year))
plt.xlabel("Ticker")
plt.ylabel("Volatility (Standard Deviation of Daily Returns)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y')
plt.show()
