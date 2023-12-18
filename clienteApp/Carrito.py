from administradorApp.models import Producto
class Carrito:

    def __init__(self, usuario):
        self.usuario = usuario
        self.carrito = getattr(usuario, 'carrito', {}) or {}

    def agregar(self, producto_id, cantidad):
        producto = Producto.objects.get(id=producto_id)
        cantidad = int(cantidad)
        if cantidad <= producto.stock:
            id = str(producto.id)
            
            if id not in self.carrito.keys():
                self.carrito[id] = {
                    "producto_id": producto.id,
                    "nombre": producto.nombre,
                    "precio": producto.precio * cantidad,
                    "precioUnitario": producto.precio,
                    "descripcion": producto.descripcion,
                    "cantidad": cantidad,
                }
                self.guardar_carrito()
                return True
            else:
                if cantidad <= (producto.stock - self.carrito[id]["cantidad"]):
                    # Actualizar la cantidad y el precio en el carrito
                    self.carrito[id]["cantidad"] += cantidad
                    self.carrito[id]["precio"] += (producto.precio * cantidad)
                    self.guardar_carrito()
                    return True
                else:
                    return False
        else:
            return False
        
    def sumarle (self, producto):
        id = str(producto.id)
        stock_disponible = int(producto.stock)
        if self.carrito[id]["cantidad"] <= stock_disponible:
            if self.carrito[id]["cantidad"] <= int(producto.stock):
                self.carrito[id]["cantidad"] += 1
                self.carrito[id]["precio"] += producto.precio
                self.guardar_carrito()
                return True
                
        else:
            print("Stock agregar")
            return False
         

    def guardar_carrito(self):
        if self.usuario and hasattr(self.usuario, 'carrito'):
            self.usuario.carrito = self.carrito
            self.usuario.save()

    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, producto):
        id = str(producto.id)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["precio"] -= producto.precio
            if self.carrito[id]["cantidad"] <= 0:
                self.eliminar(producto)
            self.guardar_carrito()


    
    def calcular_precio_total(self):
        precio_total = sum(item["precio"] for item in self.carrito.values())
        return precio_total
    
    def limpiar(self):
        self.carrito = {}  # Limpiar el carrito
        self.guardar_carrito()