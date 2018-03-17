import sys
import time
# import logging
from token import Token, InvalidTokenUriError
from progress import Progress, Bar

# logger = logging.getLogger(__name__)


def main():
    url = sys.argv[1]
    try:
        token = Token.fromString(url)

        token_code = token.generateCode()

        p = token_code.progress
        r = 1 - p
        progress = Progress(index=(token_code.progress * 30), mxm=30)

        message = 'Code = {}, progress '.format(token_code.code)
        bar = Bar(message)
        progress.attach(bar)

        # logger.debug('xxx'.format(p, r, token_code.progress))
        for i in progress.iter(range(int(r * 30))):
            time.sleep(1)

    except InvalidTokenUriError:
        pass
        # print('Invalid uri', url, file=sys.stderr)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
