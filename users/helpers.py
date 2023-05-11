import string

from django.utils.crypto import get_random_string


def generate_otp_code():
    return get_random_string(5, string.digits)
