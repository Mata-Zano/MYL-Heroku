from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class Rol(models.Model):
    ROLES = [
       ('administrador', 'Administrador'),
       ('supervisor', 'Supervisor'),
       ('cliente', 'Cliente'),
       ('vendedor', 'Vendedor'),
   ]
    nombre = models.CharField(max_length=50,choices=ROLES, default='Administrador')
    descripcion = models.CharField(max_length=150,null=True)
    def __str__(self):
        return self.nombre

class Cuenta(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    correo =  models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    



class Usuarios(models.Model):
    cuenta = models.OneToOneField(Cuenta, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=20)
    telefono = models.CharField(max_length=50)
    
    @classmethod
    def create_user(cls, rol, correo, password, nombre, apellido, telefono):
        cuenta = cls.objects.create(rol=rol, correo=correo, password=password)
        return Usuarios.objects.create(cuenta=cuenta, nombre=nombre, apellido=apellido, telefono=telefono)
    
class Categoria(models.Model):
    CATEGORIA = [
       ('alimentoMascotas', 'Alimento de Mascotas'),
       ('bebestibles', 'Bebestibles'),
       ('carbon', 'Carbón'),
       ('abarrotes', 'Abarrotes'),
   ]
    nombre = models.CharField(max_length=50, choices=CATEGORIA,)
    descripccion = models.CharField(max_length=50)
    def __str__(self):
        return self.get_nombre_display()
    
    
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=250)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    stock = models.IntegerField()
    precio = models.FloatField()

class Pedido(models.Model):
    usuario = models.ForeignKey(
        Usuarios, on_delete=models.SET_NULL,
        related_name="pedidos",
        null=True
    )
    estado = models.CharField(
        max_length=50,
        choices=(
            ("enProceso", "En proceso"),
            ("enviado", "Enviado"),
            ("cancelado", "Cancelado"),
            ("entregado", "Entregado"),
        ),
        default="en_proceso",
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaEntrega = models.DateTimeField(null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    productos = models.ManyToManyField(
        Producto,
        through='DetallePedido',
        through_fields=('pedido', 'producto'),
        related_name='pedidos'
    )
    direccion = models.CharField(max_length=250, default='0')
    comuna = models.CharField(max_length=250, default='0')
    ciudad = models.CharField(max_length=250, default='0')
    def __str__(self):
        return f"Pedido {self.id}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE,
        related_name="detalles"
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL,
        related_name="detalles",
        null=True
    )
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle de pedido {self.id}"

    def estado(self):
        return self.pedido.get_state()
    
# GRUPOS Y PERMISOS
# admin_group = Group.objects.get_or_create(name='Administrador')
# # --------------------------PERMISOS SUPERVISOR-------------------------
# # admin_index_administrador = Permission.objects.create(
# #     name='Acceder a la vista indexAdministrador',
# #     content_type=ContentType.objects.get_for_model(Cuenta),
# #     codename='index_administrador',
# # )

# # Crear el grupo 'Supervisor'
# supervisor_group = Group.objects.get_or_create(name='Supervisor')
# # Crear el grupo 'Cliente'
# cliente_group = Group.objects.get_or_create(name='Cliente')
# # Crear el grupo 'Vendedor'
# vendedor_group = Group.objects.get_or_create(name='Vendedor')