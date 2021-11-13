# trading-bot
trading bot based on moving averages in binance.
it uses two time frames, 30 minutes for checking the conditions in higher level and 5 minutes in order to find suitable situation to place an order.
it works with two different program: 
  - fetch-data.py is for gathering candlesticks data from binance for two time frames, which is mentioned above.
  - spot.py is for check the conditions and buy or sell assets.

Currently, it's under developement and just work for test environment.
I used pandas to cllecting datas and sqlite to save results.

# How to
first of all, you should create api key from binance and use them in fetch-data.py to gather candlestick datas. then run the fetch-data.py to fetch the required data and store them in your directory.
Next, you should run spot.py to check the conditions and place a suitable order (buy/ sell).
it's recommended to run both of them every 1 minute or 2 minute.
if you want to change your coin from btc to other things you should change variables in both files.

# How to contribute
it woud be a good idea to send me emails for further details: yousefi.hosein.o@gmail.com

Copyright 2021 Hosein Yousefi <yousefi.hosein.o@gmail.com>
