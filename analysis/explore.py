import pandas as pd
import numpy as np

print("Loading data...")
# Load the datasets
trader_df = pd.read_csv('historical_trader_data.csv')
fg_df = pd.read_csv('fear_greed_index.csv')

print(f"Trader data shape: {trader_df.shape}")
print(f"FearGreed data shape: {fg_df.shape}")

# Display column names
print("\nTrader data columns:")
print(trader_df.columns.tolist())
print("\nFearGreed data columns:")
print(fg_df.columns.tolist())

# Check the first few rows of each
print("\nTrader data head:")
print(trader_df.head())
print("\nFearGreed data head:")
print(fg_df.head())

# Check data types
print("\nTrader data dtypes:")
print(trader_df.dtypes)
print("\nFearGreed data dtypes:")
print(fg_df.dtypes)

# Convert timestamps to datetime for trader data
# The trader data has a column 'Timestamp IST' which is in format like '02-12-2024 22:50'
# Also there is a 'Timestamp' column which seems to be a large number (maybe nanoseconds?)
# Let's use 'Timestamp IST' for date and convert to datetime.

trader_df['Timestamp IST'] = pd.to_datetime(trader_df['Timestamp IST'], format='%d-%m-%Y %H:%M')
# Extract date for merging
trader_df['Date'] = trader_df['Timestamp IST'].dt.date

# For fear/greed index, we have a 'date' column in format 'YYYY-MM-DD'
fg_df['date'] = pd.to_datetime(fg_df['date']).dt.date

print("\nAfter conversion:")
print("Trader data date range:", trader_df['Date'].min(), "to", trader_df['Date'].max())
print("FearGreed index date range:", fg_df['date'].min(), "to", fg_df['date'].max())

# Now, let's aggregate trader data by date to get daily metrics
# We'll calculate: total volume, number of trades, average PnL, etc. per day
daily_trader = trader_df.groupby('Date').agg(
    total_trades=('Trade ID', 'count'),
    total_volume_usd=('Size USD', 'sum'),
    avg_price=('Execution Price', 'mean'),
    total_pnl=('Closed PnL', 'sum'),
    avg_pnl_per_trade=('Closed PnL', 'mean'),
    buy_count=('Side', lambda x: (x == 'BUY').sum()),
    sell_count=('Side', lambda x: (x == 'SELL').sum())
).reset_index()

print("\nDaily trader aggregation head:")
print(daily_trader.head())

# Merge with fear/greed index on date
merged_df = pd.merge(daily_trader, fg_df, left_on='Date', right_on='date', how='inner')
print("\nMerged data shape:", merged_df.shape)
print("Merged data head:")
print(merged_df.head())

# Check for missing values after merge
print("\nMissing values in merged data:")
print(merged_df.isnull().sum())

# Now, let's explore the relationship between market sentiment (classification and value) and trading metrics
# We'll compute correlations between the fear/greed value and the trading metrics

# Select numeric columns for correlation
numeric_cols = ['total_trades', 'total_volume_usd', 'avg_price', 'total_pnl', 'avg_pnl_per_trade', 'buy_count', 'sell_count', 'value']
correlation_data = merged_df[numeric_cols].corr()

print("\nCorrelation matrix:")
print(correlation_data)

# Let's also look at the average trading metrics per sentiment classification
print("\nAverage trading metrics by sentiment classification:")
grouped = merged_df.groupby('classification')[numeric_cols].mean()
print(grouped)

# Save the merged data for further analysis
merged_df.to_csv('merged_trader_sentiment.csv', index=False)
print("\nMerged data saved to 'merged_trader_sentiment.csv'")