using UnityEngine;
using System.Collections;

public class SceneManager : Singleton<SceneManager> {

    // Use this for initialization
    void Start () {
        BridgeConnectionManager.SharedInstance.Connect(); 
	}
	
	// Update is called once per frame
	void Update () {
	
	}
}
