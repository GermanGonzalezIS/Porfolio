var limite = 3;
const button = document.getElementById('id_aceptar');
button.disabled = true;
$('input.form-check-input').change(function() {
    if($("input:checked").length > limite) {
        this.checked = false;
        button.disabled = false;
    }
    else if($("input:checked").length == limite){
        button.disabled = false; 
    }
    else{
        button.disabled = true; 
    }
});