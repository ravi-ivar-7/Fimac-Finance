from django.contrib import admin
from django.urls import path,include
from code_base import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.finance_home,name='finance'),
    path('finance',views.finance_home,name='home'),
    path('commingsoon',views.commingsoon,name='commingsoon'),
]
