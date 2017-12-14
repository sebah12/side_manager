from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Marca, Item, Remito
from .forms import NewMarcaForm, NewProductForm, EditStockForm
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank,SearchVector
from django.views.generic import UpdateView, DeleteView, ListView, RedirectView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.core.urlresolvers import reverse
import qrcode

server = '192.168.1.106'

def home(request):
    qr = qrcode.make('http://' + server + '/productos')
    response = HttpResponse(content_type="image/png")
    
    qr.save(response)
    return response

@login_required
def manager(request):
    return render(request, 'manager.html', {'manager': manager})


@method_decorator(login_required, name='dispatch')
class SearchProductRedirectView(RedirectView):
    def get(self, request, *args, **kwargs):
        barcode = self.kwargs.get('item_barcode', None)
        item = Item.objects.get(barcode=barcode)
        self.url = '/productos/%s/edit' % (item.item_id)
        return super(SearchProductRedirectView, self).get(
            request, *args, **kwargs)


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

    def get_queryset(self):
        result = super(ProductoListView, self).get_queryset()
        kitem_id = self.request.GET.get('item_id')
        kbarcode = self.request.GET.get('barcode')
        kdescripcion = self.request.GET.get('descripcion')
        kmarca = self.request.GET.get('marca')
        if kitem_id:
            result = result.filter(item_id__contains=kitem_id)
        if kbarcode:
            result = result.filter(barcode=kbarcode)
        if kdescripcion:
            kdescripcion = kdescripcion.upper()
            result = result.filter(descripcion__contains=kdescripcion)
        if kmarca:
            kmarca = kmarca.upper()
            result = result.filter(marca__nombre__contains=kmarca)

        return (result)


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


@method_decorator(login_required, name='dispatch')
class DepositoListView(ListView):
    model = Item
    context_object_name = 'productos'
    template_name = 'deposito.html'
    ordering = '-stock'
    paginate_by = 10

    def get_queryset(self):
        result = super(DepositoListView, self).get_queryset()
        filter
        kitem_id = self.request.GET.get('item_id')
        kbarcode = self.request.GET.get('barcode')
        kdescripcion = self.request.GET.get('descripcion')
        kmarca = self.request.GET.get('marca')
        if kitem_id:
            result = result.filter(item_id__contains=kitem_id)
        if kbarcode:
            result = result.filter(barcode=kbarcode)
        if kdescripcion:
            kdescripcion = kdescripcion.upper()
            result = result.filter(descripcion__contains=kdescripcion)
        if kmarca:
            kmarca = kmarca.upper()
            result = result.filter(marca__nombre__contains=kmarca)

        return result


@login_required
def edit_stock(request, item_id, action):
    producto = get_object_or_404(Item, item_id=item_id)
    action = action
    if action == 'add':
        max_value = 2147483647 - producto.stock
    else:
        max_value = producto.stock
    if request.method == 'POST':
        form = EditStockForm(request.POST, max_value=max_value)
        # form.fields['cantidad'].max_value = 99
        # form.clean_cantidad(100)
        if form.is_valid():
            data = form.cleaned_data
            amount = data['cantidad']
            if action == 'add':
                producto.stock += amount
            else:
                producto.stock -= amount
            producto.save()
            return redirect('deposito')
    else:
        form = EditStockForm(max_value=max_value)
        # form.fields['cantidad'].validators = 99
    if action:
        return render(request, 'edit_stock.html', {'producto': producto,
                                                   'action': action,
                                                   'form': form})
    return render(request, 'edit_stock.html', {'producto': producto})


@method_decorator(login_required, name='dispatch')
class RemitoListView(ListView):
    model = Remito
    context_object_name = 'remitos'
    template_name = 'remitos.html'
    ordering = 'created_at'
    paginate_by = 10

    def get_queryset(self):
        result = super(RemitoListView, self).get_queryset()
        keywords = self.request.GET.get('notas')
        if keywords:
            keywords = keywords.upper()
            result = result.filter(notas__contains=keywords)

        return result
