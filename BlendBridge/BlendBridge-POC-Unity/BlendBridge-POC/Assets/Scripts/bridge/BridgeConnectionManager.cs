using UnityEngine;
using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Text;

/**
 * Reference:
 * https://msdn.microsoft.com/en-us/library/bew39x2a(v=vs.110).aspx
 * */
public class BridgeConnectionManager : Singleton<BridgeConnectionManager> {

    #region Inner class 

    public class StateObject
    {
        // Client socket.
        public Socket workSocket = null;
        // Size of receive buffer.
        public const int BufferSize = 50000;
        // Receive buffer.
        public byte[] buffer = new byte[BufferSize];
        // Received data string.
        public StringBuilder sb = new StringBuilder();
    }


    #endregion 

    public delegate void DataRecieved(string data);
    public event DataRecieved OnDataRecieved;

    public string hostname = "localhost";
    public int port = 5555;

    bool isRecieving = false;
    Socket client;

    const int maxConnectionAttempts = 5;
    const float delayBetweenConnectionAttempts = 2.0f; 
    int connectionAttempts = 0;

    ConcurrentQueue<string> queue = new ConcurrentQueue<string>(); 

    ManualResetEvent connectDone = new ManualResetEvent(false);
    ManualResetEvent sendDone = new ManualResetEvent(false);

    public bool IsConnected
    {
        get
        {
            return client != null; 
        }
    }       

    void Start () {
	
	}
	
	void Update () {
	
	}

    #region Connection methods 

    public void Connect()
    {
        if (IsConnected)
        {
            return;
        }

        if (++connectionAttempts >= maxConnectionAttempts)
        {
            throw new Exception(string.Format("Failed to connect to server {0}:{1}", hostname, port));
        }

        try
        {
            Debug.Log("Initilising Connection"); 

            client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            //IPHostEntry ipHostInfo = Dns.GetHostEntry(hostname);
            //IPAddress ipAddress = ipHostInfo.AddressList[0];
            //IPEndPoint remoteEP = new IPEndPoint(ipAddress, port);
            //client.BeginConnect(remoteEP, new AsyncCallback(ConnectCallback), client);
            //connectDone.WaitOne();

            client.Connect(hostname, port);

            Debug.Log("Connected");

            Send("0");

            //AsyncSend("0");
            //sendDone.WaitOne();

            isRecieving = true;

            BeginRecieving();

        }
        catch (Exception e)
        {
            Debug.LogWarningFormat("Error trying to connect with client {0}", e.Message); 
            Invoke("Connect", delayBetweenConnectionAttempts);
        }

    }

    public void Disconnect()
    {
        if (!IsConnected)
        {
            return;
        }

        try
        {
            isRecieving = false; 

            // Release the socket.
            client.Shutdown(SocketShutdown.Both);
            client.Close();
            client = null;
        }
        catch (Exception e)
        {
            Debug.LogWarningFormat("Failed to close Socket connection, {0}", e.Message);
        }

    }

    public bool Send(String data)
    {
        if (!IsConnected)
        {
            Debug.Log("Not connected or connection is not ready");
            return false;
        }

        Debug.Log("Sending Data");

        // Convert the string data to byte data using ASCII encoding.
        byte[] byteData = Encoding.ASCII.GetBytes(data);

        int dataSent = client.Send(byteData);

        Debug.LogFormat("Sent {0} bytes", dataSent);

        return true;
    }

    public bool AsyncSend(String data)
    {
        if (!IsConnected)
        {
            return false; 
        }

        Debug.Log("Sending Data"); 

        // Convert the string data to byte data using ASCII encoding.
        byte[] byteData = Encoding.ASCII.GetBytes(data);

        // Begin sending the data to the remote device.
        client.BeginSend(byteData, 0, byteData.Length, SocketFlags.None, new AsyncCallback(SendCallback), client); 

        return true; 
    }

    private bool BeginRecieving()
    {
        if (!IsConnected || !isRecieving)
        {
            return false; 
        }

        try
        {
            // Create the state object.
            StateObject state = new StateObject();
            state.workSocket = client;

            // Begin receiving the data from the remote device.
            client.BeginReceive(state.buffer, 0, StateObject.BufferSize, 0, new AsyncCallback(ReceiveCallback), state);

            return true; 
        }
        catch (Exception e)
        {
            Debug.LogErrorFormat("Error trying to receive from Server, {0}", e.Message);
            return false; 
        }
    }

    #region Socket Async Callbacks

    private void ReceiveCallback(IAsyncResult ar)
    {
        try
        {
            Debug.Log("ReceiveCallback"); 
            // Retrieve the state object and the client socket 
            // from the asynchronous state object.
            StateObject state = (StateObject)ar.AsyncState;
            Socket client = state.workSocket;
            
            // Read data from the remote device.
            int bytesRead = client.EndReceive(ar);

            if (bytesRead > 0)
            {
                // There might be more data, so store the data received so far.
                //state.sb.Append(Encoding.ASCII.GetString(state.buffer, 0, bytesRead));

                //string tmpString = Convert.ToBase64String(state.buffer, 0, bytesRead);

                int startValue = 123; // {
                int endValue = 125; // }
                int startIndex = -1;
                int endIndex = -1; 
                 
                for(int i=0; i< bytesRead; i++)
                {
                    if(state.buffer[i] == startValue)
                    {
                        startIndex = i;
                        break; 
                    }
                }
                for(int i=bytesRead-1; i>=0; i--)
                {
                    if (state.buffer[i] == endValue)
                    {
                        endIndex = i;
                        break;
                    }
                }

                if(startIndex >= 0 && endIndex > startIndex)
                {
                    string tmpString = Encoding.ASCII.GetString(state.buffer, startIndex, endIndex);
                    
                    if(OnDataRecieved != null)
                    {
                        OnDataRecieved(tmpString); 
                    }
                    //state.sb.Append(Convert.ToBase64String(state.buffer, 0, bytesRead));

                    Debug.LogFormat("Appending Data {0} --- {1}", bytesRead, tmpString);
                }
                else
                {
                    Debug.LogWarning("Couldn't find valid JSON object"); 
                }               

                // Get the rest of the data.
                client.BeginReceive(state.buffer, 0, StateObject.BufferSize, 0, new AsyncCallback(ReceiveCallback), state);
            }
            else
            {
                // All the data has arrived; put it in response.
                if (state.sb.Length > 1)
                {
                    string response = state.sb.ToString();
                    queue.Enqueue(response);
                    Debug.Log(response);
                }

                BeginRecieving(); 
            }
        }
        catch (Exception e)
        {
            Debug.LogWarning(e.ToString());
            BeginRecieving();
        }
    }

    private void SendCallback(IAsyncResult ar)
    {
        Debug.Log("SendCallback"); 
        try
        {
            // Retrieve the socket from the state object.
            Socket client = (Socket)ar.AsyncState;

            // Complete sending the data to the remote device.
            int bytesSent = client.EndSend(ar);
            Debug.LogFormat("Sent {0} bytes to server.", bytesSent);

            // Signal that all bytes have been sent.
            sendDone.Set();
        }
        catch (Exception e)
        {
            Debug.LogWarning(e.ToString());
        }
    }

    private void ConnectCallback(IAsyncResult ar)
    {
        Debug.Log("ConnectCallback"); 

        try
        {
            // Retrieve the socket from the state object.
            Socket client = (Socket)ar.AsyncState;

            // Complete the connection.
            client.EndConnect(ar);

            Debug.LogFormat("Socket connected to {0}", client.RemoteEndPoint.ToString());

            // Signal that the connection has been made.
            connectDone.Set();
        }
        catch (Exception e)
        {
            Debug.LogError(e.ToString());
        }
    }

    #endregion

    #endregion

}
