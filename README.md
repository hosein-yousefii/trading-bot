# trading-bot
trading bot based on moving averages in binance.
it uses two time frames, 30 minutes for checking the conditions in higher level and 5 minutes in order to find suitable situation to place an order.
it works with two different program: 
  - fetch-data.py is for gathering candlesticks data from binance for two time frames, which is mentioned above.
  - spot.py is for check the conditions and buy or sell assets.

Currently, it's under developement and just work for test environment.
I used pandas to cllecting datas and sqlite to save results.

# How to
