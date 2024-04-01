from django import forms
#'1':60,'3':180,'5':300,'15':900,'30':1800,'60':3600,'300':1800,'D':24*3600,'W':7*24*3600,'M':30*24*3600,'45':45*24*3600,'120':120*24*3600,'240':240*24*3600
# time_period_choices={'1':'1 Min','3':'3 Min','5':'5 Min','15':'15 Min','30':'30 Min','60':'1 Hour','300':'3 Hours'}
time_period_choices = [('1', '1 Min'),('3', '3 Min'),('5', '5 Min'),('15', '15 Min'),('30', '30 Min'),('60', '1 Hour'),('300', '3 Hours'),('D','1 Day'),('W','1 Week'),('M','1 Month'),('45','1.5 Months'),('120','3 Months'),('240','6 Months')]
class LiveIntradayForm(forms.Form):
    symbol=forms.CharField(max_length=50)
    start_date=forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}))
    end_date=forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}))
    time_period=forms.ChoiceField(choices=time_period_choices)