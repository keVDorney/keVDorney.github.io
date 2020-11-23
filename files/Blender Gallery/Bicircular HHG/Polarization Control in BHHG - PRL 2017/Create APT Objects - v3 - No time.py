from __future__ import division
import numpy as np
import bpy

def make_APT(x, y, z, bevel_obj='Path', name=''):

    # Create the curve data block. 
    cData = bpy.data.curves.new(name, type='CURVE')
    cData.dimensions = '3D'
    cData.resolution_u = 2
    
    coords = np.vstack((x, y, z)).transpose()
    
    # Map the coordinates to a spline function. For smoothness.
    polyline = cData.splines.new('POLY')
    polyline.points.add(len(coords-1))
    
    for i, coord in enumerate(coords):
        x, y, z = coord
        polyline.points[i].co = (x, y, z, 1)
        
    # actually create the stupid object.
    cOBJ = bpy.data.objects.new(name, cData)
    
    # Attach it to the scene. 
    scn = bpy.context.scene
    scn.objects.link(cOBJ)
    scn.objects.active = cOBJ
    cOBJ.select = True
    
    bpy.context.object.data.bevel_object = bpy.data.objects[bevel_obj]    

# Get the smoothed data from files cause Blender is dumb. 
t1, Ex1, Ey1 = np.genfromtxt('/Users/keV_Dawg/Desktop/Blender-rifiric Shiz/CP HHG - PRL - 2016-06/APT_0.1.txt', skip_header=1, unpack=True)
t2, Ex2, Ey2 = np.genfromtxt('/Users/keV_Dawg/Desktop/Blender-rifiric Shiz/CP HHG - PRL - 2016-06/APT_1.0.txt', skip_header=1, unpack=True)
t3, Ex3, Ey3 = np.genfromtxt('/Users/keV_Dawg/Desktop/Blender-rifiric Shiz/CP HHG - PRL - 2016-06/APT_4.0.txt', skip_header=1, unpack=True)

print(t1.shape)
print(Ex1.shape) 
print(Ey1.shape)
print(t2.shape)
print(Ex2.shape)
print(Ey2.shape)
print(t3.shape)
print(Ex3.shape)
print(Ey3.shape)

# make_APT(Ex1, Ey1, 0, bevel_obj='APT_BO_0.1', name='APT 0.1')
# make_APT(Ex1, Ey1, 0, bevel_obj='APT_BO_0.6', name='APT 0.6')
# make_APT(Ex2, Ey2, 0, bevel_obj='APT_BO_2.0', name='APT 2.0')