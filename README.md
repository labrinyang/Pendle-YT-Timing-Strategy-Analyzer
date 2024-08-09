# Pendle-YT-Timing-Strategy-Analyzer

This analyzer helps users find the best times to buy Yield Tokens (YT) on Pendle. It simplifies investment decisions by analyzing historical data and market trends, offering insights into optimal entry points and returns. Ideal for all DeFi investors, it provides clear visualizations and automated analysis to boost your yield farming strategy.

## Features
- **Optimal Timing Analysis**: Identifies the best times to purchase YT based on historical APY data and market trends.
- **Automated Analysis**: Automatically processes and analyzes data to generate actionable insights for your investment strategy.
- **Customizable Indicators**: Includes options for adding custom indicators like moving averages, volatility, RSI, and MACD.
- **Visualizations**: Generates clear, easy-to-interpret visualizations to help guide your investment decisions.
- **Simulated Limit Orders**: Simulate the results of placing limit orders on YT and assess potential outcomes.

## Understanding the Strategy

To gain a deeper understanding of how the YT price correlates with the implied annualized yield (APY) and the impact of holding duration on returns, please refer to the [YT Timing Strategy Overview](https://docs.google.com/document/d/1MUHDZqcMZwv5h4CJwk_2LLev8zy6GjbSdevnAwpG0LE/edit?usp=sharing).

This document covers:
- The correlation between YT price and implied APY.
- The effect of holding duration and YT leverage.
- How to achieve returns above the average by identifying optimal purchase points.
- The significance of volume-weighted implied APY in establishing a fair price line for YT.

## Prerequisites
- Python 3.x
- Required Python libraries: `requests`, `pandas`, `numpy`, `datetime`, `plotly`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Pendle-YT-Timing-Strategy-Analyzer.git
   ```
2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. **Select Network**: Choose the network where the pool is located (Ethereum, Arbitrum, Mantle).
2. **Enter Contract Addresses**: Provide the Market and YT contract addresses on the pool's homepage.
3. **Analyze & Simulate**: Use the tool to analyze your investment strategy or simulate limit orders based on historical data.
4. **Visualize Results**: Generate and view visualizations to understand YT price movements, implied APY, and points distribution.

## Author
Created by [Quant Sheep](https://twitter.com/quant_sheep?t=KqHtg0lNFy-sejP_dFOUXg&s=09)

## Support
If you find this tool useful, consider supporting: `0x334D7763eD1e23bD4052e9551DB3Dac506a64F1E`

## License
This project is licensed under the MIT License.
