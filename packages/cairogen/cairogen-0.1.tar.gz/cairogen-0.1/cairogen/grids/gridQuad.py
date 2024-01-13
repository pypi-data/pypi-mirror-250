import random as _random
from ..polys.poly import Poly
from ..lines.segment import Segment


class GridQuad:
    @staticmethod
    def coe_dir(A, B):
        if A[0] == B[0]:
            return float('inf')
        else:
            return (B[1] - A[1]) / (B[0] - A[0])

    @staticmethod
    def ord_ori(A, m):
        assert m != float('inf')

        return A[1] - m * A[0]

    @staticmethod
    def inter(mAB, pAB, mCD, pCD):
        assert mAB != float('inf')

        if mCD == float('inf'):
            x = pCD
        else:
            x = - (pAB - pCD) / (mAB - mCD)
        y = mAB * x + pAB

        return x, y

    def __init__(self, nl, nc, bbox, pointsHDBG=None):
        #
        self._nl = nl
        self._nc = nc
        # sens indirect
        self._coins = [bbox[0], (bbox[1][0], bbox[0][1]),
                       bbox[1], (bbox[0][0], bbox[1][1])]
        self.w = bbox[1][0] - bbox[0][0]
        self.h = bbox[1][1] - bbox[0][1]
        # génération des points sur les bords
        if not pointsHDBG:
            self._pth, self._ptd, self._ptb, self._ptg = (
                Segment(self._coins[0], self._coins[1]).npts(nc + 1)[1:-1],
                Segment(self._coins[1], self._coins[2]).npts(nl + 1)[1:-1],
                Segment(self._coins[3], self._coins[2]).npts(nc + 1)[1:-1],
                Segment(self._coins[0], self._coins[3]).npts(nl + 1)[1:-1]
            )
            # print(self._ptb)
        elif pointsHDBG == "random":
            self.rand_points(bbox)
        else:
            self._pth, self._ptd, self._ptb, self._ptg = pointsHDBG

        # on crée les lignes
        self._lignev, self._ligneh = self._lines_creation()
        # initialisation des quadrilatères
        self.quads = [[None for _ in range(self._nc)] for _ in range(self._nl)]

        # parcours secteur par secteur (du haut vers le bas)
        ligne_prec = [self._coins[0]] + self._pth + [self._coins[1]]
        for l in range(nl - 1):
            ligneh = self._ligneh[l]
            point_gche = self._ptg[l]
            ligne_constr = [point_gche]
            for c in range(nc - 1):
                lignev = self._lignev[c]
                I = self.inter(*ligneh, *lignev)
                self.quads[l][c] = Poly([ligne_prec[c], ligne_prec[c + 1],
                                         I, point_gche])
                self.quads[l][c].l = l
                self.quads[l][c].c = c
                point_gche = I
                ligne_constr.append(I)
            self.quads[l][nc - 1] = Poly([ligne_prec[nc - 1], ligne_prec[nc],
                                          self._ptd[l], I])
            self.quads[l][nc - 1].l = l
            self.quads[l][nc - 1].c = nc - 1
            ligne_constr.append(self._ptd[l])
            ligne_prec = ligne_constr
        # dernière ligne
        der_ligne = [self._coins[3]] + self._ptb + [self._coins[2]]
        for c in range(nc):
            self.quads[nl - 1][c] = Poly([ligne_prec[c], ligne_prec[c + 1],
                                          der_ligne[c + 1], der_ligne[c]])
            self.quads[nl - 1][c].l = nl - 1
            self.quads[nl - 1][c].c = c


    def __getitem__(self, indice):
        l = indice // self._nc
        c = indice % self._nc
        return self.quads[l][c]

    def _lines_creation(self):
        lignes_v = []
        for A, B in zip(self._pth, self._ptb):
            c = self.coe_dir(A, B)
            if c == float('inf'):
                # on se balade alors avec l'abscisse
                m = A[0]
            else:
                m = self.ord_ori(A, c)
            lignes_v.append((c, m))
        lignes_h = []
        for A, B in zip(self._ptg, self._ptd):
            c = self.coe_dir(A, B)
            m = self.ord_ori(A, c)
            lignes_h.append((c, m))
        return lignes_v, lignes_h

    def rand_points(self, bbox):
        self._pth = sorted([(self._coins[0][0] + _random.randrange(self.w),
                             bbox[0][1]) for i in range(self._nc - 1)],
                           key=lambda x: x[0])
        self._ptb = sorted([(self._coins[3][0] + _random.randrange(self.w),
                             bbox[1][1]) for i in range(self._nc - 1)],
                           key=lambda x: x[0])
        self._ptg = sorted([(bbox[0][0],
                             self._coins[0][1] + _random.randrange(self.h))
                            for i in range(self._nl - 1)],
                           key=lambda x: x[1])
        self._ptd = sorted([(bbox[1][0],
                             self._coins[1][1] + _random.randrange(self.h))
                            for i in range(self._nl - 1)],
                           key=lambda x: x[1])

    def draw(self, ctx,
             drawtype="stroke",
             f=None,
             operator=None,
             unclip=False):
        nl = list(range(self._nl))
        _random.shuffle(nl)
        nc = list(range(self._nc))
        _random.shuffle(nc)
        for l in nl:
            for c in nc:
                q = self.quads[l][c]
                ctx.save()
                q.draw(ctx, drawtype=drawtype, f=f, unclip=unclip)
                ctx.restore()
