import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.mail import send_mail
from django.conf import settings

from .models import PetOwner
from .forms import CustomUserCreationForm

def generate_otp():
    return str(random.randint(100000, 999999))

#Register View
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            PetOwner.objects.create(user=user, name=user.username)

            otp = generate_otp()
            request.session["otp"] = otp
            request.session["user_id"] = user.id

            send_mail(
                "Your OTP code",
                f"Your OTP code is: {otp}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False
            )

            #login(request, user)
            return redirect("verify_otp")
    else:
        form = CustomUserCreationForm()
    
    return render(request, "accounts/register.html", {"form": form})

def verify_otp(request):
    if request.method == "POST":
        input_otp = request.POST.get("otp")
        if input_otp == request.session.get("otp"):
            user_id = request.session.get("user_id")
            user = get_user_model().objects.get(id=user_id)
            user.is_active = True
            user.save()
            login(request, user)
            return redirect("login")
        else:
            return render(request, "accounts/verify_otp.html", {"error":"Invalid OTP."})

    return render(request, "accounts/verify_otp.html")

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
