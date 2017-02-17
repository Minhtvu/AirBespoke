from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^$', "fabrics.views.fabric_list"),
    url(r'^create/$', "fabrics.views.fabric_create"),
    url(r'^(?P<id>\d+)/$', "fabrics.views.fabric_detail"),
    url(r'^(?P<id>\d+)/edit/$', "fabrics.views.fabric_update")

]