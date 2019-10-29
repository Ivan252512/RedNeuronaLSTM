# Generated by Django 2.2.6 on 2019-10-28 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RedNeuronalResultados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clasificacion', models.TextField()),
                ('periodo', models.TextField(choices=[('DIAS', 'DIAS'), ('SEMANAS', 'SEMANAS'), ('MESES', 'MESES')])),
                ('dam', models.FloatField(blank=True, null=True)),
                ('pema', models.FloatField(blank=True, null=True)),
                ('rmse', models.FloatField(blank=True, null=True)),
                ('look_back', models.IntegerField()),
                ('neuronas', models.IntegerField()),
                ('epocas', models.IntegerField()),
                ('eval_dir', models.TextField(blank=True, null=True)),
                ('pred_dir', models.TextField(blank=True, null=True)),
                ('dam_dir', models.TextField(blank=True, null=True)),
                ('pema_dir', models.TextField(blank=True, null=True)),
                ('rmse_dir', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroVenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('empresa', models.TextField()),
                ('ruc', models.TextField()),
                ('precio', models.FloatField()),
                ('tipo', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servicio', models.TextField()),
            ],
        ),
    ]
