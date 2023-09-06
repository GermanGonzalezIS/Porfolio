Característica: Como usuario gestor del sistema 
                quiero poder asignar 3 revisores a una publicación
                para que pueda ser revisada.
    
    Escenario: Asignar 3 revisores cancelado
        Dado que ingreso al sistema con la dirección "gestion-publicaciones/lista-publicaciones"
        Y presiono el botón ver de la primera publicación de la lista
        Y presiono el botón "Asignar revisores ahora"
        Y selecciono los primeros 3 revisores de la lista
        Cuando presiono el botón "Cancelar"
        Entonces puedo ver la página "Detalle de Publicación"
    
    Escenario: Asignar más de 3 revisores
        Dado que ingreso al sistema con la dirección "gestion-publicaciones/lista-publicaciones"
        Y presiono el botón ver de la primera publicación de la lista
        Y presiono el botón "Asignar revisores ahora"
        Cuando selecciono los primeros 3 revisores de la lista
        Entonces no puedo seleccionar el 4 revisor
    
    Escenario: Asignar menos de 3 revisores
        Dado que ingreso al sistema con la dirección "gestion-publicaciones/lista-publicaciones"
        Y presiono el botón ver de la primera publicación de la lista
        Y presiono el botón "Asignar revisores ahora"
        Cuando selecciono los primeros 2 revisores de la lista
        Entonces no puedo presionar el botón Aceptar
    
    Escenario: Asignar 3 revisores correctamente
        Dado que ingreso al sistema con la dirección "gestion-publicaciones/lista-publicaciones"
        Y presiono el botón ver de la primera publicación de la lista
        Y presiono el botón "Asignar revisores ahora"
        Y selecciono los primeros 3 revisores de la lista
        Cuando presiono el botón "Aceptar"
        Entonces puedo ver a los 3 revisores en el detalle de la publicación