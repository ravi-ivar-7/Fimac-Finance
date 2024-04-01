from django.shortcuts import render
from backtesting.form import ConditionForm

import datetime as dt
import pandas as pd
import numpy as np
from pandas_datareader import data as pdr
import yfinance as yf
from multiprocessing import Process, Manager
import plotly.graph_objects as go
custom_config = {'displaylogo':False}

yf.pdr_override() 

def smas_function(**kwargs):
            stock=kwargs['stock']
            startdate=kwargs['start_date']
            enddate=kwargs['enddate']
            choosen_conditions=kwargs['choosen_conditions']
            available_conditions=kwargs['available_conditions']
            pos=0
            percentage_change=[]
            row_num=0
        #try:
            df=pdr.get_data_yahoo(stock, startdate,enddate)
            #print(df.tail())
            smaUsed=[50,100,150,200]
            for sma in smaUsed:
                df['SMA_'+str(sma)]=round(df.iloc[:,4].rolling(window=sma).mean(),2)

            df=df.iloc[max(smaUsed):]
            #print(f"Checking {stock} .......")
        
            this_row=[]
            all_row=[]
            for i in df.index:
                conditions=[] #this stores if choosen filds satisy given criteria or not
                row_num+=1
                close=df['Adj Close'][i]
                moving_average_50=df['SMA_50'][i]
                moving_average_100=df['SMA_100'][i]
                moving_average_150=df['SMA_150'][i]
                moving_average_200=df['SMA_200'][i]
                remark='N/A'
                this_row=[i,close,moving_average_50,moving_average_100,moving_average_150,moving_average_200,remark]
                condition_c_50ma=choosen_conditions[0]
                condition_c_100ma=choosen_conditions[1]
                condition_c_150ma=choosen_conditions[2]
                condition_c_200ma=choosen_conditions[3]
                condition_50ma_100ma=choosen_conditions[4]
                condition_50ma_150ma=choosen_conditions[5]
                condition_50ma_200ma=choosen_conditions[6]
                condition_100ma_150ma=choosen_conditions[7]
                condition_100ma_200ma=choosen_conditions[8]
                condition_150ma_200ma=choosen_conditions[9]

                if condition_c_50ma:
                    condition_c_50ma=close>moving_average_50
                    conditions.append(condition_c_50ma)

                if condition_c_100ma:
                    condition_c_100ma=close>moving_average_100
                    conditions.append(condition_c_100ma)

                if condition_c_150ma:
                    condition_c_150ma=close>moving_average_150
                    conditions.append(condition_c_150ma)

                if condition_c_200ma:
                    condition_c_200ma=close>moving_average_200
                    conditions.append(condition_c_200ma)

                if condition_50ma_100ma:
                    condition_50ma_100ma=moving_average_50>moving_average_100
                    conditions.append(condition_50ma_100ma)

                if condition_50ma_150ma:
                    condition_50ma_150ma=moving_average_50>moving_average_150

                    conditions.append(condition_50ma_150ma)
                if condition_50ma_200ma:
                    condition_50ma_200ma=moving_average_50>moving_average_200
                    conditions.append(condition_50ma_200ma)

                if condition_100ma_150ma:
                    condition_100ma_150ma=moving_average_100>moving_average_150
                    conditions.append(condition_100ma_150ma)

                if condition_100ma_200ma:
                    condition_100ma_200ma=moving_average_100>moving_average_200
                    conditions.append(condition_100ma_200ma)

                if condition_150ma_200ma:
                    condition_150ma_200ma=moving_average_150>moving_average_200
                    conditions.append(condition_150ma_200ma)

                if all(conditions):
                    all_conditions=True
                else:
                    all_conditions=False

                if all_conditions and pos==0:#buying condition
                    pos=1
                    bp=close
                    remark=f'Buying at {close}'
                    this_row[-1]=remark
                elif not all_conditions and pos==1: #open position and not all conditions are satisfied , we sell 
                    pos=0
                    sp=close
                    remark=f'Selling at {close}'
                    this_row[-1]=remark
                    pc=((sp/bp)-1)*100
                    percentage_change.append(pc)
                if row_num==df['Adj Close'].iloc[-1] and pos==1:#open position on last day, we need to sell it
                    pos=0
                    sp=close
                    remark=f'Selling at {close}'
                    this_row[-1]=remark
                    pc=((sp/bp)-1)*100
                    percentage_change.append(pc)
                all_row.append(this_row)

            #trade statistics
            ng=len([pc for pc in percentage_change if pc>=0]) #total profitable trades
            nl=len([pc for pc in percentage_change if pc<0]) #total looseable trades

            if ng>0:
                avg_gain=sum([pc for pc in percentage_change if pc>0])/ng
                max_gain=max(percentage_change)
            else:
                avg_gain=0
                max_gain='N/A'

            if nl>0:
                avg_loss=sum([pc for pc in percentage_change if pc<0])/nl
                max_loss=min(percentage_change)
                gain_loss_ratio=abs(avg_gain/avg_loss) #since if no loss then we won't be able to find this ratio
            else:
                avg_loss=0
                max_loss='N/A'
                gain_loss_ratio='N/A'

            batting_avg=ng/(ng+nl) if (ng+nl)>0 else 0
            #for total returns
            multiplitive_factor=[(pc/100+1) for pc in percentage_change]
            total_multiplitive_factor=np.prod([mf for mf in multiplitive_factor])
            total_return=(total_multiplitive_factor-1)*100

            all_data={'ng':ng,'nl':nl,'batting_avg':batting_avg,'gain_loss_ratio':gain_loss_ratio,'avg_gain':avg_gain,'avg_loss':avg_loss,'max_gain':max_gain,'max_loss':max_loss,'total_return':total_return,'all_row':all_row}

            return all_data

        #except Exception:
         #   print(f"No data is present for {stock}")

# Define the function mapping 
function_mapping = {
                    'smas_function':smas_function,
                    # Add other function names and corresponding functions here
                }

#timeout function
timeout = 20 # Timeout in seconds 
timeout_error = f"Computation time limit exceeded.Current time-limit is {timeout} seconds.Try with shorter time-period"
def run_with_timeout(all_info_data, **kwargs):
    #try:
        function_name=kwargs['function_name']
        function=function_mapping.get(function_name)
        all_info = function(**kwargs)
        all_info_data.update(all_info)
    #except Exception as e:
        #all_info_data['input_error'].append(str(e))


def smas_method(request):
    form = ConditionForm(request.POST or None)
    context={
             'topic_name':"Backtestings",
             'method_name':'SMAs analysis',
             'title':'Backtestings',
             'form':form
             }
    function_name='smas_function'
    if form.is_valid():
        choosen_conditions = []
        stock = form.cleaned_data['stock']
        start_date = form.cleaned_data['start_date']
        enddate = dt.datetime.now()
        for condition_num in range(1, 11):
            condition_field_name = f'condition{condition_num}'
            condition_value = form.cleaned_data[condition_field_name]
            choosen_conditions.append(condition_value)

        available_conditions=['condition_c_50ma','condition_c_100ma','condition_c_150ma','condition_c_200ma','condition_50ma_100ma','condition_50ma_150ma','condition_50ma_200ma','condition_100ma_150ma','condition_100ma_200ma','condition_150ma_200ma']

        kwargs={'stock':stock,'start_date':start_date,'enddate':enddate,'choosen_conditions':choosen_conditions,'available_conditions':available_conditions,'function_name':function_name }

        with Manager() as manager:
                    all_info_data = manager.dict() 
                    process = Process(target=run_with_timeout, args=(all_info_data,),kwargs=kwargs)
                    process.start()
                    process.join(timeout)
                    if process.is_alive():
                        process.terminate()
                        context['timeout_error']=timeout_error
                    else:
                        data=all_info_data
             
                        #plot
                        all_row=data['all_row']
                        round_off=7
                        date=[value[0] for value in all_row]
                        close_value=[value[1] for value in all_row]
                        moving_average_50=[value[2] for value in all_row]
                        moving_average_100=[value[3] for value in all_row]
                        moving_average_150=[value[4] for value in all_row]
                        moving_average_200=[value[5] for value in all_row]
                        fig=go.Figure()
                        fig.add_trace(go.Scatter(x=date,y=close_value,mode='lines',name='closing price'))
                        fig.add_trace(go.Scatter(x=date,y=moving_average_50,mode='lines',name='moving_average_50'))
                        fig.add_trace(go.Scatter(x=date,y=moving_average_100,mode='lines',name='moving_average_100'))
                        fig.add_trace(go.Scatter(x=date,y=moving_average_150,mode='lines',name='moving_average_150'))
                        fig.add_trace(go.Scatter(x=date,y=moving_average_200,mode='lines',name='moving_average_200'))
                        fig=fig.to_html(full_html=False,config=custom_config)
                        context_plot={'plot':fig}
                        #tabulate summary
                        filtered_rows=[row for row in all_row if 'N/A' not in row]
                        headings=['date','actual price','moving_average_50','moving_average_100','moving_average_150','moving_average_200','remark']
                      
                        context_table={'headings':headings,'table_output':filtered_rows}


                        context_result = {
                            'result':f"Results for {stock} from {start_date} to {enddate}, with sample size of {data['ng']+data['nl']} is:",                   
                            'batting_avg': f"Batting Avg  : {data['batting_avg']}",
                            'gain_loss_ratio':f"Gain/loss ratio: {data['gain_loss_ratio']}" ,
                            'avg_gain': f"Average Gain: {data['avg_gain']}" ,
                            'avg_loss':f"Average Loss:{data['avg_loss']} " ,
                            'max_gain':f"Max Returns: {data['max_gain']} " ,
                            'max_loss':f"Max loss: {data['max_loss']}" ,
                            'total_return':f"Total returns over {data['ng']+data['nl']} executed trades is : {data['total_return']} %" 
                        }
                        context={**context,**context_result,**context_plot,**context_table,'form': form,'choosen_conditions': choosen_conditions}
                    return render(request, 'backtesting_input_output.html', context )   
    
    return render(request,'backtesting_input_output.html',context)