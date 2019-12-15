from __future__ import division
import numpy as np

############ COMMENTS ##############
'''
'''

####################################

####### SECTION STATEMENTS #########
ShowPlots = True # Toggles plt.show() on/off in a global fashion.
####################################

######## "GLOBAL" PARAMETERS #######
c = 3e8
A = 1
####################################

######### HELPER FUNCTIONS #########
def _gaussian(x, amp, center, width):
    return amp*np.exp(-((x-center)/width)**2)

####################################

########### BEGIN CODE #############

# Compute helix.
t  = np.linspace(0, 2*np.pi, 1e3)
# ct = np.logspace(0, 1.2, 1e3)
ct = np.linspace(1.5, 2.0, 1e3)**4
r  = 0.5
ramp = np.linspace(0.3, 2, 2e3)**2

# x = r*np.cos(ct*t) * ramp[::-1]
# y = r*np.sin(ct*t) * ramp[::-1]
# z = 2*t


# Ok, can we also make it pulsed?.
x = r*np.cos(ct*t) * _gaussian(t, 0.5, 3, width=1.5)
y = r*np.sin(ct*t) * _gaussian(t, 0.5, 3, width=1.5)
z = 2*t

# X = np.hstack((x, x, x))
# Y = np.hstack((y, y, y))
# Z = np.hstack((z, z+np.max(z), z+np.max(z)*2))

X = np.hstack((x, x))
Y = np.hstack((y, y))
Z = np.hstack((z, z+np.max(z)))

X = X * ramp[::-1]
Y = Y * ramp[::-1]

############### PLOT TESTING ###################
# import matplotlib
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import axes3d
#
# # Set fontsize of ticklabels globally for 128 dpi display.
# matplotlib.rcParams['xtick.labelsize'] = 8
# matplotlib.rcParams['ytick.labelsize'] = 8
#
# fig = plt.figure(figsize=(5, 2.5), dpi=128)
# ax  = fig.add_subplot(111, projection='3d')
#
# # ax.plot(x, y, z, c='b', lw=1)
# ax.plot(X, Y, Z, c='b', lw=1)
#
# # ax.set_xlim(-3, -2.5)
# # ax.set_ylim(-1.2, 1.2)
# # ax.set_zlim(-1.2, 1.2)
#
# if ShowPlots == True:
#     plt.show()
############# END PLOT TESTING #################
import bpy
def make_curve(x,y,z,bevel_ob='circ2',name=''):
    # create the Curve Datablock
    curveData = bpy.data.curves.new(name, type='CURVE')
    curveData.dimensions = '3D'
    curveData.resolution_u = 2

    coords = np.vstack((x,y,z)).transpose()

    # map coords to spline
    polyline = curveData.splines.new('POLY')
    polyline.points.add(len(coords)-1)

    for i, coord in enumerate(coords):
        x,y,z = coord
        polyline.points[i].co = (x, y, z, 1)

    # create Object
    curveOB = bpy.data.objects.new(name, curveData)

    # attach to scene and validate context
    scn = bpy.context.scene
    scn.objects.link(curveOB)
    scn.objects.active = curveOB
    curveOB.select = True

    # bpy.context.object.data.bevel_object = bpy.data.objects[bevel_ob]



# make_curve(x,y,z,bevel_ob='circ2',name='EUV Field')
make_curve(X,Y,Z,bevel_ob='circ2',name='EUV Field')
####################################
