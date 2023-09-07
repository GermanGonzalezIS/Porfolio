from django import forms
from django.core.validators import RegexValidator

from .models import Beneficiario, BeneficiarioDireccion, EstudioSocioeconomico
from catalogos.models import Municipio, Localidad, Asentamiento

class BeneficiarioDireccionForm(forms.ModelForm):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if not self.instance.pk:
            pass
            # El formulario será utilizado para crear un nuevo registro
            # Se limpian los ComboBox de localidad y asentamiento y se 
            # les agrega el valor por default
            self.fields['municipio'].choices = [('', '---------')] + list(self.fields['municipio'].choices)
            self.fields['localidad'].choices = [('', '---------')]
            self.fields['asentamiento'].choices = [('', '---------')]
        else:
            # El formulario será utilizado para actualizar un registro
            # Se definen las opciones a mostrar en los ComboBox
            lista_localidades = list(Localidad.objects.filter(municipio_id=self.instance.municipio_id).values_list('id','localidad'))
            lista_asentamientos = list(Asentamiento.objects.filter(localidad_id=self.instance.localidad_id).values_list('id','asentamiento'))
            print(self.fields['municipio'].choices)
            self.fields['municipio'].choices = [('', '---------')] + list(self.fields['municipio'].choices)
            self.fields['localidad'].choices = [('', '---------')] + lista_localidades
            self.fields['asentamiento'].choices = [('', '---------')] + lista_asentamientos

    class Meta:
        model = BeneficiarioDireccion
        fields = '__all__'
        widgets = {
            'nombre_vialidad':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre de la vialidad'}),
            'entre_vialidades':forms.TextInput(attrs={'class':'form-control','placeholder':'Entre vialidades'}),
            'numero_exterior':forms.NumberInput(attrs={'class':'form-control','placeholder':'Número exterior'}),
            'numero_interior':forms.NumberInput(attrs={'class':'form-control','placeholder':'Número interior'}),
            'descripcion_ubicacion':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descripción de la ubicación'}),
            'municipio':forms.Select(attrs={'class':'form-control'}),
            'localidad':forms.Select(attrs={'class':'form-control'}),
            'asentamiento':forms.Select(attrs={'class':'form-control'}),
            'tipo_vialidad':forms.Select(attrs={'class':'form-control'}),
        }
 
class EstudioSocioeconomicoForm(forms.ModelForm):
    class Meta:
        model = EstudioSocioeconomico
        fields = '__all__'
        widgets = {
            'estudio_socioeconomico':forms.CheckboxInput(attrs={'class':'form-check-input', 'id':'estudio_socioeconomico'}),
            'estado_civil':forms.Select(attrs={'class':'form-control'}),
            'jefe_familia':forms.CheckboxInput(attrs={'class':'form-check-input', 'id':'jefe_familia'}),
            'ocupacion':forms.Select(attrs={'class':'form-control'}),
            'ingreso_mensual':forms.Select(attrs={'class':'form-control'}),
            'integrantes_familia':forms.NumberInput(attrs={'class':'form-control','placeholder':'Número de integrantes de la familia'}),
            'dependientes_economicos':forms.NumberInput(attrs={'class':'form-control','placeholder':'Número de dependientes económicos'}),
            # tipo de vivienda???
            'vivienda':forms.Select(attrs={'class':'form-control'}),
            'numero_habitantes_vivienda':forms.NumberInput(attrs={'class':'form-control','placeholder':'Número de habitantes de la vivienda'}),
            'vivienda_electricidad':forms.CheckboxInput(attrs={'class':'form-check-input', 'id':'vivienda_electricidad'}),
            'vivienda_agua':forms.CheckboxInput(attrs={'class':'form-check-input', 'id':'vivienda_agua'}),
            'vivienda_drenaje':forms.CheckboxInput(attrs={'class':'form-check-input', 'id':'vivienda_drenaje'}),
            'vivienda_gas':forms.CheckboxInput(attrs={'class':'form-check-input', 'id':'vivienda_gas'}),
            'vivienda_telefono':forms.CheckboxInput(attrs={'class':'form-check-input', 'id':'vivienda_telefono'}),
            'vivienda_internet':forms.CheckboxInput(attrs={'class':'form-check-input', 'id':'vivienda_internet'}),
            'nivel_estudios':forms.Select(attrs={'class':'form-control'}),
            'tipo_seguridad_social':forms.Select(attrs={'class':'form-control'}),
            'discapacidad':forms.Select(attrs={'class':'form-control'}),
            'grupo_vulnerable':forms.Select(attrs={'class':'form-control'}),
        }

class BeneficiarioForm(forms.ModelForm):
    class Meta:
        model = Beneficiario
        fields = '__all__'
        exclude = (
            'direccion',
            'estudio_socioeconomico',
        )
        # fields = ('curp','primer_apellido', 'segundo_apellido', 'nombre', 'identificacion', 'beneficiario_colectivo')
        widgets = {
                'curp':forms.TextInput(attrs={'class':'form-control','placeholder':'CURP', 'readonly':'readonly'}),
                'primer_apellido':forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido paterno'}),
                'segundo_apellido':forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido materno'}),
                'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre(s)'}),
                'identificacion':forms.Select(attrs={'class':'form-control'}),
                'beneficiario_colectivo':forms.CheckboxInput(attrs={'class':'form-check-input', 'id':'beneficiario_colectivo'}), 
        }