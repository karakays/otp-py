import sys, time
#import logging
from token import Token, InvalidTokenUriError
from progress import Progress, Bar

#logger = logging.getLogger(__name__)

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
               
        #logger.debug('xxx'.format(p, r, token_code.progress))
        for i in progress.iter(range(int(r * 30))):
            time.sleep(1)

    except InvalidTokenUriError:
        print('Invalid uri', url, file=sys.stderr)
    except KeyboardInterrupt:
        pass


def track_progress(token_code):
    rem = token_code.remaining()
    for i in range(rem + 1):
        out = ('\r[{}{}]'.format('*' * (token_code.block - token_code.remaining()), '-' * token_code.remaining()))
        sys.stdout.write(out)
        sys.stdout.flush()
        sleep(1)
    else:
        sys.stdout.write('\n')


if __name__ == '__main__':
    main()
