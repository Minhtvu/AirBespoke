from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.


def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

class Fabric(models.Model):
    name = models.CharField(max_length=120)
    height_field = models.IntegerField(default=400, null=True)
    width_field = models.IntegerField(default=400, null=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field="width_field", height_field="height_field")
    color = models.CharField(max_length=120)
    sku = models.IntegerField(max_length=8, unique=True,)

    COTTON = "C"
    WOOL = "W"
    LINEN = "L"
    FABRIC_TYPES = (
        (COTTON, 'Cotton'),
        (WOOL, 'Wool'),
        (LINEN, 'Linen'),
    )
    type = models.CharField(max_length=1, choices=FABRIC_TYPES, default=COTTON)
    # def get_all_attributes(self):
    #     return "%s %s %d" %(self.name, self.color, self.sku)
    def __unicode__(self):
        # return "Name: %s Color: %s Sku: %d Type: %s" %(self.name, self.color, self.sku, self.type)
        return self.name
    def get_absolute_url(self):
        return "/fabrics/%s/" % (self.id)
