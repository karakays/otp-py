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
import logging

import pyperclip

from otp import TOKENS, CONFIG_PATH
from otp import core
from otp.token import Token, InvalidTokenUriError

logger = logging.getLogger(__name__)


async def run(args):
    try:
        argsd = {k: v for k, v in vars(args).items() if v}

        logging.basicConfig(level=argsd.pop('loglevel'))

        cmd = argsd.get('command')

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
                print(f'{t}')
        elif cmd == 'add':
            import io, os
            issuer = argsd.pop('issuer')
            secret = argsd.pop('secret')
            token = Token(issuer, secret, **argsd)
            uri = core.create_uri(token)
            with io.open(CONFIG_PATH, 'a+', encoding='UTF-8', newline=None) as f:
                f.write(uri + os.linesep)
        elif cmd == 'rm':
            import io, os
            TOKENS.pop(args.account)
            with io.open(CONFIG_PATH, 'w', encoding='UTF-8', newline=None) as f:
                for token in TOKENS.values():
                    f.write(token.uri + os.linesep)
    except InvalidTokenUriError:
        logger.error('Invalid token', exc_info=1)
    except KeyboardInterrupt:
        pass
    except Exception:
        logger.error('🤕 Oh no, something\'s wrong here', exc_info=1)


if __name__ == '__main__':
    run(None)
