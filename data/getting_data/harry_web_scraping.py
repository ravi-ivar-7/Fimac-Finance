import pandas as pd
import sys
import requests
from bs4 import BeautifulSoup
import re
import os

def fetch_NSE_stock_price(stock_code):
    
    stock_url  = f'https://www.nseindia.com/get-quotes/equity?symbol=SBIN'
    #print(stock_url)
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
    response = requests.get(stock_url, headers=headers)
    #print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    data_array = soup.find(id='info-tradeinfo').getText().strip().split(":")
    #print(type(data_array))
    for item in data_array:
        print(item)
        if 'lastPrice' in item:
            index = data_array.index(item)+1
            latestPrice=data_array[index].split('"')[1]
            lp =  float(latestPrice.replace(',',''))
            print(lp)


fetch_NSE_stock_price('SBIN')