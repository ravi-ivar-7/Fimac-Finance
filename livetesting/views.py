import django
django.setup()
from django.shortcuts import render
from livetesting.live_nse_intraday import MCApi

from livetesting.forms import *
from data.getting_data import f_and_o_equity

# Create your views here.
def livetesting(request):
    return render(request, 'home_livetesting.html')






def get_f_o_data(request):
    obj=f_and_o_equity.index_data()
    res=obj.fetch_index_from_nse('NIFTY 50')

    return render(request, 'live_intraday.html',{'item':res})

def live_nse_intraday_data(request):
    if request.method=='POST':
        live_intraday_form=LiveIntradayForm()
        print('post ')
        if live_intraday_form.is_valid():
            print('form validity')
            symbol=live_intraday_form.changed_data['symbol']
            start_date=live_intraday_form.changed_data['start_date']
            end_date=live_intraday_form.changed_data['end_date']
            timeperiod=live_intraday_form.changed_data['timeperiod']
            response=MCApi(symbol,timeperiod,start_date,end_date)
            data=response.fetch_intraday_data()
            print(data)
            context={'live_intraday_form':live_intraday_form,'item':data}
    else:
        live_intraday_form=LiveIntradayForm() 
        data=None
    context={'live_intraday_form':live_intraday_form,}

    return render(request,'live_intraday.html',context)