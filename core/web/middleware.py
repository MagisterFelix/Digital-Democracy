import hashlib

import requests
from django.contrib.auth import logout
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from core.web.machine_learning.fraud_detector import predict_fraud
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
        if request.user.is_superuser:
            return self.get_response(request)

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

        if "/activate/" in request.path:
            response = self.get_response(request)

            if response.status_code == 302 and response.url == "/login/":
                user = User.objects.get(passport=request.session["user"])
                user.activate()

                Log.objects.filter(user=user).delete()

                self.create_log(user, x_forwarded_for, Log.Action.ACTIVATION_ATTEMPT)

                del request.session["user"]

            return response

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


class FraudDetectionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_superuser:
            return self.get_response(request)

        last_log = Log.objects.last()

        if last_log is None or Log.objects.filter(user=last_log.user).count() <= 5:
            return self.get_response(request)

        is_fraud = predict_fraud(last_log)

        if is_fraud and last_log.action != Log.Action.LOGIN_ATTEMPT:
            email_template_name = "fraud_detection.txt"
            context = {
                "protocol": request.scheme,
                "domain": request.META["HTTP_HOST"],
                "url": request.META["HTTP_HOST"],
                "uidb64": urlsafe_base64_encode(force_bytes(last_log.user.passport)),
                "token": default_token_generator.make_token(last_log.user)
            }
            message = render_to_string(email_template_name, context)

            last_log.user.email_user("Fraud detection", message)

            last_log.user.deactivate()
            logout(request)

            redirect("login")

        return self.get_response(request)
