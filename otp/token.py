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

import logging
import time
import hmac
import hashlib
import functools
import base64
from enum import Enum


logger = logging.getLogger(__name__)


class TokenCode:
    def __init__(self, code, start, end):
        self.start = start
        self.end = end
        self.code = code

    @property
    def block(self):
        return self.end - self.start

    @property
    def progress(self):
        current = time.time()

        if current >= self.end:
            return 0

        p = (current - self.start)
        return (p / self.block)

    @property
    def remaining(self):
        current = time.time()
        rem = self.end - current
        return 0 if rem <= 0 else int(rem)


class TokenType(Enum):
        HOTP, TOTP = range(2)

        @staticmethod
        def fromValue(value):
            if value == 'hotp':
                return TokenType.HOTP
            elif value == 'totp':
                return TokenType.TOTP
            else:
                return None

        def __str__(self):
            return self.name.lower()


class Token:
    def __init__(self, t_type, issuer, user, secret,
                 period, algorithm, digits):
        self.type = t_type
        self.issuer = issuer
        self.user = user
        self.secret = secret
        self.period = period
        self.algorithm = algorithm
        self.digits = digits

    def toUri(self):
        """
        otpauh://TYPE/LABEL?PARAMS where
        LABEL is issuer:user
        """
        from urllib.parse import urlunsplit, urlencode
        query = {'secret': base64.b32encode(self.secret), 'period': self.period,
                 'algorithm': self.algorithm, 'digits': self.digits}

        return urlunsplit(('otpauth', self.type.__str__(),
                           self.issuer + ':' + self.user,
                           urlencode(query), None))

    def generateCode(self):
        start = time.time()
        counter = int(start / self.period)
        logger.debug('Getting mac of counter %s', counter)
        mac = hmac.new(self.secret, counter.to_bytes(8, 'big'), hashlib.sha1)
        digest = mac.digest()
        offset = digest[len(digest) - 1] & 0x0f
        logger.debug('Found offset of %s', offset)
        buf = [digest[i + offset] << (8 * (3 - i)) for i in range(4)]
        res = functools.reduce((lambda x, y: x | y), buf)
        code = res % (10 ** self.digits)
        code = str(code)

        while len(code) < self.digits:
            code = '0' + code

        return TokenCode(code, (counter + 0) * self.period,
                         (counter + 1) * self.period)

    @classmethod
    def fromUri(cls, uri):
        from urllib.parse import parse_qs

        scheme = uri.scheme

        if scheme != 'otpauth':
            raise InvalidTokenUriError('Invalid scheme', scheme)

        token_type = TokenType.fromValue(uri.netloc)
        if not token_type:
            raise InvalidTokenUriError()

        label = uri.path
        if not label:
            raise InvalidTokenUriError()

        issuer, user = label[1:].split(':')

        params = parse_qs(uri.query)

        secret = params.get('secret')
        secret = None if not secret else secret[0]
        if not secret:
            raise InvalidTokenUriError()

        period = params.get('period')
        try:
            period = 30 if not period else int(period[0])
        except ValueError:
            raise InvalidTokenUriError()

        digits = params.get('digits')
        try:
            digits = 6 if not digits else int(digits[0])
            if digits not in (6, 7, 8):
                raise ValueError
        except ValueError:
            raise InvalidTokenUriError()

        issuer_q = params.get('issuer')
        try:
            if issuer_q:
                if issuer and issuer_q[0] != issuer:
                    raise ValueError
                else:
                    issuer = issuer_q[0]
        except ValueError:
            raise InvalidTokenUriError()

        algorithm = params.get('algorithm')
        try:
            algorithm = 'SHA1' if not algorithm else algorithm[0]
            if algorithm not in ('SHA1', 'SHA256', 'SHA512'):
                raise ValueError
        except ValueError:
            raise InvalidTokenUriError()

        return Token(token_type, issuer, user, secret,
                     period, algorithm, digits)

    @classmethod
    def fromString(cls, string):
        from urllib.parse import urlparse, unquote
        return Token.fromUri(urlparse(unquote(string)))

    def __str__(self):
        return 'Token[issuer={}, user={}, secret={}, digits={},\\\
                algorithm={}, period={}]'.format(self.issuer, self.user,
                                                 self.secret, self.digits,
                                                 self.algorithm, self.period)


class InvalidTokenUriError(Exception):
    def __init__(self, msg=None, value=None):
        self.args = (msg, value)
        self.msg = msg
        self.value = value
