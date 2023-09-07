from django import forms 
from .models import *
from django.contrib.auth.forms import UserCreationForm

class LicenciaConducirForm(forms.ModelForm):  
    class Meta:
        model = LicenciaConducir
        fields = '__all__'
        widgets = {   
            'curp':forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'acta_nacimiento':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),
            'comprobante_dom_eeuu':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),
            'referencia_dom_zac':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),
            'fotografia':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),          
            'tipo_sangre': forms.TextInput(attrs={'class':'form-control elemento-tramite', 'pattern':'^(A|B|AB|O)[-+]$'}),
            'identificacion_oficial':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),          
            'tramite':forms.TextInput(attrs={'class':'form-control','hidden':'hidden'}),   
        }
