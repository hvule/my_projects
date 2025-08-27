import ccxt
import talib as ta
import pandas as pd
import time
import datetime
import logging
from ta.volatility import AverageTrueRange
from ta.momentum import RSIIndicator
from binance.client import Client
# === Settings ===
API_KEY = 'GK1VTXryv2dBK4FR87Z9esW93lyN4IIHAejaYDitbPWIP5l4AI1c0jvrmrrfOxqQ'
API_SECRET = 'IogqBFh4GDWGopH15YPBblD1vkkqSC1WUmxDRWiLQ0vAKpH1rVwBI7rY5aZWtH8z'
BASE_URL = 'https://testnet.binance.vision'  # Binance testnet endpoint

symbol = 'SOL/USDT'
timeframe_5m = '5m'
timeframe_1h = '1h'

atr_period = 14
rsi_period = 14
moving_avg_period = 50
risk_per_trade = 0.03  # 3% of trading balance
balance_usage = 0.1    # Use 10% of total balance
price_deviation_threshold = 1.5  # In ATR multiples

tp_percent = 0.5  # Take profit in percentage
sl_percent = 0.3  # Stop loss in percentage
atr_min_threshold = 0.1  # ATR fallback threshold

active_trades = []
MAX_BUDGET = 1000  # Max capital you're willing to risk
MAX_TRADES = 5     # Max number of active positions


# === Initialize Exchange ===
binance = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'options': {'defaultType': 'spot'},
})
binance.set_sandbox_mode(True)
# binance.urls['api'] = {
#     'public': BASE_URL,
#     'private': BASE_URL,
# }

# === Initialize Logging ===
logging.basicConfig(
    filename='mean_reversion_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

print("Starting Mean-Reversion Bot...")
logging.info(f"start monitoring trading pair {symbol}")
# === Functions ===

def fetch_data(timeframe,limit = 150):
    ohlcv = binance.fetch_ohlcv(symbol, timeframe, limit=atr_period + moving_avg_period + 50)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def calculate_rsi(series, period):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_indicators(df):
    df['tpv'] = (df['close'] * df['volume'])  # typical price * volume
    df['cum_tpv'] = df['tpv'].cumsum()
    df['cum_vol'] = df['volume'].cumsum()
    df['vwap'] = df['cum_tpv'] / df['cum_vol']
    df['atr'] = AverageTrueRange(df['high'], df['low'], df['close'], window=atr_period).average_true_range()
    df['rsi'] = RSIIndicator(df['close'], window=14).rsi()
    df.dropna(inplace=True)
    df.dropna(inplace=True)
    return df 

def get_trading_balance():
    balance = binance.fetch_balance()
    usdt_balance = balance['total']['USDT']
    btc_balance = balance['total']['BTC']
    sol_balance = balance['total']['SOL']
    available_balance = usdt_balance * balance_usage
    print(f"Total USDT Balance: {usdt_balance:.2f}, Bot Trading Balance: {available_balance:.2f}")
    print(f"Total BTC Balance: {btc_balance:.2f}")
    print(f"Total SOL Balance: {sol_balance:.2f}")
    return available_balance

def calculate_position_size(available_balance, stop_loss_distance, price):
    risk_amount = available_balance * risk_per_trade
    position_size = risk_amount / stop_loss_distance
    cost = position_size * price
    if cost > available_balance:
        position_size = available_balance / price  # cap size if needed
    return round(position_size, 6)  # Binance usually accepts 6 decimal places

def place_order(signal, price, stop_loss_price, position_size, take_profit_price):
    print(f"Placing {signal.upper()} order at {price:.2f}, amount {position_size:.6f}")
    logging.info(f"Placing {signal.upper()} order at {price:.2f}, amount {position_size:.6f}")

    # Place market order
    order = binance.create_order(symbol, 'market', signal, position_size)

    # Place take-profit as limit order in opposite direction
    tp_side = 'sell' if signal == 'buy' else 'buy'
    binance.create_order(symbol, 'limit', tp_side, position_size, round(take_profit_price, 2))
    
    print(f"Stop Loss set at {stop_loss_price:.2f}, Take Profit at {take_profit_price:.2f}")
    logging.info(f"Stop Loss set at {stop_loss_price:.2f}, Take Profit at {take_profit_price:.2f}")

    active_trades.append({
    'symbol': symbol,
    'price': price,
    'amount': amount,
    'timestamp': datetime.datetime.utcnow()
    })
    logging.info(f"Active trades: {active_trades:.2f}")


def get_available_trading_budget_from_trades():
    total_exposure = sum(t['price'] * t['amount'] for t in active_trades)
    available_budget = max(0, MAX_BUDGET - total_exposure)
    print(f"Active exposure: {total_exposure:.2f}, Available budget: {available_budget:.2f}")
    return available_budget


def check_signal_5m(df):
    last_row = df.iloc[-1]
    price = last_row['close']
    vwap = last_row['vwap']
    atr = last_row['atr']
    rsi = last_row['rsi']
    if price < vwap - price_deviation_threshold * atr and rsi < 30:
        return 'buy', price, vwap, atr
    elif price > vwap + price_deviation_threshold * atr and rsi > 70:
        return 'sell', price, vwap, atr
    else:
        return None, price, vwap, atr

#updated code for multi-timeframe confirmation
def confirm_with_1h_trend(df_1h, signal_5m):
    last = df_1h.iloc[-1]
    price, vwap, rsi = last['close'], last['vwap'], last['rsi']
    if signal_5m == 'buy' and price < vwap and rsi < 50:
        return True
    elif signal_5m == 'sell' and price > vwap and rsi > 50:
        return True
    return False

def sell_sol_to_recover(client, min_usdt_needed=50):
    """Sells enough SOL to recover USDT balance."""
    try:
        balance = client.fetch_balance()  # Call the method to get the balance
        sol_balance = balance['free']['SOL']  # Free SOL balance
        if sol_balance == 0:
            print("No SOL available to sell.")
            return False

        # Sell all or part of SOL to get at least min_usdt_needed
        symbol = 'SOLUSDT'
        sol_price = float(client.fetch_ticker(symbol)['last'])  # Get the latest SOL price
        #sol_to_sell = min(sol_balance, round(min_usdt_needed / sol_price, 6))
        sol_to_sell = sol_balance  # Sell all SOL for simplicity
        if sol_to_sell <= 0:
            print("No SOL available to sell.")
            return False
        print(f"Selling {sol_to_sell} SOL at market price to regain USDT.")
        order = client.create_market_sell_order(symbol, sol_to_sell)
        print(f"Order result: {order}")
        return True
    except Exception as e:
        print(f"Failed to sell SOL: {e}")
        return False

# === Main Trading Loop ===



while True:
    try:
        available_balance = get_trading_balance()
        #if available_balance < 10:
        sell_sol_to_recover(binance, min_usdt_needed=50)
            # Update available balance after selling SOL
        print(f"new balance after selling sol: {available_balance:.2f}")
                
        df_5m = fetch_data(timeframe_5m)
        df_5m = calculate_indicators(df_5m)

        df_1h = fetch_data(timeframe_1h)
        df_1h = calculate_indicators(df_1h)
        signal, price, vwap, atr = check_signal_5m(df_5m)

        if signal  and confirm_with_1h_trend(df_1h, signal):
            if atr < atr_min_threshold:
                tp_distance = price * (tp_percent / 100)
                sl_distance = price * (sl_percent / 100)
                print(f"ATR too low ({atr:.4f}), using % fallback: TP={tp_distance:.4f}, SL={sl_distance:.4f}")
            else:
                tp_distance = 2 * atr
                sl_distance = atr

            position_size = calculate_position_size(available_balance, sl_distance, price)
            
            if signal == 'buy':
                stop_loss_price = price - sl_distance
                take_profit_price = price + tp_distance
            else:
                stop_loss_price = price + sl_distance
                take_profit_price = price - tp_distance

            place_order(signal, price, stop_loss_price, position_size, take_profit_price)
            print(f"Take Profit target: {take_profit_price:.4f}")
            logging.info(f"Take Profit target: {take_profit_price:.4f}")
        
        else:
            now = datetime.datetime.now()
            print(f"{now} - No signal. Waiting...")
            logging.info(f"{now} - No signal. Price={price:.2f}, VWAP={vwap:.2f}, ATR={atr:.2f}")

    except Exception as e:
        print(f"Error: {str(e)}")
        logging.error(f"Error: {str(e)}")

    time.sleep(60)  # Sleep 1 minute before next check
