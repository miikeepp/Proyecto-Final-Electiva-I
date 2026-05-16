from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from productos.models import Producto
from compras.models import MovimientoInventario


class Venta(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    cliente = models.CharField(max_length=150, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'

    @property
    def total(self):
        return sum(detalle.subtotal for detalle in self.detalles.all())

    def __str__(self):
        return f'Venta #{self.id} - {self.cliente or "Cliente general"}'


class DetalleVenta(models.Model):
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalles'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='detalles_venta'
    )
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'detalle de venta'
        verbose_name_plural = 'detalles de venta'

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def clean(self):
        if self.producto and self.cantidad:
            if self.producto.stock < self.cantidad:
                raise ValidationError(
                    f'No hay stock suficiente. Stock disponible: {self.producto.stock}'
                )

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None

        if es_nuevo and self.producto.stock < self.cantidad:
            raise ValidationError(
                f'No hay stock suficiente. Stock disponible: {self.producto.stock}'
            )

        super().save(*args, **kwargs)

        if es_nuevo:
            self.producto.stock -= self.cantidad
            self.producto.save()

            MovimientoInventario.objects.create(
                producto=self.producto,
                tipo='SALIDA',
                cantidad=self.cantidad,
                descripcion=f'Salida por venta #{self.venta.id}'
            )

    def __str__(self):
        return f'{self.producto.nombre} x {self.cantidad}'


