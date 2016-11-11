using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BridgeObject {

    #region inner classes 

    public class BridgeObjectMaterial
    {

    }

    #endregion 

    public string name;

    public List<Vector3> verts = new List<Vector3>();
    public List<Vector3> normals = new List<Vector3>();
    public List<Vector2> uvs = new List<Vector2>();
    public List<int> faces = new List<int>();
    public List<BridgeObjectMaterial> materials = new List<BridgeObjectMaterial>();

    public MeshFilter BindMeshFilter(MeshFilter meshFilter)
    {
        var mesh = new Mesh();

        meshFilter.mesh = mesh;

        mesh.vertices = verts.ToArray();
        mesh.normals = normals.ToArray();
        mesh.triangles = faces.ToArray(); 

        //mesh.RecalculateNormals();
        mesh.RecalculateBounds();

        return meshFilter; 
    }

    public MeshRenderer BindMeshRenderer(MeshRenderer meshRenderer)
    {

        return meshRenderer; 
    }

    #region creation methods 

    public static BridgeObject ParseJson(Dictionary<string, object> obj)
    {
        const string KEY_UVS = "uvs";
        const string KEY_VERTICES = "vertices";
        const string KEY_MATS = "materials";
        const string KEY_MAT_SPEC_COLOR = "specular_color";
        const string KEY_MAT_AMBIENT = "ambient";
        const string KEY_MAT_SPEC_SHADER = "specular_shader";
        const string KEY_MAT_DIFFUSE_SHADER = "diffuse_shader";
        const string KEY_MAT_NAME = "name";
        const string KEY_MAT_DIFFUSE_INTENSITY = "diffuse_intensity";
        const string KEY_MAT_DIFFUSE_COLOR = "diffuse_color";
        const string KEY_MAT_ALPHA = "alpha";
        const string KEY_MAT_SPEC_INTENSITY = "specular_intensity";
        const string KEY_NAME = "name";
        const string KEY_NORMALS = "normals";
        const string KEY_FACES = "faces";
        const string KEY_FACE_MATS = "face_materials";

        List<object> verts_ = obj.ContainsKey(KEY_VERTICES) ? (obj[KEY_VERTICES] as List<object>) : new List<object>();
        List<object> norms_ = obj.ContainsKey(KEY_NORMALS) ? (obj[KEY_NORMALS] as List<object>) : new List<object>();
        List<object> faces_ = obj.ContainsKey(KEY_FACES) ? (obj[KEY_FACES] as List<object>) : new List<object>();
        string name_ = obj.ContainsKey(KEY_NAME) ? (obj[KEY_NAME] as string) : "";

        BridgeObject bo = new BridgeObject(); 
        foreach(var vert in verts_)
        {
            var vertList = vert as List<object>;
            bo.verts.Add(CreateVector3((double)vertList[0], (double)vertList[1], (double)vertList[2]));
        }

        foreach (var norm in norms_)
        {
            var normList = norm as List<object>;
            bo.normals.Add(CreateVector3((double)normList[0], (double)normList[1], (double)normList[2]));
        }

        foreach(var face in faces_)
        {
            bo.faces.Add(Convert.ToInt32(face)); 
        }

        bo.name = name_; 

        return bo;
    }

    static Vector3 CreateVector3(double x, double y, double z)
    {
        return new Vector3((float)x, (float)y, (float)z); 
    }

    #endregion 
}
