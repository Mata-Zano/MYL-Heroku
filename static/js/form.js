
const selectUsuario = document.getElementById('id_usuario');
const inputNombre = document.getElementById('id_nombre');
const inputApellido = document.getElementById('id_apellido');

selectUsuario.addEventListener('change', (event) => {
    alert("HOLA")
  // Obtener los datos del usuario seleccionado
  const usuarioSeleccionado = event.target.value;
  // Actualizar los inputs de nombre y apellido
  inputNombre.value = usuarioSeleccionado.nombre;
  inputApellido.value = usuarioSeleccionado.apellido;
});