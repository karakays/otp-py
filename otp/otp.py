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
import logging

import pyperclip

from otp import configure, TOKENS
from otp import core
from otp.token import Token, TokenType, InvalidTokenUriError

logger = logging.getLogger(__name__)


async def run(args):
    try:
        args_dict = {k: v for k, v in vars(args).items() if v}

        logging.basicConfig(level=args_dict.pop('loglevel'))

        cmd = args_dict.get('command')

        logger.debug('Command=%s is being called %s', cmd)
        if cmd is None:
            if args.account:
                token = TOKENS[args.account]
                if args.copy:
                    code = token.generateCode().code
                    pyperclip.copy(code)
                    print("Code is in your clipboard ✔️")
                else:
                    await asyncio.gather(core.progress(token))
            else:
                print("🤖 Generating codes...")
                await asyncio.gather(*(core.progress(token) for token in TOKENS.values()))
        elif cmd == 'ls':
            for t in TOKENS.values():
                print(f'{t.index}: {t}')
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
    run(None)
