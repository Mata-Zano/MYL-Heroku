from django.shortcuts import get_object_or_404, redirect, render
from django.db import IntegrityError

from django.template.loader import render_to_string
from administradorApp.forms import EditarUsuariosForm
from administradorApp.models import Cuenta, DetallePedido, Pedido, Producto, Usuarios
from clienteApp.Carrito import Carrito
from clienteApp.form import DetallePedidoForm, EditarEstado, EditarPassword, EditarPerfilForm, PedidoForm
from django.db import transaction
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import make_password, check_password

from django.db import transaction
from django.contrib import messages





def indexCliente (request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "cliente":
            data = {
                'nombre': cuenta.nombre,
                'apellido': cuenta.apellido
            }
            return render(request, 'clienteAppTemplates/indexCliente.html', data)
    else:
        print("Usuario no registrado ")
        return redirect('login')
    
def catalogoCLiente(request,):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "cliente":
            if request.method == 'POST':
                producto = Producto.objects.all()
                return redirect('vendedorCarrito')

            else:
                detalle_pedido_form = DetallePedidoForm()
                producto = Producto.objects.all()
                data = {
                    'detalle_pedido_form':detalle_pedido_form,
                    'producto': producto,
                    'titulo': 'Cátalogo'
                }

            return render(request, 'clienteAppTemplates/clienteCatalogo.html', data)
        
    else:
        print("Usuario no registrado ")
        return redirect('login')
# ___________________CARRITO CLiente________________

def carritoCliente(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "cliente":
            detalleform = DetallePedidoForm()
            usuario = Usuarios.objects.get(id=request.session['usuario_id'])
            carrito = Carrito(usuario)
            total = carrito.calcular_precio_total()
            pedidoform = PedidoForm(instance=cuenta,initial={'total' : total,'value':total, 'usuario_destino':usuario})
            if request.method == 'POST':
                pedidoform = PedidoForm(request.POST)
                if pedidoform.is_valid():
                    try:
                        with transaction.atomic():
                            pedido = pedidoform.save(commit=False)
                            pedido.total = total
                            pedido.estado = 'En proceso'
                            pedido.usuario = usuario
                            pedido.save()

                            # Crear instancias de DetallePedido para cada producto en el carrito
                            productos_carrito = usuario.carrito.items()
                            detalles_pedido = []

                            for key, value in productos_carrito:
                                producto = Producto.objects.get(pk=key)
                                cantidad_vendida = value['cantidad']

                                if cantidad_vendida > producto.stock:
                                    print("No hay suficiente stock del Producto.")

                                    return redirect('clienteCarrito')

                                # Restar la cantidad vendida del stock del producto
                                producto.stock -= cantidad_vendida
                                producto.save()

                                # Crear instancia de DetallePedido
                                detalle = DetallePedido(
                                    pedido=pedido,
                                    producto=producto,
                                    cantidad=cantidad_vendida,
                                    precio_unitario=value['precioUnitario'],
                                    precio_total=value['precio'],
                                )
                                detalles_pedido.append(detalle)

                            # Guardar las instancias de DetallePedido en la base de datos
                            DetallePedido.objects.bulk_create(detalles_pedido)

                            idPedido = pedido.id
                            asunto ='Pedido realizando por cliente. '
                            fechaPedido = pedido.fechaCreacion
                            nombreDestinatario = pedido.nombre +" "+ pedido.apellido

                            
                            template = render_to_string('clienteAppTemplates/emailTemplate.html',{
                                            'idPedido':str(idPedido),
                                            'fecha': str(fechaPedido),
                                            'nameD': nombreDestinatario,
                                            'idCliente': str(usuario.id)
                                        })
                            email =  EmailMessage(
                                asunto,
                                template,
                                settings.EMAIL_HOST_USER,['distribuidoramylcalama@gmail.com']
                            )
                            email.fail_silently = False
                            email.send()

                            limpiar_carrito(request)
                            pedidoform = PedidoForm()
                            detalleform = DetallePedidoForm()
                            messages.success(request, 'Pedido realizado con exito!')
                            return redirect('clienteCarrito')
                        
                    except Exception as e:
                        print("Pedido no es válido", e)
                        print(pedidoform.errors)

                        messages.error(request, 'Error al realizar el pedido!')
                        return redirect('clienteCarrito')
                else:
                    print("Formulario invalido ", pedidoform.errors)
            data = {
                'pedidoForm': pedidoform,
                'detalleForm': detalleform,
                'carrito':carrito, 
                'total':total,
            }

            return render(request, 'clienteAppTemplates/clienteCarrito.html', data)
    else:
        return redirect('login')
    

def agregarCarritoCliente(request, id):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "cliente":
            if request.method == 'POST':
                cantidad = request.POST['cantidad']
                carrito = Carrito(cuenta)  # Asegúrate de que estás pasando request.user
                agregado = carrito.agregar(id , cantidad)

                if agregado :   
                    messages.success(request, 'Producto agregado al carrito!')
                    return redirect('clienteCatalogo')
                else:
                    messages.error(request, 'La cantidad supera el Sotck!')
                    return redirect('clienteCatalogo')
                    
    else:
        return redirect('login')


def sumarleProductoCliente(request, id):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "cliente":
            carrito = Carrito(cuenta)
            producto = Producto.objects.get(id=id)
            resultado = carrito.sumarle(producto)

            if resultado == False:
                messages.error(request, 'No hay suficiente stock para agregar el producto al carrito.')
            else:
                messages.success(request, 'Producto agregado al carrito!')
                print(str(resultado))

            return redirect('clienteCarrito')
    else:
        return redirect('login')


def eliminarProductoCarritoCliente(request, id):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "cliente":
            carrito = Carrito(cuenta)
            producto = Producto.objects.get(id=id)
            carrito.eliminar(producto)
            return redirect('clienteCarrito')
    else:
        return redirect('login')

def restar_productoCliente(request, id):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "cliente":
            carrito = Carrito(cuenta)
            producto = Producto.objects.get(id=id)
            carrito.restar(producto)
            messages.success(request, 'Producto restado del carrito!')
            return redirect('clienteCarrito')
    else:
        return redirect('login')

def limpiar_carrito(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "cliente":
            carrito = Carrito(cuenta)
            carrito.limpiar()
            return redirect('clienteCarrito')
    else:
        return redirect('login')
    
#_____________________PEDIDOS______________________________________

def clientePedido(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "cliente":
            listpedido = Pedido.objects.filter(usuario = cuenta)
            data ={
            'pedidos':listpedido,
            'titulo':'Pedidos'
            }
            return render(request, 'clienteAppTemplates/pedidosClientes.html',data)
            

    else:
            print("Usuario no registrado ")
            return redirect('login')
    

def actualizarEstadoCliente(request, id):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id= cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "cliente":
            pedido = Pedido.objects.get(id = id)
            form = EditarEstado()
            data ={
                'form' : form
            }
            if request.method == 'POST':
                form = EditarEstado(request.POST)
                if form.is_valid():
                    estado = form.cleaned_data['estado']
                    pedido.estado = estado
                    pedido.save()
                    messages.success(request, 'Modificacion exitosamente.')
                    return redirect('clientePedido')
                
                else:
                    messages.error(request, 'Modificacion denegada.')
                    return redirect('clientePedido')
            return render( request,'clienteAppTemplates/estado.html', data)
    else:
        print("Usuario no registrado ")
        return redirect('login')
    
#_______________________PERFIL__________________________
    
def clientePerfil(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "cliente":

         data ={
                'nombre': cuenta.nombre,
                'apellido':cuenta.apellido,
                'telefono':"+569 "+cuenta.telefono,
                'correo':cuenta.cuenta.correo,

                'direccion':cuenta.direccion,
                'comuna':cuenta.comuna,
                'ciudad':cuenta.ciudad,
                'perfil':'perfil'
            }
        return render(request, 'clienteAppTemplates/clientePerfil.html',data)
    else:
        # El usuario no está autenticado
        print("Usuario no registrado ")
        return redirect('login')


def editarPerfilClient(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "cliente":
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
                                              # Actualiza solo el usuario asociado a la cuenta
                        cuenta.nombre = nombre
                        cuenta.apellido = apellido
                        cuenta.telefono = telefono
                        cuenta.direccion = direccion
                        cuenta.comuna = comuna
                        cuenta.ciudad = ciudad

                        # Guarda los cambios en la base de datos
                        cuenta.save()
                        messages.success(request, 'Modificacion exitosamente.')
                        return redirect('editarPerfilClient')
                    
                    except IntegrityError:
                        messages.error(request, 'Datos invalidos.')
                        return render(request, 'clienteAppTemplates/clientePerfil.html', data)
                else:
                    messages.error(request, 'formulario invalido.')
                    return render(request, 'clienteAppTemplates/clientePerfil.html', data)
            return render(request, 'clienteAppTemplates/clientePerfil.html', data)
        
        else:
            print("Usuario no registrado ")
            return redirect('login')
    else:
        print("Usuario no registrado ")
        return redirect('login')

def editarContraClient(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "cliente":
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
                            return redirect('editarContraClient')
                    
                        else:
                            messages.error(request, 'Su contraseña no es correcta.')
                            print("La contraseña no es válida." + str(password))
                            return redirect('editarContraClient')

                    
                    except IntegrityError:
                        messages.error(request, 'Formulario Invalido.')
                        return render(request, 'clienteAppTemplates/clientePerfil.html', data)
                        
                else:
                    messages.error(request, 'Las contraseñas no concuerdan.')
                    return render(request, 'clienteAppTemplates/clientePerfil.html', data)

                    
            return render(request, 'clienteAppTemplates/clientePerfil.html', data)
            
    else:
        print("Usuario no registrado ")
        return redirect('login')
    
    

#_____________________lOGOUT______________________________________

def logoutCliente(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "cliente":
            del request.session['usuario_id']
            return redirect('login')
    else:
            print("Usuario no registrado ")
            return redirect('login')
