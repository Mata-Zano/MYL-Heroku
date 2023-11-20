from django.contrib import admin
# from django.contrib.auth.models import Group, Permission
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType
# from administradorApp.models import Cuenta


# def setup_groups_and_permissions():
#     admin_group, created = Group.objects.get_or_create(name='Administrador')
#     supervisor_group, created = Group.objects.get_or_create(name='Supervisor')
#     cliente_group, created = Group.objects.get_or_create(name='Cliente')
#     vendedor_group, created = Group.objects.get_or_create(name='Vendedor')


#     # Asignar permisos a cada grupo (en este ejemplo, el permiso 'view_cuenta')
#     content_type = ContentType.objects.get_for_model(Cuenta)
#     permission = Permission.objects.get(
#         codename='view_cuenta',
#         content_type=content_type,
#     )
#     admin_group.permissions.add(permission)
#     supervisor_group.permissions.add(permission)
#     cliente_group.permissions.add(permission)
#     vendedor_group.permissions.add(permission)

#     try:

#         cuenta = Cuenta.objects.get(correo='adm@adm.com')
#         usuario = cuenta.usuarios  # Obtiene el objeto Usuarios asociado a la cuenta
#         if cuenta.rol.id == 1:
#             admin_group.user_set.add(usuario.cuenta.user)  # Agrega el usuario al grupo
#         elif cuenta.rol.id == 2:
#             supervisor_group.user_set.add(usuario.cuenta.user)
#         elif cuenta.rol.id == 3:
#             cliente_group.user_set.add(usuario.cuenta.user)
#         elif cuenta.rol.id == 4:
#             vendedor_group.user_set.add(usuario.cuenta.user)
#     except Cuenta.DoesNotExist:
#         print('No existe la cuenta con el correo mencionado.')

# # Ejecuta la función cuando se inicia la aplicación
# setup_groups_and_permissions()

# # Register your models here.
