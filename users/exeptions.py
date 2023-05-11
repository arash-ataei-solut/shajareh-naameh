class SendOTPError(Exception):
    pass


class OTPDoesNotExist(Exception):
    pass


class OTPExpired(Exception):
    pass


class OTPIsInvalid(Exception):
    pass
