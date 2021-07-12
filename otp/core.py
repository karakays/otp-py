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
from urllib.parse import urlunsplit, urlencode

from otp import qr_code
from otp.progress import Progress, Timer


def create_uri(token):
    """
    otpauh://TYPE/LABEL?PARAMS
    where LABEL is of form issuer:account
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
    while True:
        token_code = token.generateCode()
        current = token_code.progress

        progress = Progress(index=(current * token.period), mxm=token.period)

        bar = Timer(token, token_code.code)
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
