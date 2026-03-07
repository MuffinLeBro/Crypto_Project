import socket
ADDRSERVER = "vlbelintrocrypto.hevs.ch"
PORT = 6000
class Client :
    def __init__(self,):
       self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def connect(self,IP_adress, port):
        try :
            self.sock.connect(ADDRSERVER, PORT)
            print(f"Connecté à {ADDRSERVER} : {PORT}")
        except Exception as e :
            print("Erreur de connexion à : ", ADDRSERVER)

    def send(self,message):
        try : 
            self.sock.sendall(message)
        except Exception as e :
            print("Erreur de lors de l'envoi : ", e)

    def receive(self, Timeout = 0.001):
        self.sock.settimeout(Timeout)
        try : 
            response = self.receive(4096)
            return response
        except Exception as e :
            print(f"Erreur lors de la reception : ", e)
            return None
        
    def close(self):
        self.sock.close()
        print("Connexion fermée")
        pass
