# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-14 20:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('edificios', '0017_auto_20161205_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detalle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('valor', models.BigIntegerField()),
                ('tipo', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Recibo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.PositiveIntegerField()),
                ('descripcion', models.CharField(blank=True, max_length=120, null=True)),
                ('numConsecutivo', models.IntegerField()),
                ('fecha_generacion', models.DateTimeField(auto_now=True)),
                ('fecha_cobrada', models.DateTimeField()),
                ('unidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edificios.Unidad')),
            ],
            options={
                'verbose_name_plural': 'Recibos',
                'verbose_name': 'Recibo',
            },
        ),
        migrations.AddField(
            model_name='detalle',
            name='idRecibo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagos.Recibo'),
        ),
    ]
