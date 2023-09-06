Característica: Como usuario postulante del sistema quiero subir una publicación para que ésta sea revisada.

    Escenario: Subo un archivo al sistema exitosamente. 
        Dado que me encuentro logueado en el sistema como usuario postulante
        Y me dirijo a la pantalla de inicio del sistema en la dirección "http://192.168.33.10:8000/"
        Y hago clic en la pestaña "Mis publicaciones"
        Y puedo ver el encabezado "Mis Publicaciones"
        Y hago clic en el enlace "Nueva Publicación"
        Y hago clic en el botón "Elegir archivo" y selecciono el archivo con la ruta "C:/Users/alejv/Downloads/archivo_prueba.docx"
        Y introduzco el título "Prueba Archivo" en el campo designado
        Cuando doy click en el botón "Enviar archivo a revisión"
        Entonces recibo el mensaje "Tu publicación se ha cargado con éxito y pronto será revisada".

    Escenario: El usuario no está logueado como postulante y por tanto no puede ver la opción “Mis publicaciones” en la pantalla de inicio.
        Dado que no me encuentro logueado en el sistema como usuario postulante
        Cuando me dirijo a la pantalla de inicio del sistema en la dirección "http://192.168.33.10:8000/"
        Entonces puedo ver el mensaje "Lo sentimos, tu cuenta de usuario no tiene acciones disponibles"

    Escenario: El usuario no está logueado como postulante y por tanto no puede acceder la página /mis-publicaciones/.
        Dado que no me encuentro logueado en el sistema como usuario postulante
        Cuando me dirijo a la dirección "http://192.168.33.10:8000/mis-publicaciones/"
        Entonces puedo ver el mensaje "Ups! Esta página no está disponible"

    Escenario: El usuario no está logueado como postulante y por tanto no puede acceder la página /mis-publicaciones/nueva.
        Dado que no me encuentro logueado en el sistema como usuario postulante
        Cuando me dirijo a la dirección "http://192.168.33.10:8000/mis-publicaciones/nueva"
        Entonces puedo ver el mensaje "Ups! Esta página no está disponible"
