import math as _math
from .segment import Segment


class Line:
    def __init__(self, xy, angle):
        self.xy = xy
        self.angle = angle

    def draw(self, ctx, bbox):
        # angle est transformé pour appartenir à ]-90;90]
        # 0 et 90 étant traités comme cas particuliers
        angle = _math.degrees(self.angle)
        # angle = -angle + 90
        angle = angle % 360 - 180
        if angle > 90:
            angle -= 180
        elif angle < -90:
            angle += 180
        elif angle == -90:
            angle = 90
        # bbox -> carre
        inf_gche = bbox[0]
        sup_droit = bbox[1]
        w, h = sup_droit[0] - inf_gche[0], sup_droit[1] - inf_gche[1]
        if w < h:
            d = (h - w) / 2
            inf_gche = (inf_gche[0] - d, inf_gche[1])
            sup_droit = (sup_droit[0] + d, sup_droit[1])
        elif h < w:
            d = (w - h) / 2
            inf_gche = (inf_gche[0], inf_gche[1] - d)
            sup_droit = (sup_droit[0], sup_droit[1] + d)
        # la droite perp. aux hachures passant par le centre
        centre = [(inf_gche[i] + sup_droit[i]) / 2 for i in range(2)]
        centre = self.xy
        if angle != 0 and angle != 90:
            pente = _math.tan(_math.radians(angle))
            invpente = 1 / pente
            droite = lambda x: pente * (x - centre[0]) + centre[1]
            invdroite = lambda y: (y - centre[1] + pente * centre[0]) * invpente
            if -45 <= angle <= 45:
                debut = (inf_gche[0], droite(inf_gche[0]))
                fin = (sup_droit[0], droite(sup_droit[0]))
            else:
                debut = (invdroite(inf_gche[1]), inf_gche[1])
                fin = (invdroite(sup_droit[1]), sup_droit[1])
        elif angle == 90:
            debut = (centre[0], inf_gche[1])
            fin = (centre[0], sup_droit[1])
        elif angle == 0:
            debut = (inf_gche[0], centre[1])
            fin = (sup_droit[0], centre[1])
        #
        s = Segment(debut, fin)
        s.draw(ctx)
