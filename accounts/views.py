from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import PetOwner
from .forms import CustomUserCreationForm

#Register View
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            PetOwner.objects.create(user=user, name=user.username)
            login(request, user)
            return redirect("login") #go back to login after register
    else:
        form = CustomUserCreationForm()
    
    return render(request, "accounts/register.html", {"form": form})

#Login View
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home") #go to home (landing) page
    else:
        form = AuthenticationForm()
    
    return render(request, "accounts/login.html", {"form": form})

#Logout View
def user_logout(request):
    logout(request)
    return redirect("login")  #go back to login page
