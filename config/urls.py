from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Apps del sistema
    path('productos/', include('productos.urls')),
    path('compras/', include('compras.urls')),
    path('ventas/', include('ventas.urls')),
    path('reportes/', include('reportes.urls')), 
    

    # Usuarios / dashboard / login
    path('', include('usuarios.urls')),
]
