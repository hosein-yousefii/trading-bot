import pandas as pd
import matplotlib.dates as dates
import datetime
import time
import sqlite3
import os
from finta import TA
from binance_f import RequestClient
from binance.client import Client

api_key = ''
api_secret = ''

client = Client(api_key, api_secret)

# list = [('BTCUSDT', '/root/spot/btc/btc-5m.csv', '/root/spot/btc/btc-1h.csv', '/root/espot/btc/btc-5m.csv', '/root/espot/btc/btc-1h.csv', '/root/nspot/btc/btc-5m.csv', '/root/nspot/btc/btc-1h.csv'), ('BNBUSDT', '/root/spot/bnb/bnb-5m.csv', '/root/spot/bnb/bnb-1h.csv', '/root/espot/bnb/bnb-5m.csv', '/root/espot/bnb/bnb-1h.csv', '/root/nspot/bnb/bnb-5m.csv', '/root/nspot/bnb/bnb-1h.csv'), ('ETHUSDT', '/root/spot/eth/eth-5m.csv', '/root/spot/eth/eth-1h.csv', '/root/espot/eth/eth-5m.csv', '/root/espot/eth/eth-1h.csv', '/root/nspot/eth/eth-5m.csv', '/root/nspot/eth/eth-1h.csv'), ('ADAUSDT', '/root/spot/ada/ada-5m.csv', '/root/spot/ada/ada-1h.csv', '/root/espot/ada/ada-5m.csv', '/root/espot/ada/ada-1h.csv', '/root/nspot/ada/ada-5m.csv', '/root/nspot/ada/ada-1h.csv')]
list = [('BTCUSDT', 'btc-5m.csv', 'btc-1h.csv')]


for sym,i,j in list:

    symbol = sym
    output = i
    output1 = j

    # output2 = k
    # output3 = l
    #
    # output4 = m
    # output5 = n


################################### 5m
    if os.path.isfile(output):

        f_5m = pd.read_csv(output)
        interval = '5m'
        bars = client.get_klines(symbol=symbol, interval=interval, limit=1)

        for line in bars:
            del line[6:]

        file_5m = pd.DataFrame(bars)
        file_5m.rename(columns={0: 'date', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, inplace=True)
        new_data = file_5m.iloc[-1]['date']
        exist_data = f_5m.iloc[-1]['date']

        if new_data == exist_data:

            f_5m.reset_index(drop=True)
            indexNames = f_5m[f_5m['date'] == new_data].index
            f_5m.drop(indexNames, inplace=True)
            del f_5m['ema8']
            del f_5m['ema13']
            del f_5m['ema21']
            f_5m = f_5m.append(file_5m, sort=False)
            f_5m['ema8'] = TA.EMA(f_5m, int(8))
            f_5m['ema13'] = TA.EMA(f_5m, int(13))
            f_5m['ema21'] = TA.EMA(f_5m, int(21))
            f_5m.to_csv(output, index=False)
        else:
            del f_5m['ema8']
            del f_5m['ema13']
            del f_5m['ema21']
            f_5m = f_5m.append(file_5m, sort=False)
            f_5m['ema8'] = TA.EMA(f_5m, int(8))
            f_5m['ema13'] = TA.EMA(f_5m, int(13))
            f_5m['ema21'] = TA.EMA(f_5m, int(21))
            f_5m.to_csv(output, index=False)

    else:

        interval = '5m'
        bars = client.get_klines(symbol=symbol, interval=interval, limit=80)

        for line in bars:
            del line[6:]

        file_5m = pd.DataFrame(bars)
        file_5m.rename(columns={0: 'date', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, inplace=True)

        file_5m['ema8'] = TA.EMA(file_5m, int(8))
        file_5m['ema13'] = TA.EMA(file_5m, int(13))
        file_5m['ema21'] = TA.EMA(file_5m, int(21))
        file_5m.to_csv(output)


#################################### 1h

    if os.path.isfile(output1):

        f_1h = pd.read_csv(output1)
        interval1 = '1h'
        bars = client.get_klines(symbol=symbol, interval=interval1, limit=1)

        for line in bars:
            del line[6:]

        file_1h = pd.DataFrame(bars)
        file_1h.rename(columns={0: 'date', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, inplace=True)
        new_data = file_1h.iloc[-1]['date']
        exist_data = f_1h.iloc[-1]['date']

        if new_data == exist_data:

            f_1h.reset_index(drop=True)
            indexNames = f_1h[f_1h['date'] == new_data].index
            f_1h.drop(indexNames, inplace=True)
            del f_1h['ema8']
            del f_1h['ema13']
            del f_1h['ema21']
            f_1h = f_1h.append(file_1h, sort=False)
            f_1h['ema8'] = TA.EMA(f_1h, int(8))
            f_1h['ema13'] = TA.EMA(f_1h, int(13))
            f_1h['ema21'] = TA.EMA(f_1h, int(21))
            f_1h.to_csv(output1, index=False)
        else:
            del f_1h['ema8']
            del f_1h['ema13']
            del f_1h['ema21']
            f_1h = f_1h.append(file_1h, sort=False)
            f_1h['ema8'] = TA.EMA(f_1h, int(8))
            f_1h['ema13'] = TA.EMA(f_1h, int(13))
            f_1h['ema21'] = TA.EMA(f_1h, int(21))
            f_1h.to_csv(output1, index=False)

    else:

        interval1 = '1h'
        bars = client.get_klines(symbol=symbol, interval=interval1, limit=80)

        for line in bars:
            del line[6:]

        file_1h = pd.DataFrame(bars)
        file_1h.rename(columns={0: 'date', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, inplace=True)

        file_1h['ema8'] = TA.EMA(file_1h, int(8))
        file_1h['ema13'] = TA.EMA(file_1h, int(13))
        file_1h['ema21'] = TA.EMA(file_1h, int(21))
        file_1h.to_csv(output1)
