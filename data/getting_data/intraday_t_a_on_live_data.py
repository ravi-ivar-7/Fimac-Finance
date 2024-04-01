import pandas_ta as ta
import pandas as pd
from time import sleep

from live_nse_intraday import M_C_api
#uses live_nse_intraday to get data
#trigers
macd_ok=False
ema_ok=False

obj=M_C_api('SBIN')
nd=0
while nd>-1:
    nd=obj.fetch_intraday_data()
    if nd>0:
        df=obj.dataframe.copy()
        df.rename({'h':'high','l':'low','c':'close','o':'open','v':'volume','t':'timestamp'},axis=1,inplace=True)
        df.set_index(pd.DatetimeIndex(df['dt']),inplace=True)
        custom_stratety=ta.Strategy(
            name='Custom Strategy',
            description='EMA 9,26,cross over with MACD and VWAP support',
            ta=[
                {'kind':'ema','length':9},
                {'kind':'ema','length':26},
                {'kind':'vwap'},
                {'kind':'macd','fast':12,'slow':26,'col_names':('MACD','MACD_H','MACD_S')},
            ]
        )
        df.ta.strategy(custom_stratety,timed=True) #runtime 
        print(df)
        print(df.iloc[-1])

        #enabling trigers
        prev=df.iloc[-2]
        current=df.iloc[-1]
        #for macd
        if macd_ok==False and prev['MACD']<current['MACD'] and prev['MACD_S']<current['MACD_S']:
            macd_ok=True
        elif macd_ok and current['MACD']>current['MACD_S']:
            macd_ok=False
        #for emas
        if ema_ok==False and prev['EMA_9']<current['EMA_9'] and prev['EMA_26']<current['EMA_26']:
            macd_ok=True
        elif ema_ok and current['EMA_9']<current['EMA_26']:
            ema_ok=False

        #for holding
        if ema_ok and macd_ok and current['VWAP_D']/current['close']<1.02 and current['MACD_S']>current['MACD']:#i.e less than 2% and  macd signal on crossover is +ve but also in upper/+ve direction
            print("it is high time to take a position")


        last=obj.dataframe.iloc[-1]['dt']
        if(last.hour+last.minute/60)>15.5:
            print("Market is closed")
            break
    sleep(obj.delta_time)


