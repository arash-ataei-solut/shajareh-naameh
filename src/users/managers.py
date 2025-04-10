from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.db import models

from users.helpers import generate_otp_code


class ShnUserManager(UserManager):
    def _create_user(self, mobile, password, **extra_fields):
        """
        Create and save a user with the given mobile and password.
        """
        if not mobile:
            raise ValueError("The given mobile must be set")
        user = self.model(mobile=mobile, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(mobile, password, **extra_fields)

    def create_superuser(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(mobile, password, **extra_fields)


class AuthOTPManager(models.Manager):

    def create_otp(self, **kwargs):
        otp_code = generate_otp_code()
        return self.create(code=otp_code, **kwargs)
