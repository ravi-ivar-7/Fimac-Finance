import requests 
from datetime import datetime
from time import sleep
import pandas as pd
#this file is working fine, using moneycontrol api brings all timeframe data
class MCApi:
    def __init__(self,symbol,resolution=1,data_from=None,data_to=datetime.now()) -> None:
        self.symbol=symbol
        self.resolution=resolution
        self.data_to=int(data_to.timestamp())
        self.resoution_dt={'1':60,'3':180,'5':300,'15':900,'30':1800,'60':3600,'300':1800,'D':24*3600,'W':7*24*3600,'M':30*24*3600,'45':45*24*3600,'120':120*24*3600,'240':240*24*3600}
        self.delta_time=self.resoution_dt[str(self.resolution)]
        if data_from==None:
            self.data_from=self.data_to-self.delta_time*1000 #if no start date, go back to 1000 entries back
        else:
            self.data_from=int(data_from.timestamp())#conveting time to achelon seconds

        self.session=requests.sessions.Session()
        self.session.headers['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1000.0 Safari/537.36 Edg/100.0.1000.0'
        self.session.get('https://www.moneycontrol.com/stocksmarketsindia/')
        self.symbol_meta=symbol
        self.dataframe=[]
        
    def fetch_symbol_meta(self):
        if self.symbol_meta==None:
            self.symbol_meta=self.session.get(f'https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/symbols?symbol={self.symbol}')
        return self.symbol_meta
    
    def fetch_intraday_data(self,countback=None): #countback is how much to go in past
        new_data=0
        try:
            if countback==None:
                countback=int((self.data_to-self.data_from)/self.delta_time)
                if countback>1000:
                    countback=1000

            response=self.session.get(f'https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol={self.symbol_meta}&resolution={self.resolution}&from={self.data_from}&to={self.data_to}&countback={countback}')
            data=response.json()
            if data['s']=='no_data':  #s: status: ok or no_data
                return -1
            
            df=pd.DataFrame.from_dict(data)
            df['dt']=pd.to_datetime(df['t']+19800,unit='s') #adding 5:30 hr
            n=len(self.dataframe)
            if n==0: #initially lenght will be 0 so we copy it
                self.dataframe=df.copy()
                new_data=len(self.dataframe)
            else:#after subsequent countback
                df=pd.concat([self.dataframe,df[df['t'].isin(self.dataframe['t'])==False]]).reset_index(drop=True) #removing already present entries
                self.dataframe=df.copy() #**************
                new_data=len(self.dataframe)-n

            self.data_from=self.data_to #updating date
            self.data_to+=self.delta_time #**********
        except Exception as ex:
            new_data=-1

        return new_data
    

if __name__=='__main__':
    from_date=datetime(2022,10,10,9,15)
    from pprint import pprint
    obj=MCApi('SBIN',3,from_date)
    nd=0
    while nd>-1:
        nd=obj.fetch_intraday_data()
        print(nd)
        if nd>0:
            pprint(obj.dataframe)
            print('Wait for 1 min.')
            last=obj.dataframe.iloc[-1]['dt']
            if (last.hour+last.minute/60)>15.5:
                print("Market is closed")
                break
            sleep(obj.delta_time)
        