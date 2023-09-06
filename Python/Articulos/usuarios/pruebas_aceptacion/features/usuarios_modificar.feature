Característica: Modificar usuario
    Como usuario administrador del sistema quiero poder modificar una cuenta de usuario ya existente
    para tener sus datos actualizados.

    Escenario: Modificar usuario correctamente
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Y presiono el botón de modificar correspondiente a un registro de la lista
        Y capturo "Modificado" en el nombre
        Y capturo "Modificado" en el apellido
        Y capturo "usuario_modificado" en el username
        Y capturo "modificado@gmail.com" en correo
        Y capturo "modificado123" en el password
        Cuando presiono el botón "Guardar"
        Entonces puede ver al usuario "Modificado" en la lista de usuarios

    Escenario: Modificar usuario con nombre de usuario existente
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Y presiono el botón de modificar correspondiente a un registro de la lista
        Y capturo "admin_juan" en el username
        Y capturo "modificado123" en el password
        Cuando presiono el botón "Guardar"
        Entonces puede ver el mensaje "Ya existe un usuario con ese nombre." en la página
    
    Escenario: Modificar usuario con correo ya existente
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Y presiono el botón de modificar correspondiente a un registro de la lista
        Y capturo "admin_juan@gmail.com" en correo
        Y capturo "modificado123" en el password
        Cuando presiono el botón "Guardar"
        Entonces puede ver el mensaje "Ya existe un/a Usuario con este/a Correo electronico." en la página

    Escenario: Modificar usuario sin nombre
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Y presiono el botón de modificar correspondiente a un registro de la lista
        Y capturo "" en el nombre
        Y capturo "modificado123" en el password
        Cuando presiono el botón "Guardar"
        Entonces sigo en la misma página con el título "Modificar usuario"

    
    Escenario: Modificar usuario sin primer apellido
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Y presiono el botón de modificar correspondiente a un registro de la lista
        Y capturo "" en el apellido
        Y capturo "modificado123" en el password
        Cuando presiono el botón "Guardar"
        Entonces sigo en la misma página con el título "Modificar usuario"
    
    Escenario: Modificar usuario sin username
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Y presiono el botón de modificar correspondiente a un registro de la lista
        Y capturo "" en el username
        Y capturo "modificado123" en el password
        Cuando presiono el botón "Guardar"
        Entonces sigo en la misma página con el título "Modificar usuario"
    
    Escenario: Modificar usuario sin password
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Y presiono el botón de modificar correspondiente a un registro de la lista
        Cuando presiono el botón "Guardar"
        Entonces sigo en la misma página con el título "Modificar usuario"
    
    Escenario: Modificar usuario con segundo apellido
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Y presiono el botón de modificar correspondiente a un registro de la lista
        Y capturo "Modificado" en el segundo apellido
        Y capturo "modificado123" en el password
        Cuando presiono el botón "Guardar"
        Entonces puede ver al usuario "Modificado" en la lista de usuarios
