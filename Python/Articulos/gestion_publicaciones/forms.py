from django import forms
from django.forms import fields

from usuarios.forms import UsuarioForm
from .models import Revision


class RevisionForm(forms.ModelForm):
    class Meta:
        model = Revision

        exclude = ('publicacion', 'usuario_revisor')

        widgets = {
            'archivo': forms.FileInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'})
        }
