from django.shortcuts import render,redirect
from django.http import HttpResponse
import os

# Create your views here.
def home_page(request):
    if  request.method == "GET":
        return render(request, "Home_page/home.html", {})

