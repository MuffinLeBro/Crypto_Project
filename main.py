from Client import Client
from MessageHandler import MessageHandler
import time
ADDRSERVER = "vlbelintrocrypto.hevs.ch"
PORT = 6000
def main():
   client = Client()
   client.connect(ADDRSERVER, PORT)
   client.start_receiving()
   message=["Je vais prendre une tasse de cafe bien chaud sur scala",
            "Je vais prendre une tasse de cafe bien chaud sur java",
            "Je vais prendre une tasse de cafe bien chaud sur php",
            "Je vais prendre une tasse de cafe bien chaud sur ruby",
            "Je vais prendre une tasse de cafe bien chaud sur scala",]
   handler = MessageHandler()
   for msg in message:
         handler.add_data("s", msg)
         binaryMessage = handler.get_message()
         print("Message binaire à envoyer : ", msg)
         client.send(binaryMessage)
         time.sleep(1)
         time.sleep(10)

if __name__ == "__main__":
        main()