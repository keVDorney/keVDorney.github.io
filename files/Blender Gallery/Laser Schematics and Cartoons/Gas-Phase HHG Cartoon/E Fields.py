from __future__ import division
import numpy as np



### Plot the red and blue circular pulses.


##### PARAMETERS
c = 299792458

def Efield(times=np.linspace(-30e-15, 30e-15, 5000), pdur=20e-15, A1=1, lambda1=7.90e-7, ellip=0):

    def gauss(x, A=1, x0=0, width=1):
        return A*np.exp(-(x-x0)**2/(2*(width/2.35482)**2))

    w1 = c/lambda1 * 2 * np.pi

    x = A1 * np.sin(w1 * times)  * gauss(times, width=pdur)
    y = ellip * A1 * np.cos(w1 * times)  * gauss(times, width=pdur)


    return times, x, y

# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# tt, tx, ty = Efield()
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot(tt, tx, ty, lw=2)
#
# plt.show()


import bpy
def make_field(x, y, z, bevel_obj='circ', name=''):

    # Create the data block for the curve.
    curveD = bpy.data.curves.new(name, type='CURVE')
    curveD.dimensions = '3D'
    curveD.resolution_u = 2

    coords = np.vstack((x,y,z)).transpose()

    print(coords.shape)

    # Map the coords to the figure.
    polyline = curveD.splines.new('POLY')
    polyline.points.add(len(coords-1))

    for i, coord in enumerate(coords):
        x,y,z = coord
        polyline.points[i].co = (x, y, z, 1)

    # Create the object.
    curveOBJ = bpy.data.objects.new(name, curveD)

    # Attach to scene and validate context.
    scn = bpy.context.scene
    scn.objects.link(curveOBJ)
    scn.objects.active = curveOBJ
    curveOBJ.select = True

    bpy.context.object.data.bevel_object = bpy.data.objects[bevel_obj]


t, x, y = Efield(lambda1=7.90e-7, ellip=0)
# # Multiply t by 1e15 to give it some real dimensions that Blender can handle.
make_field(t*1e15, x, y, name='Red Circ')
