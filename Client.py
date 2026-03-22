import socket
import threading
ADDRSERVER = "vlbelintrocrypto.hevs.ch"
PORT = 6000

class Client :
    def __init__(self,):
       self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
       self.running = True     

    def connect(self,IP_adress, port):
        try :
            self.sock.connect((ADDRSERVER, PORT))
            print(f"Connecté à {ADDRSERVER} : {PORT}")
        except Exception as e :
            print("Erreur de connexion à : ", ADDRSERVER)

    def send(self,message):
        try : 
            if isinstance(message, str):
                message = message.encode('utf-8')
            self.sock.sendall(message)
            print("Message envoyé")
        except Exception as e :
            print("Erreur de lors de l'envoi : ", e)

    def receive(self):
        try:
            data = self.sock.recv(4096)
            
            if data:
                return data
            return None
            
        except Exception as e:
            print("Erreur lors de la reception : ", e)
            return None

    def start_receiving(self):
               tread = threading.Thread(target=self.receive, daemon=True)
               tread.start()
    def close(self):
        self.running = False
        self.sock.close()
        print("Connexion fermée")
        pass
