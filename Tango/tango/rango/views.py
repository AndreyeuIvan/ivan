from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse('Rango starts <a href="/ "> About </a>')

def hello(request):
    return HttpResponse('Rango Says: <a href="/about/"> Index </a> page.')