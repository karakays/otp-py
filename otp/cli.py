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

import argparse
import logging


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--copy', action='store_true', help='copy code to clipboard')
    parser.add_argument('-p', '--progress', action='store_true', help='show progress bar')
    parser.add_argument('-a', '--account', action='store_const', const='default', help='select account')
    parser.add_argument('-v', '--verbose', action='store_const', const=logging.DEBUG, dest='loglevel',
                        default=logging.INFO, help='verbose output')

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = False

    subparsers.add_parser('ls')

    subparsers.add_parser('add')

    subparsers.add_parser('rm')

    return parser.parse_args()
