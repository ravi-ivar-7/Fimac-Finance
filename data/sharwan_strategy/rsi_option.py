import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
custom_config = {'displaylogo':False}
from plotly.subplots import make_subplots
import datetime as dt
from datetime import timedelta


# calculate RSI
def RSI_function(**kwargs):
        ticker=kwargs['ticker']
        df=kwargs['data']
        length=kwargs['length']
        rsi_lower_limit=kwargs['rsi_lower_limit']
        rsi_upper_limit=kwargs['rsi_upper_limit']
        df["RSI"] = ta.rsi(df["Close"], length=length, show=False)
        df = df.dropna()

        # create subplot
        fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3])

        # add close price plot
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close'),row=1, col=1)

        # add RSI plot
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI'),row=2, col=1)
        fig.add_hline(y=rsi_upper_limit, line_width=1, line_dash="dash", line_color="black",row=2,col=1,annotation_text=f'RSI={rsi_upper_limit}')
        fig.add_hline(y=rsi_lower_limit, line_width=1, line_dash="dash", line_color="black",row=2,col=1, annotation_text=f'RSI={rsi_lower_limit}')
       
        # add red dots for RSI above 70
        fig.add_trace(go.Scatter(x=df[df['RSI'] > rsi_upper_limit].index,
                                 y=df[df['RSI'] > rsi_upper_limit]['Close'],
                                 mode='markers',
                                 marker=dict(size=10,symbol='triangle-down-open', color='red'),
                                 name=f'RSI above {rsi_upper_limit}',
                                 showlegend=True),
                      row=1, col=1)

        # add green dots for RSI below 30
        fig.add_trace(go.Scatter(x=df[df['RSI'] < rsi_lower_limit].index,
                                 y=df[df['RSI'] < rsi_lower_limit]['Close'],
                                 mode='markers',
                                 marker=dict(size=10, symbol='triangle-up-open',color='green'),
                                 name=f'RSI below {rsi_lower_limit}',
                                 showlegend=True),
                      row=1, col=1)
        
        # update layout
        fig.update_layout(title=f"{ticker} Close Price and RSI", showlegend=True)

        return df,fig

def group_data_function(**kwargs):
        df=kwargs['data']
        
        group_period=kwargs['group_period']
        df_grouped=df.resample(group_period).agg({
                'Open':'first',
                'High':'max',
                'Low':'min',
                'Close':'last'
        })
        df_grouped=df_grouped.dropna() #dropping last grouped-period entry
        return df_grouped

def candle_stick_function(**kwargs):
        ticker=kwargs['ticker']
        df=kwargs['data']
        timeperiod=kwargs['timeperiod']
        fig=go.Figure(
                go.Candlestick(
                x=df.index,
                low=df['Low'],
                high=df['High'],
                close=df['Close'],
                open=df['Open'],
                increasing_line_color='green',
                decreasing_line_color='red',
                )
        )
        fig.update_layout(xaxis_rangeslider_visible=True,title=f'Candle-stick chart for {ticker} with timeperiod {timeperiod} (T: minutes)',yaxis_title=f'{ticker} price',xaxis_title='Date range selecter')
        return fig

def sarvan_strategy(**kwargs):
        df=kwargs['data']
        ticker=kwargs['ticker']
        timeperiod=kwargs['timeperiod']
        rsi_data=RSI_function(ticker=ticker,data=df,length=14,rsi_lower_limit=30,rsi_upper_limit=70)
        grouped_data=group_data_function(data=df,group_period=timeperiod)
        candle_stick_data=candle_stick_function(ticker=ticker,timeperiod=timeperiod,data=grouped_data)

        return 0




end=dt.datetime.now()
start=end-timedelta(2)#start='2020-2-2'

ticker = "AAPL"
df=yf.download(ticker, start, end, interval='1m' )
timeperiod='15T' #15 min (relative to original data)

#data from nse for future index
from futures_options_data import IndexReport
fut_opt_data=IndexReport()

#df=fut_opt_data.fetch_historical_index_data(instrumentType='OPTIDX',symbol='NIFTY',optionType='PE',expiryDate='31-Aug-2023')
df=fut_opt_data.fetch_historical_index_data(instrumentType='FUTIDX',symbol='NIFTY')
print(df)
print(df.iloc[0]) #printing a single row information


# data,rsi_plot=RSI_function(ticker=ticker,data=df,length=14,rsi_lower_limit=30,rsi_upper_limit=70)
# rsi_plot=rsi_plot.show(config=custom_config)
# grouped_data=group_data_function(data=df,group_period=timeperiod)
# candle_stick=candle_stick_function(ticker=ticker,timeperiod=timeperiod,data=grouped_data)
# candle_stick.show(config=custom_config)
# print(grouped_data)
# print(data)

# result=sarvan_strategy(data=df,timeperiod=timeperiod,ticker=ticker)
# print(result)
