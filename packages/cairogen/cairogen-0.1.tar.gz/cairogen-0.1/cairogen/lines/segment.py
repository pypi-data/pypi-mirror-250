from ..helpers.helpers import dist

class Segment:
    def __init__(self, xy0, xy1, f=None, **kwargs):
        self.f = f
        self.f_kwargs = kwargs
        self._ori = xy0
        self._ext = xy1

    def len(self):
        return dist(self._ori, self._ext)

    def npts(self, n, f=lambda x: x, ar=True, reverse=False):
        if reverse:
            deb, fin = self._ext, self._ori
        else:
            deb, fin = self._ori, self._ext

        coeffs = [f(i / (n - 1)) for i in range(n)]

        pts = []
        for i in range(n):
            c = coeffs[i]
            pts.append(
                (deb[0] + c * (fin[0] - deb[0]),
                 deb[1] + c * (fin[1] - deb[1]))
            )
        return pts

    def point(self, k):
        return (k*self._ori[0] + (1-k)*self._ext[0],
                k*self._ori[1] + (1-k)*self._ext[1])

    def slope(self):
        if self._ori[0] == self._ext[0]:
            s = float('inf')
        else:
            s = (self._ext[1] - self._ori[1]) / (self._ext[0] - self._ori[0])
        return s

    def im(self, x):
        if self._ori[0] == self._ext[0]:
            return None
        else:
            m = (self._ext[1] - self._ori[1]) / (self._ext[0] - self._ori[0])
            p = self._ori[1] - m * self._ori[0]
            return m * x + p

    def an(self, y):
        if self._ori[1] == self._ext[1]:
            return None
        elif self._ori[0] == self._ext[0]:
            return self._ori[0]
        else:
            m = (self._ext[1] - self._ori[1]) / (self._ext[0] - self._ori[0])
            p = self._ori[1] - m * self._ori[0]
            return (self._ori[1] - p) / m

    def draw(self, ctx, f=None):
        if self.f is not None:
            self.f(self._ori, self._ext, **self.f_kwargs)
        else:
            ctx.save()
            ctx.move_to(*self._ori)
            ctx.line_to(*self._ext)
            ctx.restore()
