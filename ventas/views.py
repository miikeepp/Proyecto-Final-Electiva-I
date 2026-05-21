from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from productos.models import Producto
from usuarios.decorators import administrador_u_operador

from .models import Venta, DetalleVenta


def formato_pesos(valor):
    return f"${valor:,.0f}".replace(",", ".")


def obtener_valor(valor):
    return valor() if callable(valor) else valor


@login_required
@administrador_u_operador
def lista_ventas(request):
    ventas = Venta.objects.select_related("usuario").all()
    return render(request, "ventas/lista_ventas.html", {
        "ventas": ventas
    })


@login_required
@administrador_u_operador
def crear_venta(request):
    productos = Producto.objects.filter(activo=True).order_by("nombre")

    if request.method == "POST":
        cliente = request.POST.get("cliente", "")
        producto_id = request.POST.get("producto")
        cantidad = request.POST.get("cantidad")
        precio_unitario = request.POST.get("precio_unitario")
        observacion = request.POST.get("observacion", "")

        if not producto_id or not cantidad or not precio_unitario:
            messages.error(request, "Todos los campos obligatorios deben estar completos.")
            return redirect("ventas:crear_venta")

        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, "La cantidad debe ser mayor a cero.")
            return redirect("ventas:crear_venta")

        producto = get_object_or_404(Producto, id=producto_id)

        if producto.stock < cantidad:
            messages.error(request, f"No hay stock suficiente. Stock disponible: {producto.stock}")
            return redirect("ventas:crear_venta")

        try:
            with transaction.atomic():
                venta = Venta.objects.create(
                    usuario=request.user,
                    cliente=cliente,
                    observacion=observacion
                )

                DetalleVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario
                )

            messages.success(request, "Venta registrada correctamente. El stock fue actualizado.")
            return redirect("ventas:detalle_venta", pk=venta.pk)

        except ValidationError as error:
            messages.error(request, error.message)
            return redirect("ventas:crear_venta")

    return render(request, "ventas/crear_venta.html", {
        "productos": productos
    })


@login_required
@administrador_u_operador
def detalle_venta(request, pk):
    venta = get_object_or_404(
        Venta.objects.select_related("usuario"),
        pk=pk
    )

    return render(request, "ventas/detalle_venta.html", {
        "venta": venta
    })


@login_required
@administrador_u_operador
def factura_venta_pdf(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="factura_venta_{venta.id}.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    y = height - 50

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "Factura de venta")

    y -= 35
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Factura No: {venta.id}")

    y -= 18
    pdf.drawString(50, y, f"Cliente: {venta.cliente or 'Cliente general'}")

    y -= 18
    pdf.drawString(50, y, f"Fecha: {venta.fecha.strftime('%d/%m/%Y %H:%M')}")

    y -= 18
    if venta.usuario:
        pdf.drawString(50, y, f"Atendido por: {venta.usuario.username}")
    else:
        pdf.drawString(50, y, "Atendido por: No registrado")

    y -= 35
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(50, y, "Producto")
    pdf.drawString(260, y, "Cantidad")
    pdf.drawString(340, y, "Precio")
    pdf.drawString(440, y, "Subtotal")

    y -= 10
    pdf.line(50, y, 550, y)
    y -= 20

    pdf.setFont("Helvetica", 10)

    for detalle in venta.detalles.all():
        subtotal = obtener_valor(detalle.subtotal)

        pdf.drawString(50, y, detalle.producto.nombre[:30])
        pdf.drawString(275, y, str(detalle.cantidad))
        pdf.drawString(340, y, formato_pesos(detalle.precio_unitario))
        pdf.drawString(440, y, formato_pesos(subtotal))

        y -= 20

        if y < 80:
            pdf.showPage()
            y = height - 50

    y -= 10
    pdf.line(50, y, 550, y)

    y -= 25
    total = obtener_valor(venta.total)

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(340, y, "Total:")
    pdf.drawString(440, y, formato_pesos(total))

    y -= 45
    pdf.setFont("Helvetica", 9)
    pdf.drawString(50, y, "Factura generada automaticamente por el Sistema de Gestion de Inventario.")

    pdf.showPage()
    pdf.save()

    return response
    