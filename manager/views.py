from django.http import HttpResponse
from django.shortcuts import render
from .models import Marca, Item


def home(request):
    return HttpResponse('Hello, World!')


def manager(request):
    return render(request, 'manager.html', {'manager': manager})


def marcas(request):
    marcas = Marca.objects.all()
    return render(request, 'marcas.html', {'marcas': marcas})


def productos(request):
    items = Item.objects.all()
    return render(request, 'items.html', {'productos': items})
