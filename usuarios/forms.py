from django.contrib.auth.forms import UserCreationForm

from .utils import asignar_rol_operador


class RegistroUsuarioForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            asignar_rol_operador(user)
        return user
