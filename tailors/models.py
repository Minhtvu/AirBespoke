from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from fabrics.models import Fabric
from cartridge.shop.models import Order

from django.core.urlresolvers import reverse
# Create your models here.
def upload_location(instance,filename):
    return "%s/%s" %(instance.id, filename)
class Tailor(models.Model):
    #testing these extra fields:
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    #managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="manager_sellers", blank=True)
    fabric_inventory = models.ManyToManyField(Fabric, blank=True)
    tailor_orders = models.ManyToManyField(Order, blank=True)
    active = models.BooleanField(default=True)
    # end testing
    name = models.CharField(max_length=120)
    description = models.TextField()
    height_field = models.IntegerField(default=400)
    width_field = models.IntegerField(default=400)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field="width_field", height_field="height_field")
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    #list of available fabrics
    #fabrics =
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return "/tailors/%s/" % (self.id)
    def get_tailor_inventory_url(self):
        return "/tailors/%s/inventory" % (self.id)
    def get_tailor_inventory_create_url(self):
        return "/tailors/%s/inventory/create" % (self.id)
    def get_tailor_edit_url(self):
        return "/tailors/%s/edit" % (self.id)
    def get_tailor_order_url(self):
        return "/tailors/%s/orders" % (self.id)
    def get_tailor_order_detail_url(self, orderId):
        return "/tailors/%s/orders/%s" % (self.id,orderId)
    def add_order_to_tailor(self, order):
        self.tailor_orders.add(order)
class Inventory(models.Model):
    tailorID = models.CharField(max_length=120)
    fabricID = models.CharField(max_length=120)
    def __unicode__(self):
        return self.tailorID
    def get_absolute_url(self, tailorID):
        return "/tailors/%s/fabric" % (tailorID)
    def set_tailorID(self, tailorID):
        self.tailorID = tailorID