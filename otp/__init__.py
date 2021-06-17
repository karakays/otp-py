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
import base64
import io
import os
from urllib.parse import urlparse, parse_qs, unquote

from . import core
from . import qr_code
from . import progress
from . import token
from . import configure
from .token import InvalidTokenUriError, Token

CONFIG_PATH = os.environ["HOME"] + '/.otp/' + 'config'

TOKENS = {}


def parse_otp_uri(uri):
    if uri.scheme != 'otpauth':
        raise InvalidTokenUriError('Invalid scheme')

    params = parse_qs(uri.query)

    secret = params.get('secret')
    if secret:
        secret = secret[0]
        del params['secret']
    else:
        raise InvalidTokenUriError('Invalid secret')

    kwargs = {'secret': secret, 'type': uri.netloc}
    label = uri.path[1:]
    issuer, user = label.split(':')
    kwargs['issuer'] = issuer
    kwargs['user'] = user

    for k, v in params.items():
        kwargs[k] = v[0]

    return kwargs


with io.open(CONFIG_PATH, 'rt', encoding='UTF-8', newline=None) as f:
    sanitized = (line for line in f if not line.lstrip().startswith("#"))
    for index, line in enumerate(sanitized, start=1):
        uri = urlparse(unquote(line))
        token_args = parse_otp_uri(uri)
        secret = base64.b32decode(token_args['secret'])
        period = int(token_args['period'])
        digits = int(token_args['digits'])
        t = Token(index, None, issuer=token_args['issuer'], user=token_args['user'], secret=secret,
                  period=period, algorithm=token_args['algorithm'], digits=digits)
        TOKENS[index] = t
