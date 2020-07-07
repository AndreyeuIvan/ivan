from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    context = "I am bold font from the context"
    return render(request, 'rango/index.html', {'boldmessage': context})


def hello(request):
    return HttpResponse('Rango Says: <a href="/about/"> Index </a> page.')
