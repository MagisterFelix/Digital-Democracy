import hashlib

import requests

from core.web.models.log import Log
from core.web.models.user import User


class LogsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def create_log(user, x_forwarded_for, action):
        ip = x_forwarded_for.split(",")[0]
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=country,city").json()
        location = f"{response['country']}/{response['city']}"
        Log.objects.create(user=user, action=action, ip=ip, location=location)

    def __call__(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for is None:
            return self.get_response(request)

        if request.path == "/login/" and request.method == "POST" and request.POST.get("passport"):
            passport = hashlib.sha256(str(request.POST["passport"]).encode()).hexdigest()

            user = User.objects.filter(passport=passport)

            if not user.exists():
                return self.get_response(request)

            user = user.first()

            self.create_log(user, x_forwarded_for, Log.Action.LOGIN_ATTEMPT)

            return self.get_response(request)

        if not request.user.is_authenticated:
            return self.get_response(request)

        if request.path == "/" and request.method == "POST":
            self.create_log(request.user, x_forwarded_for, Log.Action.BALLOT_CREATION_ATTEMPT)
            return self.get_response(request)

        if "/ballot/" in request.path and request.method == "POST":
            self.create_log(request.user, x_forwarded_for, Log.Action.VOTING_ATTEMPT)
            return self.get_response(request)

        self.create_log(request.user, x_forwarded_for, Log.Action.INTERACTION)

        return self.get_response(request)
