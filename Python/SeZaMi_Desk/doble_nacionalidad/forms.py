from django import forms 
from .models import *
from django.contrib.auth.forms import UserCreationForm


class DobleNacionalidadForm(forms.ModelForm):   
    def __init__(self, *args, **kwargs):
        super(DobleNacionalidadForm, self).__init__(*args, **kwargs)
        self.fields['tramite_estado'].initial = 1
    
    def __init__(self, *args, **kwargs):
        super(DobleNacionalidadForm, self).__init__(*args, **kwargs)
        self.fields['empleado'].required = False

    class Meta:
        model = DobleNacionalidad
        fields = '__all__'
        widgets = {   
            'folio':forms.HiddenInput(attrs={'class':'form-control','placeholder':'Folio'}),
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre'}),
            'apellido_paterno':forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido paterno'}),
            'apellido_materno':forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido materno'}),
            'acta_nacimiento_original':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),
            'actas_apostilladas':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),
            'comprobante_domicilio':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),
            'identificacion_oficial':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),          
            'original_copias': forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}), 
            'tramite_estado':forms.TextInput(attrs={'hidden':'hidden'}),
            'empleado':forms.HiddenInput(attrs={'class':'form-control'}) 
        } 