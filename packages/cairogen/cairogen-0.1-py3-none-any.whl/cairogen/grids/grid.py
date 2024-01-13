import cairo as _cairo
import random as _random
from ..polys.carre import Carre


class Grid:
    def __init__(self, nl, nc, dim,
                 xy=(0, 0),
                 xyO=None,
                 angle=0,
                 mode="CORNER"):
        if xyO is None:
            xyO = (nc * dim / 2, nl * dim / 2)
        self._carres = [[None for _ in range(nc)] for _ in range(nl)]
        self.nl = nl
        self.nc = nc
        self.dim = dim
        self.xy = xy
        self.xyO = xyO
        self.angle = angle
        self.liste_exclusion = []
        self._liste_couleurs = []
        self._liste_outcouleurs = []
        self._liste_rotations = []
        self._liste_extradims = []
        for l in range(nl):
            for c in range(nc):
                self._carres[l][c] = Carre(l, c, dim, grid=True, mode=mode)

    def __getitem__(self, indice):
        l = indice // self.nc
        c = indice % self.nc
        return self._carres[l][c]

    @property
    def liste_couleurs(self):
        return self._liste_couleurs

    @liste_couleurs.setter
    def liste_couleurs(self, liste_couleurs):
        self._liste_couleurs = liste_couleurs
        for l in range(self.nl):
            for c in range(self.nc):
                self._carres[l][c].color = self._liste_couleurs[l][c]

    @property
    def liste_outcouleurs(self):
        return self._liste_outcouleurs

    @liste_outcouleurs.setter
    def liste_outcouleurs(self, liste_outcouleurs):
        self._liste_outcouleurs = liste_outcouleurs
        for l in range(self.nl):
            for c in range(self.nc):
                self._carres[l][c].outcolor = self._liste_outcouleurs[l][c]

    @property
    def liste_rotations(self):
        return self._liste_rotations

    @liste_rotations.setter
    def liste_rotations(self, liste_rotations):
        self._liste_rotations = liste_rotations
        for l in range(self.nl):
            for c in range(self.nc):
                self._carres[l][c].rotation = self._liste_rotations[l][c]

    @property
    def liste_extradims(self):
        return self._liste_extradims

    @liste_extradims.setter
    def liste_extradims(self, liste_extradims):
        self._liste_extradims = liste_extradims
        for l in range(self.nl):
            for c in range(self.nc):
                self._carres[l][c].extradim = self._liste_extradims[l][c]

    def draw(self, ctx, operator=_cairo.Operator.SCREEN):
        ctx.save()
        ctx.set_operator(operator)
        ctx.translate(*self.xyO)
        ctx.rotate(-self.angle)
        ctx.translate(-self.xyO[0], -self.xyO[1])
        ctx.translate(*self.xy)
        nl = list(range(self.nl))
        _random.shuffle(nl)
        nc = list(range(self.nc))
        _random.shuffle(nc)
        for l in nl:
            for c in nc:
                if (l, c) not in self.liste_exclusion:
                    self._carres[l][c].draw(ctx)
        ctx.restore()

    def fill(self, ctx, operator=_cairo.Operator.OVER):
        ctx.save()
        ctx.set_operator(operator)
        ctx.translate(*self.xyO)
        ctx.rotate(-self.angle)
        ctx.translate(-self.xyO[0], -self.xyO[1])
        ctx.translate(*self.xy)
        nl = list(range(self.nl))
        _random.shuffle(nl)
        nc = list(range(self.nc))
        _random.shuffle(nc)
        for l in nl:
            for c in nc:
                if (l, c) not in self.liste_exclusion:
                    self._carres[l][c].fill(ctx)
        ctx.restore()

    def filldraw(self, ctx, operator=_cairo.Operator.SCREEN):
        ctx.save()
        ctx.set_operator(operator)
        ctx.translate(*self.xyO)
        ctx.rotate(-self.angle)
        ctx.translate(-self.xyO[0], -self.xyO[1])
        ctx.translate(*self.xy)
        for l in range(self.nl):
            for c in range(self.nc):
                if (l, c) not in self.liste_exclusion:
                    self._carres[l][c].fill(ctx)
                    self._carres[l][c].draw(ctx)
        ctx.restore()
