Característica: Como usuario gestor del sistema 
                quiero poder cambiar un revisor
                si este rechazo la solicitud de revisión.

    Escenario: Cambiar revisor cancelado
        Dado que ingreso al sistema con la dirección "gestion-publicaciones/lista-publicaciones"
        Y presiono el botón ver de la segunda publicación de la lista
        Y presiono el botón "Cambiar revisor"
        Y selecciono el primer revisor de la lista
        Cuando presiono el botón "Cancelar"
        Entonces puedo ver la página "Detalle de Publicación"
    
    Escenario: Asignar más de 1 revisores
        Dado que ingreso al sistema con la dirección "gestion-publicaciones/lista-publicaciones"
        Y presiono el botón ver de la segunda publicación de la lista
        Y presiono el botón "Cambiar revisor"
        Cuando selecciono el primer revisor de la lista
        Entonces no puedo seleccionar el segundo revisor
    
    Escenario: Asignar menos de 1 revisores
        Dado que ingreso al sistema con la dirección "gestion-publicaciones/lista-publicaciones"
        Y presiono el botón ver de la segunda publicación de la lista
        Y presiono el botón "Cambiar revisor"
        Entonces no puedo presionar el botón Aceptar
    
    Escenario: Cambiar revisor correctamente
        Dado que ingreso al sistema con la dirección "gestion-publicaciones/lista-publicaciones"
        Y presiono el botón ver de la segunda publicación de la lista
        Y presiono el botón "Cambiar revisor"
        Y selecciono el primer revisor de la lista
        Cuando presiono el botón "Aceptar"
        Entonces puedo ver a los 3 revisores en el detalle de la publicación