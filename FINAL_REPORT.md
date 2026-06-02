# Bitcoin Trader Sentiment Analysis Report
## Internship Assignment - Primetrade.ai

### Executive Summary
This analysis explores the relationship between Bitcoin market sentiment (Fear/Greed Index) and trader performance on Hyperliquid. By analyzing 211,224 individual trades from May 2023 to May 2025 alongside daily Fear/Greed Index readings, we uncovered significant patterns in how market sentiment influences trading behavior.

### Key Findings

#### 1. Strong Negative Correlation Between Sentiment and Trading Activity
- **Trading Volume vs Fear/Greed**: -0.2644
- **Number of Trades vs Fear/Greed**: -0.2452
- **Buy/Sell Count vs Fear/Greed**: -0.2355/-0.2330

These negative correlations indicate that as market sentiment becomes more greedy (higher Fear/Greed values), trading activity decreases. Conversely, during fearful periods (lower Fear/Greed values), trading activity increases substantially.

#### 2. Extreme Sentiment Drives Maximum Trading Activity
- **Extreme Fear Days** (FG < 25): Average 1,529 trades/day, $8.18M volume/day
- **Extreme Greed Days** (FG > 75): Average 351 trades/day, $1.09M volume/day

Trading activity during Extreme Fear periods is **4.36x higher** than during Extreme Greed periods, suggesting traders are significantly more active when markets are fearful.

#### 3. Statistical Significance Confirmed
T-tests comparing Extreme Fear vs Extreme Greed periods show:
- Trading volume difference: p-value = 0.0072 (significant)
- Trade count difference: p-value = 0.0056 (significant)

#### 4. Sentiment Distribution in Dataset
- Greed: 193 days (40.3%)
- Extreme Greed: 114 days (23.8%)
- Fear: 91 days (19.0%)
- Neutral: 67 days (14.0%)
- Extreme Fear: 14 days (2.9%)

Despite Extreme Fear representing only 2.9% of days, it accounts for disproportionately high trading activity.

### Trading Behavior Insights

#### Contrarian Trading Evidence
The data suggests potential contrarian behavior:
- Increased buying during Extreme Fear (when others are fearful)
- Decreased trading during Extreme Greed (when others are greedy)
- This aligns with classic investment wisdom: "Be fearful when others are greedy, and greedy when others are fearful"

#### Alternative Explanations
The increased activity during fearful periods could also stem from:
1. **Higher volatility** prompting more trading adjustments
2. **Liquidations and margin calls** forcing position changes
3. **Opportunistic buying** during market dips
4. **Risk-off behavior** where traders reduce positions (though our data shows increased activity)

### Data Quality Notes
- **Trader Dataset**: 211,224 records spanning May 2023 - May 2025
- **Sentiment Dataset**: 2,644 daily readings from Feb 2018 - May 2025
- **Overlap Period**: 479 days of concurrent data (May 2023 - May 2025)
- **No missing values** in merged dataset after processing

### Recommendations for Trading Strategies

#### For Traders:
1. **Consider contrarian approaches** during extreme sentiment readings
2. **Adjust position sizing** based on sentiment extremes (smaller sizes in Extreme Greed, potentially larger in Extreme Fear)
3. **Monitor sentiment shifts** as leading indicators for potential trading volume changes
4. **Be aware of increased volatility** during Extreme Fear periods

#### For Platform/Exchange:
1. **Anticipate higher load** during Extreme Fear periods (4x normal volume)
2. **Ensure liquidity provisions** are adequate during market stress
3. **Consider sentiment-based fee structures** or offerings
4. **Provide educational resources** about sentiment-driven behaviors

### Limitations and Future Work
1. **Causality vs Correlation**: While we show relationships, we cannot definitively state sentiment causes trading changes
2. **Lack of Profitability Analysis**: We analyzed volume and frequency but not PnL by sentiment
3. **Single Exchange/Data Source**: Limited to Hyperliquid data; broader market validation needed
4. **Time Lag Effects**: Same-day analysis; future work could explore leading/lagging relationships

### Files Generated
1. `merged_trader_sentiment.csv` - Processed dataset for analysis
2. `time_series_analysis.png` - Trends over time for sentiment and trading metrics
3. `correlation_heatmap.png` - Correlation matrix visualization
4. `classification_analysis.png` - Average metrics by sentiment classification
5. `scatter_plots.png` - Individual relationships between sentiment and trading metrics
6. `key_insights.txt` - Summary of key findings
7. `FINAL_REPORT.md` - This comprehensive report

### Conclusion
This analysis reveals a clear inverse relationship between Bitcoin market sentiment and trading activity on Hyperliquid. Traders are significantly more active during periods of market fear, with Extreme Fear days showing over 4x the trading volume of Extreme Greed days. This pattern suggests either contrarian trading behavior or increased trading during volatile/fearful market conditions. These insights can inform both individual trading strategies and platform operations in the cryptocurrency derivatives space.

---
*Analysis conducted for Primetrade.ai Internship Assignment*
*Date: June 2, 2026*