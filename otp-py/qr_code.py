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
