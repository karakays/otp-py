# MIT License
#
# Copyright (c) 2018 Selçuk Karakayalı
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import asyncio
import base64
import binascii
from urllib.parse import parse_qs, urlunsplit, urlencode

import cv2 as cv

from otp import qr_code
from otp.progress import Progress, Bar, Timer
from otp.token import Token, TokenType, InvalidTokenUriError


def get_otp_by_uri(uri):
    if uri.scheme != 'otpauth':
        raise InvalidTokenUriError()

    params = parse_qs(uri.query)

    secret = params.get('secret')
    if secret:
        secret = secret[0]
        del params['secret']
    else:
        raise InvalidTokenUriError('Secret cannot be null')

    kwargs = {}
    kwargs['type'] = uri.netloc
    label = uri.path[1:]
    issuer, user = label.split(':')
    kwargs['issuer'] = issuer
    kwargs['user'] = user

    for k, v in params.items():
        kwargs[k] = v[0]

    return get_otp_by_secret(secret, **kwargs)


def get_otp_by_qrcode(file):
    im = cv.imread(file)
    det = cv.QRCodeDetector()
    retval, points, straight_qrcode = det.detectAndDecode(im)
    return get_otp_by_uri(retval)


def get_otp_by_secret(secret, **kwargs):
    if not secret:
        raise InvalidTokenUriError('Secret cannot be null')

    try:
        secret = base64.b32decode(secret)
    except binascii.Error as e:
        raise InvalidTokenUriError('Invalid secret', secret) from e

    token_type = TokenType.fromValue(kwargs.get('type', 'hotp'))

    issuer = kwargs.get('issuer')
    user = kwargs.get('user')

    period = kwargs.get('period')
    try:
        period = 30 if not period else int(period)
    except ValueError as e:
        raise InvalidTokenUriError('Invalid period', period) from e

    digits = kwargs.get('digits')
    try:
        digits = 6 if not digits else int(digits)
        if digits not in (6, 7, 8):
            raise ValueError
    except ValueError as e:
        raise InvalidTokenUriError('Invalid digits', digits) from e

    algorithm = kwargs.get('algorithm')
    try:
        algorithm = 'SHA1' if not algorithm else algorithm
        if algorithm not in ('SHA1', 'SHA256', 'SHA512'):
            raise ValueError
    except ValueError as e:
        raise InvalidTokenUriError('Invalid encryption algorithm',
                                   algorithm) from e

    return Token(t_type=token_type, issuer=issuer, user=user, secret=secret, period=period,
                 algorithm=algorithm, digits=digits)


def create_uri(token):
    """
    otpauh://TYPE/LABEL?PARAMS
    where LABEL of form issuer:account
    """
    query = {'secret': base64.b32encode(token.secret), 'period': token.period,
             'algorithm': token.algorithm, 'digits': token.digits}

    path = [e for e in (token.issuer, token.user) if e]

    label = ':'.join(path)

    return urlunsplit(('otpauth', token.type.__str__(),
                       label,
                       urlencode(query), None))


def create_qrcode(token):
    uri = create_uri(token)
    return qr_code.create_qr_code(uri)


async def progress(token):
    bar = Timer()

    while True:
        token_code = token.generateCode()
        current = token_code.progress

        progress = Progress(index=(current * token.period), mxm=token.period)
        message = f'{token.issuer}, code = {token_code.code}'
        bar.message = message

        progress.attach(bar)

        # iterate the remaining range
        # let progress bar render until token expires completely
        rem_rng = range(token_code.remaining)

        for i in progress.iter(rem_rng):
            await asyncio.sleep(1)


class Account:
    def __init__(self, issuer, user):
        self.issuer = issuer
        self.user = user
