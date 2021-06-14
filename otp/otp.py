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
import logging
import os
import asyncio

from urllib.parse import urlparse, unquote, parse_qs

import pyperclip

from otp import cli
from otp import configure
from otp import core

from otp.token import Token, TokenType, InvalidTokenUriError

logger = logging.getLogger(__name__)

CONFIG_PATH = os.environ["HOME"] + '/.otp/' + '.otprc'


async def run():
    try:
        args = cli.parse_args()
        args_dict = {k: v for k, v in vars(args).items() if v}

        logging.basicConfig(level=args_dict.pop('loglevel'))

        cmd = args_dict.get('command')

        logger.debug('Command=%s is being called %s', cmd)
        if cmd == None:
            tokens = list_otp()

            if args.progress:
                print("🤖 Generating codes...")
                await asyncio.gather(*(core.progress(token) for token in tokens))

            account = None
            if args.account:
                # fetch account
                pass

            code = tokens[0].generateCode().code

            if args.copy:
                pyperclip.copy(code)
                print("Code is in your clipboard ✔️")
            else:
                print(code)
        elif cmd == 'ls':
            tokens = list_otp()
            for t in enumerate(tokens, start=1):
                print(f'{t[0]}. {t[1]}')
        elif cmd == 'config':
            configure.configure()
        else:
            assert cmd, 'Unknown command {}'.format(cmd)
    except InvalidTokenUriError:
        logger.error('Invalid token', exc_info=1)
    except KeyboardInterrupt:
        pass
    except Exception:
        logger.error('🤕 Oh no, something\'s wrong here', exc_info=1)


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


def list_otp():
    tokens = []
    with io.open(CONFIG_PATH, 'rt', encoding='UTF-8', newline=None) as f:
        for index, line in enumerate(f):
            uri = urlparse(unquote(line))
            token_args = parse_otp_uri(uri)
            secret = base64.b32decode(token_args['secret'])
            period = int(token_args['period'])
            digits = int(token_args['digits'])
            t = Token(index, None, issuer=token_args['issuer'], user=token_args['user'], secret=secret,
                      period=period, algorithm=token_args['algorithm'], digits=digits)
            tokens.append(t)
    return tokens


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

    return Token(t_type=token_type, issuer=issuer, user=user, secret=secret, period=period, algorithm=algorithm, digits=digits)


def add_token():
    pass


if __name__ == '__main__':
    run()
