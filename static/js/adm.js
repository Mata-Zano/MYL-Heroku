
// ___________________EDITAR_________________________________________
function confirmarEditarPedido(nombre, apellido, id) {
  var confirmacion = confirm('¿Estás seguro de que quieres Editar el pedido de: ' + nombre +" "+ apellido+ ", con identificador: "+ id +'?');
  if (confirmacion) {
    window.location.href = 'eliminarPedido/' + id + '/';
  }
}

function confirmarEditarProducto(nombre, id) {
  var confirmacion = confirm('¿Confirmas tu deseo de editar al siguiente Producto: ' + nombre + '?');
  if (confirmacion) {
  }
}

function confirmarEditarUsuario(nombre, id) {
  var confirmacion = confirm('¿Confirmas tu deseo de editar al siguiente Usuario: ' + nombre + '?');
}
function confirmarEditarPerfil() {
  var confirmacion = confirm('¿Confirmas tu deseo de editar los campos?');
  if (!confirmacion) {
      // Si el usuario hace clic en "Cancelar", evitamos que el formulario se envíe.
      return false;
  }
  // Si el usuario hace clic en "Aceptar", el formulario se enviará normalmente.
  return true;
}
function confirmarEditarContra() {
  var confirmacion = confirm('¿Confirmas tu deseo de cambiar la contraseña ?');
  if (!confirmacion) {
      return false;
  }
  return true;
}
function confirmarEditarEstado() {
  var confirmacion = confirm('¿Confirmas tu deseo de cambiar el estado del pedido?');
  if (!confirmacion) {
      return false;
  }
  return true;
}
// ___________________ELIMINAR_______________________________________
function confirmarEliminacionPedido(nombre, apellido, id) {
  var confirmacion = confirm('¿Estás seguro de que quieres eliminar el pedido de: ' + nombre +" "+ apellido+ ", con identificador: "+ id +'?');
  if (confirmacion) {
    window.location.href = 'eliminarPedido/' + id + '/';
  }
}

function confirmarEliminacionProducto(nombre, id) {
  var confirmacion = confirm('¿Confirmas tu deseo de eliminar al siguiente Producto: ' + nombre + '?');
  if (confirmacion) {
    window.location.href = 'eliminarProducto/' + id + '/';
  }
}


function confirmarEliminacionUsuario(nombre, id) {
  var confirmacion = confirm('¿Confirmas tu deseo de eliminar al siguiente Usuario: ' + nombre + '?');
  if (confirmacion) {
    window.location.href = 'eliminar/' + id + '/';
  }
}




