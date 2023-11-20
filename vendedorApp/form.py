from django import forms
from administradorApp.models import Producto,Pedido, DetallePedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['usuario', 'estado', 'nombre', 'apellido', 'fechaEntrega', 'total']

class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['pedido', 'producto', 'cantidad', 'precio_unitario', 'precio_total']