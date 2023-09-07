
from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = ('first_name','last_name','segundo_apellido','username','curp','email','fecha_nacimiento','entidad', 'admin', 'super_admin')
    """
    def create(self, validated_data):
        usuario = super().create(validated_data)
        usuario.set_password(validated_data['password'])
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        usuario = super().update(instance, validated_data)
        try:
            usuario.set_password(validated_data['password'])
            usuario.save()
        except KeyError:
            pass
        return usuario
    """
