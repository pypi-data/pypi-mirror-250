# import cairogen.helpers as ch
# import cairogen.grids as cg
from handd import HDD
import random
import cairo


W = 1680
H = 1050
img = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                         W, H)
ctx = HDD(img)
ctx.paint()
ctx.set_source_rgb(1, 1, 1)

nbC = random.randint(5, 50)
for i in range(nbC):
    rayon = i * H/(2*nbC)
    angle1 = random.random() * 6.3
    angle2 = angle1 + random.random() * 6.3
    ctx.arc_hdd(W/2, H/2, rayon, angle1, angle2)
    ctx.stroke()


img.write_to_png("test12.png")
