from django.shortcuts import render
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
import re,datetime
from multiprocessing import Process, Manager
import plotly.graph_objects as go
custom_config = {'displaylogo':False}
yf.pdr_override() #to activate yahoo finace workload
# # Configure the logging settings
# logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
# yf.pdr_override()

def backtesting_home(request):
    return render(request, 'backtesting_home.html')

def is_valid_ticker(ticker):
    try:
        stock_info = yf.Ticker(ticker)
        return bool(stock_info.info)
    except:
        return False
def is_valid_date(date):
     try:
          date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
          return True
     except:
          return False

def emas_function(**kwargs):
        stock=kwargs['stock']
        startdate=kwargs['startdate']
        endtime=kwargs['endtime']
        short_term_emas=kwargs['short_term_emas']
        long_term_emas=kwargs['long_term_emas']
        pos = 0 #o for close and 1 for open
        percentagechange = []
        row_num=0 #to keep track of row
        df = pdr.get_data_yahoo(stock, startdate, endtime)
        # Calculate EMAs and create columns for them
        plot_data_row=[]
        plot_data_all=[]
        for short_ema in short_term_emas:
            df[f'Ema_{short_ema}'] = df['Adj Close'].ewm(span=short_ema, adjust=False).mean()
        for long_ema in long_term_emas:
            df[f'Ema_{long_ema}'] = df['Adj Close'].ewm(span=long_ema, adjust=False).mean()
        df = df.iloc[max(long_term_emas):]
        for i in df.index:
            row_num+=1 
            close = df['Adj Close'][i]
            cmin = min([df[f'Ema_{short_ema}'][i] for short_ema in short_term_emas])
            cmax = max([df[f'Ema_{long_ema}'][i] for long_ema in long_term_emas])
            plot_data_row=[i,close,cmin,cmax]
            plot_data_all.append(plot_data_row)
            
            if cmin > cmax and pos == 0:  # Buying condition
                bp = close
                pos = 1
            elif cmin < cmax and pos == 1:  # Selling condition
                sp = close
                pos = 0
                pc = ((sp / bp) - 1) * 100
                percentagechange.append(pc)
            if row_num==df['Adj Close'].iloc[-1] and pos==1: #i.e open position on last entry of dataframe, we sell it
                sp=close
                pos=0
                # print('last position')
                pc=((sp-bp)-1)*100
                percentagechange.append(pc)
        #  trade statistics
        ng = len([pc for pc in percentagechange if pc > 0])
        nl = len([pc for pc in percentagechange if pc < 0])
        if ng > 0:
            avgGain = sum([pc for pc in percentagechange if pc > 0]) / ng
            maxR = max(percentagechange)
        else:
            avgGain = 0
            maxR = "N/A"
        if nl > 0:
            avgLosses = sum([pc for pc in percentagechange if pc < 0]) / nl
            maxL = min(percentagechange)
            ratio = abs(avgGain / avgLosses)
        else:
            avgLosses = 0
            maxL = "N/A"
            ratio = "N/A"
        totalR = round((np.prod([(pc / 100) + 1 for pc in percentagechange]) - 1) * 100, 2)
        battingAvg = ng / (ng + nl) if ng + nl > 0 else 0
        all_data={'ng':ng,'nl':nl,'battingAvg':battingAvg,'ratio':ratio,'avgGain':avgGain,'avgLosses':avgLosses,'maxR':maxR,'maxL':maxL,'totalR':totalR,'plot_data':plot_data_all}
        return all_data

# Define the function mapping 
function_mapping = {

                    'emas_function':emas_function,
                    # Add other function names and corresponding functions here
                }

#timeout function
timeout = 30 # Timeout in seconds 
timeout_error = "Computation time limit exceeded"
def run_with_timeout(all_info_data, **kwargs):
    try:
        function_name=kwargs['function_name']
        function=function_mapping.get(function_name)
        all_info = function(**kwargs)
        all_info_data.update(all_info)
    except Exception as e:
        all_info_data['input_error'].append(str(e))

def emas_method(request):
    context={'stock_input':'Enter stock ticker,( eg: for apple , enter AAPL); see symbols here: https://finance.yahoo.com/lookup/',
             'startdate':'Enter date in format: YYYY-MM-DD .',
             'short_term':'Enter short term EMAs separted by , or backspace (eg: 3 5, 8 10, 12 15)',
             'long_term':'Enter long term EMAs separted by , or backspace (eg: 30 35 40, 45 50 60)',
             'topic_name':"Backtestings",
             'method_name':'EMAs analysis',
             'title':'Backtestings',
             }
    function_name='emas_function'
    try:
            if request.method == 'POST':
                stock = request.POST.get('stock_input')
                endtime = dt.datetime.now()
                short_term_emas = re.findall(r'\d+',request.POST.get('short_term') )
                short_term_emas = [int(x) for x in short_term_emas]
                long_term_emas = re.findall(r'\d+', request.POST.get('long_term'))
                long_term_emas = [int(x) for x in long_term_emas]
                startdate = request.POST.get('startdate')
                if not is_valid_date(startdate) or not is_valid_ticker(stock):
                    context['input_error'] = "Invalid date format(Please use YYYY-MM-DD.) or invalid ticker symbol.or |Try to reload home page.| "
                    return render(request, 'backtesting_input_output.html', context)
                kwargs={'stock':stock,'startdate':startdate,'endtime':endtime,'short_term_emas':short_term_emas,'long_term_emas':long_term_emas,'function_name':function_name }
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
                        #print(data['battingAvg'],3543)
                        plot_data=data['plot_data']
                        round_off=7
                        date=[value[0] for value in plot_data]
                        close_value=[value[1] for value in plot_data]
                        ema_short_value=[value[2] for value in plot_data]
                        ema_long_value=[value[3] for value in plot_data]
                        fig=go.Figure()
                        fig.add_trace(go.Scatter(x=date,y=close_value,mode='lines',name='closing price'))
                        fig.add_trace(go.Scatter(x=date,y=ema_short_value,mode='lines',name='short term emas'))
                        fig.add_trace(go.Scatter(x=date,y=ema_long_value,mode='lines',name='long term emas'))
                        fig=fig.to_html(full_html=False,config=custom_config)
                        context_plot={'plot':fig}
                        context_result = {
                            'result':f"Results for {stock} from {startdate} to {endtime}, with sample size of {data['ng']+data['nl']} is:",
                            'enddate': str(endtime),
                       'emasUsed': f"EMAs used: short terms= {[*short_term_emas]} and long terms= {[*long_term_emas]}",
                            'batting_avg': f"Batting Avg  : {data['battingAvg']}",
                            'gain_loss_ratio':f"Gain/loss ratio: {data['ratio']}" ,
                            'avg_gain': f"Average Gain: {data['avgGain']}" ,
                            'avg_loss':f"Average Loss:{data['avgLosses']} " ,
                            'max_gain':f"Max Returns: {data['maxR']} " ,
                            'max_loss':f"Max loss: {data['maxL']}" ,
                            'total_return':f"Total returns over {data['ng']+data['nl']} executed trades is : {data['totalR']} %" 
                        }
                        context={**context,**context_result,**context_plot}
                    return render(request, 'backtesting_input_output.html', context )              

    except Exception as e:
            context['input_error']=str(e) +' '+ str('(There might be some error with stock ticker symbol or date entered.)')
            return render(request, 'backtesting_input_output.html',context)
    

    # x_series1 = [1, 2, 3, 4, 5]
    # y_values = [10, 20, 15, 25, 30]

    # x_series2 = [2, 4, 6, 8, 10]
    
    # x_series3 = [1, 3, 5, 7, 9]

    # fig = go.Figure()

    # # Adding the first series
    # fig.add_trace(go.Scatter(x=x_series1, y=y_values, mode='lines', name='Series 1'))

    # # Adding the second series
    # fig.add_trace(go.Scatter(x=x_series2, y=y_values, mode='lines', name='Series 2'))

    # # Adding the third series
    # fig.add_trace(go.Scatter(x=x_series3, y=y_values, mode='lines', name='Series 3'))

    # plot_div = fig.to_html(full_html=False,config=custom_config)
    # context_g = {
    #     'plot_div': plot_div,
    # }
    # context={**context_g,**context}

    return render(request, 'backtesting_input_output.html',context)

