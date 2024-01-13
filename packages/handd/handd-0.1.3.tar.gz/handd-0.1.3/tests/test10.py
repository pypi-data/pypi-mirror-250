import cairo
from handd import HDD
import random
from scipy.spatial import Delaunay


def points_hasard(x, y, w, h, N):
    lst = []
    moitie = N // 2
    for i in range(moitie // 3):
        if h > w:
            lst += [(x, random.randrange(y, y + h))]
            lst += [(x + w, random.randrange(y, y + h))]
        else:
            lst += [(random.randrange(x, x + w), y)]
            lst += [(random.randrange(x, x + w), y + h)]
    for i in range(moitie // 6):
        if h > w:
            lst += [(random.randrange(x, x + w), y)]
            lst += [(random.randrange(x, x + w), y + h)]
        else:
            lst += [(x, random.randrange(y, y + h))]
            lst += [(x + w, random.randrange(y, y + h))]
    lst += [(random.randrange(x, x + w), random.randrange(y, y + h))
            for _ in range(moitie)]
    return lst


def trace_triangle(lst_indices, lst):
    R = range(len(lst))
    M = [[0 for _ in R] for _ in R]
    for i, j, k in lst_indices:
        ctx.set_source_rgba(1, 1, 1, 0)
        pol, polb = ctx.lpolygon_hdd([lst[i], lst[j], lst[k]])
        ctx.save()
        ctx.set_source_rgba(1, 1, 1, 1)
        ctx.set_line_width(1)
        ctx.hatch_hdd(pol, polb,
                      n=random.randint(30, 40),
                      angle=random.random() * 3.14)
        ctx.restore()
        M[i][j] = M[j][i] = 1
        M[i][k] = M[k][i] = 1
        M[k][j] = M[j][k] = 1
    ctx.save()
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.set_line_width(3)
    for i in R:
        for j in range(i + 1, len(lst)):
            if M[i][j] == 1:
                ctx.lline_hdd([lst[i], lst[j]])
                pass
    ctx.restore()


def proc_rectangle(xy, w, h, NP):
    sommets = [xy,
               (xy[0] + w, xy[1]),
               (xy[0] + w, xy[1] + h),
               (xy[0], xy[1] + h)]
    ctx.rectangle_hdd(*xy, w, h)
    lst = points_hasard(*xy, w, h, NP) + sommets
    obj_del = Delaunay(lst)
    trace_triangle(obj_del.simplices, lst)


W = 900
H = 900
NP = 24
offset = 50
img = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                         W + 2 * offset,
                         H + 2 * offset)
ctx = HDD(img)
ctx.set_source_rgb(0, 0, 0)
ctx.paint()

HDD.deviation = 3

ctx.set_line_width(1)
ctx.set_source_rgba(1, 1, 1, 0)

ctx.translate(offset, offset)
proc_rectangle((0, 0), W / 3, 2 * H / 3, NP)
proc_rectangle((0, 2 * H / 3), 2 * W / 3, H / 3, NP)
proc_rectangle((W / 3, 0), 2 * W / 3, H / 3, NP)
proc_rectangle((2 * W / 3, H / 3), W / 3, 2 * H / 3, NP)

img.write_to_png("test10.png")
