from Client import Client
ADDRSERVER = "vlbelintrocrypto.hevs.ch"
PORT = 6000
def main():
   client = Client()
   client.connect(ADDRSERVER, PORT)
   messagae="Je suis etudient a la heso"
   client.send(messagae)
if __name__ == "__main__":
        main()