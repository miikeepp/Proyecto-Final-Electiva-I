from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .models import Venta


def formato_pesos(valor):
    return f"${valor:,.0f}".replace(",", ".")


def obtener_valor(valor):
    return valor() if callable(valor) else valor


@login_required
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
    pdf.drawString(50, y, "Factura generada automáticamente por el Sistema de Gestión de Inventario.")

    pdf.showPage()
    pdf.save()

    return response 
    