from django.shortcuts import render
from . import forms

def Index (request):
    return render(request, 'principalTemplates/index.html')
def Contacto (request):
    form = forms.mensajeContactanos()
    data={
        'titulo':'Contactos',
        'mail':'info@mlinfo@ml-distribuidora.com',
        'form': form
    }
    return render(request, 'principalTemplates/contacto.html',data)
def Catalogo (request):
    data={
        'titulo':'Catálogo'
    }
    return render(request, 'principalTemplates/catalogo.html',data)
def Sobre (request):
    data={
        'titulo':'Sobre Nosotros'
    }
    return render(request, 'principalTemplates/sobre.html',data)

# Create your views here.
