#imports:
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr

yf.pdr_override() #to activate yahoo finace workload

stock="AAPL"#input("Enter a stock ticker symbol: ")

startyear=2018
startmonth=1
startday=1

starttime=dt.datetime(startyear,startmonth,startday)
endtime=dt.datetime.now()

df=pdr.get_data_yahoo(stock, starttime,endtime)
#print(df)

# data=pdr.DataReader(stock,'yahoo',startyear,endtime)
# print(data)
delta=df['Adj Close'].diff(1)
delta.dropna(inplace=True) #droping null values

positive=delta.copy()
negative=delta.copy()
positive[positive<0]=0 #making alll -ve values in postitive columns as 0
negative[negative>0]=0

days=14
average_gain=positive.rolling(window=days).mean()
average_loss=abs(negative.rolling(window=days).mean())

relative_strength=average_gain/average_loss
RSI=100.0-(100.0/(1.0+relative_strength))
#RSI.dropna(inplace=True)

# print(RSI.tail(100))
# for index, value in RSI.items():
#     if value>70:
#         print('Buy on :',index,'at ',value)

combined_data=pd.DataFrame()
combined_data['Adj Close']=df['Adj Close']
combined_data['RSI']=RSI
combined_data.dropna(inplace=True)
#print(combined_data.iloc[14])

#1st plots
plt.figure(figsize=(12,8))
ax1=plt.subplot(211)
ax1.plot(combined_data.index,combined_data['Adj Close'],color='lightgray')
ax1.set_title('Adjusted close price',color='white')

ax1.grid(True,color='#555555')
ax1.set_axisbelow(True)
ax1.set_facecolor('black')
ax1.figure.set_facecolor('#121212')
ax1.tick_params(axis='x',color='white')
ax1.tick_params(axis='y',color='white')

#2nd plot
ax2=plt.subplot(212,sharex=ax1)
ax2.plot(combined_data.index,combined_data['RSI'],color='lightgray')
ax2.axhline(0,linestyle='--',alpha=0.5,color='#ff0000')
ax2.axhline(10,linestyle='--',alpha=0.5,color='#ffaa00')
ax2.axhline(20,linestyle='--',alpha=0.5,color='#00ff00')
ax2.axhline(30,linestyle='--',alpha=0.5,color='#cccccc')
ax2.axhline(70,linestyle='--',alpha=0.5,color='#cccccc')
ax2.axhline(80,linestyle='--',alpha=0.5,color='#00ff00')
ax2.axhline(90,linestyle='--',alpha=0.5,color='#ffaa00')
ax2.axhline(100,linestyle='--',alpha=0.5,color='#ff0000')

ax2.set_title('RSI Value',color='white')
ax2.grid(False)
ax2.set_axisbelow(True)
ax2.set_facecolor('black')
ax2.tick_params(axis='x',color='white')
ax2.tick_params(axis='y',color='white')

plt.show()