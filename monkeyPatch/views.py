from __future__ import unicode_literals


from future.builtins import int, str
from json import dumps
from django.contrib.messages import info
from django.utils.translation import ugettext as _
from mezzanine.conf import settings
from mezzanine.utils.views import render, set_cookie
from cartridge.shop.utils import recalculate_cart
from cartridge.shop.models import Product, ProductVariation, CartItem
from cartridge.shop.forms import AddProductForm
from django.shortcuts import get_object_or_404, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from tailors.models import Tailor
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _
import json
from django import forms
from .models import TailorCustomChoiceField
from fabrics.models import Fabric


#NOTE: See the form steps in order (Step 1, Step 2, Step 3) to better understand
#Initially, def product() handles everything (cartItem, custom dimensions) but now we try to split the process to 3 steps with distinct views.
#Python reads from top to bottom so that's why step 3 is above 2 and 1 so the early steps can "see" and reference the later steps

# Custom Sizes Step:
class CustomSizeStepForm(forms.Form):
    class Meta:
        model = CartItem

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        request = kwargs.pop('request', None)
        super(CustomSizeStepForm, self).__init__(*args, **kwargs)
        if request:
            if request:
                self.fields['height'] = forms.DecimalField(max_digits=5, decimal_places=2,
                                                              validators=[MinValueValidator(Decimal("0.01"))])
                self.fields['weight'] = forms.DecimalField(max_digits=5, decimal_places=2,
                                                              validators=[MinValueValidator(Decimal("0.01"))])
                self.fields['neck_size'] = forms.DecimalField(max_digits=5, decimal_places=2,
                                                              validators=[MinValueValidator(Decimal("0.01"))])
                self.fields['chest_around'] = forms.DecimalField(max_digits=5, decimal_places=2,
                                                              validators=[MinValueValidator(Decimal("0.01"))])
                self.fields['sleeve_length'] = forms.DecimalField(max_digits=5, decimal_places=2,
                                                              validators=[MinValueValidator(Decimal("0.01"))])
                self.fields['wrist_size'] = forms.DecimalField(max_digits=5, decimal_places=2,
                                                              validators=[MinValueValidator(Decimal("0.01"))])
                self.fields['full_back_length'] = forms.DecimalField(max_digits=5, decimal_places=2,
                                                              validators=[MinValueValidator(Decimal("0.01"))])
                self.fields['half_back_length'] = forms.DecimalField(max_digits=5, decimal_places=2,
                                                              validators=[MinValueValidator(Decimal("0.01"))])
                self.fields['full_shoulder_width'] = forms.DecimalField(max_digits=5, decimal_places=2,
                                                              validators=[MinValueValidator(Decimal("0.01"))])
                self.fields['stomach'] = forms.DecimalField(max_digits=5, decimal_places=2,
                                                              validators=[MinValueValidator(Decimal("0.01"))])
                self.fields['waist_size'] = forms.DecimalField(max_digits=5, decimal_places=2,
                                                              validators=[MinValueValidator(Decimal("0.01"))])
                self.fields['hip_size'] = forms.DecimalField(max_digits=5, decimal_places=2,
                                                              validators=[MinValueValidator(Decimal("0.01"))])
                self.fields['pants_length'] = forms.DecimalField(max_digits=5, decimal_places=2,
                                                              validators=[MinValueValidator(Decimal("0.01"))])
                self.fields['crotch_size'] = forms.DecimalField(max_digits=5, decimal_places=2,
                                                              validators=[MinValueValidator(Decimal("0.01"))])

#Step 3: dimension form
def CustomSizeStep(request, slug, template="multiStepForm/customSizesStepForm.html"):

    form = CustomSizeStepForm(request.POST or None, request=request)
    if request.method == 'POST':
        if form.is_valid():
            sizeData = form.cleaned_data

            #add dimensions to request.session json
            #checking to see if dimensions are among json fields
            # for field in request.session.iteritems():
            #     print "data/fields in SUBMITTED DIMENSIONS: " + str(field)

            variation = ProductVariation.objects.get(product__sku=request.session['sku'])
            variation.height = sizeData['height']
            variation.weight = sizeData['weight']
            variation.neck_size = sizeData['neck_size']
            variation.chest_around = sizeData['chest_around']
            variation.sleeve_length = sizeData['sleeve_length']
            variation.wrist_size = sizeData['wrist_size']
            variation.full_back_length = sizeData['full_back_length']
            variation.half_back_length = sizeData['half_back_length']
            variation.full_shoulder_width = sizeData['full_shoulder_width']
            variation.stomach = sizeData['stomach']
            variation.waist_size = sizeData['waist_size']
            variation.hip_size = sizeData['hip_size']
            variation.pants_length = sizeData['pants_length']
            variation.crotch_size = sizeData['crotch_size']
            variation.fabrics = Fabric.objects.get(name=request.session['fabrics'])

            request.cart.add_item(variation, int(request.session['quantity']))
            recalculate_cart(request)

            return redirect("shop_cart")

    context = {"form": form}

    return render(request, template, context)
#tailorSelectionForm


#step 2: Tailor Form class for step 2
class TailorStepForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        request = kwargs.pop('request', None)
        super(TailorStepForm, self).__init__(*args, **kwargs)
        if request:
            data = dict(request.session)
            self.fields["tailor_selection_field"] = TailorCustomChoiceField(
                queryset=Tailor.objects.filter(fabric_inventory__name=data['fabrics']),
                empty_label=None,
                widget=forms.RadioSelect,
                label="Please choose one"

            )


#Step 2: View def -> let user select tailor based on fabric (need better algorithm here)
def tailorSelectionForm(request, slug, template="multiStepForm/tailorSteps.html"):

    tailor_count = Tailor.objects.filter(fabric_inventory__name=request.session['fabrics']).count()
    form = TailorStepForm(request.POST or None, request=request)
    if request.method == 'POST':
        if form.is_valid():
            newData = form.cleaned_data

            #add tailor selection field to request.session so that it will be carried on to future steps

            request.session['tailor_selection_field'] = str(newData['tailor_selection_field'])
            # for field in request.session.iteritems():
            #     print "data/fields in SUBMITTED TAILOR: " + str(field)

            #go to the third step
            return HttpResponseRedirect("customSize")
            # return redirect("shop_cart")

    #query all tailors with fabric selected by user

    context = {"form": form, "tailor_count": tailor_count, "product_slug": slug}
    # if request.method == "POST":
    #     return redirect("shop_cart")
    return render(request, template, context)

#Step 1: show basic product info, let user update quantity and CHOOSE FABRIC.
#check below to see how data are passed among the three form steps (add fabric, add tailor, add dimensions) thanks to request.session
# original, this is the only step that generate the product.html page and BUY functionality
# do not delete any comments! They are from the original code so use them as references

def product(request, slug, template="shop/product.html",
                    form_class=AddProductForm, extra_context=None):
    print "MODIFIED DEF PRODUCT"
    """
        Display a product - convert the product variations to JSON as well as
        handling adding the product to either the cart or the wishlist.
        """
    published_products = Product.objects.published(for_user=request.user)
    product = get_object_or_404(published_products, slug=slug)
    fields = [f.name for f in ProductVariation.option_fields()]
    variations = product.variations.all()
    variations_json = dumps([dict([(f, getattr(v, f))
                                   for f in fields + ["sku", "image_id"]]) for v in variations])
    to_cart = (request.method == "POST" and
               request.POST.get("add_wishlist") is None)
    initial_data = {}
    if variations:
        initial_data = dict([(f, getattr(variations[0], f)) for f in fields])
    initial_data["quantity"] = 1
    add_product_form = form_class(request.POST or None, product=product,
                                  initial=initial_data, to_cart=to_cart)
    if request.method == "POST":
        if add_product_form.is_valid():
            if to_cart:
                quantity = add_product_form.cleaned_data["quantity"]

                data = add_product_form.cleaned_data

                data = dict(data)
                request.session['quantity'] = json.dumps(data['quantity'])
                request.session['fabrics'] = str(data['fabrics'])
                request.session['sku'] = str(add_product_form.variation.sku)

                #checking what data/fields are stored in request.session before redirecting to other steps
                # for field in request.session.iteritems():
                #     print "FIRST FIELD ITEM IS " + str(field)

                #redirect to step 2. "tailorSelect" calls the next view and is configured in the monkeyPatch/urls.py
                return HttpResponseRedirect("tailorSelect")
            else:
                skus = request.wishlist
                sku = add_product_form.variation.sku
                if sku not in skus:
                    skus.append(sku)
                info(request, _("Item added to wishlist"))
                response = redirect("shop_wishlist")
                set_cookie(response, "wishlist", ",".join(skus))
                return response

    related = []

    ###
    # fabrics = product.fabrics.all()
    if settings.SHOP_USE_RELATED_PRODUCTS:
        related = product.related_products.published(for_user=request.user)
    context = {
        "product": product,
        "editable_obj": product,
        "images": product.images.all(),
        "variations": variations,
        "variations_json": variations_json,
        "has_available_variations": any([v.has_price() for v in variations]),
        "related_products": related,
        "add_product_form": add_product_form,
    }
    context.update(extra_context or {})
    templates = [u"shop/%s.html" % str(product.slug), template]
    return render(request, templates, context)

