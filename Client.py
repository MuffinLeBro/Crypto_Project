import socket
import threading


class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.connected = False
        self.server_addr = None
        self.server_port = None
        self.on_message = None  # callback for received messages

    def connect(self, ip_address, port):
        try:
            self.sock.connect((ip_address, port))
            self.connected = True
            self.server_addr = ip_address
            self.server_port = port
            print(f"Connecté à {ip_address}:{port}")
        except Exception as e:
            print(f"Erreur de connexion à {ip_address}:{port} : {e}")

    def send(self, message):
        try:
            if isinstance(message, str):
                message = message.encode('utf-8')
            self.sock.sendall(message)
        except Exception as e:
            print("Erreur lors de l'envoi :", e)

    def receive(self):
        try:
            data = self.sock.recv(4096)
            if data:
                return data
            return None
        except Exception as e:
            if self.running:
                print("Erreur lors de la réception :", e)
            return None

    def receive_loop(self):
        while self.running:
            data = self.receive()
            if data and self.on_message:
                self.on_message(data)
            elif not data and self.running:
                print("\nConnexion perdue avec le serveur.")
                self.running = False
                break

    def start_receiving(self, callback):
        self.on_message = callback
        thread = threading.Thread(target=self.receive_loop, daemon=True)
        thread.start()

    def health(self):
        if not self.connected:
            return False
        try:
            self.sock.getpeername()
            return True
        except Exception:
            return False

    def close(self):
        self.running = False
        self.connected = False
        try:
            self.sock.close()
        except Exception:
            pass
        print("Connexion fermée")
