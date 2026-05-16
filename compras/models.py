from django.conf import settings
from django.db import models
from productos.models import Producto, Proveedor


class MovimientoInventario(models.Model):
    TIPO_MOVIMIENTO = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
    ]

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='movimientos'
    )
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'movimiento de inventario'
        verbose_name_plural = 'movimientos de inventario'

    def __str__(self):
        return f'{self.tipo} - {self.producto.nombre} - {self.cantidad}'


class Compra(models.Model):
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name='compras'
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    fecha = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'compra'
        verbose_name_plural = 'compras'

    @property
    def total(self):
        return sum(detalle.subtotal for detalle in self.detalles.all())

    def __str__(self):
        return f'Compra #{self.id} - {self.proveedor.nombre}'


class DetalleCompra(models.Model):
    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='detalles_compra'
    )
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'detalle de compra'
        verbose_name_plural = 'detalles de compra'

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None
        super().save(*args, **kwargs)

        if es_nuevo:
            self.producto.stock += self.cantidad
            self.producto.save()

            MovimientoInventario.objects.create(
                producto=self.producto,
                tipo='ENTRADA',
                cantidad=self.cantidad,
                descripcion=f'Entrada por compra #{self.compra.id}'
            )

    def __str__(self):
        return f'{self.producto.nombre} x {self.cantidad}' 
        

        