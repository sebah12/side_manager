from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Marca, Item
from .forms import NewMarcaForm, NewProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank,SearchVector
from django.views.generic import UpdateView, DeleteView, ListView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


def home(request):
    return HttpResponse('Hello, World!')


@login_required
def manager(request):
    return render(request, 'manager.html', {'manager': manager})


@method_decorator(login_required, name='dispatch')
class MarcaListView(ListView):
    model = Marca
    context_object_name = 'marcas'
    template_name = 'marcas.html'
    ordering = 'nombre'
    paginate_by = 10

    def get_queryset(self):
        result = super(MarcaListView, self).get_queryset()
        keywords = self.request.GET.get('nombre')
        if keywords:
            keywords = keywords.upper()
            result = result.filter(nombre__contains=keywords)

        return result


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


@method_decorator(login_required, name='dispatch')
class ProductoListView(ListView):
    model = Item
    context_object_name = 'productos'
    template_name = 'items.html'
    ordering = 'item_id'
    paginate_by = 10


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
class MarcaDeleteView(DeleteView):
    model = Marca
    fields = ('nombre', )
    template_name = 'delete_marca.html'
    pk_url_kwarg = 'marca_id'
    context_object_name = 'marca'

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        marca = self.get_object()
        success_url = 'marcas'
        marca.delete()
        return HttpResponseRedirect(success_url)


@method_decorator(login_required, name='dispatch')
class ItemUpdateView(UpdateView):
    model = Item
    fields = ('descripcion', 'marca', 'barcode',)
    template_name = 'edit_item.html'
    pk_url_kwarg = 'item_id'
    context_object_name = 'producto'

    def form_valid(self, form):
        producto = form.save(commit=False)
        producto.descripcion = producto.descripcion.upper()
        producto.save()
        return redirect('productos')


@method_decorator(login_required, name='dispatch')
class ItemDeleteView(DeleteView):
    model = Item
    fields = ('item_id', )
    template_name = 'delete_item.html'
    pk_url_kwarg = 'item_id'
    context_object_name = 'producto'

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        producto = self.get_object()
        success_url = 'productos'
        producto.delete()
        return HttpResponseRedirect(success_url)
