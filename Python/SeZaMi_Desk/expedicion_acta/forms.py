from django import forms 
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'


class ExpedicionActaForm(forms.ModelForm):   
    fecha_nacimiento = forms.DateField(label='Fecha de nacimiento',
    widget=DateInput(
        format='%Y-%m-%d',
        attrs={'class':'form-control elemento-tramite','placeholder':'Fecha de nacimiento'}),
        required=True)    
    class Meta:
        model = ExpedicionActa
        fields = '__all__'
        widgets = {   
            'curp':forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'nombre_solicitante': forms.TextInput(attrs={'class':'form-control elemento-tramite'}),
            'municipio_registro': forms.Select(attrs={'class':'form-control elemento-tramite'}),
            'tramite':forms.TextInput(attrs={'class':'form-control','hidden':'hidden'})  
        }
