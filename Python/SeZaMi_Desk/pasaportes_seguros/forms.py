from django import forms
from .models import Pasaporte, Seguro
from django.core.validators import RegexValidator

class DateInput(forms.DateInput):
    input_type = 'date'


class PasaporteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PasaporteForm, self).__init__(*args, **kwargs)
        self.fields['nombre_contacto_usa'].required = False
        self.fields['direccion_usa'].required = False
        self.fields['tel_contacto_usa'].required = False
        self.fields['correo'].required = False

    class Meta:
        model = Pasaporte
        fields = '__all__'

        widgets = {
            'curp':forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'acta':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite', 'id':'acta'}),
            'seguro_social':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite', 'id':'seguro_social'}),
            'identificacion_padres':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite', 'id':'identificacion_padres'}),
            'nombre_contacto_usa':forms.TextInput(attrs={'class':'form-control elemento-tramite', 'placeholder':'Nombre del contacto en Estados Unidos','id':'nombre_contacto_usa'}),
            'direccion_usa':forms.TextInput(attrs={'class':'form-control elemento-tramite', 'placeholder':'Dirección del contacto en Estados Unidos','id':'direccion_usa'}),
            'tel_contacto_usa':forms.TextInput(attrs={'class':'form-control elemento-tramite', 'placeholder':'Ejemplo:+1XXXXXXXXXX','id':'tel_contacto_usa','minlength':'12','pattern':'\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$'}),
            'correo':forms.TextInput(attrs={'class':'form-control elemento-tramite', 'placeholder':'Correo electrónico','id':'correo'}),
            'tramite':forms.HiddenInput(),      
        }

class SeguroForm(forms.ModelForm):

    class Meta:
        model = Seguro
        fields = '__all__'
        widgets = {
            'curp':forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'years_work':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite', 'id':'years_work'}),
            'years':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite', 'id':'years'}),
            'numero_seguro_social':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite', 'id':'numero_seguro_social'}),
            'tramite':forms.HiddenInput(),       
        }

opciones_entidad = (
	("AGUASCALIENTES", "AGUASCALIENTES"),
	("BAJA CALIFORNIA", "BAJA CALIFORNIA"),
	("BAJA CALIFORNIA SUR", "BAJA CALIFORNIA SUR"),
	("CAMPECHE", "CAMPECHE"), 
	("CHIAPAS", "CHIAPAS"),
	("CHIHUAHUA", "CHIHUAHUA"),
	("COAHUILA", "COAHUILA"),
	("COLIMA", "COLIMA"),
	("DISTRITO FEDERAL", "DISTRITO FEDERAL"),
	("DURANGO", "DURANGO"),
	("GUANAJUATO", "GUANAJUATO"),
	("GUERRERO", "GUERRERO"),
	("HIDALGO", "HIDALGO"),
	("JALISCO", "JALISCO"),
	("MEXICO", "CIUDAD DE MEXICO"),
	("MICHOACAN", "MICHOACAN"),
	("MORELOS", "MORELOS"),
	("NAYARIT", "NAYARIT"),
	("NUEVO LEON","NUEVO LEON"),
	("OAXACA", "OAXACA"),
	("PUEBLA", "PUEBLA"),
	("QUERETARO", "QUERETARO"),
	("QUINTANA ROO", "QUINTANA ROO"),
	("SAN LUIS POTOSI", "SAN LUIS POTOSI"),
	("SINALOA", "SINALOA"), 
	("SONORA", "SONORA"),
	("TABASCO", "TABASCO"),
	("TAMAULIPAS", "TAMAULIPAS"),
	("TLAXCALA", "TLAXCALA"),
	("VERACRUZ", "VERACRUZ"),
	("YUCATÁN", "YUCATÁN"),
	("ZACATECAS", "ZACATECAS"),
	("NACIDO EXTRANJERO", "NACIDO EXTRANJERO"),
)

opciones_sexo=(
    ("M","MUJER"),
    ("H","HOMBRE"),
)

class GenerarCURPForm(forms.Form):
    primer_apellido = forms.CharField(label='Primer Apellido',max_length=30,required=True)
    primer_apellido.widget = forms.TextInput(attrs={'class': 'form-control'})
    segundo_apellido = forms.CharField(label='Segundo Apellido',max_length=30,required=False)
    segundo_apellido.widget = forms.TextInput(attrs={'class': 'form-control'})
    nombre = forms.CharField(label='Nombre(s)',max_length=50,required=True)
    nombre.widget = forms.TextInput(attrs={'class': 'form-control'})
    fecha_nacimiento = forms.DateField(widget=DateInput())
    sexo = forms.ChoiceField(choices=opciones_sexo)
    entidad = forms.ChoiceField(choices=opciones_entidad)
