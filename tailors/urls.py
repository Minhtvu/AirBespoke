from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    #url(r'^home/$', "tailors.views.tailor_home"),
    #url(r'^create/$', "tailors.views.tailor_create"),
    url(r'^$', "tailors.views.tailor_list"),
    url(r'^(?P<id>\d+)/edit/$', "tailors.views.tailor_update"),
    url(r'^(?P<id>\d+)/inventory/$', "tailors.views.tailor_inventory_list"),
    url(r'^(?P<id>\d+)/orders/$', "tailors.views.tailor_order_list"),
    url(r'^(?P<id>\d+)/orders/(?P<orderId>\d+)/$', "tailors.views.tailor_order_detail"),
    url(r'^(?P<id>\d+)/inventory/create/$', "tailors.views.tailor_inventory_create"),
    url(r'^(?P<id>\d+)/$', "tailors.views.tailor_detail"),


]