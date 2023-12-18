from django import forms

class mensajeContactanos(forms.Form):
    nombre = forms.CharField()
    email = forms.EmailField()
    asunto = forms.CharField()
    mensaje = forms.CharField(widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
