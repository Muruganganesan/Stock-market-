import pandas as pd

# Load the data
df = pd.read_csv(r"C:\Users\admin\Music\Guvi\Driven Stock Analysis\Data\data\merged_and_sorted.csv")

# Convert 'date' to datetime and extract year
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

# Compute yearly return per stock
def compute_yearly_return(group):
    group = group.sort_values(by='date')
    first_open = group.iloc[0]['open']
    last_close = group.iloc[-1]['close']
    yearly_return = (last_close - first_open) / first_open
    return pd.Series({
        'first_open': first_open,
        'last_close': last_close,
        'yearly_return': yearly_return
    })

# Group by Ticker and year
returns_df = df.groupby(['Ticker', 'year']).apply(compute_yearly_return).reset_index()

# Select latest year
latest_year = returns_df['year'].max()
latest_returns = returns_df[returns_df['year'] == latest_year]

# Top 10 green and loss stocks
top_10_green = latest_returns.sort_values(by='yearly_return', ascending=False).head(10)
top_10_loss = latest_returns.sort_values(by='yearly_return').head(10)

# Market summary
green_stocks = (latest_returns['yearly_return'] > 0).sum()
red_stocks = (latest_returns['yearly_return'] < 0).sum()
avg_price = df['close'].mean()
avg_volume = df['volume'].mean()

# Output results
print("Top 10 Green Stocks:")
print(top_10_green[['Ticker', 'yearly_return', 'first_open', 'last_close']])

print("\nTop 10 Loss Stocks:")
print(top_10_loss[['Ticker', 'yearly_return', 'first_open', 'last_close']])

print("\nMarket Summary:")
print(f"Green Stocks: {green_stocks}")
print(f"Red Stocks: {red_stocks}")
print(f"Average Price: {avg_price:.2f}")
print(f"Average Volume: {avg_volume:.0f}")

