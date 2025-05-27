import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your dataset
df = pd.read_csv("merged_and_sorted.csv")

# Convert 'date' to datetime
df['date'] = pd.to_datetime(df['date'])

# Pivot to get a table with 'date' as index and each 'Ticker' as a column of closing prices
price_pivot = df.pivot(index='date', columns='Ticker', values='close')

# Calculate daily percentage change (returns)
returns = price_pivot.pct_change().dropna()

# Calculate correlation matrix
correlation_matrix = returns.corr()

# Plot heatmap
plt.figure(figsize=(14, 10))
sns.heatmap(correlation_matrix, cmap='coolwarm', annot=False, center=0, linewidths=0.5)
plt.title("Stock Price Correlation Heatmap")
plt.tight_layout()
plt.show()
