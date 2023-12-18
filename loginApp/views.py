from django.shortcuts import render, redirect
from loginApp.forms import LoginForm
from django.contrib.auth import authenticate, login
from administradorApp.models import Cuenta
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password


def Ingreso(request):
    message = None
    form = LoginForm()

    if 'form_message' in request.session:
        message = request.session['form_message']
        del request.session['form_message']
        data = {
            'error': message,
            'form': form
        }
        return render(request, 'loginTemplates/login.html', data)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            password = form.cleaned_data['password']
            hashp = make_password(password)

            try:
                cuenta = Cuenta.objects.get(correo = correo)
                comparacion = check_password(password, cuenta.password)
                if cuenta and comparacion:
                    request.session['usuario_id'] = cuenta.usuarios.id
                    rol = cuenta.rol.nombre.lower()
                    if rol == 'administrador':
                        return redirect('administrador')
                    elif rol == 'cliente':
                        return redirect('cliente')
                    elif rol == 'vendedor':
                        return redirect( 'vendedor')
                    elif rol == 'supervisor':
                        return redirect('supervisor')
                    else:
                        messages.error(request, 'Rol no reconocido.')

                else:
                    messages.error(request, 'La contraseña es inválida.')
                    return redirect ('login')

            except Cuenta.DoesNotExist:
                messages.error(request, 'La cuenta no existe.')

        else:
            messages.error(request, 'Datos de formulario no válidos.')

    return render(request, 'loginTemplates/login.html', {'form': form, 'error': message})

def Recuperar(request):
    return render(request, 'loginTemplates/recuperar.html')


# Create your views here.
