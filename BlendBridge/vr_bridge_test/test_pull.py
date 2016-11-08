import socket


class MySocket:
    MSGLEN = 256

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        sent = self.sock.send(msg)

    def myreceive(self):
        while True:
            resp = (self.sock.recv(1024))
            if resp:
                break

        return resp


if __name__ == "__main__":
    s = MySocket()
    s.connect("localhost", 5555)
    s.mysend(b'0')
    while True:
        print(s.myreceive())