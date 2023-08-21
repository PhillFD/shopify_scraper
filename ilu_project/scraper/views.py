from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "scraper/index.html")

def add(request):
    return(request, "scraper/add.html")
