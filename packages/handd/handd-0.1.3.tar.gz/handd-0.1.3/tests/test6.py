import cairo
from handd import HDD
import math

W = H = 800

img = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
ctx = HDD(img)

ctx.set_source_rgb(0, 0, 0)
ctx.rectangle(0, 0, W, H)
ctx.fill()

ctx.set_source_rgba(0, 0, 0, 0)
pn, bbn = ctx.circle_hdd(400, 250, 40)

ctx.set_source_rgba(1, 1, 0, .95)
ctx.set_line_width(10)
p, bb = ctx.sector_hdd(350, 400, 300,
                       math.radians(35),
                       math.radians(325),
                       dev=5)
ctx.hatch_hdd(p, bb, n=50,
              condition=lambda x, y: not HDD.is_in(x, y, pn))
ctx.stroke()


pilules = {"rouge": [(1, 0, 0), (550, 400)],
           "bleue": [(0, 0, 1), (730, 400)]}

for pill in pilules:
    ctx.set_source_rgb(0, 0, 0)
    p, bb = ctx.circle_hdd(pilules[pill][1][0], pilules[pill][1][1], 70)
    ctx.set_source_rgba(*pilules[pill][0], .90)
    ctx.set_line_width(5)
    ctx.hatch_hdd(p, bb, angle=-30, n=20)
    ctx.hatch_hdd(p, bb, angle=-50, n=20)
    ctx.stroke()

img.write_to_png("test6.png")
