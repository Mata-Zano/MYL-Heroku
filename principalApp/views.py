from django.shortcuts import redirect, render
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages


from administradorApp.models import Producto
from .forms import mensajeContactanos

def Index (request):
    return render(request, 'principalTemplates/index.html')

def enviarEmail (request):
    if request.method == 'POST':
        form = mensajeContactanos(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            asunto = 'ContactoApp : '+form.cleaned_data['asunto']
            mensaje = form.cleaned_data['mensaje']

            template = render_to_string('principalTemplates/emailTemplate.html',{
                'name': nombre,
                'email':email,
                'message':mensaje
            })

            email =  EmailMessage(
                asunto,
                template,
                settings.EMAIL_HOST_USER,['distribuidoramylcalama@gmail.com']
            )
            email.fail_silently = False
            email.send()

            messages.success(request,'Se a enviado tu correo')
            return redirect('Contacto')

def Contacto(request):
    form = mensajeContactanos()
    data={
        'titulo':'Contactos',
        'mail':'distribuidoramylcalama@gmail.com',
        'form': form
    }
    return render(request, 'principalTemplates/contacto.html',data)

def Catalogo (request):
    producto = Producto.objects.all()
    data={
        'producto':producto,
        'titulo':'Catálogo'
    }
    return render(request, 'principalTemplates/catalogo.html',data)

def Sobre (request):
    data={
        'titulo':'Sobre Nosotros'
    }
    return render(request, 'principalTemplates/sobre.html',data)

# Create your views here.
