from django.shortcuts import render

def indexCliente (request):
    return render(request, 'clienteAppTemplates/indexCliente.html')

# Create your views here.
