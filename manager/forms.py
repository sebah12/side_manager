from django import forms
from .models import Marca


class NewMarcaForm(forms.ModelForm):
    nombre = forms.CharField(
        max_length=30,
        required=True,
        help_text='Longitud máxima del texto 30 caracteres.')

    class Meta:
        model = Marca
        fields = ['nombre']
