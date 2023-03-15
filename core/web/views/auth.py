from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from core.web.forms import LoginForm


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
