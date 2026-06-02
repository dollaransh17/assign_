# Bitcoin Trader Sentiment Analysis
## Internship Assignment for Primetrade.ai

## Overview
This project analyzes the relationship between Bitcoin market sentiment (Fear/Greed Index) and trader performance on Hyperliquid exchange. The goal is to uncover patterns that can inform smarter trading strategies.

## Datasets Used
1. **Bitcoin Market Sentiment Dataset** (`fear_greed_index.csv`)
   - Columns: timestamp, value, classification, date
   - Fear/Greed Index values from 0-100 (0 = Extreme Fear, 100 = Extreme Greed)

2. **Historical Trader Data from Hyperliquid** (`historical_trader_data.csv`)
   - 211,224 individual trade records
   - Columns: Account, Coin, Execution Price, Size Tokens, Size USD, Side, Timestamp IST, Start Position, Direction, Closed PnL, etc.

## Files Generated
- `merged_trader_sentiment.csv` - Processed merged dataset
- `time_series_analysis.png` - Trends over time
- `correlation_heatmap.png` - Correlation matrix visualization
- `classification_analysis.png` - Metrics by sentiment classification
- `scatter_plots.png` - Individual relationship plots
- `key_insights.txt` - Summary of key findings
- `FINAL_REPORT.md` - Comprehensive analysis report
- `explore.py` - Initial data exploration script
- `analyze.py` - Detailed analysis and visualization script

## Key Findings
1. **Strong Negative Correlation**: As market sentiment becomes more greedy, trading activity decreases
   - Trading volume correlation: -0.264
   - Trade count correlation: -0.245

2. **Extreme Sentiment Drives Activity**: 
   - Extreme Fear days: 1,529 trades/day, $8.18M volume/day
   - Extreme Greed days: 351 trades/day, $1.09M volume/day
   - **4.36x higher activity during Extreme Fear**

3. **Statistical Significance**: T-tests confirm significant differences between sentiment extremes (p < 0.01)

4. **Trading Behavior Insight**: Traders are more active during fearful market conditions, suggesting either contrarian behavior or increased trading during volatility

## How to Reproduce
1. Install required packages in a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install pandas numpy matplotlib seaborn scipy
   ```

2. Run the analysis:
   ```bash
   python analysis/analyze.py
   ```

3. View results in the generated files, particularly `FINAL_REPORT.md` for the complete analysis.

## Requirements
- Python 3.12+
- pandas, numpy, matplotlib, seaborn, scipy

## License
This analysis was conducted for the Primetrade.ai internship assignment.# assign_
