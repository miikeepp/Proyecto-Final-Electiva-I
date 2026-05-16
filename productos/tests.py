from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import ProductoForm
from .models import Categoria, Producto, Proveedor


class ProductoFormTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Papeleria')
        self.proveedor = Proveedor.objects.create(nombre='Proveedor Uno', nit='9001')

    def test_producto_valida_precio_venta_mayor_o_igual_a_compra(self):
        form = ProductoForm(data={
            'codigo': 'P001',
            'nombre': 'Cuaderno',
            'descripcion': '',
            'categoria': self.categoria.pk,
            'proveedor': self.proveedor.pk,
            'precio_compra': '10000',
            'precio_venta': '9000',
            'stock': 10,
            'stock_minimo': 5,
            'activo': 'on',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('precio_venta', form.errors)

    def test_producto_valida_codigo_duplicado(self):
        Producto.objects.create(
            codigo='P001',
            nombre='Cuaderno',
            categoria=self.categoria,
            proveedor=self.proveedor,
            precio_compra='10000',
            precio_venta='12000',
            stock=10,
        )
        form = ProductoForm(data={
            'codigo': 'P001',
            'nombre': 'Lapiz',
            'descripcion': '',
            'categoria': self.categoria.pk,
            'proveedor': self.proveedor.pk,
            'precio_compra': '1000',
            'precio_venta': '1500',
            'stock': 10,
            'stock_minimo': 5,
            'activo': 'on',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('codigo', form.errors)


class ProductoViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='diego', password='test12345')
        self.categoria = Categoria.objects.create(nombre='Tecnologia')
        self.proveedor = Proveedor.objects.create(nombre='Proveedor Dos', nit='9002')
        self.producto = Producto.objects.create(
            codigo='T001',
            nombre='Mouse',
            categoria=self.categoria,
            proveedor=self.proveedor,
            precio_compra='20000',
            precio_venta='25000',
            stock=2,
            stock_minimo=5,
        )
        self.client.force_login(self.user)

    def test_listado_productos_permite_buscar_filtrar_y_muestra_stock_bajo(self):
        response = self.client.get(reverse('productos:producto_list'), {
            'q': 'Mouse',
            'categoria': self.categoria.pk,
            'proveedor': self.proveedor.pk,
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'T001')
        self.assertContains(response, 'Stock bajo')

    def test_desactivar_producto(self):
        response = self.client.post(reverse('productos:producto_delete', args=[self.producto.pk]))
        self.producto.refresh_from_db()

        self.assertRedirects(response, reverse('productos:producto_list'))
        self.assertFalse(self.producto.activo)
