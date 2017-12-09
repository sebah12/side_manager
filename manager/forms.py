from django import forms
from .models import Marca


class NewMarcaForm(forms.ModelForm):
    nombre = forms.CharField(max_length=50)

    class Meta:
        model = Marca
        fields = ['nombre']
