from django import forms
from django.contrib.auth.forms import UserCreationForm

from .utils import asignar_rol_operador


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(
        label='Correo',
        required=True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            asignar_rol_operador(user)
        return user
