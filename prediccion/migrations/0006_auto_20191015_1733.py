# Generated by Django 2.2.6 on 2019-10-15 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediccion', '0005_auto_20191013_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redneuronalresultados',
            name='periodo',
            field=models.CharField(blank=True, choices=[('DIAS', 'DIAS'), ('SEMANAS', 'SEMANAS'), ('MESES', 'MESES')], max_length=50, null=True),
        ),
    ]
