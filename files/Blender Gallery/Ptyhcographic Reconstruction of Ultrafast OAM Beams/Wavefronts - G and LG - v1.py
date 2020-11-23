from __future__ import division, print_function
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

############ COMMENTS ##############
''' Trying to make 3D contour plots of the wavefronts of Gaussian and LG beams for an OAM figure.

    We'll assume collimated beams (for now) for simplicity.

    2018-01-01 - Abandoning this for other efforts - KD 

'''
####################################

####### SECTION STATEMENTS #########
ShowPlots = True # Toggles plt.show() on/off in a global fashion.
####################################

######## "GLOBAL" PARAMETERS #######

####################################

######### HELPER FUNCTIONS #########
def _gaussian2D(x, y, xcenter, ycenter, waist, amp=1):
    return amp*np.exp(-(((x-xcenter)**2+(y-ycenter)**2)/waist)**2)

def _gaussianInt(x, y, z, w0, norm=True):

    # Create output array.
    Gbeam = np.zeros(shape=(len(x), len(y), len(z)))
    X, Y = np.meshgrid(x, y)
    for ddx, zi in enumerate(z):

        # Compute gaussian intensity.
        Gfield = _gaussian2D(X, Y, 0, 0, w0)
        Gbeam[:, :, ddx]   = np.abs(Gfield)**2

    if norm == True:
        Gbeam /= np.max(Gbeam)

    return Gbeam
####################################

########### BEGIN CODE #############


X = np.linspace(-50, 50, 13e2)
Y = np.linspace(-50, 50, 13e2)
Z = np.linspace(-20, 20, 13e2)

Xp, Yp = np.meshgrid(X, Y)

Gtest = _gaussianInt(X, Y, Z, 10)

fig = plt.figure(figsize=(4, 3), dpi=128)
ax1 = fig.add_subplot(111, projection='3d')

ax1.plot_surface(Xp, Yp, Gtest[:, :, 50], cmap='plasma')


####################################
if ShowPlots == True:
    plt.show()
