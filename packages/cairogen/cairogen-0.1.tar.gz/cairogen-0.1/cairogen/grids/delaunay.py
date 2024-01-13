import numpy as np
from scipy.spatial import Delaunay as _Delaunay


class Delaunay:
    def __init__(self, points):
        self.points_init = points
        self.points = np.asarray(points)

    def tri_del(self):
        self.dela = _Delaunay(self.points)
        return self.points[self.dela.simplices]
