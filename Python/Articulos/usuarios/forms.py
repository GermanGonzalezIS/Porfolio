from django import forms
from .models import Usuario


class UsuarioForm(forms.ModelForm):

    class Meta:

        model = Usuario

        fields = ('nombre', 'primer_apellido', 'segundo_apellido',
                  'correo_electronico', 'username', 'password')

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Nombre(s)',
                                             'id': 'id_nombre',
                                             'required': 'required'}),
            'primer_apellido': forms.TextInput(attrs={'class': 'form-control',
                                                      'placeholder': 'Apellido',
                                                      'id': 'id_apellido',
                                                      'required': 'required'}),
            'segundo_apellido': forms.TextInput(attrs={'class': 'form-control',
                                                       'placeholder': 'Apellido',
                                                       'id': 'id_segundo_apellido'}),
            'correo_electronico': forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Correo electrónico',
                                                         'id': 'id_email',
                                                         'required': 'required'}),
            'username': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Nombre de usuario',
                                               'id': 'id_username',
                                               'required': 'required'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Contraseña',
                                                   'id': 'id_password',
                                                   'required': 'required'}),
        }

    def save(self, commit=True):
        user = super(UsuarioForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
