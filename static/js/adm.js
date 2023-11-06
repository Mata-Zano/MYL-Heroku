function ventasAdm() {
    window.location.href = "gestionVentas";
   }
   function usuariosAdm() {
    window.location.href = "gestionUsuarios";
   }
   function perfilAdm() {
    window.location.href = "perfil";
   }
   
   function crearCuenta() {
    window.location.href = "crearCuenta";
   }
   
   function administrarCuenta() {
    window.location.href = "administrarCuenta";
   }
   
   function volverCrear() {
    window.location.href = "";
   }
   
   function confirmacionEliminacion(){
    return confirm('¿Estás seguro de que quieres eliminar estos usuarios?')
   }
   function confirmacionModificacion(){
      return confirm('¿Estás seguro de que quieres modificar estos usuarios?');
   }
   
   document.addEventListener("DOMContentLoaded", function() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    const modificarBtn = document.querySelector('button[name="action"]');
    const eliminarBtn = document.querySelector('button[name="action"]');
    // const form = document.getElementById("administrarForm");
  
    checkboxes.forEach(function(checkbox) {
      checkbox.addEventListener("change", function() {
        const anyChecked = Array.from(checkboxes).some((checkbox) => checkbox.checked);
        modificarBtn.disabled = !anyChecked;
        eliminarBtn.disabled = !anyChecked;
      });
    });});
  
//     modificarBtn.addEventListener("click", function(event) {
//       form.querySelector('input[name="action"]').value = "modificar";
//     });
  
//     eliminarBtn.addEventListener("click", function(event) {
//       form.querySelector('input[name="action"]').value = "eliminar";
//     });
  
//     form.addEventListener("submit", function(event) {
//       if (!form.querySelector('input[name="action"]').value) {
//         event.preventDefault();
//       }
//     });
//   });
  
   