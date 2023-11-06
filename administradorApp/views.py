from django.shortcuts import render, redirect
from .models import Rol, Cuenta, Usuarios
from .forms import UsuariosForm
from django.contrib import messages
from django.db import IntegrityError
def indexAdministrador (request):
    return render(request, 'administradorAppTemplates/indexAdministrador.html')

def gestionVentas(request):
    return render(request, 'administradorAppTemplates/ventas.html')
def gestionUsuarios(request):
    return render(request, 'administradorAppTemplates/usuarios.html')
def perfilAdm(request):
    return render(request, 'administradorAppTemplates/perfil.html')

# Gestion de usuarios

def administrarCuentaAdm(request):
    usuarios = Usuarios.objects.all()
    if request.method == 'POST':
        ids = request.POST.getlist('usuario')
        if ids:
            Usuarios.objects.filter(id__in=ids).delete()
            messages.success(request, 'Usuarios eliminados exitosamente.')
            return render(request, 'administradorAppTemplates/administrarCuenta.html', {'usuarios': Usuarios.objects.all()})
    else:
        messages.error(request, 'Error al eliminar los usuarios.')
        return render(request, 'administradorAppTemplates/administrarCuenta.html', {'usuarios': Usuarios.objects.all()})
    return render(request, 'administradorAppTemplates/administrarCuenta.html', {'usuarios':usuarios})


def crearCuentaAdm(request):
    if request.method == 'POST':
        form = UsuariosForm(request.POST)
        if form.is_valid():
            try:
                correo = form.cleaned_data['correo']
                password = form.cleaned_data['password']
                rol = form.cleaned_data['rol']
                nombre = form.cleaned_data['nombre']
                apellido = form.cleaned_data['apellido']
                telefono = form.cleaned_data['telefono']
                cuenta = Cuenta.objects.create(rol=rol, correo=correo, password=password)
                Usuarios.objects.create(cuenta=cuenta, nombre=nombre, apellido=apellido, telefono=telefono)
                messages.success(request, 'Usuario creado exitosamente.')
                form = UsuariosForm()
                return render(request, 'administradorAppTemplates/crearCuenta.html',{'form':form})
            except IntegrityError:
                messages.error(request, 'El correo ya está en uso.')
                return render(request, 'administradorAppTemplates/crearCuenta.html',{'form':form})
        else:
            messages.error(request, 'Error al crear el usuario.')
            return render(request, 'administradorAppTemplates/crearCuenta.html',{'form':form})
    
    else:
        form = UsuariosForm()

        return render(request, 'administradorAppTemplates/crearCuenta.html',{'form':form})
    

def modificarUsuarios(request):
   if request.method == 'POST':
       ids = request.POST.getlist('usuario')
       if ids:
           usuarios = Usuarios.objects.filter(id__in=ids)
           if request.POST.get('action') == 'modificar':
               for usuario in usuarios:
                  form = UsuariosForm(request.POST, instance=usuario)
                  if form.is_valid():
                      form.save()
                      messages.success(request, 'Usuario modificado exitosamente.')
                  else:
                      messages.error(request, 'Error al modificar el usuario.')
               return redirect('usuariosAdm')
           return render(request, 'administradorAppTemplates/administrarCuenta.html', {'usuarios': Usuarios.objects.all()})
# Create your views here.
