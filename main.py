
from Client import Client
from MessageHandler import MessageHandler
from Command import Command 
import time

ADDRSERVER = "vlbelintrocrypto.hevs.ch"
PORT = 6000

def main():
    client = Client()
    client.connect(ADDRSERVER, PORT)
    
    handler = MessageHandler()
    cmd = Command()


    handler.add_data("s", "task shift encode 6")
    client.send(handler.get_message())

    raw_instructions = client.receive()
    if raw_instructions:
        msg_type, text_instructions = handler.decode_message(raw_instructions)
        print(f"Serveur (Instructions) : {text_instructions}")
        
        shift_key = int(text_instructions.split()[-1])

    raw_word = client.receive()
    if raw_word:
        msg_type, text_word = handler.decode_message(raw_word)
        print(f"Serveur (Mot à chiffrer) : {text_word}")
        

        reponse_chiffree = cmd.encode_shift(text_word, shift_key)
        print(f"Notre réponse chiffrée : {reponse_chiffree}")
        
        handler.add_data("r", reponse_chiffree) 

        handler.add_data("s", reponse_chiffree)
        client.send(handler.get_message())
        
        raw_result = client.receive()
        if raw_result:
            msg_type, text_result = handler.decode_message(raw_result)
            print(f"Serveur (Résultat final) : {text_result}")

    client.close()

if __name__ == "__main__":
    main()