from django import forms
from django.db import models
# from django.forms.widgets import Ch
from .models import Tailor
from .models import Inventory
import fabrics
from fabrics.models import Fabric
from monkeyPatch.models import FabricMultipleChoiceField, FabricCustomChoiceField

class TailorForm(forms.ModelForm):
    class Meta:
        model = Tailor
        fields = [
            "name",
            "description",
            "image",
        ]
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Tailor
        # widgets = {'fabric_inventory': forms.widgets.CheckBoxSelectMultiple}
        fields = [
            "fabric_inventory",
        ]

    def __init__(self, *args, **kwargs):
        super(InventoryForm, self).__init__(*args, **kwargs)
        #self.fields['fabric_inventory'].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields['fabric_inventory'] = FabricMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Fabric.objects.all())
        #CheckboxSelectMultiple
        #self.fields['fabric_inventory'].queryset = Fabric.objects.all()
        # self.fields['fabric_inventory'].image_field = Fabric.objects.all().image