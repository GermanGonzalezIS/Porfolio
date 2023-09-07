from django import forms 
from .models import Visa

class DateInput(forms.DateInput):
    input_type = 'date'

class VisaForm(forms.ModelForm):
    fe_nacimiento_madre = forms.DateField(label='Fecha de nacimiento de la madre',
    widget=DateInput(
        format='%Y-%m-%d',
        attrs={'class':'form-control elemento-tramite','placeholder':'Fecha de nacimiento de la madre'}),
    required=False)

    fe_nacimiento_padre = forms.DateField(label='Fecha de nacimiento del padre',
    widget=DateInput(
        format='%Y-%m-%d',
        attrs={'class':'form-control elemento-tramite','placeholder':'Fecha de nacimiento del padre'}),
    required=False)    

    fe_ingreso_trabajo_escuela = forms.DateField(label='Fecha de ingreso al trabajo o escuela',
    widget=DateInput(
        format='%Y-%m-%d',
        attrs={'class':'form-control elemento-tramite','placeholder':'Fecha de ingreso al trabajo o escuela'}),
    required=False)

    fecha_viaje = forms.DateField(label='Fecha tentativa de viaje',
    widget=DateInput(
        format='%Y-%m-%d',
        attrs={'class':'form-control elemento-tramite'}),
    required=False)

    fecha_cita = forms.DateField(
    widget=DateInput(
        format='%Y-%m-%d',
        attrs={'class':'form-control','placeholder':'Fecha de la cita en el consulado'}),
    required=False)

    def __init__(self, *args, **kwargs):
        super(VisaForm, self).__init__(*args, **kwargs)
        self.fields['empleado'].required = False
    
    class Meta:
        model = Visa
        fields = '__all__'

        widgets = {
            'folio':forms.TextInput(attrs={'hidden':'hidden'}),
            'nombre_solicitante':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre del solicitante'}),
            'apellido_paterno_solicitante':forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido paterno del solicitante'}),
            'apellido_materno_solicitante':forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido materno del solicitante'}),
            'pasaporte':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'direccion_usa':forms.TextInput(attrs={'class':'form-control','placeholder':'Dirección en Estados Unidos'}),
            'persona_visitar':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de la persona a visitar'}),
            'tel_persona_visitar':forms.TextInput(attrs={'class':'form-control elemento-tramite', 'placeholder':'Ejemplo:+1XXXXXXXXXX','minlength':'12','pattern':'+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$'}),
            'dir_trabajo_escuela':forms.TextInput(attrs={'class':'form-control','placeholder':'Dirección del lugar de trabajo o escuela'}),
            'nom_dir_trabajo_escuela':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre del lugar de trabajo o escuela'}),
            'ingreso_mensual':forms.NumberInput(attrs={'class':'form-control','placeholder':'Ingreso mensual'}),
            'red_social_uno':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de la red social'}),
            'usuario_uno':forms.TextInput(attrs={'class':'form-control','placeholder':'Indica el nombre de usuario para la red social 1'}),
            'red_social_dos':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de la red social'}),
            'usuario_dos':forms.TextInput(attrs={'class':'form-control','placeholder':'Indica el nombre de usuario para la red social 2'}),
            'red_social_tres':forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de la red social'}),
            'usuario_tres':forms.TextInput(attrs={'class':'form-control','placeholder':'Indica el nombre de usuario para la red social 3'}),
            'correo':forms.EmailInput(attrs={'class':'form-control','placeholder':'Correo electrónico'}),
            'pago':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'empleado':forms.TextInput(attrs={'hidden':'hidden'})
        }