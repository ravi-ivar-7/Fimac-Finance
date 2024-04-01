import requests
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta
#this file is working fine, it brings equity data of nse per day from 2023
class NSE():
    def __init__(self, timeout=10) -> None:
        self.base_url = 'https://www.nseindia.com'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1000.0 Safari/537.36 Edg/100.0.1000.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/avif,*/*;q=0.8,application/signed-exchange;v=b3;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        self.timeout = timeout
        self.cookies = {}  # Use a dictionary to store cookies

    def __getCookies(self, renew=False):
        if not renew and self.cookies:  # cookies already present
            return self.cookies
        
        r = requests.get(self.base_url, timeout=self.timeout, headers=self.headers)
        self.cookies = r.cookies.get_dict()
        return self.__getCookies()

    def getHistoricalData(self, symbol, series, from_date=None, to_date=None):
        if to_date is None:
            to_date = datetime.now()

        if from_date is None:
            if to_date.weekday() < 5:
                from_date = to_date - timedelta(days=1)
            else:
                from_date = to_date - timedelta(days=to_date.weekday() - 3)

        url = f"/api/historical/cm/equity?symbol={symbol}&series=[%22{series}%22]&from={from_date.strftime('%d-%m-%Y')}&to={to_date.strftime('%d-%m-%Y')}&csv=true"
        response = requests.get(self.base_url + url, headers=self.headers, timeout=self.timeout, cookies=self.__getCookies())

        if response.status_code != 200:  # Mostly cookies get expired
            response = requests.get(self.base_url + url, headers=self.headers, timeout=self.timeout, cookies=self.__getCookies(True))

        df = pd.read_csv(BytesIO(response.content), sep=',', thousands=',')

        # Changing columns as per requirement
        df = df.rename(columns={'Date ': 'date', 'series': 'series', 'OPEN': 'open', 'HIGH': 'high', 'LOW': 'low',
                                'PREV. CLOSE': 'prev_close', 'ltp': 'ltp', 'close': 'close', '52W H': 'hi_52_wk',
                                '52W L': 'lo_52_wk', 'VOLUME': 'volume', 'VALUE': 'value', 'No of trades': 'trades'})

        df.date = pd.to_datetime(df.date).dt.strftime('%Y-%m-%d')
        return df

if __name__ == '__main__':
    api = NSE()
    df = api.getHistoricalData('SBIN', 'EQ', datetime(2023, 1, 1), datetime(2023, 10,26))
    print(df)
