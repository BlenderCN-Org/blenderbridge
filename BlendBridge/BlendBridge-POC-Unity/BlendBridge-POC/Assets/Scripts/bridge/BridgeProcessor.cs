using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MiniJSON;

[RequireComponent(typeof(BridgeConnectionManager))]
public class BridgeProcessor : Singleton<BridgeProcessor> {

    public GameObject BridgeObjectsContainer;

    Dictionary<string, BridgeGameObjectSync> bridgeGameObjects = new Dictionary<string, BridgeGameObjectSync>(); 

    ConcurrentQueue<string> queue = new ConcurrentQueue<string>(); 

	void Start () {
        GetComponent<BridgeConnectionManager>().OnDataRecieved += BridgeProcessor_OnDataRecieved;
	}           

    void Update () {
        ProcessQueue(); 
	}

    #region utils methods 

    void ProcessQueue()
    {
        if(queue.Count == 0)
        {
            return; 
        }

        string data = queue.Dequeue();
        var json = Json.Deserialize(data) as Dictionary<string, object>;

        BridgeObject bo = BridgeObject.ParseJson(json);

        if(bo != null)
        {
            ProcessBridgeObject(bo);
        } 
    }

    void ProcessBridgeObject(BridgeObject bo)
    {
        BridgeGameObjectSync bgos; 

        if (!bridgeGameObjects.ContainsKey(bo.name))
        {
            GameObject go = new GameObject(bo.name);
            bgos = go.AddComponent<BridgeGameObjectSync>();
            go.transform.parent = BridgeObjectsContainer != null ? BridgeObjectsContainer.transform : transform;
            bridgeGameObjects.Add(bo.name, bgos);
        }

        bgos = bridgeGameObjects[bo.name];
        bgos.Bind(bo);
    }

    #endregion 

    #region Callbacks 

    private void BridgeProcessor_OnDataRecieved(string data)
    {
        queue.Enqueue(data); 
    }

    #endregion 
}
