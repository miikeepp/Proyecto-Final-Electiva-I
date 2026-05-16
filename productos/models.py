from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    nit = models.CharField(max_length=50, unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True)
    correo = models.EmailField(blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    contacto = models.CharField(max_length=120, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'proveedor'
        verbose_name_plural = 'proveedores'

    def clean(self):
        super().clean()
        if self.nit == '':
            self.nit = None

    def save(self, *args, **kwargs):
        if self.nit == '':
            self.nit = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='productos')
    precio_compra = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    precio_venta = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=5)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    @property
    def stock_bajo(self):
        return self.stock <= self.stock_minimo

    def clean(self):
        super().clean()
        if self.precio_compra is not None and self.precio_compra < 0:
            raise ValidationError({'precio_compra': 'El precio de compra no puede ser negativo.'})
        if self.precio_venta is not None and self.precio_venta < 0:
            raise ValidationError({'precio_venta': 'El precio de venta no puede ser negativo.'})
        if (
            self.precio_compra is not None
            and self.precio_venta is not None
            and self.precio_venta < self.precio_compra
        ):
            raise ValidationError({
                'precio_venta': 'El precio de venta debe ser mayor o igual al precio de compra.'
            })

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'
