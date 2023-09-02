import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
import datetime
from datetime import timedelta


# import and clean data
ticker_val = 'tsla'

stock_prices = yf.Ticker(ticker_val)
stock_prices = stock_prices.history(period='max')

# set page title
st.set_page_config(page_title='Tesla Stock Price Analysis',
                   page_icon='icons/tesla.png')

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




def main():
    # define a latest date variable
    latest_date = str(stock_prices.index[-1])
    latest_date = latest_date[:10]
    

    #set selection options
    options = ['Explore Price Trends', 'Make Predictions']
    
    # using the options in a sidebar
    selection = st.sidebar.selectbox('Select a page :balloon:',options)
    
    # fill the explore page
    if selection == 'Explore Price Trends':
        # adding header
        st.header('Analysis on Tesla Stock Price :chart_with_upwards_trend:')
        st.write(f'Prices as at {latest_date}')
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # store variables for our column displays
        last_close = round(stock_prices.iloc[-1]['Close'],2)
        previous_day_price = round(stock_prices.iloc[-2]['Close'],2)
        price_difference_day = last_close - previous_day_price
        percent_change_day = round((price_difference_day/previous_day_price)*100,2)
        previous_year_price = round(stock_prices.iloc[-252]["Close"],2)
        price_difference_year = round(last_close - previous_year_price,2)
        percent_change_year = round((price_difference_year/previous_year_price)*100,2)
        
        with col1:
            st.metric('Close Price', f'${last_close}')
        with col2:
            st.metric('Previous Day Close', f'${previous_day_price}', percent_change_day)
        with col3:
            st.metric('Price Change (YoY)', f'${price_difference_year}', percent_change_year)
        with col4:
            st.metric('52 Week High',f'${stock_prices.iloc[-1]["52-week High"]:.2f}')
        with col5:
            st.metric('52 Week Low',f'${stock_prices.iloc[-1]["52-week Low"]:.2f}')
            
        # Get the latest date from DataFrame index
        latest_date = stock_prices.index.max()
        
        # Calculate the date 10 days ago from the latest date
        twenty_days_ago = latest_date - timedelta(days=30)
            
        # Add a slider for selecting date range
        start_date = st.date_input("Select start date",value=twenty_days_ago, min_value=stock_prices.index.min(), )
        end_date = st.date_input("Select end date", stock_prices.index.max())
        
        # Make selected dates timezone-aware (assuming UTC timezone)
        start_date = pd.to_datetime(start_date, utc=True)
        end_date = pd.to_datetime(end_date, utc=True)
        
        # Filter data based on selected date range
        filtered_data = stock_prices.loc[start_date:end_date]
        
        # plotting our candle stick chart
        fig = go.Figure(data=[go.Candlestick(x=filtered_data.index,
                        open=filtered_data['Open'],
                        high=filtered_data['High'],
                        low=filtered_data['Low'],
                        close=filtered_data['Close'])])
        
        # Set the title of the Plotly figure
        fig.update_layout(title="Candlestick Chart")
        
        st.plotly_chart(fig)
        
        
        
        if st.checkbox('Click to see trends with moving averages'):
            # ploting trends plot
            years = set(stock_prices.index.year)
            years =  sorted(years, reverse=True)
            year = st.selectbox('Pick a year for your trend plot', years)
            year_df = stock_prices[stock_prices.index.year == year]
            fig2 = px.line(year_df, x=year_df.index
                                 ,y=['Close','30-day MA','60-day MA',
                                     '52-week High','52-week Low']
                                 ,title="Full Year Price Trend")
            
            fig2.update_yaxes(title_text='Price ($)')
            # Set line colors and make "Close" line stand out
            # Define colors for each line
            line_colors = ['blue', 'green', 'red', 'purple', 'orange']
            cols = ['Close','30-day MA','60-day MA','52-week High','52-week Low']
            
            for i, col in enumerate(cols):
                line_color = line_colors[i % len(line_colors)]
                if col == "Close":
                    line_color = 'black'  # Stand out color for "Close" line
                fig2.update_traces(line=dict(color=line_color), selector=dict(name=col))
            st.plotly_chart(fig2)
            
# Required to let Streamlit instantiate our web app.  
if __name__ == '__main__':
	main()