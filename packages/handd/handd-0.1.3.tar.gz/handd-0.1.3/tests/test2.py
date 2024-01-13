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
        p = self.calque.regular_polygon_hdd(self.c, self.l, self.dim, 4, 1)
        self.calque.stroke()
        return p


offset = 50
W = 1_080 - offset
H = 1_080 - offset
dim = 103

img = cairo.ImageSurface(cairo.FORMAT_RGB24, W + offset, H + offset)
ctx = HDD(img)

carres = []
for l in range(H // dim):
    for c in range(W // dim):
        carres.append(Carre((offset + dim) // 2 + l * dim,
                            (offset + dim) // 2 + c * dim,
                            dim // 1.8,
                            ctx))

info_carres = []
for c in carres:
    info_carres.append((c, c.affiche()))

ctx.set_line_width(1)
noise = OpenSimplex()
for i, pack_c in enumerate(info_carres):
    c, (p, bb) = pack_c
    n = noise.noise3d(c.l / dim, c.c / dim, (dim * c.l + c.c) * .001)
    angle = n * math.pi / 2
    nb = int((1 + n) * 10)
    couleur = int((1 + n) * 60)
    #
    couleur_hsv = (0, couleur / 100, 1)
    ctx.set_source_rgb(*colorsys.hsv_to_rgb(*couleur_hsv))
    ctx.hatch_hdd(p, bb, angle=angle, n=nb)
    ctx.stroke()
    #
    couleur_hsv = (200 / 360, couleur / 100, 1)
    ctx.set_source_rgb(*colorsys.hsv_to_rgb(*couleur_hsv))
    ctx.dot_hdd(p, bb, sep=nb)
    ctx.stroke()


img.write_to_png("test2.png")
