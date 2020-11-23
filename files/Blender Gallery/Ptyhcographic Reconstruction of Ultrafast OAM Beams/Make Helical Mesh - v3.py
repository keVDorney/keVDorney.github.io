import numpy as np
import bpy
import os

# Attempting to make a mesh of a million verts and faces. Well, not really a million :)
print(os.path.dirname(os.path.abspath(__file__)))

def _createmesh(verts, faces, meshname, objectname):
    # Create a mesh.
    mesh_data = bpy.data.meshes.new(meshname)
    mesh_data.from_pydata(verts, [], faces)
    mesh_data.update()

    obj = bpy.data.objects.new(objectname, mesh_data)

    scene = bpy.context.scene
    scene.objects.link(obj)
    obj.select = True
    # scene.objects.active = obj  # make the selection active

def _createmeshop(verts, faces):

    # Operator method for creating a mesh.
    bpy.ops.object.add(type='MESH')
    obj = bpy.context.object
    mesh = obj.data

    mesh.from_pydata(verts, [], faces)
    mesh.update()

    print(np.shape(mesh.vertices))

    scene = bpy.context.scene
    scene.objects.link(obj)
    obj.select = True

def _converttoint(farray, varray):

    nfaces = [ [int(i) for i in thing] for thing in farray]
    nverts = [ thing for thing in zip(varray[:, 0].flatten(), varray[:, 1].flatten(), varray[:, 2].flatten())]
    return nfaces, nverts


# Ok, let's see if this works...
# First, load the dats.
rverts = np.load('/Users/keV_Dawg/Desktop/Blender-rifiric Shiz/CLEO 2018 - Ptychography and OAM/Datas/Red_LG_Verts_1step.npy')
rfaces = np.load('/Users/keV_Dawg/Desktop/Blender-rifiric Shiz/CLEO 2018 - Ptychography and OAM/Datas/Red_LG_Faces_1step.npy')
bverts = np.load('/Users/keV_Dawg/Desktop/Blender-rifiric Shiz/CLEO 2018 - Ptychography and OAM/Datas/Blue_LG_Verts_1step.npy')
bfaces = np.load('/Users/keV_Dawg/Desktop/Blender-rifiric Shiz/CLEO 2018 - Ptychography and OAM/Datas/Blue_LG_Faces_1step.npy')

# Convert to integers and also maybe lists?
nrfaces, nrverts = _converttoint(rfaces, rverts)
nbfaces, nbverts = _converttoint(bfaces, bverts)

# # Now, pass the vert and face data to Blender
_createmesh(nrverts, nrfaces, 'VortexMesh_Red', 'VortexMesh_Red')
_createmesh(nbverts, nbfaces, 'VortexMesh_Blue', 'VortexMesh_Blue')
