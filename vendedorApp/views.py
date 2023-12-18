from django.db import IntegrityError
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from administradorApp.forms import EditarUsuariosForm
from django.core.mail import EmailMessage
from django.conf import settings

from administradorApp.models import Cuenta, Producto,Pedido,DetallePedido
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from vendedorApp.form import DetallePedidoForm, EditarEstado, PedidoForm, EditarPassword, EditarPerfilForm
from vendedorApp.Carrito import Carrito
from administradorApp.models import Usuarios
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.db import transaction

# Create your views here.}

def indexVendedor(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "vendedor":
            data = {
                'nombre': cuenta.nombre,
                'apellido': cuenta.apellido
            }
            return render(request, 'vendedorAppTemplates/indexVendedor.html', data)
        
    # Si el rol no es "vendedor", redirige al usuario a la página de inicio de sesión
    else:
        print("Usuario no registrado ")
        return redirect('login')



# _______________CATALOGO__________________
def catalogoVendedor(request,):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "vendedor":
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

            return render(request, 'vendedorAppTemplates/vendedorCatalogo.html', data)
        
    else:
        print("Usuario no registrado ")
        return redirect('login')

# ___________________CARRITO VENDEDOR________________

def carritoVendedor(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "vendedor":
            detalleform = DetallePedidoForm()
            usuario = Usuarios.objects.get(id=request.session['usuario_id'])
            carrito = Carrito(usuario)
            total = carrito.calcular_precio_total()
            pedidoform = PedidoForm(initial={'total' : total,'value':total})
            if request.method == 'POST':
                pedidoform = PedidoForm(request.POST)
                if pedidoform.is_valid():
                    try:
                        with transaction.atomic():

                            pedido = pedidoform.save(commit=False)
                            pedido.total = total
                            pedido.estado = 'En proceso'
                            usuario_instancia = Usuarios.objects.get(id=cuenta_id)
                            pedido.usuario = usuario_instancia
                            pedido.save()

                            # Crear instancias de DetallePedido para cada producto en el carrito
                            productos_carrito = usuario.carrito.items()
                            detalles_pedido = []

                            for key, value in productos_carrito:
                                producto = Producto.objects.get(pk=key)
                                cantidad_vendida = value['cantidad']

                                if cantidad_vendida > producto.stock:
                                    print("No hay suficiente stock del Producto.")

                                    return redirect()

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

                            nombreVendedor = usuario_instancia.nombre 
                            idPedido = pedido.id
                            asunto ='Pedido realizando por vendedor. '
                            apelldioVendedor = usuario_instancia.apellido 
                            fechaPedido = pedido.fechaCreacion
                            nombreDestinatario = pedido.nombre +" "+ pedido.apellido

                            
                            template = render_to_string('vendedorAppTemplates/emailTemplate.html',{
                                            'name': nombreVendedor +" "+ apelldioVendedor,
                                            'idPedido':str(idPedido),
                                            'fecha': str(fechaPedido),
                                            'nameD': nombreDestinatario
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
                            messages.success(request, 'Producto agregado al carrito!')
                            return redirect('vendedorCarrito')
                        
                    except Exception as e:
                        print("Pedido no es válido")
                        messages.success(request, 'Error al realizar el pedido!')
                        return redirect('vendedorCarrito')
            data = {
                'pedidoForm': pedidoform,
                'detalleForm': detalleform,
                'carrito':carrito, 
                'total':total,
            }

            return render(request, 'vendedorAppTemplates/vendedorCarrito2.html', data)
    else:
        return redirect('login')
    
def agregarCarrito(request, id):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "vendedor":
            if request.method == 'POST':
                cantidad = request.POST['cantidad']
                carrito = Carrito(cuenta)  # Asegúrate de que estás pasando request.user
                agregado = carrito.agregar(id , cantidad)

                if agregado :   
                    messages.success(request, 'Producto agregado al carrito!')
                    return redirect('vendedorCatalogo')
                else:
                    messages.error(request, 'La cantidad supera el Sotck!')
                    return redirect('vendedorCatalogo')
                    
    else:
        return redirect('login')
    

def sumarleProducto(request, id):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "vendedor":
            carrito = Carrito(cuenta)
            producto = Producto.objects.get(id=id)
            resultado = carrito.sumarle(producto)

            if resultado == False:
                messages.error(request, 'No hay suficiente stock para agregar el producto al carrito.')
            else:
                messages.success(request, 'Producto agregado al carrito!')
                print(str(resultado))

            return redirect('vendedorCarrito')
    else:
        return redirect('login')

def eliminarProductoCarrito(request, id):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "vendedor":
            carrito = Carrito(cuenta)
            producto = Producto.objects.get(id=id)
            carrito.eliminar(producto)
            return redirect('vendedorCarrito')
    else:
        return redirect('login')

def restar_producto(request, id):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "vendedor":
            carrito = Carrito(cuenta)
            producto = Producto.objects.get(id=id)
            carrito.restar(producto)
            return redirect('vendedorCarrito')
    else:
        return redirect('login')

def limpiar_carrito(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "vendedor":
            carrito = Carrito(cuenta)
            carrito.limpiar()
            return redirect('vendedorCarrito')
    else:
        return redirect('login')
    
def seleccionUsuario(request, user_id):
    user = get_object_or_404(Usuarios, id=user_id)
    data = {'nombre': user.nombre, 'apellido': user.apellido, 'direccion':user.direccion,'comuna':user.comuna,'ciudad':user.ciudad,}
    
    return JsonResponse(data)
    
#_____________________PEDIDOS______________________________________

def vendedorPedido(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "vendedor":
            listpedido = Pedido.objects.filter(usuario = cuenta)
            data ={
            'pedidos':listpedido,
            'titulo':'Pedidos'
            }
            return render(request, 'vendedorAppTemplates/pedidosVendedor.html',data)

    else:
            print("Usuario no registrado ")
            return redirect('login')
    

def agregar_producto(request, producto_id):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "vendedor":
            producto = Producto.objects.get(id=producto_id)
            pedido = Pedido.objects.filter(usuario=request.user, estado='enProceso').first()

            # Si no hay un pedido en proceso, creamos uno
            if not pedido:
                pedido = Pedido.objects.create(usuario=request.user, estado='enProceso')
            # Creamos un nuevo DetallePedido para el producto
            detalle_pedido = DetallePedido.objects.create(pedido=pedido, producto=producto, cantidad=1, precio_unitario=producto.precio, precio_total=producto.precio)
            return redirect("vendedorCarrito")
    else:
            print("Usuario no registrado ")
            return redirect('login')

def actualizarEstadoVendedor(request, id):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id= cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "vendedor":
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
                        return redirect('vendedorPedido')
                    
                    if fechaEntrega == None:
                        pedido.estado = estado
                        pedido.save()
                        messages.success(request, 'Modificacion exitosamente.')
                        return redirect('vendedorPedido')
                    pedido.estado = estado
                    pedido.fechaEntrega = fechaEntrega
                    pedido.save()
                    messages.success(request, 'Modificacion exitosamente.')
                    return redirect('vendedorPedido')
                
                else:
                    messages.error(request, 'Modificacion den.')
                    return redirect('vendedorPedido')
            return render( request,'vendedorAppTemplates/estado.html', data)
    else:
        print("Usuario no registrado ")
        return redirect('login')
    
       
#_______________________PERFIL__________________________
    
def vendedorPerfil(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "vendedor":

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
        return render(request, 'vendedorAppTemplates/vendedorPerfil.html',data)
    else:
        # El usuario no está autenticado
        print("Usuario no registrado ")
        return redirect('login')
    
def editarPerfilVend(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "vendedor":
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
                        return redirect('editarPerfilVend')
                    
                    except IntegrityError:
                        messages.error(request, 'Datos invalidos.')
                        return render(request, 'vendedorAppTemplates/vendedorPerfil.html', data)
                else:
                    messages.error(request, 'formulario invalido.')
                    return render(request, 'vendedorAppTemplates/vendedorPerfil.html', data)
            return render(request, 'vendedorAppTemplates/vendedorPerfil.html', data)
        
        else:
            print("Usuario no registrado ")
            return redirect('login')
    else:
        print("Usuario no registrado ")
        return redirect('login')

def editarContraVend(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "vendedor":
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
                            return redirect('editarContraVend')
                    
                        else:
                            messages.error(request, 'Su contraseña no es correcta.')
                            print("La contraseña no es válida." + str(password))
                            return redirect('editarContraVend')

                    
                    except IntegrityError:
                        messages.error(request, 'Formulario Invalido.')
                        return render(request, 'vendedorAppTemplates/vendedorPerfil.html', data)
                        
                else:
                    messages.error(request, 'Las contraseñas no concuerdan.')
                    return render(request, 'vendedorAppTemplates/vendedorPerfil.html', data)

                    
            return render(request, 'vendedorAppTemplates/vendedorPerfil.html', data)
            
    else:
        print("Usuario no registrado ")
        return redirect('login')
    
    

#_____________________lOGOUT______________________________________

def logoutVendedor(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = get_object_or_404(Usuarios, id=cuenta_id)
        rol = cuenta.cuenta.rol.nombre.lower()
        if rol == "vendedor":
            del request.session['usuario_id']
            return redirect('login')
    else:
            print("Usuario no registrado ")
            return redirect('login')
