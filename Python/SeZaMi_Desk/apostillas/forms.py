from django import forms 
from .models import Apostilla
from django.contrib.auth.forms import UserCreationForm

class ApostillaForm(forms.ModelForm):   
    class Meta:
        model = Apostilla
        fields = '__all__'
        widgets = {                   
            'curp':forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'acta_americana':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),
            'acta_mexicana':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),
            'identificacion_padres':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),
            'curp_doc':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),
            'comprobante_domicilio':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),
            'rfc':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite'}),
            'tramite':forms.TextInput(attrs={'class':'form-control','hidden':'hidden'})        
        }