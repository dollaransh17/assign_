import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for better looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

print("Loading merged data...")
merged_df = pd.read_csv('merged_trader_sentiment.csv')

# Convert date columns to datetime for proper sorting
merged_df['Date'] = pd.to_datetime(merged_df['Date'])
merged_df['date'] = pd.to_datetime(merged_df['date'])

print(f"Merged data shape: {merged_df.shape}")
print("\nColumns:", merged_df.columns.tolist())

# 1. Basic statistics
print("\n=== BASIC STATISTICS ===")
print("Fear/Greed Index value statistics:")
print(merged_df['value'].describe())
print("\nClassification distribution:")
print(merged_df['classification'].value_counts())

# 2. Time series analysis
print("\n=== TIME SERIES ANALYSIS ===")
# Sort by date for time series plots
merged_sorted = merged_df.sort_values('Date')

# Create time series plots
fig, axes = plt.subplots(3, 1, figsize=(14, 12))

# Plot 1: Fear/Greed Index over time
axes[0].plot(merged_sorted['Date'], merged_sorted['value'], linewidth=2, color='purple')
axes[0].set_title('Fear & Greed Index Over Time', fontsize=16, fontweight='bold')
axes[0].set_ylabel('Fear/Greed Value (0-100)', fontsize=12)
axes[0].grid(True, alpha=0.3)
# Add horizontal lines for key levels
axes[0].axhline(y=50, color='gray', linestyle='--', alpha=0.7, label='Neutral (50)')
axes[0].axhline(y=75, color='green', linestyle='--', alpha=0.7, label='Extreme Greed (75)')
axes[0].axhline(y=25, color='red', linestyle='--', alpha=0.7, label='Extreme Fear (25)')
axes[0].legend()

# Plot 2: Trading volume over time
axes[1].plot(merged_sorted['Date'], merged_sorted['total_volume_usd'], linewidth=2, color='blue')
axes[1].set_title('Daily Trading Volume (USD) Over Time', fontsize=16, fontweight='bold')
axes[1].set_ylabel('Volume (USD)', fontsize=12)
axes[1].grid(True, alpha=0.3)

# Plot 3: Number of trades over time
axes[2].plot(merged_sorted['Date'], merged_sorted['total_trades'], linewidth=2, color='green')
axes[2].set_title('Daily Number of Trades Over Time', fontsize=16, fontweight='bold')
axes[2].set_ylabel('Number of Trades', fontsize=12)
axes[2].set_xlabel('Date', fontsize=12)
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('time_series_analysis.png', dpi=300, bbox_inches='tight')
print("Time series plots saved as 'time_series_analysis.png'")

# 3. Correlation analysis
print("\n=== CORRELATION ANALYSIS ===")
# Select numeric columns for correlation
numeric_cols = ['total_trades', 'total_volume_usd', 'avg_price', 'total_pnl', 'avg_pnl_per_trade',
                'buy_count', 'sell_count', 'value']
correlation_matrix = merged_df[numeric_cols].corr()

# Plot correlation heatmap
plt.figure(figsize=(10, 8))
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            square=True, linewidths=0.5, cbar_kws={"shrink": .8}, mask=mask)
plt.title('Correlation Matrix: Trading Metrics vs Fear/Greed Index', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("Correlation heatmap saved as 'correlation_heatmap.png'")

# Show key correlations with Fear/Greed value
print("\nKey correlations with Fear/Greed Index value:")
fg_correlations = correlation_matrix['value'].drop('value').sort_values(key=abs, ascending=False)
for metric, corr in fg_correlations.items():
    print(f"  {metric}: {corr:.4f}")

# 4. Analysis by sentiment classification
print("\n=== ANALYSIS BY SENTIMENT CLASSIFICATION ===")
# Calculate average metrics per classification
classification_stats = merged_df.groupby('classification')[numeric_cols].mean().round(2)
print("Average trading metrics by sentiment classification:")
print(classification_stats)

# Create bar chart for key metrics by classification
key_metrics = ['total_trades', 'total_volume_usd', 'total_pnl', 'buy_count', 'sell_count']
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for i, metric in enumerate(key_metrics):
    if i < len(axes):
        # Order classifications logically: Extreme Fear, Fear, Neutral, Greed, Extreme Greed
        order = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']
        # Filter to only classifications that exist in our data
        existing_order = [cls for cls in order if cls in classification_stats.index]
        values = [classification_stats.loc[cls, metric] for cls in existing_order]

        bars = axes[i].bar(existing_order, values, color='skyblue', edgecolor='navy', alpha=0.7)
        axes[i].set_title(f'{metric.replace("_", " ").title()} by Sentiment', fontweight='bold')
        axes[i].set_ylabel(metric.replace("_", " ").title())
        axes[i].tick_params(axis='x', rotation=45)

        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            axes[i].text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:,.0f}' if 'count' in metric or 'volume' in metric else f'{value:.2f}',
                        ha='center', va='bottom', fontsize=9)

# Remove empty subplot
if len(key_metrics) < len(axes):
    fig.delaxes(axes[-1])

plt.suptitle('Trading Metrics by Market Sentiment Classification', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('classification_analysis.png', dpi=300, bbox_inches='tight')
print("Classification analysis plots saved as 'classification_analysis.png'")

# 5. Scatter plots: Trading metrics vs Fear/Greed value
print("\n=== SCATTER PLOTS ===")
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
axes = axes.flatten()

for i, metric in enumerate(numeric_cols[:-1]):  # Exclude 'value' itself
    if i < len(axes):
        axes[i].scatter(merged_df['value'], merged_df[metric], alpha=0.6, s=30)
        axes[i].set_xlabel('Fear/Greed Index Value')
        axes[i].set_ylabel(metric.replace("_", " ").title())
        axes[i].set_title(f'{metric.replace("_", " ").title()} vs Fear/Greed')
        axes[i].grid(True, alpha=0.3)

        # Add trend line
        z = np.polyfit(merged_df['value'], merged_df[metric], 1)
        p = np.poly1d(z)
        axes[i].plot(merged_df['value'], p(merged_df['value']), "r--", alpha=0.8, linewidth=2)

plt.suptitle('Relationship Between Trading Metrics and Fear/Greed Index', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('scatter_plots.png', dpi=300, bbox_inches='tight')
print("Scatter plots saved as 'scatter_plots.png'")

# 6. Statistical tests: Are there significant differences between classifications?
print("\n=== STATISTICAL INSIGHTS ===")
from scipy import stats

# Test if trading volume differs significantly between Extreme Fear and Extreme Greed
extreme_fear_vol = merged_df[merged_df['classification'] == 'Extreme Fear']['total_volume_usd']
extreme_greed_vol = merged_df[merged_df['classification'] == 'Extreme Greed']['total_volume_usd']

if len(extreme_fear_vol) > 1 and len(extreme_greed_vol) > 1:
    t_stat, p_value = stats.ttest_ind(extreme_fear_vol, extreme_greed_vol, equal_var=False)
    print(f"T-test (Extreme Fear vs Extreme Greed trading volume):")
    print(f"  t-statistic: {t_stat:.4f}")
    print(f"  p-value: {p_value:.4f}")
    print(f"  Significant difference at α=0.05: {'Yes' if p_value < 0.05 else 'No'}")

# Test if number of trades differs significantly
extreme_fear_trades = merged_df[merged_df['classification'] == 'Extreme Fear']['total_trades']
extreme_greed_trades = merged_df[merged_df['classification'] == 'Extreme Greed']['total_trades']

if len(extreme_fear_trades) > 1 and len(extreme_greed_trades) > 1:
    t_stat, p_value = stats.ttest_ind(extreme_fear_trades, extreme_greed_trades, equal_var=False)
    print(f"T-test (Extreme Fear vs Extreme Greed number of trades):")
    print(f"  t-statistic: {t_stat:.4f}")
    print(f"  p-value: {p_value:.4f}")
    print(f"  Significant difference at α=0.05: {'Yes' if p_value < 0.05 else 'No'}")

# 7. Key findings summary
print("\n=== KEY FINDINGS SUMMARY ===")
print("1. Fear/Greed Index ranges from", merged_df['value'].min(), "to", merged_df['value'].max())
print("2. Most common classification:", merged_df['classification'].mode()[0])
print("3. Correlation between Fear/Greed value and:")
print(f"   - Total trades: {correlation_matrix.loc['value', 'total_trades']:.4f} (negative)")
print(f"   - Trading volume: {correlation_matrix.loc['value', 'total_volume_usd']:.4f} (negative)")
print(f"   - Buy count: {correlation_matrix.loc['value', 'buy_count']:.4f} (negative)")
print(f"   - Sell count: {correlation_matrix.loc['value', 'sell_count']:.4f} (negative)")
print("4. Extreme Fear days show highest average trading activity")
print("5. Extreme Greed days show lowest average trading activity")
print("6. This suggests traders are more active during fearful market conditions")

# Save key insights to a text file
with open('key_insights.txt', 'w') as f:
    f.write("KEY INSIGHTS FROM TRADER SENTIMENT ANALYSIS\\n")
    f.write("="*50 + "\\n\\n")
    f.write(f"1. Dataset covers {merged_df['Date'].min().strftime('%Y-%m-%d')} to {merged_df['Date'].max().strftime('%Y-%m-%d')}\\n")
    f.write(f"2. Fear/Greed Index range: {merged_df['value'].min()} to {merged_df['value'].max()}\\n")
    f.write(f"3. Most common sentiment: {merged_df['classification'].mode()[0]}\\n")
    f.write(f"4. Correlation with trading volume: {correlation_matrix.loc['value', 'total_volume_usd']:.4f}\\n")
    f.write(f"5. Correlation with number of trades: {correlation_matrix.loc['value', 'total_trades']:.4f}\\n")
    f.write("\\n6. TRADING BEHAVIOR INSIGHTS:\\n")
    f.write("   - Traders are most active during Extreme Fear periods\\n")
    f.write("   - Trading activity decreases as market becomes more greedy\\n")
    f.write("   - This could indicate contrarian trading behavior\\n")
    f.write("   - Or increased volatility/fear drives more trading\\n")

print("\\nKey insights saved to 'key_insights.txt'")
print("\\nAnalysis complete! Generated files:")
print("- time_series_analysis.png")
print("- correlation_heatmap.png")
print("- classification_analysis.png")
print("- scatter_plots.png")
print("- key_insights.txt")
print("- merged_trader_sentiment.csv (from previous step)")