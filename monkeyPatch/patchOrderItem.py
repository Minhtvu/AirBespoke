from copy import deepcopy
from django import forms
from decimal import Decimal
from cartridge.shop.models import Order, SelectedProduct, ProductVariation, Cart, DiscountCode, OrderItem
from cartridge.shop.forms import AddProductForm
from django.utils.encoding import force_text
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _
from monkeyPatch.models import FabricCustomChoiceField
from fabrics.models import Fabric

def patchOrder():
    ###
    ADD_PRODUCT_ERRORS = {
        "invalid_options": _("The selected options are currently unavailable."),
        "no_stock": _("The selected options are currently not in stock."),
        "no_stock_quantity": _("The selected quantity is currently unavailable."),
    }
    ###

    #Deep copy the the AddProductForm.__init__ func from the source code, then add our modification here.
    #After that, we can "overwrite" the source code by making the sourceCode.thisFunc = modifiedFunc.

    original_product_add_init = deepcopy(AddProductForm.__init__)
    def product_add_init(self, *args, **kwargs):
        original_product_add_init(self, *args, **kwargs)
        if self._product and self._product.fabrics.exists():
        #     # query all Fabrics that have reverse foreign key (Product) matched the passed in self._product
            self.fields['fabrics'] = FabricCustomChoiceField(widget=forms.RadioSelect, empty_label=None, queryset=Fabric.objects.select_related().filter(product__sku=self._product.sku).distinct())

    AddProductForm.__init__ = product_add_init

    def dimension_add_clean(self):
        """
        Determine the chosen variation, validate it and assign it as
        an attribute to be used in views.
        """
        if not self.is_valid():
            return
        # Posted data will either be a sku, or product options for
        # a variation.
        data = self.cleaned_data.copy()
        quantity = data.pop("quantity")
        fabrics = None

        if self._product:
            fabrics = data.pop("fabrics")

        # Ensure the product has a price if adding to cart.
        if self._to_cart:
            data["unit_price__isnull"] = False
        error = None
        if self._product is not None:
            # Chosen options will be passed to the product's
            # variations.
            qs = self._product.variations
        else:
            # A product hasn't been given since we have a direct sku.
            qs = ProductVariation.objects
        try:
            variation = qs.get(**data)
        except ProductVariation.DoesNotExist:
            error = "invalid_options"
        else:
            # Validate stock if adding to cart.
            if self._to_cart:
                if not variation.has_stock():
                    error = "no_stock"
                elif not variation.has_stock(quantity):
                    error = "no_stock_quantity"
        if error is not None:
            raise forms.ValidationError(ADD_PRODUCT_ERRORS[error])
        self.variation = variation
        if fabrics:
            self.variation._fabrics = fabrics

        return self.cleaned_data
    AddProductForm.clean = dimension_add_clean

    # from .models import Cart
    def add_item_mod(self, variation, quantity):
        """
        Increase quantity of existing item if SKU matches, otherwise create
        new.
        """
        if not self.pk:
            self.save()
        kwargs = {"sku": variation.sku, "unit_price": variation.price()}
        item, created = self.items.get_or_create(**kwargs)
        if created:
            item.description = force_text(variation)
            item.unit_price = variation.price()
            item.url = variation.product.get_absolute_url()
            try:
                item.fabrics = variation.fabrics
                item.height = variation.height
                item.weight = variation.weight
                item.neck_size = variation.neck_size
                item.chest_around = variation.chest_around
                item.sleeve_length = variation.sleeve_length
                item.wrist_size = variation.wrist_size
                item.full_back_length = variation.full_back_length
                item.half_back_length = variation.half_back_length
                item.full_shoulder_width = variation.full_shoulder_width
                item.stomach = variation.stomach
                item.waist_size = variation.waist_size
                item.hip_size = variation.hip_size
                item.pants_length = variation.pants_length
                item.crotch_size = variation.crotch_size
            except AttributeError:
                pass
            image = variation.image
            if image is not None:
                item.image = force_text(image.file)
            variation.product.actions.added_to_cart()
        item.quantity += quantity
        item.save()
    Cart.add_item = add_item_mod

    def setup(self, request):
        """
        Set order fields that are stored in the session, item_total
        and total based on the given cart, and copy the cart items
        to the order. Called in the final step of the checkout process
        prior to the payment handler being called.
        """
        self.key = request.session.session_key
        self.user_id = request.user.id
        for field in self.session_fields:
            if field in request.session:
                setattr(self, field, request.session[field])
        self.total = self.item_total = request.cart.total_price()
        if self.shipping_total is not None:
            self.shipping_total = Decimal(str(self.shipping_total))
            self.total += self.shipping_total
        if self.discount_total is not None:
            self.total -= Decimal(self.discount_total)
        if self.tax_total is not None:
            self.total += Decimal(self.tax_total)
        self.save()  # We need an ID before we can add related items.
        for item in request.cart:
            product_fields = [f.name for f in SelectedProduct._meta.fields]+['fabrics']+['height']+['weight']\
                             +['neck_size']+['chest_around']+['sleeve_length']+['wrist_size']+['full_back_length']\
                             +['half_back_length']+['full_shoulder_width']+['stomach']+['waist_size']+['hip_size']\
                             +['pants_length']+['crotch_size']
            item = dict([(f, getattr(item, f)) for f in product_fields])
            self.items.create(**item)
    Order.setup = setup


#Patch def complete
    from cartridge.shop.utils import clear_session
    from django.db import models
    from tailors.models import Tailor

    def complete(self, request):
        """
        Remove order fields that are stored in the session, reduce the
        stock level for the items in the order, decrement the uses
        remaining count for discount code (if applicable) and then
        delete the cart.
        """
        ###Tailor Testing
        # print "THE MONKEY PATCH IS WORKING"
        #Algorithm code
        #This code takes the fabric a customer has selected and matches thier order to a specific tailor that has that fabric

        current_order_items = OrderItem.objects.filter(order=self)

        for item in current_order_items:
            if "tailor_selection_field" not in request.session:
                request.session['tailor_selection_field'] = "Unassigned"
            item_tailor_id = request.session['tailor_selection_field']
            print item_tailor_id

            available_tailors = Tailor.objects.filter(name=item_tailor_id)
            print len(available_tailors)
            if (len(available_tailors)==1):
                tailor = available_tailors.first()
                tailor.add_order_to_tailor(self)
                print "It worked"
            elif len(available_tailors)==0:
                #tailor in this case is set to "Unassigned"
                tailor = available_tailors.first()
                tailor.add_order_to_tailor(self)
                print "No tailors were matched"
            else:
                print "Too many tailors were returned"
        # Algorithm to match on fabric
        # current_order_items = OrderItem.objects.filter(order=self)
        # for item in current_order_items:
        #     item_fabric = item.fabrics
        #     available_tailors = Tailor.objects.filter(fabric_inventory=item_fabric)
        #     if len(available_tailors) == 0:
        #         #error message saying no tailors have that fabric
        #         print "Error No Tailors were found with this fabric"
        #     elif len(available_tailors) == 1:
        #         tailor = available_tailors.first()
        #         tailor.add_order_to_tailor(self)
        #         print "Success only 1 tailor was found"
        #         print tailor
        #     else:
        #         minOrders = 999999
        #         minTailor = None
        #         for tailor in available_tailors:
        #             amount_of_orders = len(tailor.tailor_orders.all())
        #             print "Tailor: %s, Number of orders: %d" %(tailor,amount_of_orders)
        #             if amount_of_orders < minOrders:
        #                 minOrders = amount_of_orders
        #                 minTailor = tailor
        #         if minTailor is not None:
        #             minTailor.add_order_to_tailor(self)
        #             print "Success out of multiple tailors"
        #             print minTailor
        #         else:
        #             #print error message
        #             print "Error didn't find a min order tailor"


        #for field in orderItem[0]._meta.fields:
             #print field.name
        #print orderItem[0].fabrics
        #fabric = orderItem[0].fabrics
        #print tailors
        #size = len(tailors)
        #tailor = Tailor.objects.filter(fabric_inventory=fabric).first()
        #print tailor
        #if tailor is not None:
            #tailor.add_order_to_tailor(self)
            #print "Success"
        #else:
            #print "Fail"
        self.save()  # Save the transaction ID.
        discount_code = request.session.get('discount_code')
        clear_session(request, "order", *self.session_fields)
        for item in request.cart:
            try:
                variation = ProductVariation.objects.get(sku=item.sku)
            except ProductVariation.DoesNotExist:
                pass
            else:
                variation.update_stock(item.quantity * -1)
                variation.product.actions.purchased()
        if discount_code:
            DiscountCode.objects.active().filter(code=discount_code).update(
                uses_remaining=models.F('uses_remaining') - 1)
        request.cart.delete()
        del request.session['cart']
    Order.complete = complete

