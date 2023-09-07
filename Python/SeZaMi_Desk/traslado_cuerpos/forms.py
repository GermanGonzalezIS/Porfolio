from django import forms 
from .models import TrasladoCuerpo

class DateInput(forms.DateInput):
    input_type = 'date'

class TrasladoCuerpoForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(label='Fecha de nacimiento',
    widget=DateInput(
        format='%Y-%m-%d',
        attrs={'class':'form-control'}))

    fecha_deceso = forms.DateField(label='Fecha del deceso',
    widget=DateInput(
        format='%Y-%m-%d',
        attrs={'class':'form-control'}))    

    def __init__(self, *args, **kwargs):
        super(TrasladoCuerpoForm, self).__init__(*args, **kwargs)
        self.fields['empleado'].required = False

    class Meta:
        model = TrasladoCuerpo
        fields = '__all__'
        widgets = {
            'folio':forms.TextInput(attrs={'hidden':'hidden'}),
            'nombre_fallecido':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre del fallecido'}),
            'causa_muerte':forms.TextInput(attrs={'class':'form-control','placeholder':'Causa de muerte'}),
            'lugar_deceso':forms.TextInput(attrs={'class':'form-control','placeholder':'Lugar de deceso'}),
            'lugar_origen':forms.TextInput(attrs={'class':'form-control','placeholder':'Lugar de origen'}),
            'anios_en_eu':forms.NumberInput(attrs={'class':'form-control','placeholder':'Años que duró la persona en Estados Unidos'}),
            'meses_en_eu':forms.NumberInput(attrs={'class':'form-control','placeholder':'Meses que duró la persona en Estados Unidos'}),
            'situacion_migratoria':forms.Select(attrs={'class':'form-control'}),
            'nombre_familiar_mexicano':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre del familiar mexicano'}),    
            'telefono':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ejemplo:+1XXXXXXXXXX','minlength':'12','pattern':'+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$'}),
            'empleado':forms.TextInput(attrs={'hidden':'hidden'})
        }