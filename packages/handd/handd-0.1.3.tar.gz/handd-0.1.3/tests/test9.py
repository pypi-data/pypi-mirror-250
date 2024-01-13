import cairo
from handd import HDD
import random
import math


def im_translation(M, vecteur):
    """ M et vecteur sont des complexes"""

    return M + vecteur


def im_rotation(M, angle, centre):
    """M et centre sont des complexes
    angle est en radians
    """

    e_i_theta = math.cos(angle) + math.sin(angle) * 1j
    return centre + e_i_theta * (M - centre)


def von_koch(contexte, position, angle, longueur, niveau,
             couleur="white", epais=1):
    """position est un nombre complexe"""

    rangle = math.radians(angle)
    if longueur <= 1 or niveau == 1:
        debut = position
        fin = im_rotation(im_translation(debut, longueur), rangle, debut)
        contexte.set_line_width(epais)
        contexte.set_source_rgb(*couleur)
        # contexte.move_to(debut.real, debut.imag)
        # contexte.line_to(fin.real, fin.imag)
        contexte.lline_hdd([(debut.real, debut.imag), (fin.real, fin.imag)])
        contexte.stroke()
    else:
        nv_longueur = longueur / 3

        A = position
        B = im_rotation(im_translation(A, nv_longueur),
                        rangle,
                        A)
        C = im_rotation(im_translation(B, nv_longueur),
                        rangle + math.pi / 3,
                        B)
        D = im_rotation(im_translation(B, nv_longueur),
                        rangle,
                        B)

        von_koch(contexte, A, angle, nv_longueur, niveau - 1, couleur, epais)
        von_koch(contexte, B, angle + 60, nv_longueur, niveau - 1, couleur, epais)
        von_koch(contexte, C, angle - 60, nv_longueur, niveau - 1, couleur, epais)
        von_koch(contexte, D, angle, nv_longueur, niveau - 1, couleur, epais)



HDD.debug = not True

W = 800
H = 800
img = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
ctx = HDD(img)
ctx.set_source_rgb(0, 0, 0)
ctx.rectangle(0, 0, W, H)
ctx.fill()

longueur = W * math.sqrt(2)
von_koch(ctx, 0, 45, longueur, 5, (0, 0, 1), 3)

img.write_to_png("test9.png")
