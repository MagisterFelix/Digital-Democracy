from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode

from core.web.forms import LoginForm
from core.web.models.user import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            passport = form.cleaned_data["passport"]
            password = form.cleaned_data["password"]

            user = authenticate(passport=passport, password=password)

            if user is None:
                return render(request, "login.html", context={"form": form, "error": "No active user was found."})

            login(request, user)

            return redirect("home")

    return render(request, "login.html", context={"form": LoginForm()})


def logout_view(request):
    logout(request)
    return redirect("login")


def activation_view(request, uidb64, token):
    if request.user.is_authenticated:
        return redirect("home")

    try:
        passport = urlsafe_base64_decode(uidb64).decode()
    except (UnicodeDecodeError, ValueError):
        return HttpResponseForbidden()

    try:
        user = User.objects.get(passport=passport)
    except User.DoesNotExist:
        return HttpResponseForbidden()

    if not default_token_generator.check_token(user, token):
        return HttpResponseForbidden()

    request.session["user"] = user.passport

    return redirect("login")
