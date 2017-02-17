from django.contrib import admin
from copy import deepcopy
from cartridge.shop.admin import ProductAdmin
from .models import Fabric

#add fabric selection fields to Product admin page

ProductAdmin.fieldsets[0][1]["fields"].insert(2, "fabrics")
admin.site.register(Fabric)