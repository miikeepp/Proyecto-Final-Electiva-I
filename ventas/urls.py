from django.urls import path
from . import views

app_name = "ventas"

urlpatterns = [
    path("", views.lista_ventas, name="lista_ventas"),
    path("nueva/", views.crear_venta, name="crear_venta"),
    path("<int:pk>/", views.detalle_venta, name="detalle_venta"),
    path("factura/<int:venta_id>/pdf/", views.factura_venta_pdf, name="factura_pdf"),
] 