# 🌟 Pendle-YT-Timing-Strategy-Analyzer V6 🌟

![GitHub contributors](https://img.shields.io/github/contributors/labrinyang/Pendle-YT-Timing-Strategy-Analyzer)
![GitHub forks](https://img.shields.io/github/forks/labrinyang/Pendle-YT-Timing-Strategy-Analyzer)
![GitHub stars](https://img.shields.io/github/stars/labrinyang/Pendle-YT-Timing-Strategy-Analyzer)
![GitHub license](https://img.shields.io/github/license/labrinyang/Pendle-YT-Timing-Strategy-Analyzer)
![GitHub issues](https://img.shields.io/github/issues/labrinyang/Pendle-YT-Timing-Strategy-Analyzer)
![GitHub pull requests](https://img.shields.io/github/issues-pr/labrinyang/Pendle-YT-Timing-Strategy-Analyzer)

![GitHub last commit](https://img.shields.io/github/last-commit/labrinyang/Pendle-YT-Timing-Strategy-Analyzer)
![GitHub repo size](https://img.shields.io/github/repo-size/labrinyang/Pendle-YT-Timing-Strategy-Analyzer)
![GitHub top language](https://img.shields.io/github/languages/top/labrinyang/Pendle-YT-Timing-Strategy-Analyzer)
![GitHub language count](https://img.shields.io/github/languages/count/labrinyang/Pendle-YT-Timing-Strategy-Analyzer)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/labrinyang/Pendle-YT-Timing-Strategy-Analyzer)

The **Pendle-YT-Timing-Strategy-Analyzer V6** is an enhanced tool designed to help DeFi users optimize their Yield Token (YT) investments on Pendle by analyzing real-time trade-by-trade data, predicting limit order completion times, and visualizing counterparty order density and wait times.

## 🎯 Key Features in V6

- **Real-time Data Analysis**: Switch from hourly implied APY calculations to real-time trade-by-trade data, improving the accuracy of the YT fair value curve.
- **Enhanced Limit Order Placement Assistance**: Users can input the quantity of YT or PT they want to buy or sell. The system predicts how long it will take for the order to be filled based on market conditions.
- **Counterparty Order Density Visualization**: Visualizes the density of opposing orders and estimates wait times, assisting in more efficient order placements.
- **Customizable Indicators**: Retains the ability to add custom indicators like moving averages, volatility, RSI, and MACD for detailed strategy customization.
- **Advanced Visualization**: Provides more precise visualizations of the fair value curve, market trends, and simulated order outcomes.

## 🔍 Strategy Overview

The V6 strategy incorporates insights from implied APY and real-time YT price movements. Key updates include:

- **Fair Value Calculation**: Uses volume-weighted implied APY to calculate the fair price line for YT, adjusting for holding periods and market sentiment.
- **Optimized Timing**: Helps users identify the best purchase or sell times by comparing YT prices with their fair value. Users can balance between high-leverage, short-duration buys and low-leverage, long-duration holds.
  
For a full breakdown of the strategy, please refer to the [YT Timing Strategy Overview](https://docs.google.com/document/d/1MUHDZqcMZwv5h4CJwk_2LLev8zy6GjbSdevnAwpG0LE/edit?usp=sharing).

## 📦 Prerequisites
- Python 3.x
- Required Python libraries: `requests`, `pandas`, `numpy`, `datetime`, `plotly`, `sklearn`, `tabulate`,`matplotlib`

## 📘 Colab Notebook OR 🚀 Installation

You can explore the analysis directly on Google Colab, no setup required:

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1oD_czxq3yVFYXujP_n9dcbNJ1z7iqbLm?authuser=0#scrollTo=BEtIVZVI6elN)

Alternatively, you can clone the repository and run the analysis locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/labrinyang/Pendle-YT-Timing-Strategy-Analyzer.git
   ```
2. **Install the required Python libraries**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the notebook**:
   Open the Jupyter Notebook or Python script locally and start your analysis.

## 💡 Usage

1. **Select Network**: Choose the network where the pool is located (Ethereum, Arbitrum, Mantle).
2. **Enter Contract Addresses**: Provide the Market and YT contract addresses on the pool's homepage.
3. **Analyze & Simulate**: Use the updated tool to analyze your investment strategy or simulate limit orders with real-time data.
4. **Visualize Results**: Generate updated visualizations to understand YT price movements, implied APY, and counterparty order distribution.

## 🤝 Contributing

We welcome contributions from Pendle enthusiasts! In V6, we focus on refining the prediction accuracy and visualization features. If you have ideas for further improvements, we’d love to see your contributions.

### How to Contribute

1. **Fork the repository**: Click the "Fork" button at the top-right corner of this page.
2. **Create your feature branch**: 
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**:
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a pull request**: Navigate to your fork on GitHub and click the "Pull Request" button to submit your changes for review.

We look forward to your contributions! ✨

## 👥 Authors & Contributors
Created by [Quant Sheep](https://twitter.com/quant_sheep?t=KqHtg0lNFy-sejP_dFOUXg&s=09) — *Collaborating with DeFi enthusiasts around the world!*


## 📜 License
This project is licensed under the MIT License.
