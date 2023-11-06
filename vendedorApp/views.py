from django.shortcuts import render

# Create your views here.
def indexVendedor (request):
    return render(request, 'vendedorAppTemplates/indexVendedor.html')