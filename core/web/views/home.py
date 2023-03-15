from django.shortcuts import redirect, render


def home_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "home.html")
