# Generated by Django 2.2.6 on 2019-10-26 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediccion', '0016_auto_20191026_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registroventaproducto',
            name='tipo',
            field=models.CharField(max_length=50),
        ),
    ]
