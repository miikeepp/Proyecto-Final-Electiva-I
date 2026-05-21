from django.urls import path
from . import views

app_name = "compras"

urlpatterns = [
    path("", views.lista_compras, name="lista_compras"),
    path("nueva/", views.crear_compra, name="crear_compra"),
    path("<int:pk>/", views.detalle_compra, name="detalle_compra"),
    path("movimientos/", views.lista_movimientos, name="lista_movimientos"),
]
