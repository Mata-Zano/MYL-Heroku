from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from administradorApp.models import Cuenta

def Ingreso(request):
   form = LoginForm()
   if request.method == 'POST':
       form = LoginForm(request.POST)
       if form.is_valid():
           correo = form.cleaned_data['correo']
           password = form.cleaned_data['password']
           try:
               cuenta = Cuenta.objects.get(correo = correo)
               if password == cuenta.password:
                  if cuenta.rol.id == 1:
                      return redirect('administrador')
                  elif cuenta.rol.id == 2:
                      return redirect('cliente')
                  elif cuenta.rol.id == 3:
                      return redirect('vendedor')
                  else:
                      return redirect('login')
               else:
                  messages.error(request, 'Los datos no son validos')
           except Cuenta.DoesNotExist:
               messages.error(request, 'La cuenta no existe')

           return render(request, 'loginTemplates/login.html', {'form': form})
   else:
       return render(request, 'loginTemplates/login.html', {'form': form})


def Recuperar (request):
    return render(request, 'loginTemplates/recuperar.html')


# Create your views here.
