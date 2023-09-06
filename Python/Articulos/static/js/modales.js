function muestraModal(url){
    document.getElementById('formEliminar').action = url;
    document.getElementById('modalCuerpo').innerHTML = 
    `¿Está seguro que desea eliminar el registro?`;
}

function eliminarRegistro(url){
    Swal.fire({
        title: '¿Está seguro que desea eliminar el registro?',
        text: "¡No podrás revertir esta acción!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, estoy seguro',
        cancelButtonText: 'Cancelar'
    }).then(function(result) {
        if (result.isConfirmed) {
            document.getElementById('formEliminarRegistro').action = url;
            document.getElementById('formEliminarRegistro').submit();
        }
    })
}