import argparse


def parse_args():
    """
    Usage:
    vatan.py pull
    vatan.py reg <url>
    """

    parser = argparse.ArgumentParser()

#    parser.add_argument('-v', '--verbose', help='verbose output',
#                        action='store_const', dest='loglevel',
#                        const=logging.DEBUG, default=logging.INFO)

    subparsers = parser.add_subparsers(dest='command')

    get = subparsers.add_parser('get')
#    group = get.add_mutually_exclusive_group(required=True)
#    group.add_argument('--uri', type=None)
#    group.add_argument('--secret')

#    uri = subparsers.add_parser('uri')
#    uri.add_argument('secret')
#    uri.add_argument('--issuer')
#    uri.add_argument('--user')
#    uri.add_argument('--period')
#    uri.add_argument('--digits')

    qr_code = subparsers.add_parser('qrcode')

    config = subparsers.add_parser('configure')
#    qr_code.add_argument('secret')
#    qr_code.add_argument('--issuer')
#    qr_code.add_argument('--user')
#    qr_code.add_argument('--period')
#    qr_code.add_argument('--digits')

    return parser.parse_args()
