# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-30 20:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('identificacion', models.CharField(max_length=30)),
                ('nombre', models.CharField(max_length=30)),
                ('apellido', models.CharField(max_length=30)),
                ('email', models.BigIntegerField()),
                ('celular', models.BigIntegerField()),
                ('telefono', models.CharField(blank=True, max_length=100, null=True, verbose_name='Teléfono')),
                ('tipo', models.IntegerField(choices=[(1, 'Natural'), (2, 'Juridica')], default=1)),
                ('administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Administrador')),
            ],
            options={
                'verbose_name_plural': 'Personas',
                'verbose_name': 'Persona',
            },
        ),
        migrations.CreateModel(
            name='Propiedad',
            fields=[
                ('idlegal', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True, verbose_name='iden')),
                ('nombre', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=50)),
                ('telefono', models.IntegerField()),
                ('area', models.IntegerField()),
                ('tipo', models.IntegerField(choices=[(1, 'Residencial'), (2, 'Comercial'), (3, 'Mixto')], default=1)),
                ('presupuesto_anual', models.IntegerField()),
                ('dia_cobro', models.IntegerField()),
                ('porcentaje_mora', models.FloatField()),
                ('Imagen', models.ImageField(blank=True, upload_to='Img/Propiedad/')),
                ('administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Administrador')),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Ciudad')),
            ],
            options={
                'verbose_name_plural': 'Propiedades',
                'verbose_name': 'Propiedad',
            },
        ),
        migrations.CreateModel(
            name='Unidad',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('torre', models.CharField(max_length=5)),
                ('numero', models.IntegerField()),
                ('estado', models.IntegerField(choices=[(1, 'Habitado'), (2, 'Deshabitado'), (3, 'En construccion')], default=1)),
                ('dia_cobro', models.IntegerField()),
                ('Responsable', models.IntegerField(choices=[(1, 'Residente'), (2, 'Propietario'), (3, 'Arrendatario')], default=2)),
                ('fecha_registro', models.DateField(auto_now_add=True)),
                ('forma_recibo', models.IntegerField(choices=[(1, 'Fisico'), (2, 'Email')], default=2)),
                ('saldo_favor', models.IntegerField()),
                ('porcentaje_mora', models.FloatField()),
                ('valor_mora', models.IntegerField()),
                ('coeficiente', models.FloatField()),
                ('valor_pago', models.IntegerField()),
                ('arrendatario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests_arrendatario', to='edificios.Persona')),
                ('propiedad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edificios.Propiedad')),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests_propietario', to='edificios.Persona')),
                ('residente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests_residente', to='edificios.Persona')),
            ],
            options={
                'verbose_name_plural': 'Unidades',
                'verbose_name': 'Unidad',
            },
        ),
    ]
