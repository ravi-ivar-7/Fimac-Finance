from django.contrib import admin
from django.urls import path
from backtesting import views
from backtesting import smas
#from backtesting import bhav
urlpatterns = [
    path('backtesting',views.backtesting_home,name='backtesting'),
    path('emas',views.emas_method,name='emas'),
    path('smas',smas.smas_method,name='smas'),

]
