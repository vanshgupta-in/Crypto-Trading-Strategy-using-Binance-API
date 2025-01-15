import ccxt
import math
import pandas as pd
import pytz
from datetime import datetime, timedelta

# Fetch Historical Data
def Coinm(symbol, timeframe, stime, etime):
    binancecoinm = ccxt.binance({
        'enableRateLimit': True,
        'timeout': 30000,
        'apikey': 'your_api_key',  # Replace with your Binance API key
        'secret': 'your_secret_key'  # Replace with your Binance secret key
    })

    stime = pd.to_datetime(stime)
    etime = pd.to_datetime(etime)
    start_time = int(stime.timestamp() * 1000)
    end_time = int(etime.timestamp() * 1000)

    ohlcv = []
    while start_time <= end_time:
        data = binancecoinm.fetch_ohlcv(symbol, timeframe=timeframe, since=start_time, limit=1500)
        if len(data) == 0:
            break
        ohlcv.extend(data)
        start_time = data[-1][0] + 1

    df = pd.DataFrame(ohlcv, columns=['Date', 'open', 'high', 'low', 'close', 'volume'])
    df['Date'] = pd.to_datetime(df['Date'], unit='ms', utc=True)
    df['Date'] = df['Date'].dt.tz_convert('Asia/Kolkata')

    return df

# Moving Average Calculation
def sma(src, length):
    src['SMA'] = src['close'].rolling(window=length).mean()
    return src

# Standard Deviation Calculation
def deviation(src, length):
    ndf = pd.DataFrame(src)
    std_manual = [None] * (length - 1)

    for i in range(length - 1, len(ndf)):
        window = ndf['close'][i - length + 1:i + 1]
        mean = sum(window) / length
        variance = sum((x - mean) ** 2 for x in window) / length
        std_manual.append(math.sqrt(variance))

    ndf['stdev'] = std_manual
    return ndf

# Parameters
sma_length = 20
std_multiplier = 2
risk_reward_ratio = 1 / 2
risk_per_trade = 0.02  # 2% of the portfolio per trade


# Fetch data
today_date = pd.to_datetime("today")
symbol = 'BTC/USD'
timeframe = '1m'
stime = '2024-01-01'
etime = today_date


df = Coinm(symbol, timeframe, stime, etime)
df = sma(df, sma_length)
df = deviation(df, sma_length)


df['dev'] = std_multiplier * df['stdev']
df['basis'] = df['SMA']
df['upper'] = df['SMA'] + df['dev']
df['lower'] = df['SMA'] - df['dev']


df = df[['Date', 'open', 'high', 'low', 'close', 'volume', 'basis', 'upper', 'lower']]



# Trading Logic
entries = []
entry_found = False
stored_price = 0
target_price = 0
stop_loss = 0
portfolio_balance = 100000

for i in range(1, len(df)):
    
    if not entry_found:
        
        # Buy Signal
        if df['high'][i - 1] > df['upper'][i - 1]:
            stored_price = df['high'][i - 1]
            target_price = stored_price + risk_reward_ratio * stored_price * risk_per_trade
            stop_loss = stored_price - stored_price * risk_per_trade
            entry_found = True
            entry_side = "BUY"
            trigger_date = df['Date'][i - 1]

        # Sell Signal
        elif df['low'][i - 1] < df['lower'][i - 1]:
            stored_price = df['low'][i - 1]
            target_price = stored_price - risk_reward_ratio * stored_price * risk_per_trade
            stop_loss = stored_price + stored_price * risk_per_trade
            entry_found = True
            entry_side = "SELL"
            trigger_date = df['Date'][i - 1]


    if entry_found:
        
        # Buy Exit Conditions
        if entry_side == "BUY":
            
            if df['high'][i] >= target_price or df['low'][i] <= stop_loss:
                pnl = (target_price if df['high'][i] >= target_price else stop_loss) - stored_price
                exit_type = "Target" if df['high'][i] >= target_price else "Stop Loss"
                
                
                entries.append({
                    'Entry Time': trigger_date,
                    'Entry Price': stored_price,
                    'Side': entry_side,
                    'Target Price': target_price,
                    'Stop Loss': stop_loss,
                    'Exit Type': exit_type,
                    'Exit Price': target_price if df['high'][i] >= target_price else stop_loss,
                    'Exit Time': df['Date'][i],
                    'PnL': pnl
                })
                
                portfolio_balance += pnl
                entry_found = False

        # Sell Exit Conditions
        elif entry_side == "SELL":
            
            if df['low'][i] <= target_price or df['high'][i] >= stop_loss:
                pnl = stored_price - (target_price if df['low'][i] <= target_price else stop_loss)
                exit_type = "Target" if df['low'][i] <= target_price else "Stop Loss"
                
                
                entries.append({
                    'Entry Time': trigger_date,
                    'Entry Price': stored_price,
                    'Side': entry_side,
                    'Target Price': target_price,
                    'Stop Loss': stop_loss,
                    'Exit Type': exit_type,
                    'Exit Price': target_price if df['low'][i] <= target_price else stop_loss,
                    'Exit Time': df['Date'][i],
                    'PnL': pnl
                })
                
                portfolio_balance += pnl
                entry_found = False



# Output
entry_df = pd.DataFrame(entries)
print(entry_df)
print(f"Final Portfolio Balance: {portfolio_balance}")

# Store data into Trade.csv file
entry_df.to_csv(f"Trade.csv", index=False)
print(f"DataFrame has been saved to Trade.csv")
