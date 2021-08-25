import pandas as pd
import matplotlib.dates as dates
import datetime
import time
import sqlite3
import os
from finta import TA

DB_buy = 'eth-buy.db'
DB_sell = 'eth-sell.db'
symbol ='ETHUSDT'
output = 'eth-5m.csv'
output1 = 'eth-30m.csv'
log_buy = "/var/www/html/nspot/result-buy-eth"
log_sell = "/var/www/html/nspot/result-sell-eth"



con_buy = sqlite3.connect(DB_buy)

empty = []
con_buy.execute("CREATE TABLE IF NOT EXISTS {} (time TEXT DEFAULT '0' NOT NULL, state TEXT DEFAULT 'NULL' NOT NULL, balance FLOAT(9) DEFAULT 300 , price FLOAT(9) DEFAULT 0, amount FLOAT(9) DEFAULT 0, percent FLOAT(9) DEFAULT 0, total FLOAT(9) DEFAULT 0, last FLOAT(9) DEFAULT 0,valuep FLOAT(9) DEFAULT 0, valuen FLOAT(9) DEFAULT 0, fee FLOAT(9) DEFAULT 0, start_close FLOAT(9) DEFAULT 0 );".format(symbol))
time = con_buy.execute("SELECT time from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()
if time == empty:
    con_buy.execute("INSERT INTO {} (price, amount, total, percent, last, state, valuep, valuen, fee,start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);".format(symbol), (0, 0, 0, 0, 0, 'Sell', 0, 0, 0, 0))
con_buy.commit()

con_sell = sqlite3.connect(DB_sell)

empty = []
con_sell.execute("CREATE TABLE IF NOT EXISTS {} (time TEXT DEFAULT '0' NOT NULL, state TEXT DEFAULT 'NULL' NOT NULL, balance FLOAT(9) DEFAULT 300 , price FLOAT(9) DEFAULT 0, amount FLOAT(9) DEFAULT 0, percent FLOAT(9) DEFAULT 0, total FLOAT(9) DEFAULT 0, last FLOAT(9) DEFAULT 0,valuep FLOAT(9) DEFAULT 0, valuen FLOAT(9) DEFAULT 0, fee FLOAT(9) DEFAULT 0, start_close FLOAT(9) DEFAULT 0 );".format(symbol))
time = con_sell.execute("SELECT time from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()
if time == empty:
    con_sell.execute("INSERT INTO {} (price, amount, total, percent, last, state, valuep, valuen, fee,start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);".format(symbol), (0, 0, 0, 0, 0, 'Sell', 0, 0, 0, 0))
con_sell.commit()


######################### check the conditions

a_5m = pd.read_csv(output)
a_30m = pd.read_csv(output1)

ema8_30m = a_30m.iloc[-1]['ema8']
ema13_30m = a_30m.iloc[-1]['ema13']
close_30m = a_30m.iloc[-1]['close']

ema8_5m = a_5m.iloc[-2]['ema8']
close_5m = a_5m.iloc[-2]['close']
close = a_5m.iloc[-1]['close']
time_5m = a_5m.iloc[-2]['date']
lema8_5m = a_5m.iloc[-3]['ema8']
lclose_5m = a_5m.iloc[-3]['close']

if (lclose_5m < lema8_5m) and (close_5m > ema8_5m) :


    state = con_buy.execute("SELECT state from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
    start_close = con_buy.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]

    if state == 'Buy':

        pclose_5m = float(start_close) - (float(start_close) * 1.1 / 100)
        fee = con_buy.execute("SELECT fee from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]

        if close < pclose_5m:
            levrage = 10
            date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
            amount = con_buy.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            balance = con_buy.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            total = con_buy.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            state = 'Sell'
            result = float(amount) * float(close)
            percent = con_buy.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last = con_buy.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last_price = con_buy.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            commission = format((float(amount) * float(last_price) * 0.002 / 100) + (float(amount) * float(close) * 0.002 / 100), ".4f")
            fees = format((float(close) * 100 / float(last_price) - 100) * levrage, ".2f")
            balance = (float(result) * float(fees) / 100 + float(result)) + float(total) - float(commission)
            fee = 0

            if float(fees) > 0:
                valueps = con_buy.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuen = con_buy.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuep = float(fees) + float(valueps)
                percent = 1 + percent
            else:

                valuep = con_buy.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuens = con_buy.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuen = float(fees) + float(valuens)
                last = 1 + last

            start_close = 0
            con_buy.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, 0, percent, last, valuep, valuen, fee, start_close))

        elif fee == 4:

            levrage = 10
            date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
            amount = con_buy.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            balance = con_buy.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            total = con_buy.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            state = 'Sell'
            result = float(amount) * float(close)
            percent = con_buy.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last = con_buy.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last_price = con_buy.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            commission = format((float(amount) * float(last_price) * 0.002 / 100) + (float(amount) * float(close) * 0.002 / 100), ".4f")
            fees = format((float(close) * 100 / float(last_price) - 100) * levrage, ".2f")
            balance = (float(result) * float(fees) / 100 + float(result)) + float(total) - float(commission)
            fee = 0

            if float(fees) > 0:
                valueps = con_buy.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuen = con_buy.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuep = float(fees) + float(valueps)
                percent = 1 + percent
            else:

                valuep = con_buy.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuens = con_buy.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuen = float(fees) + float(valuens)
                last = 1 + last

            start_close = 0
            con_buy.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, 0, percent, last, valuep, valuen, fee, start_close))

        else:

            date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
            total = con_buy.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            balance = con_buy.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            percent = con_buy.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            amount = con_buy.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last = con_buy.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuep = con_buy.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuen = con_buy.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            start_close = con_buy.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            fee += 1
            con_buy.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, total, percent, last, valuep, valuen, fee, start_close))
    else:

        if (close_30m > ema8_30m) :

            date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
            whole = con_buy.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            state = con_buy.execute("SELECT state from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuep = con_buy.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuen = con_buy.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            balance = float(whole) / 5
            total = float(whole) - float(balance)
            amount = float(balance) / float(close)
            percent = con_buy.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last = con_buy.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            state = 'Buy'
            start_close = close
            fee = 0
            con_buy.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, 0, close, amount, total, percent, last, valuep, valuen, fee, start_close))

        else:

            date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
            total = con_buy.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            balance = con_buy.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            percent = con_buy.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            amount = con_buy.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last = con_buy.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuep = con_buy.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuen = con_buy.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            start_close = con_buy.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            fee = 0
            con_buy.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, total, percent, last, valuep, valuen, fee, start_close))

elif  (close_30m < ema8_30m):

    state = con_buy.execute("SELECT state from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]

    if state == 'Buy':

        levrage = 10
        date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
        amount = con_buy.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        balance = con_buy.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        total = con_buy.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        state = 'Sell'
        result = float(amount) * float(close)
        percent = con_buy.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        last = con_buy.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        last_price = con_buy.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        commission = format((float(amount) * float(last_price) * 0.002 / 100) + (float(amount) * float(close) * 0.002 / 100), ".4f")
        fees = format((float(close) * 100 / float(last_price) - 100) * levrage, ".2f")
        balance = (float(result) * float(fees) / 100 + float(result)) + float(total) - float(commission)
        fee = 0

        if float(fees) > 0:
            valueps = con_buy.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuen = con_buy.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuep = float(fees) + float(valueps)
            percent = 1 + percent
        else:

            valuep = con_buy.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuens = con_buy.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuen = float(fees) + float(valuens)
            last = 1 + last

        start_close = 0
        con_buy.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, 0, percent, last, valuep, valuen, fee, start_close))

    else:

        date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
        total = con_buy.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        balance = con_buy.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        percent = con_buy.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        amount = con_buy.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        last = con_buy.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        valuep = con_buy.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        valuen = con_buy.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        start_close = con_buy.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        fee = 0
        con_buy.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, total, percent, last, valuep, valuen, fee, start_close))

else:
    state = con_buy.execute("SELECT state from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
    start_close = con_buy.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]

    if state == 'Buy':

        pclose_5m = float(start_close) - (float(start_close) * 1.1 / 100)
        fee = con_buy.execute("SELECT fee from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]

        if close < pclose_5m:
            levrage = 10
            date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
            amount = con_buy.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            balance = con_buy.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            total = con_buy.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            state = 'Sell'
            result = float(amount) * float(close)
            percent = con_buy.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last = con_buy.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last_price = con_buy.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            commission = format((float(amount) * float(last_price) * 0.002 / 100) + (float(amount) * float(close) * 0.002 / 100), ".4f")
            fees = format((float(close) * 100 / float(last_price) - 100) * levrage, ".2f")
            balance = (float(result) * float(fees) / 100 + float(result)) + float(total) - float(commission)
            fee = 0

            if float(fees) > 0:
                valueps = con_buy.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuen = con_buy.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuep = float(fees) + float(valueps)
                percent = 1 + percent
            else:

                valuep = con_buy.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuens = con_buy.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuen = float(fees) + float(valuens)
                last = 1 + last

            start_close = 0
            con_buy.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, 0, percent, last, valuep, valuen, fee, start_close))

        elif fee == 4:

            levrage = 10
            date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
            amount = con_buy.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            balance = con_buy.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            total = con_buy.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            state = 'Sell'
            result = float(amount) * float(close)
            percent = con_buy.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last = con_buy.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last_price = con_buy.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            commission = format((float(amount) * float(last_price) * 0.002 / 100) + (float(amount) * float(close) * 0.002 / 100), ".4f")
            fees = format((float(close) * 100 / float(last_price) - 100) * levrage, ".2f")
            balance = (float(result) * float(fees) / 100 + float(result)) + float(total) - float(commission)
            fee = 0

            if float(fees) > 0:
                valueps = con_buy.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuen = con_buy.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuep = float(fees) + float(valueps)
                percent = 1 + percent
            else:

                valuep = con_buy.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuens = con_buy.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuen = float(fees) + float(valuens)
                last = 1 + last

            start_close = 0
            con_buy.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, 0, percent, last, valuep, valuen, fee, start_close))

        else:

            date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
            total = con_buy.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            balance = con_buy.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            percent = con_buy.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            amount = con_buy.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last = con_buy.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuep = con_buy.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuen = con_buy.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            start_close = con_buy.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            fee += 1
            con_buy.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, total, percent, last, valuep, valuen, fee, start_close))
    else:


        date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
        total = con_buy.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        balance = con_buy.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        percent = con_buy.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        amount = con_buy.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        last = con_buy.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        valuep = con_buy.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        valuen = con_buy.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        start_close = con_buy.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        fee = 0
        con_buy.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, total, percent, last, valuep, valuen, fee, start_close))

res = con_buy.execute("SELECT * from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()
f = open(log_buy, "w")
f.write(str(res))
f.write("\n")
f.close()
con_buy.commit()




##################################      SELL
##################################

ema8_30m = a_30m.iloc[-1]['ema8']
ema13_30m = a_30m.iloc[-1]['ema13']
close_30m = a_30m.iloc[-1]['close']

ema8_5m = a_5m.iloc[-2]['ema8']
close_5m = a_5m.iloc[-2]['close']
close = a_5m.iloc[-1]['close']
time_5m = a_5m.iloc[-2]['date']
lema8_5m = a_5m.iloc[-3]['ema8']
lclose_5m = a_5m.iloc[-3]['close']

if (lclose_5m > lema8_5m) and (close_5m < ema8_5m):

    state = con_sell.execute("SELECT state from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
    start_close = con_sell.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]

    if state == 'Buy':

        pclose_5m = float(start_close) + (float(start_close) * 1.1 / 100)
        fee = con_sell.execute("SELECT fee from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]

        if close > pclose_5m:
            levrage = 10
            date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
            amount = con_sell.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            balance = con_sell.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            total = con_sell.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            state = 'Sell'
            result = float(amount) * float(close)
            percent = con_sell.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last = con_sell.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last_price = con_sell.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            commission = format((float(amount) * float(last_price) * 0.002 / 100) + (float(amount) * float(close) * 0.002 / 100), ".4f")
            fees = format((float(last_price) * 100 / float(close) - 100) * levrage, ".2f")
            balance = (float(result) * float(fees) / 100 + float(result)) + float(total) - float(commission)
            fee = 0

            if float(fees) < 0:
                valueps = con_sell.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuen = con_sell.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuep = float(fees) + float(valueps)
                percent = 1 + percent
            else:

                valuep = con_sell.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuens = con_sell.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuen = float(fees) + float(valuens)
                last = 1 + last

            start_close = 0
            con_sell.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, 0, percent, last, valuep, valuen, fee, start_close))

        elif fee == 4:

            levrage = 10
            date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
            amount = con_sell.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            balance = con_sell.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            total = con_sell.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            state = 'Sell'
            result = float(amount) * float(close)
            percent = con_sell.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last = con_sell.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last_price = con_sell.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            commission = format((float(amount) * float(last_price) * 0.002 / 100) + (float(amount) * float(close) * 0.002 / 100), ".4f")
            fees = format((float(last_price) * 100 / float(close) - 100) * levrage, ".2f")
            balance = (float(result) * float(fees) / 100 + float(result)) + float(total) - float(commission)
            fee = 0

            if float(fees) < 0:
                valueps = con_sell.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuen = con_sell.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuep = float(fees) + float(valueps)
                percent = 1 + percent
            else:

                valuep = con_sell.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuens = con_sell.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuen = float(fees) + float(valuens)
                last = 1 + last

            start_close = 0
            con_sell.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, 0, percent, last, valuep, valuen, fee, start_close))

        else:

            date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
            total = con_sell.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            balance = con_sell.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            percent = con_sell.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            amount = con_sell.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last = con_sell.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuep = con_sell.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuen = con_sell.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            start_close = con_sell.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            fee += 1
            con_sell.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, total, percent, last, valuep, valuen, fee, start_close))
    else:

        if (close_30m < ema8_30m) :

            date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
            whole = con_sell.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            state = con_sell.execute("SELECT state from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuep = con_sell.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuen = con_sell.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            balance = float(whole) / 5
            total = float(whole) - float(balance)
            amount = float(balance) / float(close)
            percent = con_sell.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last = con_sell.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            state = 'Buy'
            start_close = close
            fee = 0
            con_sell.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, 0, close, amount, total, percent, last, valuep, valuen, fee, start_close))

        else:
            date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
            total = con_sell.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            balance = con_sell.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            percent = con_sell.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            amount = con_sell.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last = con_sell.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuep = con_sell.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuen = con_sell.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            start_close = con_sell.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            fee = 0
            con_sell.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, total, percent, last, valuep, valuen, fee, start_close))

elif  (close_30m > ema8_30m):

    state = con_sell.execute("SELECT state from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]

    if state == 'Buy':

        levrage = 10
        date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
        amount = con_sell.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        balance = con_sell.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        total = con_sell.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        state = 'Sell'
        result = float(amount) * float(close)
        percent = con_sell.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        last = con_sell.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        last_price = con_sell.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        commission = format((float(amount) * float(last_price) * 0.002 / 100) + (float(amount) * float(close) * 0.002 / 100), ".4f")
        fees = format((float(last_price) * 100 / float(close) - 100) * levrage, ".2f")
        balance = (float(result) * float(fees) / 100 + float(result)) + float(total) - float(commission)
        fee = 0

        if float(fees) < 0:
            valueps = con_sell.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuen = con_sell.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuep = float(fees) + float(valueps)
            percent = 1 + percent
        else:

            valuep = con_sell.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuens = con_sell.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuen = float(fees) + float(valuens)
            last = 1 + last

        start_close = 0
        con_sell.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, 0, percent, last, valuep, valuen, fee, start_close))
    else:
        date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
        total = con_sell.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        balance = con_sell.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        percent = con_sell.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        amount = con_sell.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        last = con_sell.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        valuep = con_sell.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        valuen = con_sell.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        start_close = con_sell.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        fee = 0
        con_sell.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, total, percent, last, valuep, valuen, fee, start_close))
else:

    state = con_sell.execute("SELECT state from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
    start_close = con_sell.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]

    if state == 'Buy':

        pclose_5m = float(start_close) + (float(start_close) * 1.1 / 100)
        fee = con_sell.execute("SELECT fee from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]

        if close > pclose_5m:
            levrage = 10
            date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
            amount = con_sell.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            balance = con_sell.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            total = con_sell.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            state = 'Sell'
            result = float(amount) * float(close)
            percent = con_sell.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last = con_sell.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last_price = con_sell.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            commission = format((float(amount) * float(last_price) * 0.002 / 100) + (float(amount) * float(close) * 0.002 / 100), ".4f")
            fees = format((float(last_price) * 100 / float(close) - 100) * levrage, ".2f")
            balance = (float(result) * float(fees) / 100 + float(result)) + float(total) - float(commission)
            fee = 0

            if float(fees) < 0:
                valueps = con_sell.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuen = con_sell.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuep = float(fees) + float(valueps)
                percent = 1 + percent
            else:

                valuep = con_sell.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuens = con_sell.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuen = float(fees) + float(valuens)
                last = 1 + last

            start_close = 0
            con_sell.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, 0, percent, last, valuep, valuen, fee, start_close))

        elif fee == 4:

            levrage = 10
            date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
            amount = con_sell.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            balance = con_sell.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            total = con_sell.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            state = 'Sell'
            result = float(amount) * float(close)
            percent = con_sell.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last = con_sell.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last_price = con_sell.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            commission = format((float(amount) * float(last_price) * 0.002 / 100) + (float(amount) * float(close) * 0.002 / 100), ".4f")
            fees = format((float(last_price) * 100 / float(close) - 100) * levrage, ".2f")
            balance = (float(result) * float(fees) / 100 + float(result)) + float(total) - float(commission)
            fee = 0

            if float(fees) < 0:
                valueps = con_sell.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuen = con_sell.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuep = float(fees) + float(valueps)
                percent = 1 + percent
            else:

                valuep = con_sell.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuens = con_sell.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
                valuen = float(fees) + float(valuens)
                last = 1 + last

            start_close = 0
            con_sell.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, 0, percent, last, valuep, valuen, fee, start_close))

        else:

            date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
            total = con_sell.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            balance = con_sell.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            percent = con_sell.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            amount = con_sell.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            last = con_sell.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuep = con_sell.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            valuen = con_sell.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            start_close = con_sell.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
            fee += 1
            con_sell.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, total, percent, last, valuep, valuen, fee, start_close))
    else:
        date = datetime.datetime.utcfromtimestamp(time_5m / 1000)
        total = con_sell.execute("SELECT total from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        balance = con_sell.execute("SELECT balance from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        percent = con_sell.execute("SELECT percent from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        amount = con_sell.execute("SELECT amount from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        last = con_sell.execute("SELECT last from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        valuep = con_sell.execute("SELECT valuep from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        valuen = con_sell.execute("SELECT valuen from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        start_close = con_sell.execute("SELECT start_close from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()[0][0]
        fee = 0
        con_sell.execute("INSERT INTO {} (time, state, balance, price, amount, total, percent, last, valuep, valuen, fee, start_close) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );".format(symbol), (date, state, balance, close, amount, total, percent, last, valuep, valuen, fee, start_close))

res = con_sell.execute("SELECT * from {} ORDER BY rowid DESC LIMIT 1;".format(symbol)).fetchall()
f = open(log_sell, "w")
f.write(str(res))
f.write("\n")
f.close()
con_sell.commit()

