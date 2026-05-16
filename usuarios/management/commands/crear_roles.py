from django.core.management.base import BaseCommand

from usuarios.utils import crear_grupos_y_permisos


class Command(BaseCommand):
    help = 'Crea los grupos Administrador y Operador con permisos base.'

    def handle(self, *args, **options):
        grupo_admin, grupo_operador = crear_grupos_y_permisos()

        self.stdout.write(
            self.style.SUCCESS(
                f'Grupos creados o actualizados: {grupo_admin.name}, {grupo_operador.name}'
            )
        )
