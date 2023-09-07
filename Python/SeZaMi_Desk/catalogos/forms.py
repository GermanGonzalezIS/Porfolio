from django import forms

from .models import *

class MunicipioForm(forms.ModelForm):
    class Meta:
        model = Municipio
        fields = ('municipio',)
        widgets = {
            'municipio': forms.Select(attrs={'class':'form-control'}),
        }

class LocalidadForm(forms.ModelForm):
    class Meta:
        model = Localidad
        fields = ('localidad',)
        widgets = {
            'localidad':forms.Select(attrs={'class':'form-control'}),
        }     

class AsentamientoForm(forms.ModelForm):
    class Meta:
        model = Asentamiento
        fields = ('asentamiento',)
        widgets = {
            'asentamiento':forms.Select(attrs={'class':'form-control','id':'asentamiento_id'}),
        }