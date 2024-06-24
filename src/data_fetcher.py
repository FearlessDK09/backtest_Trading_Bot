import pandas as pd
import ta
from binance.client import Client, BinanceAPIException
from config.config import BINANCE_API_KEY, BINANCE_API_SECRET
import time

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

def get_hourly_data(symbol, start_date):
    try:
        frame = pd.DataFrame(client.get_historical_klines(symbol, "1h", start_date))
    except BinanceAPIException as e:
        print(e)
        time.sleep(60)
        frame = pd.DataFrame(client.get_historical_klines(symbol, "1h", '24hour ago UTC'))
    frame = frame.iloc[:, :6]
    frame.columns = ["Time", 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit="ms")
    frame = frame.astype(float)
    frame["price"] = frame.Open.shift(-1)
    frame["ema50"] = ta.trend.ema_indicator(frame.Close, window=50, fillna=False)
    frame["ema200"] = ta.trend.ema_indicator(frame.Close, window=200, fillna=False)
    frame["ATR"] = ta.volatility.average_true_range(high=frame.High, low=frame.Low, close=frame.Close) + 1
    frame["RSI"] = ta.momentum.rsi(frame.Close, window=14)
    frame["MACD"] = ta.trend.macd(frame.Close)
    frame["Signal"] = frame.MACD.ewm(span=9).mean()
    frame["condition"] = (frame.ema50 > frame.ema200)
    return frame
