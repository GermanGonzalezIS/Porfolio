from django import forms
from .models import CorazonPlata, GrupoVisa
from django.core.validators import RegexValidator

class DateInput(forms.DateInput):
    input_type = 'date'
    
class CorazonPlataForm(forms.ModelForm):
    class Meta:
        model = CorazonPlata
        fields = '__all__'

        widgets={
            'credencial':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite', 'id':'credencial'}),
            'pasaporte':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite', 'id':'pasaporte'}),
            'curp':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite', 'id':'curp'}),
            'persona_zacatecana':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite', 'id':'persona_zacatecana'}),
            'certificado_medico':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite', 'id':'certificado_medico'}),
            'padrino':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite', 'id':'padrino'}),
            'no_antecedentes':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite', 'id':'no_antecedentes'}),
            'nombre_ahijado':forms.TextInput(attrs={'class':'form-control', 'id':'nombre_ahijado'}),
            'ap_paterno_ahijado':forms.TextInput(attrs={'class':'form-control', 'id':'ap_paterno_ahijado'}),
            'ap_materno_ahijado':forms.TextInput(attrs={'class':'form-control', 'id':'ap_materno_ahijado'}),
            'nombre_padrino':forms.TextInput(attrs={'class':'form-control', 'id':'nombre_padrino'}),

            'datos_completos':forms.CheckboxInput(attrs={'class':'form-check-input elemento-tramite', 'hidden':'hidden', 'id':'datos_completos'}),
            'grupo_visa':forms.Select(attrs={'class':'form-control', 'hidden':'hidden'})
        }

class GrupoVisaForm(forms.ModelForm):
    cita_secretaria = forms.DateField(label='Cita en la secretaría',
    widget=DateInput(
        format='%Y-%m-%d',
        attrs={'class':'form-control'}), required=False)

    cita_consulado = forms.DateField(label='Cita en el consulado',
    widget=DateInput(
        format='%Y-%m-%d',
        attrs={'class':'form-control'}), required=False)


    class Meta:
        model = GrupoVisa
        fields = '__all__'

        widgets = {
            'federacion':forms.Select(attrs={'class':'form-control'}),
            'representante':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre completo del representante del grupo'})
        }