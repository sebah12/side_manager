from django import forms
from .models import Marca, Item, Remito
from django.core.validators import ValidationError


class NewMarcaForm(forms.ModelForm):
    nombre = forms.CharField(
        max_length=30,
        required=True,
        help_text='Longitud máxima del texto 30 caracteres.')

    class Meta:
        model = Marca
        fields = ['nombre']


def getKey(item):
    return item[1]


def get_my_choices():
    choices_list = []
    for marca in Marca.objects.all():
        choices_list.append((marca.marca_id, marca.nombre))
        choices_list = sorted(choices_list, key=getKey)
    return choices_list


class NewProductForm(forms.ModelForm):
    descripcion = forms.CharField(
        max_length=50,
        required=True,
        help_text='Descripción del producto')
    marca = forms.TypedChoiceField(
        choices=get_my_choices())
    barcode = forms.NumberInput()
    precio = forms.NumberInput()
    marca = 1

    class Meta:
        model = Item
        fields = ['item_id', 'descripcion', 'marca', 'barcode', 'precio']


class EditStockForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.maximo = kwargs.pop('max_value')
        super(EditStockForm, self).__init__(*args, **kwargs)
        self.fields['cantidad'] = forms.IntegerField(required=True,
                                                     max_value=self.maximo,
                                                     min_value=1)

    cantidad = forms.IntegerField(required=True,
                                  min_value=1)


class NewRemitoForm(forms.ModelForm):
    notas = forms.CharField(
        max_length=200,
        required=True,
        help_text='Descripción del remito')
    
    class Meta:
        model = Remito
        fields = ['notas']    
