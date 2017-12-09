from django import forms
from .models import Marca, Item


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
    item_id = forms.NumberInput()
    descripcion = forms.CharField(
        max_length=50,
        required=True,
        help_text='Descripción del producto')
    marca = forms.TypedChoiceField(
        choices=get_my_choices())
    barcode = forms.NumberInput()
    marca = Marca.objects.get(marca_id=7)

    class Meta:
        model = Item
        fields = ['item_id', 'descripcion', 'marca', 'barcode']
