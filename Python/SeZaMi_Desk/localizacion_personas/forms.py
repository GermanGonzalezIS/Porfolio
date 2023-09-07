from django import forms
from .models import PersonaDesaparecida
from django.core.validators import RegexValidator

class DateInput(forms.DateInput):
    input_type = 'date'

class PersonaDesaparecidaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonaDesaparecidaForm, self).__init__(*args, **kwargs)
        self.fields['estatus'].initial = 1
    
    def __init__(self, *args, **kwargs):
        super(PersonaDesaparecidaForm, self).__init__(*args, **kwargs)
        self.fields['empleado'].required = False

    fecha_nacimiento_desaparecido = forms.DateField(label='Fecha de nacimiento',
    widget=DateInput(format='%Y-%m-%d',attrs={'class':'form-control','placeholder':'Fecha de nacimiento'}))
    
    fecha_desaparicion = forms.DateField(label='Fecha de desaparición',
    widget=DateInput(format='%Y-%m-%d',attrs={'class':'form-control','placeholder':'Fecha de desaparición'}))
    class Meta:
        model = PersonaDesaparecida
        fields = '__all__'
        widgets = {
                'folio':forms.HiddenInput(attrs={'class':'form-control','placeholder':'Folio'}),
                'nombre_desaparecido':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre'}),
                'apellido_paterno_desaparecido':forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido paterno'}),
                'apellido_materno_desaparecido':forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido materno'}),
                'direccion_desaparecido':forms.TextInput(attrs={'class':'form-control','placeholder':'Dirección'}),
                'observaciones':forms.Textarea(attrs={'class':'form-control','placeholder':'Observaciones','rows':4}),
                'estatus':forms.Select(attrs={'class':'form-select'}),
                'ultimo_lugar':forms.TextInput(attrs={'class':'form-control','placeholder':'Último lugar dónde se sabe al desaparecido(a)'}),
                'telefono_solicitante':forms.TextInput(attrs={'class':'form-control','placeholder':'Número de télefono'}),
                'nombre_solicitante':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre'}),
                'apellido_paterno_solicitante':forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido paterno'}),
                'apellido_materno_solicitante':forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido materno'}),
                'parentesco':forms.TextInput(attrs={'class':'form-control','placeholder':'Parentesco'}),
                'empleado':forms.HiddenInput(attrs={'class':'form-control'})
        }