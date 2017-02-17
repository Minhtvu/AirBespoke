from django import forms

class TailorForm(forms.Form):
    tailor_name = forms.CharField(required=False)
