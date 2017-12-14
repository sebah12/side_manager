from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.utils import timezone


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(
            SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()


# Create your models here.


class Marca(SoftDeletionModel):
    marca_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.nombre


class Item(SoftDeletionModel):
    item_id = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=50)
    marca = models.ForeignKey(
        Marca, related_name='items', blank=True, null=True)
    barcode = models.BigIntegerField(unique=True, blank=True, null=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.descripcion


class Remito(SoftDeletionModel):
    remito_id = models.IntegerField(primary_key=True)
    notas = models.CharField(max_length=200)
    created_by = models.ForeignKey(
        User, related_name='remitos_preparados')
    received_by = models.ForeignKey(
        User, related_name='remitos_recibidos')
    created_at = models.DateTimeField(blank=True, null=True)
    received_at = models.DateTimeField(blank=True, null=True)


class CampoRemito(models.Model):
    campo_remito_id = models.IntegerField(primary_key=True)
    remito = models.ForeignKey(
        Remito, related_name='campos')
    item = models.ForeignKey(
        Item, related_name='+')
