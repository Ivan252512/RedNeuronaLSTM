from prediccion_productos.models import Producto, RegistroVenta

def populate_producto():
    ventas = RegistroVenta.objects.all()

    productos = [i.producto for i in Producto.objects.all()]

    for i in ventas:
        if not i.tipo in productos:
            productos.append(i.tipo)
    
    for i in productos:
        if i!=None:
            Producto.objects.create(producto=i)

populate_producto()