from django import forms
from django.forms import ModelForm, ModelChoiceField
from .models import Rol, Cuenta, Usuarios

class UsuariosForm(ModelForm):
    rol = ModelChoiceField(queryset=Rol.objects.all())
    nombre = forms.CharField(max_length=20)
    apellido = forms.CharField(max_length=20)
    telefono = forms.IntegerField()
    
    correo = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirmar_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuarios
        fields = ['rol', 'nombre', 'apellido', 'telefono', 'correo']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")

        if password and confirmar_password and password != confirmar_password:
            self.add_error('confirmar_password',"Las contraseñas no coinciden.")

        return cleaned_data

# class UsuariosForm(ModelForm):
#     rol = ModelChoiceField(queryset=Rol.objects.all())
#     correo = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)


#     class Meta:
#         model = Usuarios
#         fields = ['nombre', 'apellido', 'telefono']