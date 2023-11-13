from django.db import models

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
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    stock = models.IntegerField()
    precio = models.FloatField()
