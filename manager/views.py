from django.http import HttpResponse
from .models import Marca


def home(request):
    return HttpResponse('Hello, World!')


def marcas(request):
    marcas = Marca.objects.all()
    nombres_marcas = list()

    for marca in marcas:
        nombres_marcas.append(marca.nombre)

    response_html = '<br>'.join(nombres_marcas)

    return HttpResponse(response_html)
