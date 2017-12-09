from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Marca, Item
from .forms import NewMarcaForm, NewProductForm


def home(request):
    return HttpResponse('Hello, World!')


def manager(request):
    return render(request, 'manager.html', {'manager': manager})


def marcas(request):
    marcas = Marca.objects.all().order_by('nombre')
    return render(request, 'marcas.html', {'marcas': marcas})


def marca(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    return render(request, 'marca.html', {'marca': marca})


def new_marca(request):
    if request.method == 'POST':
        form = NewMarcaForm(request.POST)
        if form.is_valid():
            marca = form.save(commit=False)
            marca.nombre = marca.nombre.upper()
            marca.save()
            return redirect('marcas')
    else:
        form = NewMarcaForm()
    return render(request, 'new_marca.html', {
        'new_marca': new_marca, 'form': form})


def productos(request):
    items = Item.objects.all().order_by('item_id')
    return render(request, 'items.html', {'productos': items})


def new_item(request):
    if request.method == 'POST':
        form = NewProductForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            # marca = Marca.objects.get(nombre=producto.marca)
            # producto.marca = marca
            producto.save()
            return redirect('productos')
    else:
        form = NewProductForm()
    return render(request, 'new_item.html', {
        'new_item': new_item, 'form': form})
