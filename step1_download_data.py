from yahoofinancials import YahooFinancials
import pandas as pd
import numpy as np
import json

#load TSX stock data
df = pd.read_csv('./Data/tsx_tickers.csv', delimiter=',', na_filter = False)
#extract the tickers
tsx_stocks = df['Ticker'].tolist()

#calculate returns from Yahoo Finance
stock_returns = {}
failed_to_parse = []
for ticker in tsx_stocks:
    #modify tickers to Yahoo Finance format
    if '.UN' in ticker:
        continue
    elif '.' in ticker:
        ticker = ticker[:ticker.index('.')] + '-' +ticker[ticker.index('.') + 1:]
    ticker = ticker + '.TO'
    stock_info = YahooFinancials(ticker)     
    try:
        yahoo_financials = YahooFinancials(ticker)
        data = yahoo_financials.get_historical_price_data(start_date='2019-01-01', 
                                                          end_date='2019-12-31', 
                                                          time_interval='daily')
        stock_data = pd.DataFrame(data[ticker]['prices'])
        stock_data = stock_data.drop('date', axis=1).set_index('formatted_date')
        stock_data = stock_data.rename(columns = {'formatted_date': 'Date'})
        stock_data.columns = ['High', 'Low', 'Open', 'Close', 'Volume', 'Adj Close']
        stock_data.index = stock_data.index.rename('Date')
        stock_data.to_csv(f'./Data/{ticker}.csv')
    except:
        print(f"fail to parse {ticker}")
        failed_to_parse.append(ticker)
        continue
