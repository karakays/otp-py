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
from datetime import datetime, timedelta


CURSOR_POS = 1
ANSI_CSI = "\x1B["

PB_PERIOD = 0.1
PB_FREQUENCY = int(1 / PB_PERIOD)
PB_TIME_STEP = PB_PERIOD


class AnsiEscapes(object):

    @staticmethod
    def cursor_up(count=1):
        return f"{ANSI_CSI}{str(count)}A"

    @staticmethod
    def cursor_down(count=1):
        return f"{ANSI_CSI}{str(count)}B"

    @staticmethod
    def cursor_forward(count=1):
        return f"{ANSI_CSI}{str(count)}C"

    @staticmethod
    def cursor_backward(count=1):
        return f"{ANSI_CSI}{str(count)}D"

    @staticmethod
    def cursor_move(x, y):
        direction = ''
        if x > 0:
            direction = AnsiEscapes.cursor_forward(x)
        elif x < 0:
            direction = AnsiEscapes.cursor_backward(abs(x))

        if y > 0:
            direction += AnsiEscapes.cursor_up(y)
        elif y < 0:
            direction += AnsiEscapes.cursor_down(abs(y))

        return direction

    @staticmethod
    def hide_cursor():
        return f"{ANSI_CSI}?25l"

    @staticmethod
    def show_cursor():
        return f"{ANSI_CSI}?25h"

    @staticmethod
    def clear_line():
        return f"{ANSI_CSI}2K"

    @staticmethod
    def red_color(text):
        return f"{ANSI_CSI}32m{text}{ANSI_CSI}0m"

    @staticmethod
    def green_color(text):
        return f"{ANSI_CSI}31m{text}{ANSI_CSI}0m"

    @staticmethod
    def yellow_color(text):
        return f"{ANSI_CSI}33m{text}{ANSI_CSI}0m"


class Progress(object):
    def __init__(self, **kwargs):
        self._index = kwargs.get('index', 0)
        self._finish = kwargs.get('mxm', 100)
        self.created = datetime.now()
        self.start_time = self.created - timedelta(seconds=self._index)
        self.step_start = self.created
        self.avg = 0
        self.observers = []
        sys.stdout.write(AnsiEscapes.hide_cursor())

    @property
    def elapsed_time(self):
        return datetime.now() - self.start_time

    @property
    def progress(self):
        return min(1, self._index / self._finish)

    @property
    def percent(self):
        return self.progress * 100

    @property
    def remaining(self):
        return max(0, self._finish - self._index)

    @property
    def remaining_time(self):
        return timedelta(seconds=max(0, self._finish - self._index))

    def finalize(self):
        sys.stdout.write(AnsiEscapes.show_cursor())
        sys.stdout.flush()

    def next(self, i=1):
        now = datetime.now()
        dt = now - self.step_start
        self.step_start = now
        self._index = self._index + i
        self.notify()

    def iter(self, it):
        try:
            for i in it:
                yield i
                self.next(PB_TIME_STEP)
                raise Exception
        except Exception:
            self.finalize()
            raise

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for o in self.observers:
            o.update(self)

    def __str__(self):
        return f"Progress index={self._index}," \
               f"fin={self._finish}," \
               f"remaining={self.remaining}," \
               f"remaining_time={self.remaining_time}" \
               f"elapsed_time={self.elapsed_time}"


class Bar(object):
    fill = '*'
    empty = '-'
    width = 40

    def __init__(self, token, code):
        self.token = token
        self.code = code

    # https://tldp.org/HOWTO/Bash-Prompt-HOWTO/x361.html
    def update(self, progress):
        global CURSOR_POS
        p = int(progress.progress * self.width)
        r = self.width - p

        if progress.percent > 80:
            token_code = AnsiEscapes.green_color(self.code)
        elif progress.percent > 60:
            token_code = AnsiEscapes.yellow_color(self.code)
        else:
            token_code = AnsiEscapes.red_color(self.code)

        out = f"\r🔑 {self.token.issuer} {token_code} [{p * self.fill}{r * self.empty}]"

        cursor_pos = CURSOR_POS - self.token._index
        sys.stdout.write(AnsiEscapes.cursor_move(0, cursor_pos))
        sys.stdout.write(out)
        sys.stdout.flush()
        CURSOR_POS = self.token._index


class Timer(object):
    spinner = '⠁⠉⠙⠸⢰⣠⣄⡆⠇⠃'
    issuer_padding = 0

    def __init__(self, token, code):
        self.spinner_index = 0
        self.token = token
        self.code = code

    def update(self, progress):
        global CURSOR_POS

        self.spinner_index = (self.spinner_index + 1) % len(Timer.spinner)

        if progress.percent > 80:
            token_code = AnsiEscapes.green_color(self.code)
        elif progress.percent > 60:
            token_code = AnsiEscapes.yellow_color(self.code)
        else:
            token_code = AnsiEscapes.red_color(self.code)

        if len(self.token.id) > Timer.issuer_padding:
            Timer.issuer_padding = len(self.token.id)

        out = f"\r🔑️ {self.token.id.ljust(Timer.issuer_padding)} ➡ {token_code} " \
              f"{Timer.spinner[self.spinner_index]} {int(progress.remaining_time.seconds)}"

        cursor_pos = CURSOR_POS - self.token._index
        sys.stdout.write(AnsiEscapes.cursor_move(0, cursor_pos))
        sys.stdout.write(AnsiEscapes.clear_line())
        sys.stdout.write(out)
        sys.stdout.flush()
        CURSOR_POS = self.token._index
