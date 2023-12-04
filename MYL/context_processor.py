def total_carrito(request):
    total = 0
    if request.user.is_authenticated:
        if "carrito" in request.session.keys():
            for key, value in request.session["carrito"].items():
                acumulado_value = value.get("precio", 0)
                total += int(acumulado_value)
    return {"total_factura": total}
