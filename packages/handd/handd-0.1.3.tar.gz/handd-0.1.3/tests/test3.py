import cairo
from handd import HDD
from opensimplex import OpenSimplex
import colorsys
import math


class Carre:
    def __init__(self, l, c, dim, calque):
        self.l = l
        self.c = c
        self.dim = dim
        self.calque = calque

    def affiche(self):
        self.calque.set_line_width(0)
        p = self.calque.regular_polygon_hdd(self.c, self.l, self.dim,
                                            4, math.pi / 4)
        self.calque.stroke()
        return p


offset = 0
W = 1_080 - offset
H = 1_920 - offset
dim = 120

N = 10
for j in range(N):
    HDD.deviation = (N - 1) * 2 - 2 * j
    img = cairo.ImageSurface(cairo.FORMAT_RGB24, W + offset, H + offset)
    ctx = HDD(img)

    # les carrés
    carres = []
    for l in range(H // dim):
        for c in range(W // dim):
            carres.append(Carre((offset + dim) // 2 + l * dim,
                                (offset + dim) // 2 + c * dim,
                                dim / math.sqrt(2),
                                ctx))

    noise = OpenSimplex()
    info_carres = []
    for c in carres:
        info_carres.append((c, c.affiche()))

    ctx.set_line_width(4)
    for i, pack_c in enumerate(info_carres):
        n = noise.noise3d(c.l / dim, c.c / dim,
                          (dim * c.l + c.c) * .01)
        c, (p, bb) = pack_c
        angle = n * math.pi / 2
        nb = max(10, int((1 + n) * 30))
        couleur = int((1 + n) * 60)
        couleur_hsv = (10 / 360, couleur / 100, 1)
        ctx.set_source_rgb(*colorsys.hsv_to_rgb(*couleur_hsv))
        ctx.hatch_hdd(p, bb, angle=angle, n=10)
        ctx.stroke()

    img.write_to_png(f"animation{j:02}_test3.png")
