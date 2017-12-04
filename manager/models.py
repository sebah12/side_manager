from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Marca(models.Model):
    marca_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre


class Item(models.Model):
    item_id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50, unique=True)
    marca = models.ForeignKey(Marca, related_name='items')
