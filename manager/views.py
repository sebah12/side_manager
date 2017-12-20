from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Marca, Item, Remito, CampoRemito, ItemLogs
from .forms import NewMarcaForm, NewProductForm, EditStockForm, NewRemitoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views.generic import UpdateView, DeleteView, ListView, RedirectView
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
import qrcode
import datetime
from .my_functions import get_stats
from side_project import settings

server = settings.server
qr_dir1 = 'http://zxing.appspot.com/scan?ret=http%3A%2F%2F' + server
if settings.DEBUG:
    qr_dir1 = qr_dir1 + ':8000'
qr_dir2 = '%2F?barcode%3D%7BCODE%7D&%2F&SCAN_FORMATS=UPC_A,EAN_13'


def home(request):
    # qr = qrcode.make('http://' + server + '/manager')
    # response = HttpResponse(content_type="image/png")
    # qr.save(response)
    return render(request, 'googlechart.html')


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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProductoListView, self).get_context_data(**kwargs)
        context['qrdir'] = qr_dir1 + '%2Fproductos' + qr_dir2
        return context

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


@method_decorator(login_required, name='dispatch')
class ProductoDetailListView(ListView):
    model = ItemLogs
    context_object_name = 'logs'
    template_name = 'item.html'
    ordering = '-created_at'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProductoDetailListView, self).get_context_data(
            **kwargs)
        item = Item.objects.get(item_id=self.kwargs['item_id'])
        context['item'] = item
        stats = get_stats(self.kwargs['item_id'])
        if stats[0][4]:
            promedio = (round(item.stock/(stats[0][4]/20)))
        else:
            promedio = 9999
        context['stats'] = stats
        context['prom'] = promedio
        return context

    def get_queryset(self):
        result = super(ProductoDetailListView, self).get_queryset()
        result = result.filter(item=self.kwargs['item_id'])
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
class MarcaUpdateView(UserPassesTestMixin, UpdateView):
    permission_denied_message = 'Permission Denied'
    model = Marca
    fields = ('nombre', )
    template_name = 'edit_marca.html'
    pk_url_kwarg = 'marca_id'
    context_object_name = 'marca'

    def test_func(self):
        # print("checking if user passes test....")
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('manager')

    def form_valid(self, form):
        marca = form.save(commit=False)
        marca.nombre = marca.nombre.upper()
        marca.save()
        return redirect('marcas')


@method_decorator(login_required, name='dispatch')
class MarcaDeleteView(UserPassesTestMixin, DeleteView):
    model = Marca
    fields = ('nombre', )
    template_name = 'delete_marca.html'
    pk_url_kwarg = 'marca_id'
    context_object_name = 'marca'

    def test_func(self):
        # print("checking if user passes test....")
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('manager')

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
class ItemUpdateView(UserPassesTestMixin, UpdateView):
    model = Item
    fields = ('descripcion', 'marca', 'barcode',)
    template_name = 'edit_item.html'
    pk_url_kwarg = 'item_id'
    context_object_name = 'producto'

    def test_func(self):
        # print("checking if user passes test....")
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('manager')

    def form_valid(self, form):
        producto = form.save(commit=False)
        producto.descripcion = producto.descripcion.upper()
        producto.save()
        return redirect('productos')


@method_decorator(login_required, name='dispatch')
class ItemDeleteView(UserPassesTestMixin, DeleteView):
    model = Item
    fields = ('item_id', )
    template_name = 'delete_item.html'
    pk_url_kwarg = 'item_id'
    context_object_name = 'producto'

    def test_func(self):
        # print("checking if user passes test....")
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('manager')

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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DepositoListView, self).get_context_data(**kwargs)
        context['qrdir'] = qr_dir1 + '%2Fdeposito' + qr_dir2
        return context

    def get_queryset(self):
        result = super(DepositoListView, self).get_queryset()
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
    log = ItemLogs()
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
                log.action = 1
            else:
                producto.stock -= amount
                log.action = 0
            log.cantidad = amount
            log.created_by = request.user
            log.created_at = datetime.datetime.now()
            log.item = producto
            producto.save()
            log.save()
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
            result = result.filter(notas__contains=keywords)

        return result


@login_required
def new_remito(request):
    if request.method == 'POST':
        form = NewRemitoForm(request.POST)
        if form.is_valid():
            remito = form.save(commit=False)
            remito.created_by = request.user
            remito.created_at = datetime.datetime.now()
            remito.save()
            return redirect('/remitos/%s-edit' % (remito.remito_id))
    else:
        form = NewRemitoForm()
    return render(request, 'new_remito.html', {
        'new_remito': new_remito, 'form': form})


def remito_qr(request, remito_id):
    remito = get_object_or_404(Remito, remito_id=remito_id)
    qr = qrcode.make('http://' + server + '/remitos/' +
                     str(remito.remito_id) + '-ver')
    response = HttpResponse(content_type="image/png")
    qr.save(response, "PNG")
    return response


@method_decorator(login_required, name='dispatch')
class RemitoNewFieldListView(ListView):
    model = Item
    context_object_name = 'productos'
    template_name = 'new_remito_field.html'
    ordering = '-item_id'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(RemitoNewFieldListView, self).get_context_data(
            **kwargs)
        context['remito_id'] = self.kwargs['remito_id']
        return context

    def get_queryset(self):
        result = super(RemitoNewFieldListView, self).get_queryset()
        result = result.filter(stock__gt=0)
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


@method_decorator(login_required, name='dispatch')
class RemitoEditListView(ListView):
    model = CampoRemito
    context_object_name = 'fields'
    template_name = 'edit_remito.html'
    ordering = 'item_id'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(RemitoEditListView, self).get_context_data(**kwargs)
        context['remito'] = Remito.objects.get(
            remito_id=self.kwargs['remito_id'])
        context['remito_id'] = self.kwargs['remito_id']
        context['action'] = self.kwargs['action']
        return context

    def get_queryset(self):
        result = super(RemitoEditListView, self).get_queryset()
        result = result.filter(remito_id=self.kwargs['remito_id'])
        return result


@method_decorator(login_required, name='dispatch')
class RemitoFieldRedirectView(RedirectView):
    def get(self, request, *args, **kwargs):
        remito = self.kwargs.get('remito_id')
        remito = Remito.objects.get(remito_id=remito)
        item = self.kwargs.get('item_id')
        value = 'cantidad_' + str(item)
        item = Item.objects.get(item_id=item)
        cantidad = request.GET[value]
        if item.stock > int(cantidad):
            item.stock -= int(cantidad)
        else:
            cantidad = item.stock
            item.stock = 0
        item.save()
        log = ItemLogs()
        log.cantidad = int(cantidad)
        log.created_by = request.user
        log.created_at = datetime.datetime.now()
        log.item = item
        log.action = 0
        log.save()
        campo_remito = CampoRemito()
        campo_remito.item = item
        campo_remito.remito = remito
        campo_remito.cantidad = int(cantidad)
        campo_remito.save()
        self.url = '/remitos/%s-edit' % (remito.remito_id)
        return super(RemitoFieldRedirectView, self).get(
            request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class RemitoRecepcionRedirectView(RedirectView):
    def get(self, request, *args, **kwargs):
        remito = self.kwargs.get('remito_id')
        remito = Remito.objects.get(remito_id=remito)
        if not remito.received_at:
            remito.received_by = self.request.user
            remito.received_at = datetime.datetime.now()
            remito.save()
        self.url = '/remitos/%s-ver' % (remito.remito_id)
        return super(RemitoRecepcionRedirectView, self).get(
            request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ItemLogsListView(ListView):
    model = ItemLogs
    context_object_name = 'logs'
    template_name = 'item_logs.html'
    ordering = '-created_at'
    paginate_by = 20

    def get_queryset(self):
        result = super(ItemLogsListView, self).get_queryset()
        # keywords = self.request.GET.get('nombre')
        # if keywords:
        #     keywords = keywords.upper()
        #     result = result.filter(nombre__contains=keywords)

        return result
