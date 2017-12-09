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

        return redirect('marcas')

    return render(request, 'new_marca.html', {'new_marca': new_marca})


def productos(request):
    items = Item.objects.all()
    return render(request, 'items.html', {'productos': items})


def new_item(request):
    if request.method == 'POST':
        item_id = request.POST['item_id']
        descripcion = request.POST['descripcion']
        marca = request.POST['marca']
        barcode = request.POST['barcode']
        user = User.objects.first()
        # TODO: get the currently logged in user

        item = Item.objects.create(
            item_id=item_id,
            descripcion=descripcion,
            marca=marca,
            barcode=barcode
        )

        return redirect('productos')

    return render(request, 'new_item.html', {'new_item': new_item})
