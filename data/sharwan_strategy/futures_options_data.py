import pandas as pd
import requests
from datetime import datetime, timedelta

class IndexReport:
    def __init__(self)-> None:
        self.base_url='https://www.nseindia.com'
        self.session=requests.sessions.Session()
        self.session.headers['User-Agent']='Moxilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'
        self.session.get(self.base_url, timeout=10)

    def fetch_historical_index_data(self,instrumentType,symbol,from_date=None,to_date=datetime.now(),year=None,expiryDate=None,optionType=None,strikePrice=None):
        df=[]
        
        if from_date==None:
            if to_date.weekday()<5:
                from_date=to_date-timedelta(days=1)
            else:
                from_date=to_date-timedelta(days=to_date.weekday()-3)
        
        from_date=from_date.strftime('%d-%m-%Y')
        to_date=to_date.strftime('%d-%m-%Y')

        api_url=f'/api/historical/foCPV?from={from_date}&to={to_date}&instrumentType={instrumentType}&symbol={symbol}'
        print(api_url)
        if instrumentType[0:3]=='OPT':
            if optionType!=None:
                api_url+=f"&optionType={optionType}"
            else:
                print("Please set optionType")
                return df
            if strikePrice!=None:
                api_url+=f"&strikePrice={strikePrice}"
        
        if year!=None:
            api_url+=f"&year={year}"
        if expiryDate!=None:
            api_url+=f"&expiryDate={expiryDate}"
        
        res=self.session.get(self.base_url+api_url, timeout=10)
        if res.status_code==200:
            res_json=res.json()
            if 'data' in res_json:
                df=pd.json_normalize(res_json['data'])
            else:
                print("NO data sent by NSE")
                print(res_json)
        else:
            print('HTTP unsuccessful request: ')
            print(res)
        
        return df


if __name__=='__main__':
    ir=IndexReport()
    print(ir.fetch_historical_index_data(instrumentType='FUTIDX',symbol='NIFTY'))
    #df=ir.fetch_historical_index_data(instrumentType='OPTIDX',symbol='NIFTY',optionType='CE',expiryDate='31-Oct-2023')
   
    # df=df['FH_STRIKE_PRICE']
    # print(df)
    #print(df.loc['STRIKE']) #printing a single row information
    # print(df)