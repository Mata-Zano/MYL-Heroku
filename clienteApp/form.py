from django import forms
from administradorApp.models import Usuarios,Pedido, DetallePedido,Cuenta

class PedidoForm(forms.ModelForm):
    usuario_destino = forms.ModelChoiceField(
        queryset=None,  # El queryset se actualizará dinámicamente en el formulario
        to_field_name='id',  # El campo del modelo a mostrar en lugar de str()
        label='Clientes Registrados'
    )

    class Meta:
        model = Pedido
        fields = ['usuario_destino',  'nombre', 'apellido','telefono','fechaEntrega', 'total', 'direccion', 'ciudad', 'comuna']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar el campo usuario_destino para mostrar los clientes registrados
        self.fields['usuario_destino'].widget = forms.Select(attrs={'id': 'id_usuario_destino'})
        self.fields['usuario_destino'].queryset = Usuarios.objects.filter(cuenta__rol__nombre='cliente')
        self.fields['usuario_destino'].label_from_instance = lambda obj: f"{obj.nombre} {obj.apellido}"

        # Configurar otros campos del formulario
        self.fields['nombre'].widget = forms.TextInput(attrs={'id': 'id_nombre'})


        self.fields['apellido'].widget = forms.TextInput(attrs={'id': 'id_apellido'})
        self.fields['direccion'].widget = forms.TextInput(attrs={'id': 'id_direccion'})
        self.fields['comuna'].widget = forms.TextInput(attrs={'id': 'id_comuna'})
        self.fields['ciudad'].widget = forms.TextInput(attrs={'id': 'id_ciudad'})
        
        self.fields['usuario_destino'].widget.attrs['style'] = 'display: none;'

        # Agregar clases al formulario
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


class EditarEstado(forms.ModelForm):
    
    class Meta:
        model = Pedido
        fields = ['estado']
        labels = {
            'estado': 'Estados:',

        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            self.fields['estado'].widget = forms.Select(choices=[
            ("Entregado", "Entregado"),
            ("Cancelado", "Cancelado"),
            ], attrs={'class': 'form-control text-center'})
            field.widget.attrs.update({'class': 'form-control text-center'})
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    



class EditarPerfilForm(forms.ModelForm):
    nombre = forms.CharField(max_length=150)
    apellido = forms.CharField(max_length=150)
    telefono = forms.CharField()
    direccion = forms.CharField(max_length=20, label='Dirección')
    ciudad = forms.CharField(max_length=20)
    comuna = forms.CharField(max_length=20)

    class Meta:
        model = Usuarios
        fields = ['nombre', 'apellido', 'telefono', 'direccion', 'ciudad', 'comuna', ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
class EditarPassword(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    newPassword = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Cuenta
        fields = ['password']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control text-center'})
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        newPassword = cleaned_data.get("password")

        
        return cleaned_data
    