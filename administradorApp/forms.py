from django import forms
from django.forms import DateTimeInput, ModelForm, ModelChoiceField
from .models import Rol, Cuenta, Usuarios, Categoria, Producto, Pedido

class UsuariosForm(ModelForm):
    rol = ModelChoiceField(queryset=Rol.objects.all())
    nombre = forms.CharField(max_length=150)
    apellido = forms.CharField(max_length=150)
    telefono = forms.IntegerField()
    correo = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirmar_password = forms.CharField(widget=forms.PasswordInput)
    direccion = forms.CharField(max_length=20, label='Dirección')
    ciudad = forms.CharField(max_length=20)
    comuna = forms.CharField(max_length=20)


    class Meta:
        model = Usuarios
        fields = ['rol', 'nombre', 'apellido', 'telefono', 'correo','direccion', 'ciudad','comuna']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")
        telefono = cleaned_data.get('telefono')



        if password and confirmar_password and password != confirmar_password :
            self.add_error('confirmar_password',"Las contraseñas no coinciden.")

        if telefono and len(str(telefono)) > 8:
            self.add_error('telefono', "Número de teléfono supera los 8 dígitos.")


        return cleaned_data
    
class ProductosForm(ModelForm):
    imagen_url = forms.TextInput()
    categoria = ModelChoiceField(queryset=Categoria.objects.all())
    nombre = forms.CharField(max_length=20)
    descripcion = forms.Textarea()
    stock = forms.IntegerField()
    precio = forms.FloatField()
    class Meta:
        model = Producto
        fields = ['imagen_url' , 'categoria', 'nombre', 'stock', 'precio','descripcion']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


#----------EDITAR------------------
class EditarUsuariosForm(ModelForm):
    nombre = forms.CharField(max_length=150)
    apellido = forms.CharField(max_length=150)
    telefono = forms.CharField()
    direccion = forms.CharField(max_length=20, label='Dirección')
    ciudad = forms.CharField(max_length=20)
    comuna = forms.CharField(max_length=20)

    class Meta:
        model = Usuarios
        fields = ['nombre', 'apellido', 'telefono', 'direccion', 'ciudad', 'comuna']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
class EditarPerfilForm(ModelForm):
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
    
class EditarPassword(ModelForm):

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
    

class EditarEstado(ModelForm):
    
    class Meta:
        model = Pedido
        fields = ['estado', 'fechaEntrega']

        widgets = {
            'fechaEntrega': DateTimeInput(attrs={'type': 'datetime-local'}),

        }
        labels = {
            'fechaEntrega': 'Fecha de Entrega:',
            'estado': 'Estados:',

        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control text-center'})
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    


