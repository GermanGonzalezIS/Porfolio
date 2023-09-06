Característica: Modificar permisos usuario
                Como usuario administrador del sistema 
                quiero  modificar los permisos a una cuenta de usuario ya existente
                para que el usuario pueda realizar tareas  específicas dentro del sistema.
    
    Escenario: Asignar permisos usuario correctamente
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Y presiono el botón de modificar correspondiente a un registro de la lista
        Y capturo "modificadopermisos123" en el password
        Y selecciono el permiso Administrador
        Y selecciono el permiso Gestor
        Y selecciono el permiso Postulante
        Y selecciono el permiso Revisor
        Cuando presiono el botón "Guardar"
        Entonces puedo ver la página de "Lista de usuarios"