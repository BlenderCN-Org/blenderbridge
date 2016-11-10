using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MiniJSON;

[RequireComponent(typeof(BridgeConnectionManager))]
public class BridgeProcessor : Singleton<BridgeProcessor> {

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

    }

    #endregion 

    #region Callbacks 

    private void BridgeProcessor_OnDataRecieved(string data)
    {
        queue.Enqueue(data); 
    }

    #endregion 
}
