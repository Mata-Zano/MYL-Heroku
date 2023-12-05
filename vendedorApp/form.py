from django import forms
from administradorApp.models import Usuarios,Pedido, DetallePedido


class PedidoForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(
        queryset=None,  # El queryset se actualizará dinámicamente en el formulario
        to_field_name='id',  # El campo del modelo a mostrar en lugar de str()
    )

    class Meta:
        model = Pedido
        fields = ['usuario', 'estado', 'nombre', 'apellido', 'fechaEntrega', 'total', 'direccion', 'ciudad', 'comuna',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].widget = forms.Select(attrs={'id': 'id_usuario'})
        # Actualizar el queryset para que muestre nombres de usuario en lugar de "Usuario object()"
        self.fields['usuario'].queryset = Usuarios.objects.filter(cuenta_id__rol__nombre = 'cliente')
        # Opcional: También puedes personalizar cómo se muestra cada opción en el widget
        # En este caso, estamos mostrando el nombre y apellido del usuario
        self.fields['usuario'].label_from_instance = lambda obj: f"{obj.nombre} {obj.apellido}"
        self.fields['nombre'].widget = forms.TextInput(attrs={'id': 'id_nombre'})
        self.fields['apellido'].widget = forms.TextInput(attrs={'id': 'id_apellido'})

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})



class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['pedido', 'producto', 'cantidad', 'precio_unitario', 'precio_total']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
