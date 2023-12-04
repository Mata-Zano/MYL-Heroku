from django import forms


class LoginForm(forms.Form):
    correo = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(label='Contraseña')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
