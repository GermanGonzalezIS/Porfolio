from django import forms 
from .models import *

class CorreccionActaForm(forms.ModelForm):   
    class Meta:
        model = CorreccionActa
        fields = '__all__'
        widgets = {   
            'curp':forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'acta_a_corregir':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),
            'documentos_comprobantes':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),
            'testimonial':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),         
            'solicitud_firmado': forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),
            'original_copias': forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),
            'tramite':forms.TextInput(attrs={'class':'form-control','hidden':'hidden'})   
        }   
