from django.contrib import admin
from .models import Marca, Item, Remito, CampoRemito, ItemLogs, Precio

admin.site.register(Marca)
admin.site.register(Item)
admin.site.register(Remito)
admin.site.register(CampoRemito)
admin.site.register(ItemLogs)
admin.site.register(Precio)
