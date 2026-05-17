from django.contrib import admin
from .models import Compra, DetalleCompra, MovimientoInventario


class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    extra = 1


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'proveedor', 'fecha', 'usuario', 'total')
    list_filter = ('fecha', 'proveedor')
    search_fields = ('proveedor__nombre', 'observacion')
    inlines = [DetalleCompraInline]


@admin.register(DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'compra', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    list_filter = ('producto',)


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'tipo', 'cantidad', 'fecha', 'descripcion')
    list_filter = ('tipo', 'fecha')
    search_fields = ('producto__nombre', 'descripcion')

