from django.db import models

# Create your models here.

class Servicio(models.Model):
    servicio = models.TextField()


class RegistroVenta(models.Model):
    CLASIFICACION = (
        #(i.servicio, i.servicio) for i in Servicio.objects.all()
    )
   
    fecha = models.DateField(auto_now=False, auto_now_add=False)
    empresa = models.TextField()
    ruc = models.TextField()
    precio = models.FloatField()
    tipo = models.TextField(choices=(CLASIFICACION))
    
class RedNeuronalResultados(models.Model):
    CLASIFICACION = (
        #(i.servicio, i.servicio) for i in Servicio.objects.all().order_by('-id')
    )

    PERIODO = (
        ('DIAS', 'DIAS'),
        ('SEMANAS', 'SEMANAS'),
        ('MESES', 'MESES'),
    )


    clasificacion = models.TextField(choices=(CLASIFICACION))
    periodo = models.TextField(choices=(PERIODO))
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