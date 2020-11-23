from __future__ import division, print_function
import numpy as np
import scipy.io
import scipy.ndimage
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider
from skimage import measure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

############ COMMENTS ##############
''' COMMENTS:

    Creating Isosurfaces of the reconstructed wavefronts for the Experimental Scheme.
'''

# Set fontsize of ticklabels globally for 128 dpi display.
matplotlib.rcParams['xtick.labelsize'] = 8
matplotlib.rcParams['ytick.labelsize'] = 8
####################################

####### SECTION STATEMENTS #########
ShowPlots = True # Toggles plt.show() on/off in a global fashion.
####################################

######## "GLOBAL" PARAMETERS #######

####################################

######### HELPER FUNCTIONS #########

####################################

########### BEGIN CODE #############

# Load the .mat files and extra the volume data.
rdict = scipy.io.loadmat('./roundred.mat',  mat_dtype=True)
bdict = scipy.io.loadmat('./roundblue.mat', mat_dtype=True)

rdata = rdict['roundred']
bdata = bdict['roundblue']

# Ok, now that we have the volume data, we use skimage to extract the isosurface.
rverts, rfaces, rnormals, rvalues = measure.marching_cubes_lewiner(rdata, level=2.7, spacing=[1.0, 1.0, 1.0], step_size=1)
bverts, bfaces, bnormals, bvalues = measure.marching_cubes_lewiner(bdata, level=2.6, spacing=[1.0, 1.0, 1.0], step_size=1)

print(np.shape(rverts), np.shape(rfaces))
print(np.shape(bverts), np.shape(bfaces))

# rmesh = Poly3DCollection(rverts[rfaces[::2, :]])
# bmesh = Poly3DCollection(bverts[bfaces[::2, :]])
# rmesh.set_edgecolor('r')
# bmesh.set_edgecolor('b')

# Try plotting.
fig = plt.figure(figsize=(7, 3), dpi=128)
fig.subplots_adjust(left=0.0, right=0.98, wspace=0.0)
ax1 = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122, projection='3d')

# ax1.add_collection3d(rmesh)
# ax2.add_collection3d(bmesh)

# ax1.set_xlim()

ax1.plot_trisurf(rverts[:, 2], rverts[:, 1], rfaces, rverts[:, 0], color='r', lw=1, shade=True)
ax2.plot_trisurf(bverts[:, 2], bverts[:, 1], bfaces, bverts[:, 0], color='b', lw=1, shade=True)

for axi in [ax1, ax2]:
    axi.view_init(elev=90, azim=-135)


# # Let's save the verts and faces data as NumPy arrays.
# np.save('./Red_LG_Verts_1step.npy', rverts)
# np.save('./Red_LG_Faces_1step.npy', rfaces)
# np.save('./Blue_LG_Verts_1step.npy', bverts)
# np.save('./Blue_LG_Faces_1step.npy', bfaces)

####################################
if ShowPlots == True:
    plt.show()
