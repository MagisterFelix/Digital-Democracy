import hashlib

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, passport, email, password, **extra_fields):
        if passport is None or passport == "":
            raise ValueError("Users must have a passport.")

        if email is None or email == "":
            raise ValueError("Users must have an email.")

        if password is None or password == "":
            raise ValueError("Users must have a password.")

        user = self.model(
            passport=hashlib.sha256(passport.encode()).hexdigest(),
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, passport, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(passport, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    passport = models.CharField(
        max_length=128,
        primary_key=True,
        unique=True,
        error_messages={
            "unique": "A user with that passport already exists.",
        })
    email = models.EmailField(
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        error_messages={
            "unique": "A user with this email already exists.",
        })

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "passport"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return str(self.passport)

    class Meta:
        db_table = "user"
