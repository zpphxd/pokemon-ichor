"""gTileset_Parnassos: Route 28, the Sacred Olives and the Kastalian Gorge.

Delphoi's sister secondary: the god's olive plain and the gorge's Titan muster
didn't fit one secondary's 504 tiles with the sanctuary. Every piece is drawn
by delphoi_art.py's painters, in its palettes, so the cliffs and laurels meet
Delphoi's pixel for pixel.
"""
import delphoi_art as D

NAME = "parnassos"
GROUPS = D.GROUPS
validate = D.validate


def build():
    return D.build_parnassos()


def write_catalog(used, structs):
    D.write_catalog(used, structs, name=NAME, maps="Route 28: the Sacred Olives and the Kastalian Gorge")
