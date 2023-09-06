Característica: Crear usuario
    Como usuario administrador del sistema quiero poder crear una cuenta de usuario
    para un trabajador del INIFAP para que pueda comenzar a utilizar el sistema.

    Escenario: Crear usuario correctamente
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Y hago click en el botón "Nuevo usuario"
        Y capturo "Juan" en el nombre
        Y capturo "Ramírez" en el apellido
        Y capturo "admin_juan" en el username
        Y capturo "admin_juan@gmail.com" en correo
        Y capturo "juanR123" en el password
        Cuando presiono el botón "Guardar"
        Entonces puede ver al usuario "admin_juan" en la lista de usuarios

    Escenario: Crear usuario con nombre de usuario existente
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Y hago click en el botón "Nuevo usuario"
        Y capturo "Juan" en el nombre
        Y capturo "Pacheco" en el apellido
        Y capturo "admin_juan" en el username
        Y capturo "juanPacheco@gmail.com" en correo
        Y capturo "juan47887878" en el password
        Cuando presiono el botón "Guardar"
        Entonces puede ver el mensaje "Ya existe un usuario con ese nombre." en la página
    
    Escenario: Crear usuario con correo ya existente
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Y hago click en el botón "Nuevo usuario"
        Y capturo "Juan" en el nombre
        Y capturo "Pacheco" en el apellido
        Y capturo "admin_juan_pacheco" en el username
        Y capturo "admin_juan@gmail.com" en correo
        Y capturo "juan47887878" en el password
        Cuando presiono el botón "Guardar"
        Entonces puede ver el mensaje "Ya existe un/a Usuario con este/a Correo electronico." en la página

    Escenario: Crear usuario sin nombre
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Y hago click en el botón "Nuevo usuario"
        Y capturo "Pacheco" en el apellido
        Y capturo "admin_juan_pacheco" en el username
        Y capturo "admin_juan_pacheco@gmail.com" en correo
        Y capturo "juan47887878" en el password
        Cuando presiono el botón "Guardar"
        Entonces sigo en la misma página con el título "Nuevo usuario"

    
    Escenario: Crear usuario sin primer apellido
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Y hago click en el botón "Nuevo usuario"
        Y capturo "Juan" en el nombre
        Y capturo "admin_juan_pacheco" en el username
        Y capturo "admin_juan_pacheco@gmail.com" en correo
        Y capturo "juan47887878" en el password
        Cuando presiono el botón "Guardar"
        Entonces sigo en la misma página con el título "Nuevo usuario"
    
    Escenario: Crear usuario sin username
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Y hago click en el botón "Nuevo usuario"
        Y capturo "Juan" en el nombre
        Y capturo "Pacheco" en el apellido
        Y capturo "admin_juan_pacheco@gmail.com" en correo
        Y capturo "juan47887878" en el password
        Cuando presiono el botón "Guardar"
        Entonces sigo en la misma página con el título "Nuevo usuario"
    
    Escenario: Crear usuario sin password
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Y hago click en el botón "Nuevo usuario"
        Y capturo "Juan" en el nombre
        Y capturo "Pacheco" en el apellido
        Y capturo "admin_juan_pacheco" en el username
        Y capturo "admin_juan@gmail.com" en correo
        Cuando presiono el botón "Guardar"
        Entonces sigo en la misma página con el título "Nuevo usuario"
    
    Escenario: Crear usuario con segundo apellido
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Y hago click en el botón "Nuevo usuario"
        Y capturo "Juan" en el nombre
        Y capturo "Pacheco" en el apellido
        Y capturo "Salas" en el segundo apellido
        Y capturo "admin_juan_pacheco" en el username
        Y capturo "admin_juan_pacheco@gmail.com" en correo
        Y capturo "juan47887878" en el password
        Cuando presiono el botón "Guardar"
        Entonces puede ver al usuario "admin_juan" en la lista de usuarios
