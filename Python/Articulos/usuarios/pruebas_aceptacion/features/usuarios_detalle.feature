Característica: Detalle usuario
    Como usuario administrador del sistema quiero poder ver una cuenta de usuario ya existente
    para saber sus datos.

    Escenario: Ver usuario correctamente
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Cuando presiono el botón de ver correspondiente a un registro de la lista
        Entonces puedo ver la página de "Detalle del Usuario"