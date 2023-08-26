import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf


# import and clean data
ticker_val = 'tsla'

stock_prices = yf.Ticker(ticker_val)
stock_prices = stock_prices.history(period='max')

# feature engineering
# create columns for moving avearages
stock_prices['30-day MA'] = stock_prices['Close'].rolling(window=30).mean()
stock_prices['60-day MA'] = stock_prices['Close'].rolling(window=60).mean()
stock_prices['90-day MA'] = stock_prices['Close'].rolling(window=90).mean()

#add columns to show closing price 52 week highs and lows
stock_prices['52-week High'] = stock_prices['Close'].rolling(window=364).max()
stock_prices['52-week Low'] = stock_prices['Close'].rolling(window=364).min()

# deleting the stocksplit and dividends columns
del stock_prices['Stock Splits'] 
del stock_prices['Dividends']


latest_date = str(stock_prices.index[-1])
latest_date = latest_date[:10]

# adding header
st.header('Analysis on Stock')
st.write(f'Prices as at {latest_date}')

if st.checkbox('View Price for Last 10 Trading Days'):
    st.dataframe(stock_prices.tail(10))
    
col1, col2, col3, col4 = st.columns(4)

# store variables for our column displays
last_close = stock_prices['Close'].tail(1).tolist()
last_close = round(last_close[0],2)

with col1:
    st.metric('Last Closing Price', f'${last_close}')