from django import forms

from .models import Fabric

class FabricForm(forms.ModelForm):
    class Meta:
        model = Fabric
        fields = [
            "name",
            "type",
            "color",
            "sku",
            "image",
        ]