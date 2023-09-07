let form_ben = document.getElementById("form_beneficiario");

// Se ejecuta cada vez que la página carga
window.onload = function() {
    // Inicialmente se oculta el formulario del beneficiario
    form_ben.style = "display:None";
    mostrarFormBeneficiario();
  };

function mostrarFormBeneficiario(){
    // Se copia el valor de la CURP del tramite específico al formulario
    // del beneficiario
    let curpElements = document.getElementsByName('curp');
    let curp = curpElements[0].value;
    curpElements[1].value = curp;
    let formularioCompleto = detectarFormularioCompletado();

    // Si ya se han completado todos los elementos requeridos del formulario 
    // del trámite en cuestión, entonces se muestran los campos del beneficiario
    if(formularioCompleto){
        // Se muestra el formulario del beneficiario
        form_ben.style = "display: block";
        let formTramite = document.getElementById("tramite");
        desabilitarElementos(formTramite);
        // Se desaparecen los botones de regresar y enviar el formulario de los documentos
        // del tramite.
        let botones = document.getElementsByName("botones-formulario");
        botones[0].style = "display:None";
        botones[1].style = "display:None";
        // Se recorre la página hacia los formularios del beneficiario
        location.href = "#form_beneficiario";
    }
}

// Se comprueba que los datos del formulario específico se hayan completado
function detectarFormularioCompletado() {
    let docs = document.getElementsByClassName('elemento-tramite');
    let count = 0;
    
    console.log(docs);
    for(let x=0;x<docs.length;x++){
        console.log(docs[x].value);
        if(docs[x].type == "checkbox") {
            if(docs[x].checked){
                count++;
            }   
        } else {
            if(docs[x].value.length > 0)  {
                count++;
            }
        }
    }

    // Todos los campos fueron llenados
    if(docs.length == count) {
        return true;
    }
    // Hay algún campo que falta
    return false;
}

function desabilitarElementos(formulario) {
    // Se deshabilitan los elementos del formulario de los documentos del tramite
    let elements = formulario.elements;
    for (let i = 0; i < elements.length; i++) {
        elements[i].disabled = true;
    }
}

// Se autollena el selector de las localidades en función del municipio elegido
$('#id_municipio').on('change', function () { 
    var token = $('[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        type: "post",
        url: `/catalogos/localidades/`,
        data: {'id':this.value,'csrfmiddlewaretoken':token},
        success: function (response) {
            var html = "";
            if(response[0].hasOwnProperty('error')) {
                html+=`<option value="">${response[0].error}</option>`;
            }
            else {
                html+=`<option value="">---------</option>`;
                $.each(response, function(llave,valor) {
                    html+=`<option value="${valor.id}">${valor.nombre}</option>`;
                });
            }
            $("#id_localidad").html(html);
            $("#id_localidad").trigger("change");
        },
        error: function(param) {
            console.log('Error en la petición');
            $("#id_localidad").html(`<option value="">---------</option>`);
            $("#id_localidad").trigger("change");
        }
    });
});

    
// Se autollena el selector de los asentamientos en función de la localidad elegida
$('#id_localidad').on('change', function () { 
    var token = $('[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        type: "post",
        url: `/catalogos/asentamientos/`,
        data: {'id':this.value,'csrfmiddlewaretoken':token},
        success: function (response) {
            var html = "";
            if(response[0].hasOwnProperty('error')) {
                html+=`<option value="">${response[0].error}</option>`;
            }
            else {
                html+=`<option value="">---------</option>`;
                $.each(response, function(llave,valor) {
                    html+=`<option value="${valor.id}">${valor.nombre}</option>`;
                });
            }
            $("#id_asentamiento").html(html);
        },
        error: function(param) {
            console.log('Error en la petición');
            $("#id_asentamiento").html(`<option value="">---------</option>`);
        }
    });
}); 