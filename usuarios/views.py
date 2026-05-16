from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import RegistroUsuarioForm
from .utils import es_administrador, es_operador, obtener_rol_usuario


@login_required
def dashboard(request):
    usuario_es_admin = es_administrador(request.user)
    usuario_es_operador = es_operador(request.user)

    contexto = {
        'rol_usuario': obtener_rol_usuario(request.user),
        'es_administrador': usuario_es_admin,
        'es_operador': usuario_es_operador,
        'tarjetas': [
            {'titulo': 'Productos', 'valor': 0, 'color': 'primary'},
            {'titulo': 'Compras', 'valor': 0, 'color': 'success'},
            {'titulo': 'Ventas', 'valor': 0, 'color': 'info'},
            {'titulo': 'Bajo inventario', 'valor': 0, 'color': 'warning'},
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
