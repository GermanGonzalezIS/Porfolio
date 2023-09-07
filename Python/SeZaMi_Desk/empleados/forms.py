from django import forms
from django.contrib.auth.models import Group
from .models import Empleado 

class EmpleadoForm(forms.ModelForm):

    class Meta:
        model = Empleado
        
        fields = ('first_name','last_name','segundo_apellido','telefono','username','password','grupo')

        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre(s)'}),
            'last_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Primer apellido'}),
            'segundo_apellido':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Segundo apellido'}),
            'telefono':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Teléfono','pattern':'[0-9]+'}),
            'username':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de usuario'}),
            'password':forms.TextInput(attrs={'class':'form-control','placeholder':'Contraseña'}),
            'grupo':forms.Select(attrs={'class':'form-control'}),
        }

    def save(self, commit=True):
        user = super(EmpleadoForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class EmpleadoModificarForm(forms.ModelForm):

    class Meta:
        model = Empleado
        
        fields = ('first_name','last_name','segundo_apellido','telefono','username','contra')

        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre(s)'}),
            'last_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Primer apellido'}),
            'segundo_apellido':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Segundo apellido'}),
            'telefono':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Teléfono','pattern':'[0-9]+'}),
            'username':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de usuario'}),
            'contra':forms.TextInput(attrs={'class':'form-control','placeholder':'Contraseña'}),
            'grupo':forms.Select(attrs={'class':'form-control'}),
        }

    def save(self, commit=True):
        user = super(EmpleadoModificarForm, self).save(commit=False)
        user.set_password(self.cleaned_data['contra'])
        if commit:
            user.save()
        return user