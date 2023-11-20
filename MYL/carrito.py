class Carrito:
    productos = []
    total = 0
    
    def agregar_producto(self, producto, cantidad):
        self.productos.append((producto, cantidad))
        self.total += producto.precio * cantidad

    def eliminar_producto(self, producto):
        for i, (p, c) in enumerate(self.productos):
            if p == producto:
                del self.productos[i]
                self.total -= p.precio * c
                break

    def calcular_total(self):
        return self.total