# Crypto-Trading-Strategy-using-Binance-API

This project implements a cryptocurrency trading strategy using Bollinger Bands for generating buy and sell signals. It fetches historical data from Binance using the `ccxt` library, calculates key indicators like Moving Averages and Standard Deviation, and simulates trades with predefined risk management.

## Features

- **Data Fetching**: Fetch historical OHLCV data from Binance.
- **Bollinger Bands**: Calculate Bollinger Bands for technical analysis.
- **Trading Logic**:
  - Generate Buy/Sell signals based on Bollinger Bands.
  - Simulate trades with defined risk-reward ratio and stop-loss.
- **Risk Management**:
  - Limit risk to a fixed percentage of the portfolio per trade.
  - Use a customizable risk-reward ratio.
- **Output**:
  - Print trade details and final portfolio balance.
  - Save trade logs to a CSV file for further analysis.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Parameters](#parameters)
4. [Example Output](#example-output)
5. [Future Enhancements](#future-enhancements)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/crypto-trading-strategy-using-binance-api.git
   cd crypto-trading-strategy-using-binance-api
   ```

2. Install required Python packages:

   ```bash
   pip install ccxt pandas pytz
   ```

3. Replace the placeholders in the script with your Binance API key and secret:

   ```python
   'apikey': 'your_api_key',  # Replace with your Binance API key
   'secret': 'your_secret_key'  # Replace with your Binance secret key
   ```

## Usage

1. Set the parameters in the script:

   - Symbol: The trading pair, e.g., `'BTC/USD'`.
   - Timeframe: The interval for OHLCV data, e.g., `'1m'`.
   - Start and end dates: E.g., `'2024-01-01'` to today.

2. Run the script:

   ```bash
   python trading_strategy.py
   ```

3. View the output:

   - Trade details will be printed in the console.
   - Final portfolio balance will be displayed.
   - A CSV file (`Trade.csv`) will be saved containing trade logs.

## Parameters

- **`sma_length`**: Length of the Simple Moving Average window (default: 20).
- **`std_multiplier`**: Multiplier for the standard deviation in Bollinger Bands (default: 2).
- **`risk_reward_ratio`**: Ratio of risk to reward per trade (default: 1:2).
- **`risk_per_trade`**: Percentage of the portfolio risked per trade (default: 2%).

## Example Output

### Console Output:

```
           Entry Time    Entry Price Side  Target Price  Stop Loss Exit Type  Exit Price          Exit Time    PnL
0 2024-01-02 10:45:00    35000.0   BUY    35700.0       34300.0   Target     35700.0     2024-01-02 11:10:00  700.0
1 2024-01-03 15:30:00    36000.0   SELL   35300.0       36700.0   Stop Loss  36700.0     2024-01-03 16:00:00 -700.0

Final Portfolio Balance: 100700
DataFrame has been saved to Trade.csv
```

### CSV File:

The CSV file contains:

- Entry/Exit Time
- Entry Price
- Trade Side (Buy/Sell)
- Target Price
- Stop Loss
- Exit Type (Target/Stop Loss)
- Exit Price
- Profit/Loss (PnL)

## Future Enhancements

- Add live trading functionality using Binance API.
- Implement additional technical indicators.
- Improve standard deviation calculation using vectorized operations.
- Add backtesting and performance metrics.
- Optimize parameters using machine learning.

---

## Disclaimer

This script is for educational purposes only. Use it at your own risk. Cryptocurrency trading involves a significant risk of loss and is not suitable for every investor.

