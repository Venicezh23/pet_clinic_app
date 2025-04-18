from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import PetOwner

# Register View
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            PetOwner.objects.create(user=user, name=user.username)  # Auto-create PetOwner
            login(request, user)  # Log in the new user
            return redirect("login")  # Redirect to the main page
    else:
        form = UserCreationForm()
    
    return render(request, "accounts/register.html", {"form": form})

# Login View
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")  # Redirect after login
    else:
        form = AuthenticationForm()
    
    return render(request, "accounts/login.html", {"form": form})

# Logout View
def user_logout(request):
    logout(request)
    return redirect("login")  # Redirect to login page after logout
