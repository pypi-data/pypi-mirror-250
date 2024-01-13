class Particle:
    def __init__(self, xy,
                 vit=(0, 0),
                 accel=(0, 0),
                 masse=1,
                 lifetime=100,
                 color=(0, 0, 0),
                 bbox=[(0, 0), (1000, 1000)]):
        self.xy = xy
        self.vit = vit
        self.accel = accel
        self.masse = masse
        self.lifetime = lifetime
        self.color = color
        self.bbox = bbox

    def edges(self):
        x, y = self.xy
        infg, supd = self.bbox
        if x >= supd[0] or x <= infg[0]:
            x = max(infg[0], min(x, supd[0]))
            self.vit = (-self.vit[0], self.vit[1])
        elif y <= infg[1] or y > supd[1]:
            self.vit = (self.vit[0], -self.vit[1])
            y = max(infg[1], min(y, supd[1]))
        self.xy = (x, y)

    def translate(self, xy):
        self.xy = tuple([a + b for a, b in zip(self.xy, xy)])

    def evolve(self, duree, frottement=.05):
        i = 0
        while self.lifetime > 0 and i < duree:
            self.accel_inst = (self.accel[0] - frottement * self.vit[0],
                               self.accel[1] - frottement * self.vit[1])
            self.vit = tuple([a + b for a, b in zip(self.accel_inst, self.vit)])
            self.translate(self.vit)
            self.edges()
            self.lifetime -= 1
            i += 1

    def draw(self, ctx, color=None):
        if self.lifetime > 0:
            ctx.save()
            ctx.set_line_width(1)
            if not color:
                ctx.set_source_rgba(*self.color)
            else:
                ctx.set_source_rgba(*color)
            ctx.arc(*self.xy, 2, 0, 6.284)
            ctx.fill()
            ctx.restore()
