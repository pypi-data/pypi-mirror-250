import cairo as _cairo


class Poly:
    def __init__(self, poly):
        self._poly = poly
        self._poly_init = poly
        self._color = (0, 0, 0)
        self._outcolor = (1, 1, 1)
        self._scale = 1
        self._rotate = 0
        self.visible = True
        self._matrix = None
        self._l = None
        self._c = None

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, m):
        self._matrix = m

    @property
    def l(self):
        return self._l

    @l.setter
    def l(self, l):
        self._l = l

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, c):
        self._c = c

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def outcolor(self):
        return self._outcolor

    @outcolor.setter
    def outcolor(self, outcolor):
        self._outcolor = outcolor

    @property
    def poly(self):
        return self._poly

    @poly.setter
    def poly(self, poly):
        self._poly = poly

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale
        self._set_matrix()

    @property
    def rotate(self):
        return self._rotate

    @rotate.setter
    def rotate(self, rotate):
        self._rotate = rotate
        self._set_matrix()

    def _set_matrix(self):
        X, Y = self.center()
        self._matrix = _cairo.Matrix()
        self._matrix.translate(X, Y)
        self._matrix.rotate(self._rotate)
        self._matrix.scale(self._scale, self._scale)
        self._matrix.translate(-X, -Y)

    def get_poly_points(self):
        return [self._matrix.transform_point(*pt)
                for pt in self._poly]

    def get_bbox(self):
        pts = self.get_poly_points()
        minX = min(pts, key=lambda x: x[0])
        maxX = max(pts, key=lambda x: x[0])
        minY = min(pts, key=lambda x: x[1])
        maxY= max(pts, key=lambda x: x[1])
        return [(minX, minY), (maxX, maxY)]

    def center(self):
        X = sum(x[0] for x in self._poly) / len(self._poly)
        Y = sum(x[1] for x in self._poly) / len(self._poly)
        return X, Y

    def _ext_fun(self, ctx, xy, f):
        X, Y = xy
        ctx.save()
        ctx.translate(X, Y)
        f(ctx, self)
        ctx.restore()

    def draw(self, ctx,
             drawtype="stroke",
             f=None,
             unclip=False):
        X, Y = self.center()
        M = _cairo.Matrix()
        M.translate(X, Y)
        M.rotate(self._rotate)
        M.scale(self._scale, self._scale)
        M.translate(-X, -Y)
        self._matrix = M
        ctx.transform(M)
        ctx.move_to(*self._poly[0])
        for point in self._poly[1:]:
            ctx.line_to(*point)
        ctx.close_path()
        p = ctx.copy_path()
        #
        if drawtype == "fill":
            ctx.save()
            ctx.set_source_rgba(*self.color)
            ctx.fill()
            ctx.restore()
        elif drawtype == "fillstroke":
            ctx.save()
            ctx.set_source_rgba(*self.outcolor)
            ctx.stroke()
            ctx.append_path(p)
            ctx.set_source_rgba(*self.color)
            ctx.fill()
            ctx.restore()
        elif drawtype == "stroke":
            ctx.save()
            ctx.set_source_rgba(*self.outcolor)
            ctx.stroke()
            ctx.restore()
        else:
            pass
        #
        if not unclip:
            ctx.append_path(p)
            ctx.clip()
        if f is not None:
            self._ext_fun(ctx, (X, Y), f)
        if not unclip:
            ctx.reset_clip()

    def draw_segment(self, ctx, index):
        ctx.move_to(*self._poly[index])
        ctx.line_to(*self._poly[index + 1])
