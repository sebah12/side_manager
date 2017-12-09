from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Marca, Item


def home(request):
    return HttpResponse('Hello, World!')


def manager(request):
    return render(request, 'manager.html', {'manager': manager})


def marcas(request):
    marcas = Marca.objects.all()
    return render(request, 'marcas.html', {'marcas': marcas})


def marca(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    return render(request, 'marca.html', {'marca': marca})


def productos(request):
    items = Item.objects.all()
    return render(request, 'items.html', {'productos': items})
