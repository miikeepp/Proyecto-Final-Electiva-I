from django.contrib import admin

from .models import Categoria, Producto, Proveedor


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('activo', 'fecha_creacion')


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nit', 'telefono', 'correo', 'activo')
    search_fields = ('nombre', 'nit', 'telefono', 'correo', 'contacto')
    list_filter = ('activo', 'fecha_creacion')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'nombre',
        'categoria',
        'proveedor',
        'precio_venta',
        'stock',
        'stock_minimo',
        'activo',
    )
    search_fields = ('codigo', 'nombre', 'descripcion')
    list_filter = ('activo', 'categoria', 'proveedor', 'fecha_creacion')
