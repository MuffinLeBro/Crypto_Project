from Client import Client
import time
ADDRSERVER = "vlbelintrocrypto.hevs.ch"
PORT = 6000
def main():
   client = Client()
   client.connect(ADDRSERVER, PORT)
   client.start_receiving()
   message="Je vais prendre une tasse de cafe bien chaud sur scala"
   print("Message to send: ", message)
   client.send(message)

   time.sleep(4000000)  # Attendre un peu pour recevoir les messages du serveur
   client.close()

if __name__ == "__main__":
        main()