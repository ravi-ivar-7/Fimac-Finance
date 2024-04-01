import pandas as pd
import requests
from datetime import datetime, timedelta
import time

#this file is working fine, for getting equity data for f and o

class index_data:
    def __init__(self) -> None:
        self.session=requests.sessions.Session()
        self.session.headers['User-Agent']='Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36 Edg/116.0.1938.62'
        #dummy request
        self.session.get('https://nseindia.com',timeout=10)#all the cookies will be set in this
        #self.url='https://www.nseindia.com/api/equity-stockIndices?index='#NIFTY%2050
        self.url='https://www.nseindia.com/api/equity-stock?index=allcontracts'

    def fetch_index_from_nse(self,index_symbol):
        df=[]#in case of any issue we will return empty dataframe
        res=self.session.get(self.url,timeout=10) #storing response we get from nse on sending url
        if res.status_code==200:#we only return if successful response,  
            res_json=res.json()
            #we check if json contains data filed , we only then proceed further
            if 'value' in res_json:
                df=pd.json_normalize(res_json['value'])
                print(df)
            else:
                print("Data not returned by NSE")
                print(res_json)   
        else:
            print("HTTP request failed.")
            print(res)
        return df

    #for exporting/saving data for futher analysis
    def save_index_to_csv(self,index_symbol,csv_file_name=None,delimiter=',',index=True,header=True):
        if csv_file_name==None:
            csv_file_name=index_symbol+'.csv'
        df=self.fetch_index_from_nse(index_symbol)
        if len(df)>0:#we save only if there is some data
            df.to_csv(csv_file_name,sep=delimiter,index=index,header=header)
            return True
        return False
    
    #tesing
if __name__=='__main__':
    from pprint import pprint
    obj=index_data()
    while True:
        res=obj.fetch_index_from_nse('NIFTY 50')
        print(res.iloc[0])
        time.sleep(5)
    # if obj.save_index_to_csv('NIFTY IT'):#we can give our name also to this file
    #     print('csv file saved ')
    # else:
    #     print('Unable to save csv file')
    


