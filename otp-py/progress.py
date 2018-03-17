import time, sys

from datetime import timedelta


class Progress(object):
    def __init__(self, *args, **kwargs):
        index = kwargs.get('index')
        self.index = index if index else 0
        mxm = kwargs.get('mxm')
        self.max = mxm if mxm else 100
        self.start = time.time()
        self.avg = 0
        self.step_start = self.start
        self.observers = []

    @property
    def elapsed(self):
        return int(time.time() - self.start)

    @property
    def elapsed_td(self):
        return timedelta(seconds = self.elapsed)

    @property
    def progress(self):
        return min(1, self.index / self.max)

    @property
    def percent(self):
        return self.progress * 100

    @property
    def remaining(self):
        return max(0, self.max - self.index)

    def finish(self):
        pass

    def next(self, i = 1):
        now = time.time()
        dt = now - self.step_start
        self.step_start = now
        self.index = self.index + i
        self.notify()

    def iter(self, it):
        try:
            for i in it:
                yield i
                self.next()
        finally:
                self.finish()

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for o in self.observers:
            o.update(self)


class Bar(object):
    fill = '*'
    empty = '-'
    width = 40

    def __init__(self, message=''):
        self.message = message

    def update(self, progress):
        p = int(progress.progress * self.width)
        r = self.width - p

        out = ('\r{}[{}{}]'.format(self.message, p * self.fill , r * self.empty))
        sys.stdout.write(out)
        sys.stdout.flush()

