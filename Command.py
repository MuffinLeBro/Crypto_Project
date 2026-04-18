import hashlib


class Command:
    def _normalize_vigenere_key(self, key):
        normalized_key = [char.upper() for char in key if char.isalpha()]
        if not normalized_key:
            raise ValueError("La cle Vigenere doit contenir au moins une lettre.")
        return normalized_key

    def _transform_vigenere_char(self, char, key_char, direction):
        if not char.isalpha():
            return char

        alphabet_start = ord('A') if char.isupper() else ord('a')
        char_offset = ord(char) - alphabet_start
        key_offset = ord(key_char) - ord('A')
        transformed_offset = (char_offset + (direction * key_offset)) % 26
        return chr(alphabet_start + transformed_offset)

    def encode_shift(self, message, shift):
        result = ''
        for letter in message:
            new_code = (ord(letter) + shift)
            result += chr(new_code)
        return result

    def decode_shift(self, message, shift):
        result = ''
        for letter in message:
            new_code = (ord(letter) - shift)
            result += chr(new_code)
        return result

    def xor(self, message, key):
        result = []
        for idx in range(len(message)):
            key_byte = key[idx % len(key)]
            result.append(message[idx] ^ key_byte)
        return bytes(result)

    def encode_vigenere(self, message, key):
        normalized_key = self._normalize_vigenere_key(key)
        result = ''
        key_index = 0
        for char in message:
            if char.isalpha():
                key_char = normalized_key[key_index % len(normalized_key)]
                result += self._transform_vigenere_char(char, key_char, 1)
                key_index += 1
            else:
                result += char
        return result

    def decode_vigenere(self, message, key):
        normalized_key = self._normalize_vigenere_key(key)
        result = ''
        key_index = 0
        for char in message:
            if char.isalpha():
                key_char = normalized_key[key_index % len(normalized_key)]
                result += self._transform_vigenere_char(char, key_char, -1)
                key_index += 1
            else:
                result += char
        return result

    # --- RSA ---

    def _find_private_key_d(self, e, phi):
        for d in range(2, phi):
            if (e * d) % phi == 1:
                return d
        return -1

    def rsa_generate(self, p=23, q=37, e=17):
        """Générer une paire de clés RSA. Renvoie (e, d, n)."""
        n = p * q
        phi = (p - 1) * (q - 1)
        d = self._find_private_key_d(e, phi)
        return e, d, n

    def encode_rsa(self, message, pub, mod):
        """Encode each character with RSA: c = m^pub mod n. Returns list of ints."""
        encrypted_list = []
        for letter in message:
            number_version = ord(letter)
            encrypted_number = pow(number_version, pub, mod)
            encrypted_list.append(encrypted_number)
        return encrypted_list

    def decode_rsa(self, encrypted_list, priv, mod):
        """Decode list of ints with RSA: m = c^priv mod n. Returns string."""
        decrypted_word = ""
        for secret_number in encrypted_list:
            decrypted_number = pow(secret_number, priv, mod)
            letter = chr(decrypted_number)
            decrypted_word += letter
        return decrypted_word

    # --- Hash ---

    def sha256(self, message):
        """SHA-256 hash of the message."""
        return hashlib.sha256(message.encode('utf-8')).hexdigest()

