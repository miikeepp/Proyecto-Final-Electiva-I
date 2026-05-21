from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from productos.models import Producto, Proveedor
from usuarios.decorators import administrador_u_operador

from .models import Compra, DetalleCompra, MovimientoInventario


@login_required
@administrador_u_operador
def lista_compras(request):
    compras = Compra.objects.select_related("proveedor", "usuario").all()
    return render(request, "compras/lista_compras.html", {
        "compras": compras
    })


@login_required
@administrador_u_operador
def crear_compra(request):
    productos = Producto.objects.filter(activo=True).order_by("nombre")
    proveedores = Proveedor.objects.filter(activo=True).order_by("nombre")

    if request.method == "POST":
        proveedor_id = request.POST.get("proveedor")
        producto_id = request.POST.get("producto")
        cantidad = request.POST.get("cantidad")
        precio_unitario = request.POST.get("precio_unitario")
        observacion = request.POST.get("observacion", "")

        if not proveedor_id or not producto_id or not cantidad or not precio_unitario:
            messages.error(request, "Todos los campos obligatorios deben estar completos.")
            return redirect("compras:crear_compra")

        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, "La cantidad debe ser mayor a cero.")
            return redirect("compras:crear_compra")

        proveedor = get_object_or_404(Proveedor, id=proveedor_id)
        producto = get_object_or_404(Producto, id=producto_id)

        with transaction.atomic():
            compra = Compra.objects.create(
                proveedor=proveedor,
                usuario=request.user,
                observacion=observacion
            )

            DetalleCompra.objects.create(
                compra=compra,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario
            )

        messages.success(request, "Compra registrada correctamente. El stock fue actualizado.")
        return redirect("compras:detalle_compra", pk=compra.pk)

    return render(request, "compras/crear_compra.html", {
        "productos": productos,
        "proveedores": proveedores
    })


@login_required
@administrador_u_operador
def detalle_compra(request, pk):
    compra = get_object_or_404(
        Compra.objects.select_related("proveedor", "usuario"),
        pk=pk
    )

    return render(request, "compras/detalle_compra.html", {
        "compra": compra
    })


@login_required
@administrador_u_operador
def lista_movimientos(request):
    movimientos = MovimientoInventario.objects.select_related("producto").all()
    return render(request, "compras/lista_movimientos.html", {
        "movimientos": movimientos
    })

