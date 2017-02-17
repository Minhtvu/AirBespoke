from django.shortcuts import render, redirect
from django.contrib.auth import (authenticate, get_user_model, login, logout)
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from .forms import UserLoginForm, UserRegisterForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
import fabrics
from fabrics.models import Fabric
import tailors
from tailors.models import Tailor

def login_view(request):
    #Algorithm to check who is a tailor
    #######################
    tailors = Tailor.objects.all()
    users = User.objects.all()

    for user in users:
        for tailor in tailors:
            tailoruser = tailor.user
            if (tailoruser == user):
                user.isTailor = True
                break
            else:
                user.isTailor = False
        user.save()
    ######################
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        print(request.user.is_authenticated())
        if(user.isTailor):
            instance = Tailor.objects.filter(user=user).first()
            return HttpResponseRedirect(instance.get_absolute_url())
            #return redirect("/")
        else:
            return redirect("/")

    return render(request, "accounts/login_form.html", {"form":form, "title": title})
def register_view(request):
    print(request.user.is_authenticated())
    if request.user.is_authenticated():
        return HttpResponse("You are already logged in.")
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect("/")

    context = {
        "form": form,
        "title": title
    }
    return render(request, "accounts/login_form.html", context)
def logout_view(request):
    logout(request)
    print(request.user.is_authenticated())

    return redirect("/")
    #return render(request, "accounts/login_form.html", {})

