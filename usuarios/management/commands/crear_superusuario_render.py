import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Crea o actualiza un superusuario desde variables de entorno.'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    'Superusuario omitido: faltan DJANGO_SUPERUSER_USERNAME o DJANGO_SUPERUSER_PASSWORD.'
                )
            )
            return

        User = get_user_model()
        user, creado = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True,
            },
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        accion = 'creado' if creado else 'actualizado'
        self.stdout.write(
            self.style.SUCCESS(f'Superusuario {accion}: {username}')
        )
