from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoriaForm, ProductoForm, ProveedorForm
from .models import Categoria, Producto, Proveedor


@login_required
def categoria_list(request):
    categorias = Categoria.objects.all()
    buscar = request.GET.get('q', '').strip()
    if buscar:
        categorias = categorias.filter(
            Q(nombre__icontains=buscar) | Q(descripcion__icontains=buscar)
        )

    return render(request, 'productos/categoria_list.html', {
        'categorias': categorias,
        'buscar': buscar,
    })


@login_required
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria creada correctamente.')
            return redirect('productos:categoria_list')
    else:
        form = CategoriaForm()

    return render(request, 'productos/categoria_form.html', {
        'form': form,
        'titulo': 'Nueva categoria',
    })


@login_required
def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria actualizada correctamente.')
            return redirect('productos:categoria_list')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'productos/categoria_form.html', {
        'form': form,
        'titulo': 'Editar categoria',
        'categoria': categoria,
    })


@login_required
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.activo = False
        categoria.save(update_fields=['activo'])
        messages.success(request, 'Categoria desactivada correctamente.')
        return redirect('productos:categoria_list')

    return render(request, 'productos/categoria_confirm_delete.html', {
        'categoria': categoria,
    })


@login_required
def proveedor_list(request):
    proveedores = Proveedor.objects.all()
    buscar = request.GET.get('q', '').strip()
    if buscar:
        proveedores = proveedores.filter(
            Q(nombre__icontains=buscar)
            | Q(nit__icontains=buscar)
            | Q(telefono__icontains=buscar)
            | Q(correo__icontains=buscar)
            | Q(contacto__icontains=buscar)
        )

    return render(request, 'productos/proveedor_list.html', {
        'proveedores': proveedores,
        'buscar': buscar,
    })


@login_required
def proveedor_create(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor creado correctamente.')
            return redirect('productos:proveedor_list')
    else:
        form = ProveedorForm()

    return render(request, 'productos/proveedor_form.html', {
        'form': form,
        'titulo': 'Nuevo proveedor',
    })


@login_required
def proveedor_update(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado correctamente.')
            return redirect('productos:proveedor_list')
    else:
        form = ProveedorForm(instance=proveedor)

    return render(request, 'productos/proveedor_form.html', {
        'form': form,
        'titulo': 'Editar proveedor',
        'proveedor': proveedor,
    })


@login_required
def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.activo = False
        proveedor.save(update_fields=['activo'])
        messages.success(request, 'Proveedor desactivado correctamente.')
        return redirect('productos:proveedor_list')

    return render(request, 'productos/proveedor_confirm_delete.html', {
        'proveedor': proveedor,
    })


@login_required
def producto_list(request):
    productos = Producto.objects.select_related('categoria', 'proveedor')
    buscar = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '').strip()
    proveedor_id = request.GET.get('proveedor', '').strip()

    if buscar:
        productos = productos.filter(Q(nombre__icontains=buscar) | Q(codigo__icontains=buscar))
    if categoria_id.isdigit():
        productos = productos.filter(categoria_id=categoria_id)
    if proveedor_id.isdigit():
        productos = productos.filter(proveedor_id=proveedor_id)

    contexto = {
        'productos': productos,
        'categorias': Categoria.objects.all(),
        'proveedores': Proveedor.objects.all(),
        'buscar': buscar,
        'categoria_id': categoria_id,
        'proveedor_id': proveedor_id,
    }
    return render(request, 'productos/producto_list.html', contexto)


@login_required
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('productos:producto_detail', pk=producto.pk)
    else:
        form = ProductoForm()

    return render(request, 'productos/producto_form.html', {
        'form': form,
        'titulo': 'Nuevo producto',
    })


@login_required
def producto_detail(request, pk):
    producto = get_object_or_404(
        Producto.objects.select_related('categoria', 'proveedor'),
        pk=pk,
    )
    return render(request, 'productos/producto_detail.html', {
        'producto': producto,
    })


@login_required
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto = form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('productos:producto_detail', pk=producto.pk)
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'productos/producto_form.html', {
        'form': form,
        'titulo': 'Editar producto',
        'producto': producto,
    })


@login_required
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.activo = False
        producto.save(update_fields=['activo'])
        messages.success(request, 'Producto desactivado correctamente.')
        return redirect('productos:producto_list')

    return render(request, 'productos/producto_confirm_delete.html', {
        'producto': producto,
    })
