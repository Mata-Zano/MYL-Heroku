from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from administradorApp.models import Cuenta

class LoginForm(forms.Form):
   correo = forms.EmailField(label='Correo electrónico')
   password = forms.CharField(label='Contraseña')

