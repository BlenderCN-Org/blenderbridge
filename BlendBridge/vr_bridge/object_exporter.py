from vr_bridge.singleton import Singleton
import io
import bpy
import mathutils
import json


class BObject(object):

    def __init__(self, name, vertices, normals, faces, face_materials, uvs, materials):
        self.name = name
        self.vertices = vertices
        self.normals = normals
        self.faces = faces
        self.face_materials = face_materials
        self.uvs = uvs
        self.materials = materials

    def to_dict(self):
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
        return json.dumps(self.to_dict())


class BlenderBridgeSceneParser:

    @staticmethod
    def face_to_triangle(face):
        triangles = []

        if len(face) == 4:
            triangles.append([face[0], face[1], face[2]])
            triangles.append([face[2], face[3], face[0]])
        else:
            triangles.append(face)

        return triangles

    @staticmethod
    def create_verts_array(vertices, matrix):
        return [(matrix * vert.co)[:] for vert in vertices]

    @staticmethod
    def create_normals_array(vertices):
        return [vert.normal[:] for vert in vertices]

    @staticmethod
    def create_indices_array(faces):
        indices = []

        for face in faces:
            if len(face.vertices) == 3:
                indices.extend(face.vertices)
            else:
                indices.extend(face.vertices)
                indices.extend([face.vertices[0], face.vertices[2], face.vertices[3]])

        return indices

    @staticmethod
    def create_material_indices_array(faces):
        indices = []

        for face in faces:
            indices.append(face.material_index)

        return indices

    @staticmethod
    def create_materials_array(face_materials):
        """
        https://www.blender.org/api/blender_python_api_2_67_release//bpy.types.Material.html
        https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Code_snippets/Materials_and_textures
        """
        materials = []

        for face_material in face_materials:
            mat = {
                "name": face_material.name,
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

    @staticmethod
    def parse_object(obj):
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
            vertices=BlenderBridgeSceneParser.create_verts_array(vertices, matrix),
            normals=BlenderBridgeSceneParser.create_normals_array(vertices),
            faces=BlenderBridgeSceneParser.create_indices_array(faces),
            face_materials=BlenderBridgeSceneParser.create_material_indices_array(faces),
            uvs=facesuvs,
            materials=BlenderBridgeSceneParser.create_materials_array(facesMaterials)
        )

        return bobject