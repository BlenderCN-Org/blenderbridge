using UnityEngine;
using System.Collections;

public class Singleton<T> : MonoBehaviour where T : Singleton<T>
{

    private static T _sharedInstance; 

    public static T SharedInstance
    {
        get
        {
            if(_sharedInstance == null)
            {
                _sharedInstance = FindObjectOfType<T>(); 
            }

            if(_sharedInstance == null)
            {
                GameObject go = new GameObject(typeof(T).Name);
                _sharedInstance = go.AddComponent<T>(); 
            }

            return _sharedInstance; 
        }
    }

}
