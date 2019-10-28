from django.db import models

# Create your models here.

class Servicio(models.Model):
    servicio = models.CharField(max_length=50)


class RegistroVenta(models.Model):
    CLASIFICACION = (
        (i.servicio, i.servicio) for i in Servicio.objects.all()
    )
   
    fecha = models.DateField(auto_now=False, auto_now_add=False)
    empresa = models.CharField(max_length=50)
    ruc = models.CharField(max_length=11)
    precio = models.FloatField()
    tipo = models.CharField(max_length=50, choices=(CLASIFICACION))
    
class RedNeuronalResultados(models.Model):
    CLASIFICACION = (
        (i.servicio, i.servicio) for i in Servicio.objects.all().order_by('-id')
    )

    PERIODO = (
        ('DIAS', 'DIAS'),
        ('SEMANAS', 'SEMANAS'),
        ('MESES', 'MESES'),
    )


    clasificacion = models.CharField(max_length=50, choices=(CLASIFICACION))
    periodo = models.CharField(max_length=50, choices=(PERIODO))
    dam = models.FloatField( blank=True, null=True)
    pema = models.FloatField( blank=True, null=True)
    rmse = models.FloatField( blank=True, null=True)
    look_back = models.IntegerField()
    neuronas = models.IntegerField()
    epocas = models.IntegerField()
    eval_dir = models.TextField(blank=True, null=True)
    pred_dir = models.TextField(blank=True, null=True)
    dam_dir = models.TextField(blank=True, null=True)
    pema_dir = models.TextField(blank=True, null=True)
    rmse_dir = models.TextField(blank=True, null=True)
