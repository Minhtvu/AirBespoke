from django.conf.urls import url

from mezzanine.conf import settings


import views

_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns = [
    url("^product/(?P<slug>.*)/customSize%s$" % _slash,
        views.CustomSizeStep,
        name="size_update"),
    url("^product/(?P<slug>.*)/tailorSelect%s$" % _slash,
        views.tailorSelectionForm,
        name="tailor_update"),

    url("^product/(?P<slug>.*)%s$" % _slash,
        views.product,
        name="shop_product"),


    # url("^cart%s$" % _slash, override_cartridge.cart, name="shop_cart"),
]