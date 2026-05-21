from django.contrib.auth.models import Group, Permission


GRUPO_ADMINISTRADOR = 'Administrador'
GRUPO_OPERADOR = 'Operador'


def es_administrador(user):
    if not user.is_authenticated:
        return False
    return user.is_superuser or user.groups.filter(name=GRUPO_ADMINISTRADOR).exists()


def es_operador(user):
    if not user.is_authenticated:
        return False
    return user.groups.filter(name=GRUPO_OPERADOR).exists()


def obtener_rol_usuario(user):
    if es_administrador(user):
        return GRUPO_ADMINISTRADOR
    if es_operador(user):
        return GRUPO_OPERADOR
    return 'Sin rol asignado'


def asignar_rol_operador(user):
    grupo_operador, _ = Group.objects.get_or_create(name=GRUPO_OPERADOR)
    user.groups.add(grupo_operador)
    return user


def crear_grupos_y_permisos():
    grupo_admin, _ = Group.objects.get_or_create(name=GRUPO_ADMINISTRADOR)
    grupo_operador, _ = Group.objects.get_or_create(name=GRUPO_OPERADOR)

    permisos_admin = Permission.objects.filter(
        content_type__app_label='auth',
        content_type__model__in=['user', 'group'],
    )
    grupo_admin.permissions.set(permisos_admin)

    # Los permisos de inventario se agregaran aqui cuando existan sus modelos.
    grupo_operador.permissions.clear()

    grupos_anteriores = {
        'admin': grupo_admin,
        'operador': grupo_operador,
    }
    for nombre_anterior, grupo_nuevo in grupos_anteriores.items():
        try:
            grupo_anterior = Group.objects.get(name=nombre_anterior)
        except Group.DoesNotExist:
            continue

        for user in grupo_anterior.user_set.all():
            user.groups.add(grupo_nuevo)

    return grupo_admin, grupo_operador
