import cairogen.helpers as ch
import cairogen.grids as cg
from handd import HDD
import random

W = 1920
H = 1080
NP = 10
offset = 3
img = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                         W + 2 * offset,
                         H + 2 * offset)
ctx = HDD(img)
ch.bg(img, (0, 0, 0))


img.write_to_png("test11.png")
