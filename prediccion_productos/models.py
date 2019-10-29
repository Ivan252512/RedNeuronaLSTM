from django.db import models

# Create your models here.

class Producto(models.Model):
    producto = models.TextField()


class RegistroVenta(models.Model):
    CLASIFICACION = (
        #(i.producto, i.producto) for i in Producto.objects.all()
    ) 
   
    fecha = models.DateField(auto_now=False, auto_now_add=False)
    empresa = models.TextField(blank=True, null=True)
    ruc = models.TextField(blank=True, null=True)
    precio = models.FloatField(blank=True, null=True)
    tipo = models.TextField(choices=(CLASIFICACION), blank=True, null=True)
    
class RedNeuronalResultados(models.Model):
    CLASIFICACION = (
        ("PRODUCTOS", "PRODUCTOS"),
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
