from prediccion.models import Servicio, RegistroVenta

def populate_producto():
    ventas = RegistroVenta.objects.all()

    servicios = [i.producto for i in Servicio.objects.all()]

    for i in ventas:
        if not i.tipo in servicios:
            servicios.append(i.tipo)
    
    for i in servicios:
        if i!=None:
            Servicio.objects.create(servicio=i)

populate_producto()