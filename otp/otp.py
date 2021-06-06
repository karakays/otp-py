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

CONFIG_PATH = os.environ["HOME"] + '/.otp/'+ '.otprc'


async def run():
    try:
        args = cli.parse_args()
        args_dict = {k: v for k, v in vars(args).items() if v}

        logging.basicConfig(level=args_dict.pop('loglevel'))

        cmd = args_dict.get('command')

        logger.debug('Command=%s is being called %s', cmd)
        if cmd == None:
            #config = configure.read()
            #uri = urlparse(unquote(config))
            #token = core.get_otp_by_uri(uri)

            tokens = list_otp()

            # logger.debug('Built a new token %s', token)
            if args.progress:
                # while True:
                    #for token in tokens:
                        #await core.progress(token)
                    # core.progress_wrapper(token)
                print("✨ Generating codes...")
                await asyncio.gather(*(core.progress(token) for token in tokens))

            account = None
            if args.account:
                # fetch account
                pass

            code = tokens[0].generateCode().code

            if args.copy:
                pyperclip.copy(code)
                print("🥳 Code is in your clipboard!")
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
        logger.error('Something\'s wrong here', exc_info=1)


if __name__ == '__main__':
    run()
