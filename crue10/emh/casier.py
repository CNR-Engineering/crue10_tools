# coding: utf-8
"""
Classes for `Casier` in major bed (floodplain):
- ProfilCasier
- Casier

Not supported yet:
- TypeDPTGCasiers: SplanBati, ZBatiTotal (dptg.xml)
"""
import numpy as np

from crue10.utils import CrueError


class ProfilCasier:
    """
    ProfilCasier
    - id <str>: profil casier identifier
    - distance <float>: applied length (or width)
    - xz <2D-array>: ndarray(dtype=float, ndim=2)
        Array containing series of transversal abscissa and elevation (first axis should be strictly increasing)
    - xt_min <float: first curvilinear abscissa (for LitUtile)
    - xt_max <float>: last curvilinear abscissa (for LitUtile)
    - comment <str>: optional text explanation
    """
    def __init__(self, nom_profil_casier):
        self.id = nom_profil_casier
        self.distance = 0
        self.xz = None
        self.xt_min = -1
        self.xt_max = -1
        self.comment = ''

    def set_xz(self, coords):
        self.xz = coords

    def interp_z(self, xt):
        if xt < self.xt_min or xt > self.xt_max:
            raise CrueError("xt=%f is ouside range [%f, %f] for %s" % (xt, self.xt_min, self.xt_max, self))
        return np.interp(xt, self.xz[:, 0], self.xz[:, 1])

    def __str__(self):
        return "ProfilCasier #%s" % self.id


class Casier:
    """
    Casier (or storage area/reservoir)
    - id <str>: casier identifier
    - geom <shapely.geometry.LinearRing>: polygon
    - noeud <str>: related node name
    - profils_casier <[ProfilCaser]>: profils casier (usually length=1)
    - CoefRuis <float>: "coefficient modulation du débit linéique de ruissellement"
    - comment <str>: optional text explanation
    """
    def __init__(self, nom_casier, nom_noeud, is_active=False):
        self.id = nom_casier
        self.is_active = is_active
        self.geom = None
        self.nom_noeud = nom_noeud
        self.profils_casier = []
        self.CoefRuis = 0.0
        self.comment = ''

    def set_geom(self, geom):
        self.geom = geom

    def add_profil_casier(self, profil_casier):
        self.profils_casier.append(profil_casier)

    def __str__(self):
        return "Casier #%s" % self.id
