from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import activate
from .models import Cuenta, Usuarios, Producto, Pedido, DetallePedido
from .forms import EditarUsuariosForm, UsuariosForm, ProductosForm, EditarPerfilForm, EditarPassword, EditarEstado
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password

# @login_required(login_url='login')
def indexAdministrador(request):

    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "administrador":
            nombre = cuenta.nombre
            apellido = cuenta.apellido
            data ={
                'nombre':nombre,
                'apellido':apellido

            }
            return render(request, 'administradorAppTemplates/indexAdministrador.html', data)
        
        request.session['form_message'] = "Acceda a su cuenta de usuario."
        return redirect('login')
        
    else:
        print("Usuario no registrado ")
        return redirect('login')

def gestionVentas(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "administrador":
            return render(request, 'administradorAppTemplates/ventas.html')
        
        request.session['form_message'] = "Acceda a su cuenta de usuario."
        return redirect('login')
        
    else:
        print("Usuario no registrado ")
        return redirect('login')


def gestionUsuarios(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "administrador":
            return render(request, 'administradorAppTemplates/usuarios.html')
        request.session['form_message'] = "Acceda a su cuenta de usuario."
        return redirect('login')
    else:
        print("Usuario no registrado ")
        return redirect('login')

#_______________________PERFIL________________________________________
def perfilAdm(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id= cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "administrador":
            data ={
                'nombre': cuenta.nombre,
                'apellido':cuenta.apellido,
                'telefono':"+569 "+cuenta.telefono,
                'direccion':cuenta.direccion,
                'comuna':cuenta.comuna,
                'ciudad':cuenta.ciudad,
                'perfil':'perfil'
            }
            return render(request, 'administradorAppTemplates/perfil.html',data)
        request.session['form_message'] = "Acceda a su cuenta de Usuario."
        return redirect('login')
    else:
        print("Usuario no registrado ")
        return redirect('login')
    
def editarPerfil(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id= cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "administrador":
            form = EditarPerfilForm(instance=cuenta)
            data ={
                'modificar':'modificar',
                'form':form
            }
            if request.method == 'POST':
                form = EditarUsuariosForm(request.POST,instance=cuenta)
                if form.is_valid():
                    try:

                        nombre = form.cleaned_data['nombre']
                        apellido = form.cleaned_data['apellido']
                        telefono = str(form.cleaned_data['telefono'])
                        direccion = form.cleaned_data['direccion']
                        comuna = form.cleaned_data['comuna']
                        ciudad = form.cleaned_data['ciudad']
                        cuenta.nombre = nombre
                        cuenta.apellido = apellido
                        cuenta.telefono = telefono
                        cuenta.direccion = direccion
                        cuenta.comuna = comuna
                        cuenta.ciudad = ciudad
                        cuenta.save()
                        messages.success(request, 'Modificacion exitosamente.')
                        return redirect('editarPerfil')
                    
                    except IntegrityError:
                        messages.error(request, 'Datos invalidos.')
                        return render(request, 'administradorAppTemplates/perfil.html', data)
                else:
                    messages.error(request, 'formulario invalido.')
                    return render(request, 'administradorAppTemplates/perfil.html', data)
            return render(request, 'administradorAppTemplates/perfil.html', data)
        
        else:
            print("Usuario no registrado ")
            return redirect('login')
    else:
        print("Usuario no registrado ")
        return redirect('login')

def editarContra(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id= cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "administrador":
            form = EditarPassword()
            data ={
                'contraseña':'contraseña',
                'form':form
            }
            if request.method == 'POST':
                form = EditarPassword(request.POST)
                if form.is_valid():
                    cuenta = Usuarios.objects.get( id = cuenta_id )
                    try:    
                        password = form.cleaned_data['password']
                        newPassword = form.cleaned_data['newPassword']
                        passUsuario = cuenta.cuenta.password
                        
                        if check_password(password, passUsuario):
                            hashPassword = make_password(newPassword)
                            cuenta = Cuenta.objects.update( password=hashPassword)

                            messages.success(request, 'Contraseña Modificada.')
                            print("La contraseña se modifico.")
                            return redirect('editarContra')
                    
                        else:
                            messages.error(request, 'Su contraseña no es correcta.')
                            print("La contraseña no es válida." + str(password))
                            return redirect('editarContra')

                    
                    except IntegrityError:
                        messages.error(request, 'Formulario Invalido.')
                        return render(request, 'administradorAppTemplates/perfil.html', data)
                        
                else:
                    messages.error(request, 'Las contraseñas no concuerdan.')
                    return render(request, 'administradorAppTemplates/perfil.html', data)

                    
            return render(request, 'administradorAppTemplates/perfil.html', data)
            
    else:
        print("Usuario no registrado ")
        return redirect('login')
    
    

# _____________________Gestion de usuarios_______________________________

def administrarCuentaAdm(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id= cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "administrador":
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

    else:
        print("Usuario no registrado ")
        return redirect('login')
    
    

def crearCuentaAdm(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id= cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "administrador":
            if request.method == 'POST':
                form = UsuariosForm(request.POST)
                if form.is_valid():
                    try:
                        correo = form.cleaned_data['correo']
                        password = form.cleaned_data['password']
                        rol = form.cleaned_data['rol']
                        nombre = form.cleaned_data['nombre']
                        apellido = form.cleaned_data['apellido']
                        telefono = str(form.cleaned_data['telefono'])
                        direccion = form.cleaned_data['direccion']
                        comuna = form.cleaned_data['comuna']
                        ciudad = form.cleaned_data['ciudad']
            
                        hashPassword = make_password(password)
                        
                        cuenta = Cuenta.objects.create(
                            rol=rol, correo=correo, password=hashPassword)
                        Usuarios.objects.create(
                            cuenta=cuenta, nombre=nombre, apellido=apellido, telefono=telefono, direccion = direccion, comuna = comuna, ciudad = ciudad)
                        messages.success(request, 'Usuario creado exitosamente.')
                        form = UsuariosForm()
                        return render(request, 'administradorAppTemplates/crearCuenta.html', {'form': form, 'devolverse':'usuariosAdm'})
                    
                    except IntegrityError:
                        messages.error(request, 'El correo ya está en uso.')
                        return render(request, 'administradorAppTemplates/crearCuenta.html', {'form': form,'devolverse':'usuariosAdm'})
                else:
                    messages.error(request, 'Las contraseñas no concuerdan.')
                    return render(request, 'administradorAppTemplates/crearCuenta.html', {'form': form,'devolverse':'usuariosAdm'})

            else:
                form = UsuariosForm()

                return render(request, 'administradorAppTemplates/crearCuenta.html', {'form': form,'devolverse':'usuariosAdm'})

            
    else:
        print("Usuario no registrado ")
        return redirect('login')
    


def modificarUsuarios(request,id):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id= cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "administrador":
            usuario = Usuarios.objects.get(id = id)
            form = EditarUsuariosForm(instance=usuario)
            if request.method == 'POST':
                form = EditarUsuariosForm(request.POST, instance=usuario)
                if form.is_valid():

                    form.save()
                    print("valido")

                if not form.is_valid():
                    print(form.errors)
                return redirect('administrarCuenta')
 

    

            data = {
                'form':form,
                'nombre':usuario.nombre,
                'apellido':usuario.apellido,
                'editar':'editar',
                'devolverse':'administrarCuenta'

                }
            return render(request, 'administradorAppTemplates/crearCuenta.html', data)
    else:
        print("Usuario no registrado ")
        return redirect('login')
    


def eliliminarUsuario(request, id):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id= cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "administrador":
            usuario = Usuarios.objects.get(id = id)
            usuario.delete()
            return redirect('administrarCuenta')
    else:
        print("Usuario no registrado ")
        return redirect('login')
    




# ----------------PEDIDOS----------------------
def listPedidos(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id= cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "administrador":
            activate('es')
            pedido = Pedido.objects.all()
            data = {
                'pedido':pedido
            }
            return render(request, 'administradorAppTemplates/listadoPedido.html', data)
    else:
        print("Usuario no registrado ")
        return redirect('login')
    



#Listo
def eliliminarPedidos(request, id):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id= cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "administrador":
            pedidido = Pedido.objects.get(id = id)
            pedidido.delete()
            return redirect('listaPedidos')
    else:
        print("Usuario no registrado ")
        return redirect('login')
    

#En proceso

def actualizarEstado(request, id):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id= cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "administrador":
            pedido = Pedido.objects.get(id = id)
            form = EditarEstado()
            data ={
                'form' : form
            }
            if request.method == 'POST':
                form = EditarEstado(request.POST)
                if form.is_valid():
                    estado = form.cleaned_data['estado']
                    fechaEntrega = form.cleaned_data['fechaEntrega']
                    print(fechaEntrega)
                    print(estado)
                    if estado == "Entregado" and fechaEntrega == None:
                        messages.error(request, '¡No se puede entregar sin seleccionar la fecha de entrega!')
                        return redirect('listaPedidos')
                    
                    if fechaEntrega == None:
                        pedido.estado = estado
                        pedido.save()
                        messages.success(request, 'Modificacion exitosamente.')
                        return redirect('listaPedidos')
                    pedido.estado = estado
                    pedido.fechaEntrega = fechaEntrega
                    pedido.save()
                    messages.success(request, 'Modificacion exitosamente.')
                    return redirect('listaPedidos')
                
                else:
                    messages.error(request, 'Modificacion den.')
                    return redirect('listaPedidos')


            return render( request,'administradorAppTemplates/estado.html', data)

    else:
        print("Usuario no registrado ")
        return redirect('login')
    
       

def listDetalle(request,id):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id= cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "administrador":
            detalle = DetallePedido.objects.filter( pedido = id )
            sumTotal= sum(d.precio_total for d in detalle)
            data = {
            'detalle':detalle,
            'total':sumTotal
            }
            return render(request, 'administradorAppTemplates/detallePedido.html', data)

    else:
        print("Usuario no registrado ")
        return redirect('login')



#  ---------------PRODUCTOS-----------------------------------


def listProductos(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id= cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "administrador":
            productos = Producto.objects.all()
            data = {
            'productos':productos
            }
            return render(request, 'administradorAppTemplates/listadoProducto.html', data)
    else:
        print("Usuario no registrado ")
        return redirect('login')



def eliliminarProducto(request, id):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id= cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "administrador":
            producto = Producto.objects.get(id = id)
            producto.delete()
            return redirect('listaProductos')
    else:
        print("Usuario no registrado ")
        return redirect('login')

def actualizarProducto(request, id):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id= cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "administrador":
            producto = Producto.objects.get(id = id)
            nombre = producto.nombre
            form = ProductosForm(instance=producto)
            if request.method == 'POST':
                form = ProductosForm(request.POST, instance=producto)
                if form.is_valid():
                    form.save()
                return redirect('listaProductos')
            
            data = {'form':form,
                    'modificacion':'modificacion',
                    'nombre':nombre,}
            return render(request, 'administradorAppTemplates/agregarProducto.html', data)

    else:
        print("Usuario no registrado ")
        return redirect('login')

def agregarProducto(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id= cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "administrador":
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
                        imagen_url = form.cleaned_data['imagen_url']
                        Producto.objects.create(
                            categoria = categoria,nombre = nombre,descripcion = descripcion, stock = stock, precio = precio, imagen_url = imagen_url
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

    else:
        print("Usuario no registrado ")
        return redirect('login')
         
#------------------LOGOUT ADMINISTRADOR------------------------#

def logoutVendedor(request):
    del request.session['usuario_id']
    return redirect('login')
# Create your views here.
