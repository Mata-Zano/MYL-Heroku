from django.shortcuts import render,redirect
from administradorApp.models import Cuenta, Producto,Pedido,DetallePedido
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from vendedorApp.form import DetallePedidoForm, PedidoForm
from MYL.Carrito import Carrito
from administradorApp.models import Usuarios

# Create your views here.}

def indexVendedor(request):
    cuenta_id = request.session.get('usuario_id')
    cuenta = Cuenta.objects.get(id=cuenta_id)
    rol =cuenta.rol.nombre.lower()
    if rol == "vendedor":
        usuario = cuenta.usuarios
        # Haz algo con el usuari
        data = {
            'nombre': usuario.nombre,
            'apellido':usuario.apellido
        }
        return render(request, 'vendedorAppTemplates/indexVendedor.html', data)
    else:
        # El usuario no está autenticado
        print("Usuario no registrado o no es vendedor.")
        return redirect('login')
    


# En la vista catalogoVendedor
def catalogoVendedor(request,):
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


# -------------------------En la vista carritoVendedor----------------
def carritoVendedor(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        pedidoform = PedidoForm()
        detalleform = DetallePedidoForm()
        if request.method == 'POST':
            pedidoform = PedidoForm(request.POST)

            if pedidoform.is_valid():
                pedidoform.save()
                detalleform = DetallePedidoForm(request.POST)
                if detalleform.is_valid():
                    detalleform.save()
                else:
                    print("Detalle no es valido")
                    print(detalleform.errors)
            else :
                print("Pedido no es valido")
                print(pedidoform.errors)
        data = {
            'pedidoForm':pedidoform,
            'detalleForm':detalleform
            
            }
        return render(request, 'vendedorAppTemplates/vendedorCarrito.html',data)
    else:
        return redirect('login')
    
def agregarCarrito(request, id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id =id)
    carrito.agregar(producto)
    return redirect('vendedorCatalogo')

def sumarleProducto(request, id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id =id)
    carrito.agregar(producto)
    return redirect('vendedorCarrito')

def eliminarProductoCarrito(request, id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id =id)
    carrito.eliminar(producto)
    return redirect('vendedorCarrito')

def restar_producto(request, id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id = id)
    carrito.restar(producto)
    return redirect('vendedorCarrito')

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('vendedorCarrito')

def seleccionUsuario(request, user_id):
    user = get_object_or_404(Usuarios, id=user_id)
    data = {'nombre': user.nombre, 'apellido': user.apellido}
    return JsonResponse(data)
    

    # if request.method == 'POST':
    #     pedido_form = PedidoForm(request.POST)
    #     detalle_pedido_form = DetallePedidoForm(request.POST)

    #     if pedido_form.is_valid() and detalle_pedido_form.is_valid():
    #         pedido = pedido_form.save()
    #         detalle_pedido = detalle_pedido_form.save(commit=False)
    #         detalle_pedido.pedido = pedido
    #         detalle_pedido.save()
    #         return redirect('vendedorCarrito')  # Cambia 'tu_vista_exitosa' con la vista que desees
    # else:
    #     pedido_form = PedidoForm()
    #     detalle_pedido_form = DetallePedidoForm()

    # return render(request, 'vendedorAppTemplates/vendedorCarrito.html',  {'pedidoForm': pedido_form, 'detallePedidoForm': detalle_pedido_form})

       # if request.method == 'POST':
        #     pedido_form = PedidoForm(request.POST)
        #     if pedido_form.is_valid():
        #         pedido = pedido_form.save(commit=False)
        #         pedido.usuario = usuario
        #         pedido.save()

        #         carrito = request.session.get('carrito', [])
        #         for producto_id in carrito:
        #             producto = Producto.objects.get(id=producto_id)
        #             DetallePedido.objects.create(pedido=pedido, producto=producto, cantidad=1,
        #                                          precio_unitario=producto.precio, precio_total=producto.precio)

        #         # Vaciamos el carrito
        #         request.session['carrito'] = []

        #         return redirect('vendedorCarrito')

        # else:
        #     pedido_form = PedidoForm()

        # detalles_pedido = []
        # total_pedido = 0

        # # Obtén los detalles del carrito
        # carrito = request.session.get('carrito', [])
        # for producto_id in carrito:
        #     producto = Producto.objects.get(id=producto_id)
        #     detalles_pedido.append({
        #         'producto': producto,
        #         'cantidad': 1,
        #         'precio_unitario': producto.precio,
        #         'precio_total': producto.precio
        #     })
        #     total_pedido += producto.precio

        # data = {
        #     'nombre': usuario.nombre,
        #     'apellido': usuario.apellido,
        #     'pedidoForm': pedido_form,
        #     'detalles_pedido': detalles_pedido,
        #     'total_pedido': total_pedido,
        # }
        # return render(request, 'vendedorAppTemplates/vendedorCarrito.html', data)

def vendedorPerfil(request):
    cuenta_id = request.session.get('usuario_id')
    if cuenta_id is not None:
        cuenta = Cuenta.objects.get(id=cuenta_id)
        usuario = cuenta.usuarios
        # Haz algo con el usuario
        data = {
            'nombre': usuario.nombre,
            # ... el resto de tus datos ...
        }
        return render(request, 'vendedorAppTemplates/vendedorPerfil.html')
    else:
        # El usuario no está autenticado
        print("Usuario no registrado ")
        return redirect('login')
    




def vendedorPedido(request):
    data ={
        'titulo':'Pedidos'
    }
    return render(request, 'vendedorAppTemplates/pedidosVendedor.html',data)

def agregar_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    pedido = Pedido.objects.filter(usuario=request.user, estado='enProceso').first()

    # Si no hay un pedido en proceso, creamos uno
    if not pedido:
        pedido = Pedido.objects.create(usuario=request.user, estado='enProceso')
    # Creamos un nuevo DetallePedido para el producto
    detalle_pedido = DetallePedido.objects.create(pedido=pedido, producto=producto, cantidad=1, precio_unitario=producto.precio, precio_total=producto.precio)
    return redirect("vendedorCarrito")


def logoutVendedor(request):
    del request.session['usuario_id']
    return redirect('login')