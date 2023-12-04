from django.shortcuts import render, redirect
from .models import Rol, Cuenta, Usuarios, Producto
from .forms import UsuariosForm, ProductosForm
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import permission_required,login_required

# @login_required(login_url='login')
def indexAdministrador(request):
    cuenta_id = request.session.get('usuario_id')
    cuenta = Cuenta.objects.get(id=cuenta_id)
    if cuenta_id is not None:
        usuario = Usuarios.objects.get(cuenta = cuenta_id)
        nombre = usuario.nombre
        apellido = usuario.apellido
        data ={
            'nombre':nombre,
            'apellido':apellido

        }
        return render(request, 'administradorAppTemplates/indexAdministrador.html', data)
    else:
        print("Usuario no registrado ")
        return redirect('login')

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
    return render(request, 'administradorAppTemplates/administrarCuenta.html', {'usuarios': usuarios})



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
                cuenta = Cuenta.objects.create(
                    rol=rol, correo=correo, password=password)
                Usuarios.objects.create(
                    cuenta=cuenta, nombre=nombre, apellido=apellido, telefono=telefono)
                messages.success(request, 'Usuario creado exitosamente.')
                form = UsuariosForm()
                return render(request, 'administradorAppTemplates/crearCuenta.html', {'form': form})
            except IntegrityError:
                messages.error(request, 'El correo ya está en uso.')
                return render(request, 'administradorAppTemplates/crearCuenta.html', {'form': form})
        else:
            messages.error(request, 'Error al crear el usuario.')
            return render(request, 'administradorAppTemplates/crearCuenta.html', {'form': form})

    else:
        form = UsuariosForm()

        return render(request, 'administradorAppTemplates/crearCuenta.html', {'form': form})



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
                        messages.success(
                            request, 'Usuario modificado exitosamente.')
                    else:
                        messages.error(
                            request, 'Error al modificar el usuario.')
                return redirect('usuariosAdm')
            return render(request, 'administradorAppTemplates/administrarCuenta.html', {'usuarios': Usuarios.objects.all()})


# Productos


def listProductos(request):
    productos = Producto.objects.all()
    data = {
    'productos':productos
    }
    return render(request, 'administradorAppTemplates/listadoProducto.html', data)

def eliliminarProducto(request, id):
    producto = Producto.objects.get(id = id)
    producto.delete()
    return redirect('listaProductos')

def actualizarProducto(request, id):
    producto = Producto.objects.get(id = id)
    form = ProductosForm(instance=producto)
    if request.method == 'POST':
        form = ProductosForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
        return redirect('listaProductos')
    data = {'form':form}
    return render(request, 'administradorAppTemplates/agregarProducto.html', data)





def listPedidos(request):
    return render(request, 'administradorAppTemplates/listadoPedido.html')



def agregarProducto(request):
    productos = Producto()
    form = ProductosForm()
    data = {
        'form': form,
        'productos': productos
    }
    if request.method == 'POST':
        form = ProductosForm(request.POST)
        if form.is_valid():
            try:
                categoria = form.cleaned_data['categoria']
                nombre = form.cleaned_data['nombre']
                descripcion = form.cleaned_data['descripcion']
                stock = form.cleaned_data['stock']
                precio = form.cleaned_data['precio']
                Producto.objects.create(
                    categoria = categoria,nombre = nombre,descripcion = descripcion, stock = stock, precio = precio
                )
                messages.success(request, 'Producto creado exitosamente.')
                form = ProductosForm()
                data['form'] = form
                return render(request, 'administradorAppTemplates/agregarProducto.html', data)
            
            except IntegrityError:
                messages.error(request, 'Error al ingresar el producto.')
                data['form'] = form
                return render(request, 'administradorAppTemplates/agregarProducto.html', data)
        else:
            messages.error(request, 'Dato invalido.')
            data['form'] = form
            return render(request, 'administradorAppTemplates/agregarProducto.html', data)

    else:
        form = ProductosForm()

        return render(request, 'administradorAppTemplates/agregarProducto.html', data)

def logoutVendedor(request):
    del request.session['usuario_id']
    return redirect('login')
# Create your views here.
