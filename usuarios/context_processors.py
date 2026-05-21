from .utils import es_administrador, es_operador, obtener_rol_usuario


def roles_usuario(request):
    user = getattr(request, 'user', None)

    if not user or not user.is_authenticated:
        return {}

    return {
        'es_administrador': es_administrador(user),
        'es_operador': es_operador(user),
        'rol_usuario': obtener_rol_usuario(user),
    }
