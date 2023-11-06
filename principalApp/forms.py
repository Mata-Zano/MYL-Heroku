from django import forms

class mensajeContactanos(forms.Form):
    nombre = forms.CharField()
    email = forms.EmailField()
    asunto = forms.CharField()
    mensaje = forms.CharField()