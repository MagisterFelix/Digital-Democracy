import hashlib

from django.contrib.auth.backends import BaseBackend

from core.web.models.user import User


class UserBackend(BaseBackend):

    def authenticate(self, request, passport, password):
        try:
            user = User.objects.get(passport=hashlib.sha256(passport.encode()).hexdigest())

            if not user.check_password(password):
                return None

            return user
        except User.DoesNotExist:
            return None
