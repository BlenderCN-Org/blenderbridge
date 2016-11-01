
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

    @staticmethod
    def parse_scene(apply_mods=True, triangulate=True):
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
                vertices=BlenderBridgeSceneParser.create_verts_array(vertices, matrix),
                normals=BlenderBridgeSceneParser.create_normals_array(vertices),
                faces=BlenderBridgeSceneParser.create_indices_array(faces),
                face_materials=BlenderBridgeSceneParser.create_material_indices_array(faces),
                uvs=facesuvs,
                materials=BlenderBridgeSceneParser.create_materials_array(facesMaterials)
            )

            bobjects.append(bobject)

        return bobjects


def save(context, filepath, *, use_triangles=True, use_normals=True, use_uvs=True, use_materials=True,
         use_mesh_modifiers=True, use_selection=True, use_animation=False, global_matrix=None, path_mode='AUTO'):

    objs = BlenderBridgeSceneParser.parse_scene()

