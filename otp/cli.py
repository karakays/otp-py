import argparse


def parse_args():
    parser = argparse.ArgumentParser()

#    parser.add_argument('-v', '--verbose', help='verbose output',
#                        action='store_const', dest='loglevel',
#                        const=logging.DEBUG, default=logging.INFO)

    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('get')

    subparsers.add_parser('qrcode')

    subparsers.add_parser('config')

    return parser.parse_args()
