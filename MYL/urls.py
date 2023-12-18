"""
URL configuration for MYL project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import include, path
from principalApp.views import *
from loginApp.views import *
from administradorApp.views import *
from vendedorApp.views import *
from clienteApp.views import *

urlpatterns = [
# ________________________________________________________________________________________________

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('',Index, name='index'),
    path('catálogo/',Catalogo, name='Catalogo'),
    path('contacto/',Contacto, name='Contacto'),
    path('enviar/',enviarEmail, name='enviarEmail'),

    path('sobreNosotros/',Sobre, name='Sobre'),

# ---------------------------------RECUPERAR---------------------------------------------
    path('ingreso/',Ingreso, name='login'),
    path('ingreso/recuperar/',Recuperar, name='recuperar'),

# _____________________________________________________________________________________________
    #                       ADM
    path('MYL/administrador/', indexAdministrador, name='administrador'),
    path('MYL/administrador/gestionVentas/', gestionVentas, name='ventasAdm'),
    path('MYL/administrador/gestionUsuarios/', gestionUsuarios, name='usuariosAdm'),
    #--------Perfil-------------------------------------------------
    path('MYL/administrador/perfil/', perfilAdm, name='perfilAdm'),
    path('MYL/administrador/perfil/editarPerfil', editarPerfil, name='editarPerfil'),
    path('MYL/administrador/perfil/editarContra', editarContra, name='editarContra'),


    #--------Gestion de cuentas -----------------
    path('MYL/administrador/gestionUsuarios/crearCuenta/', crearCuentaAdm, name='crearCuenta'),
    path('MYL/administrador/gestionUsuarios/administrarCuenta/', administrarCuentaAdm, name='administrarCuenta'),
    path('MYL/administrador/gestionUsuarios/administrarCuenta/editar/<int:id>/', modificarUsuarios, name='modificarUsuario'),
    path('MYL/administrador/gestionUsuarios/administrarCuenta/eliminar/<int:id>/', eliliminarUsuario, name='eliminarUsuario'),



    #---------Lista Productos----------------- 
    path('MYL/administrador/gestionVentas/listaProductos/', listProductos, name='listaProductos'),
    path('MYL/administrador/gestionVentas/agregarProductos/', agregarProducto, name='agregarProductos'),
    path('MYL/administrador/gestionVentas/listaProductos/eliminarProducto/<int:id>/', eliliminarProducto, name='eliminarProductos'),
    path('actualizarProducto/<int:id>', actualizarProducto, name='actualizarProducto'),
    

    #----------Listar Pedidos-----------------
    path('MYL/administrador/gestionVentas/listPedidos/', listPedidos, name='listaPedidos'),
    path('MYL/administrador/gestionVentas/detallePedido/<int:id>', listDetalle, name='detallePedido'),
    path('MYL/administrador/gestionVentas/listPedidos/eliminarPedido/<int:id>/', eliliminarPedidos, name='eliminarPedido'),
    path('actualizarEstado/<int:id>', actualizarEstado, name='ModificarEstado'),
# _____________________________________________________________________________


# _____________________________________________VENDEDOR________________________________________________________________
    path('MYL/vendedor/', indexVendedor, name='vendedor'),
#--------------------------CATALOGO------------------------------------------------------------------
    path('MYL/vendedor/catalogo', catalogoVendedor, name='vendedorCatalogo'),
    path('vendedor/agregar_a_Carrito/<int:id>', agregarCarrito, name='agregarCarrito'),
#--------------------------------------------CARRITO---------------------------------------------------------------
    path('MYL/vendedor/carrito', carritoVendedor, name='vendedorCarrito'),
    path('vendedor/eliminar_producto_Carrito/<int:id>', eliminarProductoCarrito, name='eliminarProductoCarrito'),
    path('vendedor/sumarleProducto/<int:id>', sumarleProducto, name='sumarleProducto'),
    path('vendedor/restar_producto_Carrito/<int:id>', restar_producto, name='restarProductoCarrito'),
    path('MYL/vendedor/seleccionUsuario/<int:user_id>', seleccionUsuario, name='SeleccionUsuario'),

#------------------------------PERFIL---------------------------------------------------------
    path('MYL/vendedor/perfil', vendedorPerfil, name='vendedorPerfil'),
    path('MYL/vendedor/perfil/editarPerfil', editarPerfilVend, name='editarPerfilVend'),
    path('MYL/vendedor/perfil/editarContra', editarContraVend, name='editarContraVend'),
#-----------------------------PEDIDO------------------------------------------------------------
    path('MYL/vendedor/pedidos', vendedorPedido, name='vendedorPedido'),
    path('vendedor/actualizarEstado/<int:id>', actualizarEstadoVendedor, name='ModificarEstadoVendedor'),
    

#----------------------------LOGAUT--------------------------------------------------------------
    path('MYL/vendedor/Salir', logoutVendedor, name='salirVendedor'),





# ________________________________ Cliente________________________________________________________________
    path('MYL/cliente/', indexCliente, name='cliente'),
#--------------------------CATALOGO------------------------------------------------------------------
    path('MYL/cliente/catalogo', catalogoCLiente, name='clienteCatalogo'),
    path('cliente/agregar_a_Carrito/<int:id>', agregarCarritoCliente, name='agregarCarritoCliente'),

    #--------------------------------------------CARRITO---------------------------------------------------------------
    path('MYL/cliente/carrito', carritoCliente, name='clienteCarrito'),
    path('cliente/sumarleProducto/<int:id>', sumarleProductoCliente, name='sumarleProductoCliente'),
    path('cliente/eliminar_producto_Carrito/<int:id>', eliminarProductoCarritoCliente, name='eliminarProductoCarritoCliente'),
    path('cliente/restar_producto_Carrito/<int:id>', restar_productoCliente, name='restarProductoCarritoCliente'),

#-----------------------------PEDIDO------------------------------------------------------------
    path('MYL/cliente/pedidos', clientePedido, name='clientePedido'),
    path('cliente/actualizarEstado/<int:id>', actualizarEstadoCliente, name='ModificarEstadoCliente'),
#------------------------------PERFIL---------------------------------------------------------
    path('MYL/cliente/perfil', clientePerfil, name='clientePerfil'),
    path('MYL/cliente/perfil/editarPerfil', editarPerfilClient, name='editarPerfilClient'),
    path('MYL/cliente/perfil/editarContra', editarContraClient, name='editarContraClient'),
# -----------------------------Logout----------------------------------------
    path('MYL/cliente/Salir', logoutCliente, name='salirCliente'),


] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


