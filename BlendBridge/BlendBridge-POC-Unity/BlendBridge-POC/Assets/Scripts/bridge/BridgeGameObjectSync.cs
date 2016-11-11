using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(MeshFilter))]
[RequireComponent(typeof(MeshRenderer))]
public class BridgeGameObjectSync : MonoBehaviour {

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		
	}

    public void Bind(BridgeObject bo)
    {
        bo.BindMeshFilter(GetComponent<MeshFilter>());
        bo.BindMeshRenderer(GetComponent<MeshRenderer>());
    }
}
