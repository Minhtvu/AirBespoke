from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect

import os
PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_APP = os.path.basename(PROJECT_APP_PATH)
PROJECT_ROOT = BASE_DIR = os.path.dirname(PROJECT_APP_PATH)

from .models import Tailor
from .models import Inventory
from .forms import TailorForm
from .forms import InventoryForm
from django.contrib.auth.models import User
import fabrics
from fabrics.models import Fabric
from cartridge.shop.models import Order
from cartridge.shop.models import OrderItem
# from os.path.join(BASE_DIR, 'fabrics.models') import Fabric
# from src.fabrics.models import Fabric
# Create your views here.]

def tailor_home(request):
    print(request.user.is_authenticated())
    if request.user.is_authenticated():
        return HttpResponse("We are AirBespoke Tailors.")
    else:
        return HttpResponse("You are not logged in.")

def tailor_create(request):
    form = TailorForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        print form.cleaned_data.get("title")
        instance.save()
        #messages.success(request, "Sucessfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "tailor/tailor_form.html", context)

def tailor_list(request):
    queryset_list = Tailor.objects.all().order_by("-timestamp")
    paginator = Paginator(queryset_list, 25)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
            "object_list": queryset,
            "title": "Tailors",
            "page_request_var": page_request_var,
    }
    return render(request, "tailor/tailor_list.html", context)

def tailor_detail(request, id):
    #instance = Post.objects.get(id=5)
    #request.user.isTailor = False
    #request.user.save()
    #print(request.user.isTailor)
    instance = get_object_or_404(Tailor, id=id)
    isTailor = False
    if ((request.user.is_authenticated() and request.user == instance.user) or (request.user.is_superuser)):
        isTailor = True
    context = {
        "title": instance.name,
        "instance": instance,
        "isTailor": isTailor
    }
    return render(request, "tailor/tailor_detail.html", context)

def tailor_update(request, id):
    instance = get_object_or_404(Tailor, id=id)
    form = TailorForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "instance": instance,
        "title": instance.name,
        "form": form,
    }
    if not ((request.user.is_authenticated() and request.user == instance.user) or (request.user.is_superuser)):
        return render(request, "error_page.html", context)
    return render(request, "tailor/tailor_form.html", context)
def tailor_inventory_list(request, id):
    instance = get_object_or_404(Tailor, id=id)
    queryset_list = instance.fabric_inventory.all()
    # queryset_name = 
    paginator = Paginator(queryset_list, 25)
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        "currentTailor": instance,
        "title": "Fabrics",
        "page_request_var": page_request_var,
    }
    if not ((request.user.is_authenticated() and request.user == instance.user) or (request.user.is_superuser)):
        return render(request, "error_page.html",context)
    return render(request, "tailor/tailor_fabric_list.html", context)

def tailor_order_list(request, id):
    instance = get_object_or_404(Tailor, id=id)
    #orderitem = OrderItem.objects.all()
    # for field in orderitem[0]._meta.fields:
    #     print field.name
    items = []
    for tailor_order in instance.tailor_orders.all():
        items.append(OrderItem.objects.filter(order=tailor_order))
    #
    # print("Order Items: ")
    # print (items)
    #
    #
    # for item in items:
    #     print item[0].order.transaction_id
    # for item in instance.tailor_orders.all():
    #     print item.transaction_id

    context = {
        "currentTailor": instance,
        "title": "Orders",
        "items": items,
    }
    if not ((request.user.is_authenticated() and request.user == instance.user) or (request.user.is_superuser)):
        return render(request, "error_page.html",context)
    return render(request, "tailor/tailor_order_list.html", context)

def tailor_order_detail(request, id, orderId):
    item = OrderItem.objects.filter(id=orderId)
    print item
    #instance = Post.objects.get(id=5)
    #request.user.isTailor = False
    #request.user.save()
    instance = get_object_or_404(Tailor, id=id)
    #currentOrder = instance.tailor_orders.filter()
    if not ((request.user.is_authenticated() and request.user == instance.user) or (request.user.is_superuser)):
        return HttpResponse("Error You are not the correct user.")
    context = {
        "currentTailor": instance,
        "title": "Order Details",
        "item": item

    }
    if not ((request.user.is_authenticated() and request.user == instance.user) or (request.user.is_superuser)):
        return render(request, "error_page.html",context)
    return render(request, "tailor/tailor_order_detail.html", context)

def tailor_inventory_create(request, id):
    instance = get_object_or_404(Tailor, id=id)
    form = InventoryForm(request.POST or None, request.FILES or None, instance=instance)
    if not ((request.user.is_authenticated() and request.user == instance.user) or (request.user.is_superuser)):
        return render(request, "error_page.html",)
    #print instance.user
    if form.is_valid():
        # instance = form.save(commit=False)
        # print form.cleaned_data.get("title")
        # #instance.set_userID(id)
        # instance.save()
        # # messages.success(request, "Sucessfully Created")
        #new_fabric_inventory = request.FILES['fabric_inventory']
        #form.save(update_fields=["fabric_inventory"])
        # instance.fabric_inventory = new_fabric_inventory
        form.save()
        #form.save_m2m()

        return HttpResponseRedirect(instance.get_tailor_inventory_url()) #instance.get_absolute_url()
    context = {
        "form": form,
    }
    # instance = get_object_or_404(Tailor, id=id)
    # #fabric = Fabric(name="Testing123", color="blue", sku="123456")
    #
    # #instance.fabric_inventory.add(fabric)
    # context = {
    #     "currentTailor": instance,
    #     "title": "Fabric List",
    #
    # }
    return render(request, "tailor/tailor_fabric_form.html", context)

