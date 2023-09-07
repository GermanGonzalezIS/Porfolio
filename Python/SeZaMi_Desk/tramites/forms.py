from django import forms
from .models import EstadoTramite, Tramite 
from django.db.models import Q
from django.core.validators import RegexValidator

class DateInput(forms.DateInput):
    input_type = 'date'

class PedirCurpForm(forms.Form):
    curp = forms.CharField(label='Indica la CURP del beneficiario',max_length=18,required=True)
    curp.widget = forms.TextInput(attrs={'class': 'form-control', 'maxlength':'18'})

    
class EditarForm(forms.ModelForm):
    fecha_fin = forms.DateField(
        widget=DateInput(
        format='%Y-%m-%d',
        attrs={'class':'form-control elemento-tramite','placeholder':'Fecha de nacimiento de la madre'}),
        required=False)

    def __init__(self, *args, **kwargs):
        super(EditarForm, self).__init__(*args, **kwargs)
        self.fields['fecha_fin'].required = False
        self.fields['estado'].queryset =  EstadoTramite.objects.filter(Q(estado='En trámite') | Q(estado='Finalizado'))

    class Meta:
            model = Tramite
            fields = ('estado','fecha_fin')
            widgets = {
                'estado':forms.Select(attrs={'class':'form-control'}),
                'fecha_fin':forms.DateInput(attrs={'class':'form-control'}),
            }

class EditarPasaporteSeguroForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditarPasaporteSeguroForm, self).__init__(*args, **kwargs)
        self.fields['estado'].queryset =  EstadoTramite.objects.filter(Q(estado='En trámite') | Q(estado='Finalizado'))

    class Meta:
            model = Tramite
            fields = ('estado',)
            widgets = {
                'estado':forms.Select(attrs={'class':'form-control'}),
            }
