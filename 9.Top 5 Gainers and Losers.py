import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv(r"C:\Users\admin\Music\Guvi\Driven Stock Analysis\Data\data\merged_and_sorted.csv")
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.to_period('M')

# Calculate monthly return per stock
monthly_data = df.sort_values(by=['Ticker', 'date'])
monthly_return = monthly_data.groupby(['Ticker', 'month'])['close'].agg(['first', 'last'])
monthly_return['monthly_return'] = (monthly_return['last'] - monthly_return['first']) / monthly_return['first']
monthly_return.reset_index(inplace=True)

# Unique months in the data
unique_months = monthly_return['month'].unique()

# Set up the plot grid
fig, axs = plt.subplots(nrows=6, ncols=2, figsize=(18, 30))
axs = axs.flatten()

# Loop through each month to generate plots
for idx, month in enumerate(sorted(unique_months)):
    ax = axs[idx]

    # Filter data for the month
    month_df = monthly_return[monthly_return['month'] == month].copy()

    # Sort by monthly return
    top_gainers = month_df.sort_values(by='monthly_return', ascending=False).head(5)
    top_losers = month_df.sort_values(by='monthly_return', ascending=True).head(5)

    # Combine gainers and losers
    combined = pd.concat([top_gainers, top_losers])
    colors = ['green'] * 5 + ['red'] * 5

    # Plot
    ax.bar(combined['Ticker'], combined['monthly_return'] * 100, color=colors)
    ax.set_title(f"Top 5 Gainers & Losers - {month}")
    ax.set_ylabel("Monthly Return (%)")
    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_xticklabels(combined['Ticker'], rotation=45)

# Adjust layout
plt.tight_layout()
plt.show()
