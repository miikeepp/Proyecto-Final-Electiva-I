from functools import wraps

from django.shortcuts import redirect, render

from .utils import es_administrador, es_operador


def usuario_con_permiso(test_func):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if not test_func(request.user):
                return render(request, '403.html', status=403)
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def solo_administrador(view_func):
    return usuario_con_permiso(es_administrador)(view_func)


def solo_operador(view_func):
    return usuario_con_permiso(es_operador)(view_func)


def administrador_u_operador(view_func):
    return usuario_con_permiso(lambda user: es_administrador(user) or es_operador(user))(view_func)
