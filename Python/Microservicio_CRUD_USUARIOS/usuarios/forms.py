from django import forms
from .models import Usuario, Entidad_Federativa
from django.core.validators import RegexValidator

class DateInput(forms.DateInput):
    input_type = 'date'

class UsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario

        fields = ('first_name','segundo_nombre','last_name','segundo_apellido','username','password','curp','correo','fecha_nacimiento')

        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Primer nombre'}),
            'segundo_nombre':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Segundo nombre'}),
            'last_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Primer apellido'}),
            'segundo_apellido':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Segundo apellido'}),
            'username':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de usuario'}),
            'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña'}),
            'curp':forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'correo':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Correo electrónico','id':'correo'}),
            'fecha_nacimiento':forms.DateField(widget=DateInput()),
        }
    
    def save(self, commit=True):
        user = super(UsuarioForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
