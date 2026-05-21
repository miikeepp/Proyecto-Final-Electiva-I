from django.urls import path
from . import views

app_name = "reportes"

urlpatterns = [
    path("", views.dashboard_reportes, name="dashboard_reportes"),
    path("excel/", views.exportar_reporte_excel, name="exportar_reporte_excel"),
] 
