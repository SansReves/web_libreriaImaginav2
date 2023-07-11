
function formatRut(input) {
    // Obtener el valor del campo
    let rut = input.value;
  
    // Remover todos los caracteres excepto dígitos y "K"
    rut = rut.replace(/[^0-9K]/gi, '');
  
    // Agregar el guion después de los primeros 6 dígitos
    if (rut.length > 8) {
      rut = rut.slice(0, -1) + '-' + rut.slice(-1);
      rut = rut.slice(0, -5) + '.' + rut.slice(-5);
      rut = rut.slice(0, -9) + '.' + rut.slice(-9);
    }
  
    // Mostrar el valor formateado en el campo
    input.value = rut;
  }