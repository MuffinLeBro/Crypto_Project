import socket
import threading

class Server:

    PORT = 6000
    SERVER = "vlbelintrocrypto"
    ADDR = (SERVER, PORT)

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

    def handle_client(self, conn, addr):
        pass

    def start(self):
        self.server.listen()
        while True:
            conn, addr = self.server.accept()