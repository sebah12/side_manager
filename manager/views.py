from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Marca, Item
from .forms import NewMarcaForm, NewProductForm
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator


def home(request):
    return HttpResponse('Hello, World!')


@login_required
def manager(request):
    return render(request, 'manager.html', {'manager': manager})


@login_required
def marcas(request):
    marcas = Marca.objects.all().order_by('nombre')
    return render(request, 'marcas.html', {'marcas': marcas})


@login_required
def marca(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    return render(request, 'marca.html', {'marca': marca})


@login_required
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


@login_required
def productos(request):
    items = Item.objects.all().order_by('item_id')
    return render(request, 'items.html', {'productos': items})


@login_required
def new_item(request):
    if request.method == 'POST':
        form = NewProductForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            # marca = Marca.objects.get(nombre=producto.marca)
            producto.descripcion = producto.descripcion.upper()
            producto.save()
            return redirect('productos')
    else:
        form = NewProductForm()
    return render(request, 'new_item.html', {
        'new_item': new_item, 'form': form})


@method_decorator(login_required, name='dispatch')
class MarcaUpdateView(UpdateView):
    model = Marca
    fields = ('nombre', )
    template_name = 'edit_marca.html'
    pk_url_kwarg = 'marca_id'
    context_object_name = 'marca'

    def form_valid(self, form):
        marca = form.save(commit=False)
        marca.nombre = marca.nombre.upper()
        marca.save()
        return redirect('marcas')


@method_decorator(login_required, name='dispatch')
class ItemUpdateView(UpdateView):
    model = Item
    fields = ('descripcion', 'marca', 'barcode',)
    template_name = 'edit_item.html'
    pk_url_kwarg = 'item_id'
    context_object_name = 'items'

    def form_valid(self, form):
        producto = form.save(commit=False)
        producto.descripcion = producto.descripcion.upper()
        producto.save()
        return redirect('productos')
