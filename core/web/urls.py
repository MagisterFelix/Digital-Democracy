from django.urls import path

from core.web.views.auth import activation_view, login_view, logout_view
from core.web.views.ballot import ballot_view
from core.web.views.home import home_view

urlpatterns = [
    path("", home_view, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("ballot/<ballot_id>/", ballot_view, name="ballot"),
    path("activate/<uidb64>/<token>/", activation_view, name="activate"),
]
