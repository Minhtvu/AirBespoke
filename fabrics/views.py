from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect

from .models import Fabric
from .forms import FabricForm
# Create your views here.]

def fabric_home(request):
    return HttpResponse("We are AirBespoke Fabrics.")

def fabric_create(request):
    form = FabricForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        print form.cleaned_data.get("title")
        instance.save()
        #messages.success(request, "Sucessfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "fabric/fabric_form.html", context)


def fabric_list(request):
    queryset_list = Fabric.objects.all().order_by("sku")
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
            "title": "Fabrics",
            "page_request_var": page_request_var,
    }
    return render(request, "fabric/fabric_list.html", context)

def fabric_detail(request, id):
    #instance = Post.objects.get(id=5)
    instance = get_object_or_404(Fabric, id=id)
    context = {
        "title": instance.name,
        "instance": instance,

    }
    return render(request, "fabric/fabric_detail.html", context)

def fabric_update(request, id):
    instance = get_object_or_404(Fabric, id=id)
    form = FabricForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "instance": instance,
        "title": instance.name,
        "form": form,
    }
    return render(request, "fabric/fabric_form.html", context)

