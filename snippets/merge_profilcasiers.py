# coding: utf-8
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np

from crue10.study import Study


study = Study('../../Crue10_examples/Etudes-tests/Etu_GE2009_Conc/Etu_GE2009_Conc.etu.xml')
submodel = study.get_submodel('Sm_GE2009_conc')
submodel.read_all()

fig1, ax_xz = plt.subplots(figsize=(16, 9))
fig2, ax_vol = plt.subplots(figsize=(16, 9))

casier = submodel.get_casier('Ca_N8')
old_casier = deepcopy(casier)
for pc in casier.profils_casier:
    ax_xz.plot(pc.xz[:, 0], pc.xz[:, 1], marker='.', label=pc.id)
    z_array = np.unique(np.sort(pc.xz[:, 1]))
    ax_vol.plot(z_array, [pc.compute_volume(z) for z in z_array], marker='.', label=pc.id)
casier.merge_profil_casiers()

z_array = casier.profils_casier[0].xz[:, 1]
ax_vol.plot(z_array, [old_casier.compute_volume(z) for z in z_array],
            marker='.', label='SOMME VOLUMES')
ax_vol.plot(z_array, [casier.compute_volume(z) for z in z_array],
            marker='x', linestyle=':', label='Merged ProfilCasiers')

ax_xz.set_xlabel("Distance [m]")
ax_xz.set_ylabel("Z [mNGFO]")
ax_xz.legend()

ax_vol.set_xlabel("Z [mNGFO]")
ax_vol.set_ylabel("Volume [m3]")
ax_vol.legend()

plt.show()
