#URLS for login, logout and register
from django.urls import path
from .views import register, user_login, user_logout, verify_otp

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("verify-otp/", verify_otp, name="verify_otp"),
]
