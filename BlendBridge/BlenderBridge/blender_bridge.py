"""
https://svn.blender.org/svnroot/bf-extensions/trunk/py/scripts/addons/io_mesh_raw/export_raw.py
"""
import io
import bpy
import mathutils

bl_info = {
    "name":         "Blender Bridge",
    "author":       "Joshua Newnham",
    "blender":      (2,7,8),
    "version":      (0,0,1),
    "description":  "VR Streaming",
    "category":     "Object"
}


class BObject(object):

    def __init__(self):
        self.vertices = []
        self.faces = []
        self.uvs = []

class BlenderBridgeOp(bpy.types.Operator):
    """ """
    bl_idname = "object.blenderbridge"
    bl_label = "Blender Bridge"

    def execute(self, context):
        faces = self.parse_scene()

        print(faces)

        return {"FINISHED"}

    def face_to_triangle(self, face):
        triangles = []

        if len(face) == 4:
            triangles.append([face[0], face[1], face[2]])
            triangles.append([face[2], face[3], face[0]])
        else:
            triangles.append(face)

        return triangles

    def calc_face_values(self, face, mesh, matrix):
        fv = []

        for verti in face.vertices:
            fv.append((matrix * mesh.vertices[verti].co)[:])

        return fv

    def parse_scene(self, apply_mods=True, triangulate=True):
        faces = []

        scene = bpy.context.scene

        for obj in bpy.context.selected_objects:
            if apply_mods or obj.type != 'MESH':
                try:
                    mesh = obj.to_mesh(scene, True, 'PREVIEW')
                except:
                    mesh = None
                is_tmp_mesh = True
            else:
                mesh = obj.data
                if not mesh.tessfaces and mesh.polygons:
                    mesh.calc_tessface()
                is_tmp_mesh = False

        if mesh is not None:
            matrix = obj.matrix_world.copy()
            for face in mesh.tessfaces:
                fv = self.calc_face_values(face, mesh, matrix)
                if triangulate:
                    faces.extend(self.face_to_triangle(fv))
                else:
                    faces.append(fv)

            if is_tmp_mesh:
                bpy.data.meshes.remove(mesh)

        return faces
