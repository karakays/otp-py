import os
import io
import base64
import binascii
from urllib.parse import urlparse, unquote
from otp import core


CONFIG_HOME = os.environ["HOME"] + '/.otp/'
CONFIG_PATH = CONFIG_HOME + '.otprc'


def create_dir_if_not_exists():
    exists = os.path.exists(CONFIG_HOME)
    if not exists:
        os.mkdir(CONFIG_HOME, 0o774)
    return exists


def configure():
    while True:
        secret = input('Secret key: ').strip()
        try:
            base64.b32decode(secret)
            break
        except binascii.Error:
            pass

    issuer = input('Issuer: ').strip()

    user = input('User: ').strip()

    period = input('Period (30 seconds): ').strip()
    if not period:
        period = 30

    digits = input('Digits (6): ').strip()
    if not period:
        digits = 6

    algorithm = input('Algorithm (SHA-256): ').strip()
    if not period:
        algorithm = 'SHA-256'

    create_dir_if_not_exists()

    token = core.get_otp_by_secret(secret, issuer=issuer, user=user,
                                   period=period, digits=digits,
                                   algorithm=algorithm)

    uri = core.create_uri(token)

    abs_path = CONFIG_HOME + '.otprc'
    with io.open(abs_path, 'wt', encoding='UTF-8', newline=None) as f:
        f.write(uri + os.linesep)


def read():
    with io.open(CONFIG_PATH, 'rt', encoding='UTF-8', newline=None) as f:
        line = f.readline()
        return line


