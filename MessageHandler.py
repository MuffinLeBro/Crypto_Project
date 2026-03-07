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