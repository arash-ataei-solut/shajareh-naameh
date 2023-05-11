from django.db import models

from users.helpers import generate_otp_code


class AuthOTPManager(models.Manager):

    def create_otp(self, **kwargs):
        otp_code = generate_otp_code()
        return self.create(code=otp_code, **kwargs)
