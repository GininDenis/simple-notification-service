import binascii
import os


def generate_key(length: int=10) -> str:
    """
    Generate random string of letters and digits
    :param length: length of returned string
    :return: random string
    """
    return binascii.hexlify(os.urandom(length)).decode()[:length]
