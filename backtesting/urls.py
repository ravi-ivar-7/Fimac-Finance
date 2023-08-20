from django.contrib import admin
from django.urls import path
from backtesting import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('backtesting',views.backtesting_home,name='backtesting'),
    path('emas',views.emas,name='emas'),

]
