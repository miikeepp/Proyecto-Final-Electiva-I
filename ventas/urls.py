from django.urls import path
from . import views

app_name = "ventas"

urlpatterns = [
    path("factura/<int:venta_id>/pdf/", views.factura_venta_pdf, name="factura_pdf"),
]