# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-14 15:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manager', '0007_auto_20171212_1953'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampoRemito',
            fields=[
                ('campo_remito_id', models.IntegerField(primary_key=True, serialize=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='manager.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Remito',
            fields=[
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('remito_id', models.IntegerField(primary_key=True, serialize=False)),
                ('notas', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('received_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remitos_preparados', to=settings.AUTH_USER_MODEL)),
                ('received_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remitos_recibidos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='camporemito',
            name='remito',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campos', to='manager.Remito'),
        ),
    ]
