"""ventas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import (
                    VentasPronostico, 
                    RegistroVentaView, 
                    PronosticoCompra, 
                    PronosticoGeneral, 
                    ErrorPronostico,
                    EntrenarRedView,
                    ProductoView,
                    ProductoUpdateView,
                    ProductosView,
                    ProductoDeleteView,
                    VentasView,
                    VentaUpdateView,
                    VentaDeleteView,
                    RedesView)

urlpatterns = [
    path('ventas_pronostico/<str:periodo>/', VentasPronostico.as_view(), name='productos_ventas_pronostico'),
    path('registro_venta', RegistroVentaView.as_view(), name='productos_registro_venta'),
    path('pronostico_compra/<str:periodo>/', PronosticoCompra.as_view(), name='productos_pronostico_compra'),
    path('error_pronostico/<str:periodo>/', ErrorPronostico.as_view(), name='productos_error_pronostico'),
    path('Producto', ProductoView.as_view(), name='productos_Producto'),
    path('Producto_update/<int:pk>', ProductoUpdateView.as_view(), name='productos_Producto_update'),
    path('Producto_delete/<int:pk>', ProductoDeleteView.as_view(), name='productos_Producto_delete'),
    path('Productos', ProductosView.as_view(), name='productos_Productos'),
    path('venta_update/<int:pk>', VentaUpdateView.as_view(), name='productos_venta_update'),
    path('venta_delete/<int:pk>', VentaDeleteView.as_view(), name='productos_venta_delete'),
    path('ventas', VentasView.as_view(), name='productos_ventas'),
    path('redes', RedesView.as_view(), name='productos_redes'),

    #Red neuronal
    path('entrenar_red/', EntrenarRedView.as_view(), name='productos_entrenar_red'),
]
