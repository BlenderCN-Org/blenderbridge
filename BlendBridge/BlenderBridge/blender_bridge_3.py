"""
https://www.yousry.de/porting-your-export-script-to-blender-2-63/

weights:
http://blender.stackexchange.com/questions/621/return-list-of-associated-vertex-index-weight-values-for-a-given-vertex-group

triangles:
http://gamedev.stackexchange.com/questions/45683/mesh-with-quads-to-triangle-mesh

materials:
https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Code_snippets/Materials_and_textures

code snippets (mesh)
https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Code_snippets/Meshes

other:
https://en.wikibooks.org/wiki/Blender_3D:_Noob_to_Pro/Advanced_Tutorials/Python_Scripting/Introductionv
https://en.wikibooks.org/wiki/Blender_3D:_Noob_to_Pro/Advanced_Tutorials/Python_Scripting/Export_scripts
https://www.blender.org/api/blender_python_api_2_65_5/info_overview.html#info-overview
https://cgcookiemarkets.com/2014/12/11/writing-first-blender-script/
http://brucesutherland.blogspot.co.uk/2012/05/blender-262-writing-export-script.html
https://github.com/pisuke/brad/blob/master/superseded/mesh2radgrid.py

add on:
https://www.blender.org/api/blender_python_api_2_65_5/info_tutorial_addon.html
http://michelanders.blogspot.co.uk/p/creating-blender-26-python-add-on.html


"""

import io
import bpy
import mathutils
import json

bl_info = {
    "name":         "Blender Bridge 3",
    "author":       "Joshua Newnham",
    "blender":      (2,7,8),
    "version":      (0,0,1),
    "description":  "VR Streaming",
    "category":     "Object"
}


class BObject(object):

    def __init__(self, name, vertices, normals, faces, face_materials, uvs, materials):
        self.name = name
        self.vertices = vertices
        self.normals = normals
        self.faces = faces
        self.face_materials = face_materials
        self.uvs = uvs
        self.materials = materials

    def __dict__(self):
        return {
            'name': self.name,
            'vertices': self.vertices,
            'normals': self.normals,
            'faces': self.faces,
            'face_materials': self.face_materials,
            'uvs': self.uvs,
            'materials': self.materials
        }

    def to_json(self):
        return json.dumps({
            'name': self.name,
            'vertices': self.vertices,
            'normals': self.normals,
            'faces': self.faces,
            'face_materials': self.face_materials,
            'uvs': self.uvs,
            'materials': self.materials
        })


class BlenderBridgeOp(bpy.types.Operator):
    """ class BlenderBridgeOp 3 """
    bl_idname = "object.blenderbridge3"
    bl_label = "Blender Bridge 3"

    def execute(self, context):
        objs = self.parse_scene()

        print(objs[0].to_json())

        return {"FINISHED"}

    def face_to_triangle(self, face):
        triangles = []

        if len(face) == 4:
            triangles.append([face[0], face[1], face[2]])
            triangles.append([face[2], face[3], face[0]])
        else:
            triangles.append(face)

        return triangles

    def create_verts_array(self, vertices, matrix):
        return [(matrix * vert.co)[:] for vert in vertices]

    def create_normals_array(self, vertices):
        return [vert.normal[:] for vert in vertices]

    def create_indices_array(self, faces):
        indices = []

        for face in faces:
            if len(face.vertices) == 3:
                indices.extend(face.vertices)
            else:
                indices.extend(face.vertices)
                indices.extend([face.vertices[0], face.vertices[2], face.vertices[3]])

        return indices

    def create_material_indices_array(self, faces):
        indices = []

        for face in faces:
            indices.append(face.material_index)

        return indices

    def create_materials_array(self, face_materials):
        materials = []

        for face_material in face_materials:
            mat = {
                "diffuse_color": [face_material.diffuse_color[0], face_material.diffuse_color[1], face_material.diffuse_color[2]],
                "diffuse_shader": face_material.diffuse_shader,
                "diffuse_shader": face_material.diffuse_shader,
                "diffuse_intensity": face_material.diffuse_intensity,
                "specular_color": [face_material.specular_color[0], face_material.specular_color[1], face_material.specular_color[2]],
                "specular_shader": face_material.specular_shader,
                "specular_intensity": face_material.specular_intensity,
                "alpha": face_material.alpha,
                "ambient": face_material.ambient
            }

            materials.append(mat)

        return materials

    def parse_scene(self, apply_mods=True, triangulate=True):
        bobjects = []

        #scene = bpy.context.scene

        for obj in bpy.context.selected_objects:
            matrix = obj.matrix_world.copy()

            obj.data.calc_tessface()
            faces = obj.data.tessfaces
            vertices = obj.data.vertices
            facesMaterials = obj.data.materials
            if obj.data.tessface_uv_textures.active is not None:
                facesuvs = obj.data.tessface_uv_textures.active.data
            else:
                facesuvs = []

            bobject = BObject(
                name=obj.name,
                vertices=self.create_verts_array(vertices, matrix),
                normals=self.create_normals_array(vertices),
                faces=self.create_indices_array(faces),
                face_materials=self.create_material_indices_array(faces),
                uvs=facesuvs,
                materials=self.create_materials_array(facesMaterials)
            )

            bobjects.append(bobject)

        return bobjects


def menu_func(self, context):
    self.layout.operator(BlenderBridgeOp.bl_idname, text="My Model Format(.fmt)");

def add_object_button(self, context):
    self.layout.operator(BlenderBridgeOp.bl_idname, text=BlenderBridgeOp.__doc__, icon='PLUGIN')


def register():
    bpy.utils.register_class(BlenderBridgeOp)
    bpy.types.VIEW3D_MT_object.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(BlenderBridgeOp)


if __name__ == '__main__':
    register()