import pandas as pd
import matplotlib.pyplot as plt

# Load main dataset
df = pd.read_csv("merged_and_sorted.csv")

# Load sector mapping
sector_df = pd.read_csv("Sector_data.csv") 

# Convert date and extract year
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
latest_year = df['year'].max()

# Filter for latest year
yearly_df = df[df['year'] == latest_year].copy()

# Sort and calculate daily returns
yearly_df = yearly_df.sort_values(by=['Ticker', 'date'])
yearly_df['daily_return'] = yearly_df.groupby('Ticker')['close'].pct_change()
yearly_df['daily_return'] = yearly_df['daily_return'].fillna(0)

# Calculate cumulative return for the year
yearly_df['yearly_return'] = yearly_df.groupby('Ticker')['daily_return'].transform(lambda x: (1 + x).cumprod() - 1)

# Get final return for each stock
final_returns = yearly_df.groupby('Ticker')['yearly_return'].last().reset_index()

# Merge with sector info
final_with_sector = pd.merge(final_returns, sector_df, on='Ticker', how='left')

# Calculate average return per sector
sector_performance = final_with_sector.groupby('sector')['yearly_return'].mean().sort_values(ascending=False)

# Plot sector performance
plt.figure(figsize=(12, 6))
sector_performance.plot(kind='bar', color='skyblue')
plt.title(f"Average Yearly Return by Sector ({latest_year})")
plt.xlabel("sector")
plt.ylabel("Average Yearly Return")
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y')
plt.show()
