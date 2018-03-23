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
import sys
import time
# import logging
import core
from urllib.parse import urlparse, unquote
from token import Token, InvalidTokenUriError
from progress import Progress, Bar

# logger = logging.getLogger(__name__)


def main():
    arg = sys.argv[1]
    try:
        uri = urlparse(unquote(arg))

        token = core.get_otp_by_uri(uri)

        token_code = token.generateCode()

        p = token_code.progress
        r = 1 - p
        progress = Progress(index=(token_code.progress * 30), mxm=30)

        message = 'Code = {}, progress '.format(token_code.code)
        bar = Bar(message)
        progress.attach(bar)

        # logger.debug('xxx'.format(p, r, token_code.progress))
        #for i in progress.iter(range(int(r * 30))):
        #    time.sleep(1)

        qr_code = core.create_qr_code(token)
        print(qr_code)

    except InvalidTokenUriError as e:
        print(e)
        pass
        # print('Invalid uri', url, file=sys.stderr)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
