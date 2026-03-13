class Command:
    def encode_shift(self, message, shift):
        result = ''
        for letter in message:
            new_code = (ord(letter)-32 + shift) % 1114112
            result += chr(new_code)
        return result

    def xor(self, message, key):
        result=[]
        for idx in range(len(message)):
            key_byte = key[idx%len(key)]
            result.append(message[idx]^key_byte)
        return bytes(result)

    def encode_vigenere(self, message, key):
        result = ''
        for i, char in enumerate(message):
            key_char = key[i % len(key)]
            new_code = (ord(char) + ord(key_char))
            result += chr(new_code)
        return result
        
    def decode_vigenere(self, message, key):
        result = ''
        for i, char in enumerate(message):
            key_char = key[i % len(key)]
            new_code = (ord(char) - ord(key_char))
            result += chr(new_code)
        return result