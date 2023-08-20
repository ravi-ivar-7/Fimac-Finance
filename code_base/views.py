from django.shortcuts import render,redirect
from django.contrib.auth import logout
from code_base.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def finance_home(request):
    return render(request,'finance_home.html',)

def commingsoon(request):
    return render(request,'commingsoon.html',)
