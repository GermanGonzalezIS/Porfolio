from django import forms

class CurpForm(forms.Form):
    curp = forms.CharField(label='CURP',min_length = 18,max_length = 18,required=True)

class FolioForm(forms.Form):
    folio = forms.CharField(label='Folio', min_length = 9, required=True)