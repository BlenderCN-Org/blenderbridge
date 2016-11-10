
import threading
from vr_bridge.singleton import Singleton
import bpy
import time
import sys
import zmq
import queue


class Bridge(metaclass=Singleton):
    """

    """
    def __init__(self):
        self.running = False

        self._send_loop_running = False
        self._receive_loop_running = False

        self._send_thread = None
        self._receive_thread = None

        self.observing_objects = []
        self.context = None
        self.socket = None

        self.packet_queue = queue.Queue()

        self.start()

    def start(self):
        if self.running:
            return

        self.running = True

        self.open_connection()

        # self._send_thread = threading.Thread(target=self.receive_loop)
        # self._send_thread.start()

        self._receive_thread = threading.Thread(target=self.send_loop)
        self._receive_thread.start()

    def open_connection(self):
        """
        https://www.digitalocean.com/community/tutorials/how-to-work-with-the-zeromq-messaging-library
        http://nichol.as/zeromq-an-introduction
        http://zguide.zeromq.org/py:hwserver
        :return:
        """
        try:
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.PUSH)
            self.socket.bind("tcp://*:5555")

        except:
            raise Exception('Unable to start Thread')

    def close_connection(self):
        self.socket.close()

    def stop(self):
        if not self.running:
            return

        self.running = False

    def enqueue_packet(self, packet):
        print("enqueue_packet {}".format(packet))
        self.packet_queue.put(packet)

    def send_loop(self):
        print("Starting send_loop")
        self._send_loop_running = True

        while self.running:
            while not self.packet_queue.empty():
                packet = self.packet_queue.get()
                self.socket.send_string(packet)

            time.sleep(0.2)

        self._send_loop_running = False

        if not self._receive_loop_running:
            self.close_connection()

        print("Finished send_loop")

    def receive_loop(self):
        print("Starting receive_loop")
        self._receive_loop_running = True

        while self.running:
            try:
                message = self.socket.recv()
                print("Received request: %s" % message)
            except Exception as e:
                print("Exception while trying to receive data; {}".format(e))
                break

        self._receive_loop_running = False

        if not self._send_loop_running:
            self.close_connection()

        print("Finished receive_loop")


