Característica: Como usuario revisor del sistema quiero poder descargar una publicación para realizar mi revisión.

    Escenario: La publicación fue descargada correctamente.
        Dado que ya me encuentro logueado como usuario revisor
        Y me dirijo a la página de inicio del sistema
        Y doy clic en la pestaña "Mis revisiones"
        Y doy clic en el botón "Ver" una publicación
        Cuando doy clic en el botón "Descargar publicación"
        Entonces puedo encontrar el archivo en la carpeta de descargas

    Escenario: El usuario no tiene permiso para descargar el archivo.
        Dado que NO me encuentro logueado en el sistema como usuario revisor
        Cuando me dirijo a la dirección "http://192.168.33.10:8000/revisar-publicaciones/"
        Entonces puedo ver el mensaje "Ups! Esta página no está disponible"


