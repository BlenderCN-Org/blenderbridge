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

    public List<float> verts = new List<float>();
    public List<float> uvs = new List<float>();
    public List<int> triangles = new List<int>();
    public List<BridgeObjectMaterial> materials = new List<BridgeObjectMaterial>();

    public void BindMeshFilter(MeshFilter meshFilter)
    {

    }

    public void BindMeshRenderer(MeshRenderer meshRenderer)
    {

    }

    #region creation methods 

    public static BridgeObject ParseJson(Dictionary<string, object> obj)
    {
        return null;
    }

    #endregion 
}
