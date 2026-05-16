from django.contrib.auth.decorators import login_required

from django.shortcuts import render


def obtener_rol_usuario(user):
    if user.is_superuser or user.groups.filter(name='admin').exists():
        return 'Admin'
    if user.groups.filter(name='operador').exists():
        return 'Operador'
    return 'Sin rol asignado'


@login_required
def dashboard(request):
    contexto = {
        'rol_usuario': obtener_rol_usuario(request.user),
        'tarjetas': [
            {'titulo': 'Productos', 'valor': 0, 'color': 'primary'},
            {'titulo': 'Compras', 'valor': 0, 'color': 'success'},
            {'titulo': 'Ventas', 'valor': 0, 'color': 'info'},
            {'titulo': 'Bajo inventario', 'valor': 0, 'color': 'warning'},
        ],
    }
    return render(request, 'usuarios/dashboard.html', contexto)
