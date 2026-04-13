import hashlib
import random


class Command:
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

    # --- RSA ---

    def _find_private_key_d(self, e, phi):
        for d in range(2, phi):
            if (e * d) % phi == 1:
                return d
        return -1

    def rsa_generate(self, p=23, q=37, e=17):
        """Generate RSA key pair. Returns (e, d, n)."""
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

    # --- Diffie-Hellman ---

    def _is_prime(self, n):
        if n < 2:
            return False
        if n < 4:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def dh_generate(self, max_mod=None):
        """Generate DH parameters (mod, gen). Returns (p, g)."""
        if max_mod is None:
            max_mod = 1000
        primes = [p for p in range(3, max_mod) if self._is_prime(p)]
        p = random.choice(primes)
        g = random.randint(2, p - 1)
        return p, g

    def dh_halfkey(self, mod, gen, priv_a=None):
        """Compute DH half key: A = g^a mod p. Returns (A, a)."""
        if priv_a is None:
            priv_a = random.randint(2, mod - 2)
        half_key = pow(gen, priv_a, mod)
        return half_key, priv_a

    def dh_secret(self, mod, gen, priv_a, gB):
        """Compute DH shared secret: s = gB^a mod p."""
        return pow(gB, priv_a, mod)