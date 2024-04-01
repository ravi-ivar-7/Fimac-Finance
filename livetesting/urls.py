
from django.urls import path
from livetesting import views

urlpatterns = [
    path('livetesting',views.livetesting,name='livetesting'),
    path('get_f_o_data',views.get_f_o_data,name='get_f_o_data'),
    path('live_nse_intraday_data',views.live_nse_intraday_data,name='live_nse_intraday_data'),
]