from __future__ import unicode_literals

from django.db import models

# Create your models here.

#THIS MONKEYPATCH app is used for monkey patching the functions in the source code.
#We don't want to modify the source code because it will always change when updated.

#Therefore, most of the monkey patch are in page_processors.py

#Monkey patched def product in shop.views is in monkeyPatch.views.product

from django.forms import ModelChoiceField, ModelMultipleChoiceField
from django.utils.html import conditional_escape, mark_safe

class FabricCustomChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        """
        Shows an image with the label
        """
        if obj.image:
            image = conditional_escape(obj.image.url)
            title = conditional_escape(obj.name + " - " + obj.color)
            width = 100
            height = 100
            label = """%s<p><img src="%s" class="img-thumbnail" alt=%s height="%d" width="%d"/></p>""" % (title, image, title, width, height)
        else:
            return obj.name + " - " + obj.color

        return mark_safe(label)
class FabricMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        """
        Shows an image with the label
        """
        if obj.image:
            image = conditional_escape(obj.image.url)
            title = conditional_escape(obj.name + " - " + obj.color)
            width = 100
            height = 100
            label = """%s<p><img src="%s" class="img-thumbnail" alt=%s height="%d" width="%d"/></p>""" % (title, image, title, width, height)
        else:
            return obj.name + " - " + obj.color

        return mark_safe(label)

class TailorCustomChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        """
        Shows an image with the label
        """
        if obj.image:
            image = conditional_escape(obj.image.url)
            title = conditional_escape(obj.name)
            description = conditional_escape(obj.description)
            width = 200
            height = 200
            label = """%s<div class="tailor_center"><h5 class="tailor_description">%s</h5></div>
            <img src="%s" class="img-circle" alt=%s height="%d" width="%d"/>""" % (title, description, image, title, width, height)

        else:
            return obj.name

        return mark_safe(label)