from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import redirect, render

from .forms import RegistroUsuarioForm
from .utils import es_administrador, es_operador, obtener_rol_usuario

from productos.models import Producto
from compras.models import Compra
from ventas.models import Venta


@login_required
def dashboard(request):
    usuario_es_admin = es_administrador(request.user)
    usuario_es_operador = es_operador(request.user)

    total_productos = Producto.objects.count()
    total_compras = Compra.objects.count()
    total_ventas = Venta.objects.count()

    bajo_inventario = Producto.objects.filter(
        stock__lte=F('stock_minimo')
    ).count()

    contexto = {
        'rol_usuario': obtener_rol_usuario(request.user),
        'es_administrador': usuario_es_admin,
        'es_operador': usuario_es_operador,
        'tarjetas': [
            {
                'titulo': 'Productos',
                'valor': total_productos,
                'color': 'primary'
            },
            {
                'titulo': 'Compras',
                'valor': total_compras,
                'color': 'success'
            },
            {
                'titulo': 'Ventas',
                'valor': total_ventas,
                'color': 'info'
            },
            {
                'titulo': 'Bajo inventario',
                'valor': bajo_inventario,
                'color': 'warning'
            },
        ],
    }

    return render(request, 'usuarios/dashboard.html', contexto)


def registro(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'usuarios/register.html', {'form': form}) 