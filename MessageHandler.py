import struct

class MessageHandler:
    def __init__(self, bytesPerChar=4):
        self.header = b'ISC'
        self.bytesPerChar = bytesPerChar
        self.binaryMessage = b''

    def add_data(self, msg_type, text):
        typeByte = msg_type.encode('utf-8')
        
        nChar = len(text)
        lengthByte = struct.pack('>H', nChar)
        
        bodyBytes = b""
        for char in text:
            charEncoded = char.encode('utf-8')
            bodyBytes += charEncoded.rjust(self.bytesPerChar, b'\x00')
            
        self.binaryMessage = self.header + typeByte + lengthByte + bodyBytes

    def get_message(self):
        return self.binaryMessage
    
    def decode_message(self, raw_bytes):
        if not raw_bytes or len(raw_bytes) < 6:
            return None, None
            
        header = raw_bytes[0:3]
        if header != b'ISC':
            print("Erreur : En-tête invalide")
            return None, None
                
        msg_type = raw_bytes[3:4].decode('utf-8')
        
        n_chars = struct.unpack('>H', raw_bytes[4:6])[0]
        
        body_bytes = raw_bytes[6:]
        message = ""
        
        for i in range(n_chars):
            char_bytes = body_bytes[i*4 : (i+1)*4]
            # Retrait du formatage pour lire la lettre
            char = char_bytes.replace(b'\x00', b'').decode('utf-8')
            message += char
            
        return msg_type, message