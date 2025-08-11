# [Description]: 
#   - This module includes the primitives to support blender manipulation.
#   - Unfortunately, there are no tests for this module.

# -------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------
import bpy
import numpy            as     np
import msim.geo.mesh    as mMesh
import msim.helpers     as mHelp

# -------------------------------------------------------------------------
# Load mMesh to bMesh
# -------------------------------------------------------------------------
def from_mMesh(bm,mVerts,mFaces):
    
    # mVerts to bVerts
    bVerts = tuple(bm.verts.new(iVert.asVector()) for iVert in mVerts)

    # Ensure look-up table is correct
    bm.verts.ensure_lookup_table()
    
    for iFace in mFaces:
        vertIndex = mMesh.Face.getVertIndex(iFace,mVerts)
        cVertLst = []
        for index in vertIndex:
            cVertLst.append(bVerts[index])

        bm.faces.new(cVertLst)

# -------------------------------------------------------------------------
# Load mMesh to bMesh
# -------------------------------------------------------------------------
def to_scene(bm,aName):

    # Create a new Mesh datablock
    mesh_data = bpy.data.meshes.new(aName)

    # Push bmesh data to the mesh datablock
    bm.to_mesh(mesh_data)
    bm.free()

    # Create actual object:
    bObj = bpy.data.objects.new(aName,mesh_data)
    bpy.context.collection.objects.link(bObj)

    # Optionally, make it active and select it
    bpy.context.view_layer.objects.active = bObj

    # Make sure objects have updated mesh data
    bpy.context.view_layer.update()

    # Set active object:
    bpy.ops.object.select_all(action='DESELECT')
    bObj.select_set(True)
    bpy.context.view_layer.objects.active = bObj

    return bObj
