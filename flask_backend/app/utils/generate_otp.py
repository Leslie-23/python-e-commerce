import random
import string


def generate_otp(length=6):
    """
    Generate a random OTP of specified length
    """
    return ''.join(random.choices(string.digits, k=length))
