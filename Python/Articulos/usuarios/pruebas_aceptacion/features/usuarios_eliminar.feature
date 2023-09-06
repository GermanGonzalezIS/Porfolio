Característica: Eliminar usuario
    Como usuario administrador quiero eliminar un usuario.

    Escenario: Eliminado correcto
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Y presiono el botón de eliminar correspondiente a un registro de la lista
        Y presiono el botón "Sí, estoy seguro"
        Entonces puedo ver la alerta "¡Usuario eliminado exitosamente!" en la página

    Escenario: Eliminado cancelado
        Dado que ingreso al sistema con la dirección "usuarios/lista"
        Y presiono el botón de eliminar correspondiente a un registro de la lista
        Y presiono el botón "Cancelar"
        Entonces puedo ver la página de "Lista de usuarios"