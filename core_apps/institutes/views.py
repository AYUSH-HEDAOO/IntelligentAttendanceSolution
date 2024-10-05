from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages

# Create your views here.

def dashboard(request):
    return render(request,"institutes/dashboard.html")


