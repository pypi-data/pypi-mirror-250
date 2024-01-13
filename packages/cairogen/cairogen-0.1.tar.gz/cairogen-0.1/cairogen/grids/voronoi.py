from scipy.spatial import Voronoi as _Voronoi
from ..polys.poly import Poly


class Voronoi:
    @staticmethod
    def pointage(supgch, infdrt, nbx, nby):
        x1, y1 = supgch
        x2, y2 = infdrt
        w = abs(x2 - x1)
        h = abs(y2 - y1)
        if x2 < x1:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        liste_x = [x1 + i * w / (nbx - 1) for i in range(nbx)]
        liste_y = [y1 + i * h / (nby - 1) for i in range(nby)]
        return [(a, b) for a in liste_x for b in liste_y]

    def reste_dans_limites(self, pt):
        return 0 <= pt[0] < self.W and 0 <= pt[1] < self.H

    @staticmethod
    def centre_bb(A, B):
        return tuple([(a + b) / 2 for a, b in zip(A, B)])

    # @staticmethod
    # def _poly(self, p):
    #     self.ctx.save()
    #     self.ctx.set_source_rgba(0, 0, 0, 0)
    #     self.move_to(*p[0])
    #     for pt in p[1:]:
    #         self.line_to(*pt)
    #     self.close_path()
    #     p = self.ctx.copy_path()
    #     self.ctx.retore()
    #     return p

    def __init__(self, xy0, xy1, xdim, ydim):
        self.points_init = self.pointage(xy0, xy1, xdim, ydim)
        self.points = self.points_init

    def poly_vor(self, W, H, f=lambda xy: xy):
        self.W = W
        self.H = H
        self.points = [f(xy) for xy in self.points]
        eloignement = 3
        self.points.append((-(eloignement - 1) * W, -(eloignement - 1) * H))
        self.points.append((eloignement * W, -(eloignement - 1) * H))
        self.points.append((-(eloignement - 1) * W, eloignement * H))
        self.points.append((eloignement * W, eloignement * H))

        self.points.append((-(eloignement - 1) * W, H / 2))
        self.points.append((eloignement * W, H / 2))
        self.points.append((W / eloignement, -(eloignement - 1) * H))
        self.points.append((W / eloignement, eloignement * H))

        self.vor = _Voronoi(self.points)
        polys = []
        for p in self.vor.regions:
            if p and -1 not in p:
                poly = [self.vor.vertices[i] for i in p]
                if all(map(self.reste_dans_limites, poly)):
                    polys.append(Poly(poly))
        return polys
