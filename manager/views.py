from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
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


def new_marca(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        user = User.objects.first()
        # TODO: get the currently logged in user

        marca = Marca.objects.create(
            nombre=nombre,
        )

        return redirect('marcas')  # TODO: redirect to the created topic page

    return render(request, 'new_marca.html', {'new_marca': new_marca})


def productos(request):
    items = Item.objects.all()
    return render(request, 'items.html', {'productos': items})
