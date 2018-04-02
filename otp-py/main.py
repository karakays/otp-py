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

# import logging
import cli
import core
import configure
from urllib.parse import urlparse, unquote
from token import InvalidTokenUriError

# logger = logging.getLogger(__name__)


def main():
    try:
        args = {k: v for k, v in vars(cli.parse_args()).items() if v}
        cmd = args.pop('command')

        if cmd == 'get':
            config = configure.read()
            uri = urlparse(unquote(config))
            token = core.get_otp_by_uri(uri)
            print(token)
            # iterate progress
            for i in core.progress(token):
                pass
        elif cmd == 'qrcode':
            config = configure.read()
            uri = urlparse(unquote(config))
            token = core.get_otp_by_uri(uri)
            print(core.create_qrcode(token))
        elif cmd == 'config':
            configure.configure()
        else:
            assert cmd, 'Unknown command {}'.format(cmd)
    except InvalidTokenUriError as e:
        print(e)
        pass
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print('Caught it', e)


if __name__ == '__main__':
    main()
