import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime as dt
from datetime import timedelta

# get stock data
ticker = "AAPL"
end=dt.datetime.now()
start=end-timedelta(3)
df=yf.download(ticker, start, end, interval="1m")

# calculate RSI

df["RSI"] = ta.rsi(df["Close"], length=14, show=False)
df = df.dropna()

# create subplot
fig = make_subplots(rows=2, cols=1, row_heights=[0.7, 0.3])

# add close price plot
fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close'),row=1, col=1)

# add RSI plot
fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI'),row=2, col=1)

# add red dots for RSI above 70
fig.add_trace(go.Scatter(x=df[df['RSI'] > 70].index,
                         y=df[df['RSI'] > 70]['Close'],
                         mode='markers',
                         marker=dict(size=6, color='red'),
                         name='RSI above 70',
                         showlegend=True),
              row=1, col=1)

# add green dots for RSI below 30
fig.add_trace(go.Scatter(x=df[df['RSI'] < 30].index,
                         y=df[df['RSI'] < 30]['Close'],
                         mode='markers',
                         marker=dict(size=6, color='green'),
                         name='RSI below 30',
                         showlegend=True),
              row=1, col=1)

# update layout
fig.update_layout(title=f"{ticker} Close Price and RSI", showlegend=True)

# show plot
fig.show()