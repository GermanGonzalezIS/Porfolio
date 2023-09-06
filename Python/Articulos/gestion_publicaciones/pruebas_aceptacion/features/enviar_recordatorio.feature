Característica: Como usuario gestor del sistema 
                quiero poder enviar un correo electrónico a un 
                revisor de una publicación con un solo click
                para recordarle que tiene una revisión pendiente.
    
    Escenario: Envio recordatorio correcto
        Dado que ingreso al sistema con la dirección "gestion-publicaciones/lista-publicaciones"
        Y presiono el botón ver de la segunda publicación de la lista
        Cuando presiono el botón "Envíar recordatorio"
        Entonces puedo ver el mensaje "Se envió recordatorio al usuario"