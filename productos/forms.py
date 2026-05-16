from django import forms
from django.db.models import Q

from .models import Categoria, Producto, Proveedor


class BootstrapModelForm(forms.ModelForm):
    checkbox_fields = {'activo'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.checkbox_fields:
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})


class CategoriaForm(BootstrapModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre'].strip()
        queryset = Categoria.objects.filter(nombre__iexact=nombre)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError('Ya existe una categoria con este nombre.')
        return nombre


class ProveedorForm(BootstrapModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'nit', 'telefono', 'correo', 'direccion', 'contacto', 'activo']

    def clean_nombre(self):
        return self.cleaned_data['nombre'].strip()

    def clean_nit(self):
        nit = self.cleaned_data.get('nit')
        if not nit:
            return None
        nit = nit.strip()
        queryset = Proveedor.objects.filter(nit__iexact=nit)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError('Ya existe un proveedor con este NIT.')
        return nit


class ProductoForm(BootstrapModelForm):
    class Meta:
        model = Producto
        fields = [
            'codigo',
            'nombre',
            'descripcion',
            'categoria',
            'proveedor',
            'precio_compra',
            'precio_venta',
            'stock',
            'stock_minimo',
            'activo',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categoria_queryset = Categoria.objects.filter(activo=True)
        proveedor_queryset = Proveedor.objects.filter(activo=True)

        if self.instance.pk:
            categoria_queryset = Categoria.objects.filter(
                Q(activo=True) | Q(pk=self.instance.categoria_id)
            )
            proveedor_queryset = Proveedor.objects.filter(
                Q(activo=True) | Q(pk=self.instance.proveedor_id)
            )

        self.fields['categoria'].queryset = categoria_queryset
        self.fields['proveedor'].queryset = proveedor_queryset

        for field_name in ['precio_compra', 'precio_venta', 'stock', 'stock_minimo']:
            self.fields[field_name].widget.attrs.update({'min': '0'})

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo'].strip()
        queryset = Producto.objects.filter(codigo__iexact=codigo)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError('Ya existe un producto con este codigo.')
        return codigo

    def clean_nombre(self):
        return self.cleaned_data['nombre'].strip()

    def clean_precio_compra(self):
        precio_compra = self.cleaned_data['precio_compra']
        if precio_compra < 0:
            raise forms.ValidationError('El precio de compra no puede ser negativo.')
        return precio_compra

    def clean_precio_venta(self):
        precio_venta = self.cleaned_data['precio_venta']
        if precio_venta < 0:
            raise forms.ValidationError('El precio de venta no puede ser negativo.')
        return precio_venta

    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock < 0:
            raise forms.ValidationError('El stock no puede ser negativo.')
        return stock

    def clean_stock_minimo(self):
        stock_minimo = self.cleaned_data['stock_minimo']
        if stock_minimo < 0:
            raise forms.ValidationError('El stock minimo no puede ser negativo.')
        return stock_minimo

    def clean(self):
        cleaned_data = super().clean()
        precio_compra = cleaned_data.get('precio_compra')
        precio_venta = cleaned_data.get('precio_venta')
        if precio_compra is not None and precio_venta is not None and precio_venta < precio_compra:
            self.add_error(
                'precio_venta',
                'El precio de venta debe ser mayor o igual al precio de compra.',
            )
        return cleaned_data
