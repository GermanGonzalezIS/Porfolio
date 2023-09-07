from django import forms 
from .models import *

class MandamientosJudicialesForm(forms.ModelForm):   
    class Meta:
        model = MandamientosJudiciales
        fields = '__all__'
        widgets = {   
            'curp':forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'acta_nac_original':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),
            'curp_act':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),
            'comprobante_domicilio':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),          
            'pasaporte_vigente': forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),  
            'matricula_consular': forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),  
            'pago_en_caja_fiscalia':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),          
            'fotografia': forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),  
            'ine_familiar': forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),  
            'tramite':forms.TextInput(attrs={'class':'form-control','hidden':'hidden'})   
        }
