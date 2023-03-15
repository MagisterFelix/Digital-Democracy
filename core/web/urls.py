from django.urls import path

from core.web.views.auth import login_view, logout_view
from core.web.views.home import home_view

urlpatterns = [
    path("", home_view, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
