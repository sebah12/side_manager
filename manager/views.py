from django.http import HttpResponse
from django.shortcuts import render
from .models import Marca


def home(request):
    return HttpResponse('Hello, World!')


def marcas(request):
    marcas = Marca.objects.all()
    return render(request, 'marcas.html', {'marcas': marcas})
