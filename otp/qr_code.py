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

import pyqrcode
from enum import Enum


class RenderTargetType(Enum):
    TERMINAL = ('terminal')
    TEXT     = ('text')
    SVG      = ('svg')

    def __init__(self, renderer):
        self.renderer = renderer

    def render(self, qr):
        func = getattr(qr, self.renderer)
        return func(quiet_zone=1)

    @staticmethod
    def fromValue(value):
        for r in RenderTargetType:
            if(value.upper() == r.name):
                return r
        else:
            return None


def create_qr_code(url, render_target=RenderTargetType.TERMINAL):
    code = pyqrcode.create(url, error='L', version=5, encoding='utf-8')
    return render_target.render(code)
