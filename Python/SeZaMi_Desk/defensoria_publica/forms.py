from django import forms 
from .models import *

class DefensoriaPublicaForm(forms.ModelForm):   
    class Meta:
        model = DefensoriaPublica
        fields = '__all__'
        widgets = {   
            'curp':forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'tramite_realizar': forms.TextInput(attrs={'class':'form-control elemento-tramite'}),
            'localidad':forms.Select(attrs={'class':'form-control elemento-tramite'}),
            'num_telefonico':forms.TextInput(attrs={'class':'form-control elemento-tramite', 'placeholder':'Ejemplo:+1XXXXXXXXXX','id':'num_telefonico','minlength':'12','pattern':'\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Correo Electrónico'}),
            'tramite':forms.TextInput(attrs={'class':'form-control','hidden':'hidden'})  
        }

