from .poly import Poly


class Carre(Poly):
    def __init__(self, ligne, colonne, dim,
                 extradim=0, mode="CORNER", grid=False):
        self._mode = mode
        self._x = colonne
        self._y = ligne
        self.dim = dim
        self._extradim = extradim
        self.rotation = 0
        if grid:
            self._x *= self.dim
            self._y *= self.dim
        self._init_dim()
        super().__init__(self._mon_carre)

    def _init_dim(self):
        if self._mode == "CORNER":
            self._mon_carre = [(self._x,
                                self._y),
                               (self._x + self.dim + self._extradim,
                                self._y),
                               (self._x + self.dim + self._extradim,
                                self._y + self.dim + self._extradim),
                               (self._x,
                                self._y + self.dim + self._extradim)]
        elif self._mode == "CENTER":
            d2 = (self.dim + self._extradim) / 2
            self._mon_carre = [(self._x - d2, self._y - d2),
                               (self._x + d2, self._y - d2),
                               (self._x + d2, self._y + d2),
                               (self._x - d2, self._y + d2)]

    @property
    def extradim(self):
        return self._extradim

    @extradim.setter
    def extradim(self, extradim):
        self._extradim = extradim
        self._init_dim()
        self.poly = self._mon_carre

    def fill(self, ctx):
        ctx.save()
        if self._mode == "CORNER":
            X = self._x
            Y = self._y
        elif self._mode == "CENTER":
            X = self._x# + self.dim / 2
            Y = self._y# + self.dim / 2
        ctx.translate(X, Y)
        ctx.rotate(self.rotation)
        ctx.translate(-X, -Y)
        ctx.set_source_rgba(*self.color)
        super().draw(ctx, drawtype="fill")
        ctx.fill()
        ctx.restore()

    def draw(self, ctx):
        ctx.save()
        if self._mode == "CORNER":
            X = self._x
            Y = self._y
        elif self._mode == "CENTER":
            X = self._x# + self.dim / 2
            Y = self._y# + self.dim / 2
        ctx.translate(X, Y)
        ctx.rotate(self.rotation)
        ctx.translate(-X, -Y)
        ctx.set_source_rgba(*self.outcolor)
        super().draw(ctx, drawtype="stroke")
        ctx.stroke()
        ctx.restore()
