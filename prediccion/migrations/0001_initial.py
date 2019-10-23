# Generated by Django 2.2.6 on 2019-10-13 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RegistroVenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_comprobante', models.IntegerField()),
                ('fecha', models.DateField()),
                ('empresa', models.CharField(max_length=50)),
                ('ruc', models.CharField(max_length=11)),
                ('precio', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='RegistroVentaProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_comprobante', models.IntegerField()),
                ('fecha', models.DateField()),
                ('empresa', models.CharField(max_length=50)),
                ('ruc', models.CharField(max_length=11)),
                ('producto', models.TextField()),
                ('cantidad', models.IntegerField()),
            ],
        ),
    ]
