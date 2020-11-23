from __future__ import division
import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
import bpy

### Plot the red and blue circular pulses.


##### PARAMETERS
c = 299792458

def Efield(times=np.linspace(-10e-15, 10e-15, 5000), pdur=7e-15, E0=1, lambda1=7.90e-7, ellip=1):

    def gauss(x, A=E0, x0=0, width=1):
        return A*np.exp(-(x-x0)**2/(2*(width/2.35482)**2))

    w1 = c/lambda1 * 2 * np.pi

    x = np.sin(w1 * times)  * gauss(times, width=pdur)
    y = ellip * np.cos(w1 * times)  * gauss(times, width=pdur)


    return times, x, y


def make_field(x, y, z, name=''):

    print(name)
    print(name + '_BevObj')

    # Create the data block for the curve.
    curveD = bpy.data.curves.new(name, type='CURVE')
    curveD.dimensions = '3D'
    curveD.resolution_u = 2

    # Create the bevel object for the curve.
    bevel_name = name + '_BevObj'
    bpy.ops.curve.primitive_nurbs_circle_add(radius=0.118, location=(0.0, 0.0, 10.0))
    bevelobj = bpy.context.object
    bevelobj.name = bevel_name

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
    scn.objects.active = bpy.data.objects[name]

    bpy.context.object.data.bevel_object = bevelobj

#tt, tx, ty = Efield()
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.plot(tt, tx, ty, lw=2)
#
#plt.show()

# Create a few different E-fields based on the following intensity ratios.
Irats = np.array([0.1, 0.5, 1.0, 2.0, 4.0])

for rat in Irats:

    tr, xr, yr =  Efield(lambda1=7.90e-7, ellip=1)
    tb, xb, yb =  Efield(lambda1=3.95e-7, ellip=-1)

    # Make the combined field.
    xc = (xr + xb) / np.max((xr + xb))
    yc = (yr + yb) / np.max((yr + yb))

    # Now, get the APT with the correct intensity ratio.
    fn = '/Users/keV_Dawg/Desktop/Blender-rifiric Shiz/CLEO 2017 - CPHHG/APT Data/_%1.1f.txt'%rat
    tp, Expt, Eypt = np.genfromtxt('/Users/keV_Dawg/Desktop/Blender-rifiric Shiz/CLEO 2017 - CPHHG/APT Data/APT_0.1.txt', skip_header=1, unpack=True)

    # Create the Blender objects.
    make_field(tr*1e15, xr, yr, name='RedField_%1.1f'%rat)
    make_field(tr*1e15, xb, yb, name='BlueField_%1.1f'%rat)
    make_field(tr*1e15, xc, yc, name='BiCircField_%1.1f'%rat)
    make_field(tp, Expt, Eypt, name='APTField_%1.1f'%rat)
