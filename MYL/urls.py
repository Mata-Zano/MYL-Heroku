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
from django.urls import path
from principalApp.views import *
from loginApp.views import *
from administradorApp.views import *
from vendedorApp.views import *
from clienteApp.views import *

urlpatterns = [
# ________________________________________________________________________________________________

    path('admin/', admin.site.urls),
    path('',Index, name='index'),
    path('catálogo/',Catalogo, name='Catalogo'),
    path('contacto/',Contacto, name='Contacto'),
    path('sobreNosotros/',Sobre, name='Sobre'),

# ---------------------------------RECUPERAR---------------------------------------------
    path('ingreso/',Ingreso, name='login'),
    path('ingreso/recuperar/',Recuperar, name='recuperar'),

# _____________________________________________________________________________________________
    #ADM
    path('MYL/administrador/', indexAdministrador, name='administrador'),
    path('MYL/administrador/gestionVentas/', gestionVentas, name='ventasAdm'),
    path('MYL/administrador/gestionUsuarios/', gestionUsuarios, name='usuariosAdm'),
    path('MYL/administrador/perfil/', perfilAdm, name='perfilAdm'),
    # Gestion de cuentas adm
    path('MYL/administrador/gestionUsuarios/crearCuenta/', crearCuentaAdm, name='crearCuenta'),
    path('MYL/administrador/gestionUsuarios/administrarCuenta/', administrarCuentaAdm, name='administrarCuenta'),
    #Lista Productos 
    path('MYL/administrador/gestionVentas/listaProductos/', listProductos, name='listaProductos'),
    path('MYL/administrador/gestionVentas/listPedidos/', listPedidos, name='listaPedidos'),
    path('MYL/administrador/gestionVentas/agregarProductos/', agregarProducto, name='agregarProductos'),
    path('eliminarProyecto/<int:id>', eliliminarProducto, name='eliminarProductos'),
    path('actualizarProyecto/<int:id>', actualizarProducto, name='actualizarProducto'),
# _____________________________________________________________________________
    # VENDEDOR
    path('MYL/vendedor/', indexVendedor, name='vendedor'),
    path('MYL/vendedor/catalogo', catalogoVendedor, name='vendedorCatalogo'),
    path('MYL/vendedor/carrito', carritoVendedor, name='vendedorCarrito'),
    path('MYL/vendedor/perfil', vendedorPerfil, name='vendedorPerfil'),
    path('MYL/vendedor/pedidos', vendedorPedido, name='vendedorPedido'),
    path('MYL/vendedor/Salir', logoutVendedor, name='salirVendedor'),





    # path('carritoVendedor/<int:id>', agregar_producto, name='agregarCarrito'),.
    #CLIENTE
    path('MYL/cliente/', indexCliente, name='cliente'),

] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


