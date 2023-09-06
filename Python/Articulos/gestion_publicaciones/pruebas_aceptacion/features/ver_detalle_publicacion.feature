Característica: Como usuario gestor del sistema 
                quiero poder revisar el estatus de una publicación
                para saber si ya se revisó.

    Escenario: Ver estatus de una publicación
        Dado que ingreso al sistema con la dirección "gestion-publicaciones/lista-publicaciones"
        Y presiono el botón ver de la primera publicación de la lista
        Entonces puedo ver en la descripción de la publicación su estatus
    
    Escenario: Ver revisores de una publicación
        Dado que ingreso al sistema con la dirección "gestion-publicaciones/lista-publicaciones"
        Y presiono el botón ver de la segunda publicación de la lista
        Entonces puedo ver a los 3 revisores en el detalle de la publicación