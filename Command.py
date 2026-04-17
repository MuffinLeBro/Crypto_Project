import hashlib
import random


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
import os

BANNER = """
================================================
            AVAILABLE COMMANDS
================================================
/help                       - Show this message
/health                     - Check server connection
/quit, /exit                - Disconnect and exit
/send <text>|plain|encoded [-s] - Send text or buffer
/clear                      - Clear the screen
/clearbuf [plain|encoded]   - Clear buffers
/set <plain|encoded> <text> - Set buffer
/show                       - Show current buffers
/list [n]                   - Show last n messages (default 10)
/select <i> [e|c]           - Select message for encoded/plain buffer
/encode shift <k>           - Encode plain buffer with shift
/decode shift <k>           - Decode encoded buffer with shift

/decode isc [hex_message]   - Decode ISC frame from hex or encoded buffer
/encode vigenere <key>
/decode vigenere <key>
/encode rsa <pub> <mod>
/decode rsa <priv> <mod>
/rsa generate               - Generate RSA keys
/hash                       - SHA-256 of plain buffer
/dh generate [max_mod]
/dh halfkey <mod> <gen> [priv_a]
/dh secret <mod> <gen> <priv_a> <gB>
<text>                      - Send clear message to other clients
================================================
"""
from Command import Command
from Client import Client
from MessageHandler import MessageHandler
ADDRSERVER = "vlbelintrocrypto.hevs.ch"
PORT = 6000
class CLI:
    def __init__(self):
        self.client = Client()
        self.handler = MessageHandler()
        self.cmd = Command()
        self.plain_buffer = ""
        self.encoded_buffer = ""  # str for shift/vigenere, list[int] for RSA
        self.messages = []  # list of (direction, msg_type, text)
        self.last_decoded_isc = None

    def show_banner(self):
        print(BANNER)
        print("Type a message and press ENTER to send.")
        print("Type /help to see available commands.\n")

    def on_message_received(self, raw_data):
        try:
            decoded_message = self.handler.parse_message(raw_data)
        except (TypeError, ValueError, UnicodeDecodeError) as exc:
            print(f"\n[Serveur] Trame ISC invalide: {exc}")
            print("> ", end="", flush=True)
            return

        self.last_decoded_isc = decoded_message
        self.messages.append(("recv", decoded_message.msg_type, decoded_message.text))
        print(f"\n[Serveur] ({decoded_message.msg_type}): {decoded_message.text}")
        print("> ", end="", flush=True)

    def send_to_server(self, msg_type, text, silent=False):
        try:
            payload = self.handler.build_message(msg_type, text)
        except (TypeError, ValueError) as exc:
            print(f"Impossible d'encoder la trame ISC: {exc}")
            return

        self.client.send(payload)
        self.messages.append(("sent", msg_type, text))
        if not silent:
            print(f"Message envoyé: {text}")

    def run(self):
        self.client.connect(ADDRSERVER, PORT)
        if not self.client.connected:
            print("Impossible de se connecter au serveur. Arrêt.")
            return

        self.client.start_receiving(self.on_message_received)
        self.show_banner()

        try:
            while self.client.running:
                try:
                    user_input = input("> ")
                except EOFError:
                    break

                if not user_input.strip():
                    continue

                if user_input.startswith("/"):
                    self.handle_command(user_input.strip())
                else:
                    self.send_to_server("s", user_input)
        except KeyboardInterrupt:
            print("\nInterruption.")
        finally:
            self.client.close()

    def handle_command(self, input_str):
        parts = input_str.split()
        command = parts[0].lower()
        args = parts[1:]

        if command == "/help":
            print(BANNER)

        elif command in ("/quit", "/exit"):
            print("Déconnexion...")
            self.client.running = False

        elif command == "/health":
            if self.client.health():
                print("Connexion au serveur : OK")
            else:
                print("Connexion au serveur : PERDUE")

        elif command == "/clear":
            os.system("clear" if os.name != "nt" else "cls")

        elif command == "/clearbuf":
            self._cmd_clearbuf(args)

        elif command == "/set":
            self._cmd_set(args)

        elif command == "/show":
            self._cmd_show()

        elif command == "/list":
            self._cmd_list(args)

        elif command == "/select":
            self._cmd_select(args)

        elif command == "/send":
            self._cmd_send(args)

        elif command == "/encode":
            self._cmd_encode(args)

        elif command == "/decode":
            self._cmd_decode(args)

        elif command == "/rsa":
            self._cmd_rsa(args)

        elif command == "/hash":
            self._cmd_hash()

        elif command == "/dh":
            self._cmd_dh(args)

        else:
            print(f"Commande inconnue : {command}. Tapez /help pour l'aide.")

    # --- Buffer commands ---

    def _cmd_clearbuf(self, args):
        if not args:
            self.plain_buffer = ""
            self.encoded_buffer = ""
            print("Buffers vidés.")
        elif args[0] == "plain":
            self.plain_buffer = ""
            print("Plain buffer vidé.")
        elif args[0] == "encoded":
            self.encoded_buffer = ""
            print("Encoded buffer vidé.")
        else:
            print("Usage: /clearbuf [plain|encoded]")

    def _cmd_set(self, args):
        if len(args) < 2:
            print("Usage: /set <plain|encoded> <text>")
            return
        buf_type = args[0]
        text = " ".join(args[1:])
        if buf_type == "plain":
            self.plain_buffer = text
            print(f"Plain buffer = \"{self.plain_buffer}\"")
        elif buf_type == "encoded":
            self.encoded_buffer = text
            print(f"Encoded buffer = \"{self.encoded_buffer}\"")
        else:
            print("Usage: /set <plain|encoded> <text>")

    def _cmd_show(self):
        print(f"Plain buffer   : \"{self.plain_buffer}\"")
        if isinstance(self.encoded_buffer, list):
            print(f"Encoded buffer : {self.encoded_buffer}  (RSA int list)")
        else:
            print(f"Encoded buffer : \"{self.encoded_buffer}\"")

    # --- Message history ---

    def _cmd_list(self, args):
        n = 10
        if args:
            try:
                n = int(args[0])
            except ValueError:
                print("Usage: /list [n]")
                return
        recent = self.messages[-n:]
        if not recent:
            print("Aucun message.")
            return
        start_idx = max(0, len(self.messages) - n)
        for i, (direction, msg_type, text) in enumerate(recent):
            idx = start_idx + i
            arrow = "<-" if direction == "recv" else "->"
            print(f"  [{idx}] {arrow} ({msg_type}) {text}")

    def _cmd_select(self, args):
        if not args:
            print("Usage: /select <i> [e|c]")
            return
        try:
            idx = int(args[0])
        except ValueError:
            print("Usage: /select <i> [e|c]")
            return
        if idx < 0 or idx >= len(self.messages):
            print(f"Index invalide. Messages disponibles : 0-{len(self.messages) - 1}")
            return
        _, _, text = self.messages[idx]
        target = args[1].lower() if len(args) > 1 else "c"
        if target == "e":
            self.encoded_buffer = text
            print(f"Encoded buffer = \"{text}\"")
        else:
            self.plain_buffer = text
            print(f"Plain buffer = \"{text}\"")

    # --- Send ---

    def _cmd_send(self, args):
        if not args:
            print("Usage: /send <text>|plain|encoded [-s]")
            return
        silent = "-s" in args
        send_args = [a for a in args if a != "-s"]
        keyword = send_args[0] if send_args else ""

        if keyword == "plain":
            if not self.plain_buffer:
                print("Plain buffer est vide.")
                return
            self.send_to_server("s", self.plain_buffer, silent)
        elif keyword == "encoded":
            if not self.encoded_buffer:
                print("Encoded buffer est vide.")
                return
            self.send_to_server("s", self.encoded_buffer, silent)
        else:
            text = " ".join(send_args)
            self.send_to_server("s", text, silent)

    # --- Encode / Decode ---

    def _cmd_encode(self, args):
        if not args:
            print("Usage: /encode shift <k> | /encode vigenere <key> | /encode rsa <pub> <mod>")
            return
        method = args[0].lower()
        if method == "shift":
            if len(args) < 2:
                print("Usage: /encode shift <k>")
                return
            try:
                k = int(args[1])
            except ValueError:
                print("La clé doit être un entier.")
                return
            if not self.plain_buffer:
                print("Plain buffer est vide. Utilisez /set plain <text>")
                return
            self.encoded_buffer = self.cmd.encode_shift(self.plain_buffer, k)
            print(f"Encoded buffer = \"{self.encoded_buffer}\"")

        elif method == "vigenere":
            if len(args) < 2:
                print("Usage: /encode vigenere <key>")
                return
            key = args[1]
            if not self.plain_buffer:
                print("Plain buffer est vide. Utilisez /set plain <text>")
                return
            try:
                self.encoded_buffer = self.cmd.encode_vigenere(self.plain_buffer, key)
            except ValueError as exc:
                print(exc)
                return
            print(f"Encoded buffer = \"{self.encoded_buffer}\"")

        elif method == "rsa":
            if len(args) < 3:
                print("Usage: /encode rsa <pub> <mod>")
                return
            try:
                pub = int(args[1])
                mod = int(args[2])
            except ValueError:
                print("pub et mod doivent être des entiers.")
                return
            if not self.plain_buffer:
                print("Plain buffer est vide. Utilisez /set plain <text>")
                return
            self.encoded_buffer = self.cmd.encode_rsa(self.plain_buffer, pub, mod)
            print(f"Encoded buffer = {self.encoded_buffer}")

        else:
            print("Méthode inconnue. Utilisez: shift, vigenere, rsa")

    def _cmd_decode(self, args):
        if not args:
            print("Usage: /decode shift <k> | /decode isc [hex_message] | /decode vigenere <key> | /decode rsa <priv> <mod>")
            return
        method = args[0].lower()
        if method == "isc":
            self._cmd_decode_isc(args[1:])

        elif method == "shift":
            if len(args) < 2:
                print("Usage: /decode shift <k>")
                return
            try:
                k = int(args[1])
            except ValueError:
                print("La clé doit être un entier.")
                return
            if not self.encoded_buffer:
                print("Encoded buffer est vide.")
                return
            self.plain_buffer = self.cmd.decode_shift(self.encoded_buffer, k)
            print(f"Plain buffer = \"{self.plain_buffer}\"")

        elif method == "vigenere":
            if len(args) < 2:
                print("Usage: /decode vigenere <key>")
                return
            key = args[1]
            if not self.encoded_buffer:
                print("Encoded buffer est vide.")
                return
            try:
                self.plain_buffer = self.cmd.decode_vigenere(self.encoded_buffer, key)
            except ValueError as exc:
                print(exc)
                return
            print(f"Plain buffer = \"{self.plain_buffer}\"")

        elif method == "rsa":
            if len(args) < 3:
                print("Usage: /decode rsa <priv> <mod>")
                return
            try:
                priv = int(args[1])
                mod = int(args[2])
            except ValueError:
                print("priv et mod doivent être des entiers.")
                return
            if not self.encoded_buffer:
                print("Encoded buffer est vide.")
                return
            if not isinstance(self.encoded_buffer, list):
                print("Encoded buffer n'est pas au format RSA (liste d'entiers). Encodez d'abord avec /encode rsa.")
                return
            self.plain_buffer = self.cmd.decode_rsa(self.encoded_buffer, priv, mod)
            print(f"Plain buffer = \"{self.plain_buffer}\"")

        else:
            print("Méthode inconnue. Utilisez: isc, shift, vigenere, rsa")

    def _cmd_decode_isc(self, args):
        if args:
            raw_hex_message = " ".join(args)
            self.encoded_buffer = raw_hex_message
        else:
            if not self.encoded_buffer:
                print("Usage: /decode isc [hex_message]")
                return
            if isinstance(self.encoded_buffer, list):
                print("Encoded buffer n'est pas une trame ISC hexadecimale.")
                return
            raw_hex_message = self.encoded_buffer

        try:
            decoded_message = self.handler.parse_hex_message(raw_hex_message)
        except (TypeError, ValueError, UnicodeDecodeError) as exc:
            print(f"Impossible de decoder la trame ISC: {exc}")
            if str(exc).startswith("En-tete ISC invalide"):
                example_hex_message = self.handler.build_message("s", "Hi").hex().upper()
                print(f"Exemple de trame ISC valide : {example_hex_message}")
                print(f"Exemple de commande         : /decode isc {example_hex_message}")
            return

        self.last_decoded_isc = decoded_message
        self.plain_buffer = decoded_message.text
        print("Message ISC decode:")
        print(f"  Type     : {decoded_message.msg_type}")
        print(f"  Longueur : {decoded_message.char_count}")
        print(f"  Texte    : {decoded_message.text}")
        print(f"Plain buffer = \"{self.plain_buffer}\"")

    # --- RSA ---

    def _cmd_rsa(self, args):
        if not args or args[0].lower() != "generate":
            print("Usage: /rsa generate")
            return
        pub, priv, mod = self.cmd.rsa_generate()
        print(f"RSA Keys generated:")
        print(f"  Public Key  (e, n) = ({pub}, {mod})")
        print(f"  Private Key (d, n) = ({priv}, {mod})")

    # --- Hash ---

    def _cmd_hash(self):
        if not self.plain_buffer:
            print("Plain buffer est vide. Utilisez /set plain <text>")
            return
        h = self.cmd.sha256(self.plain_buffer)
        print(f"SHA-256: {h}")

    # --- Diffie-Hellman ---

    def _cmd_dh(self, args):
        if not args:
            print("Usage: /dh generate [max_mod] | /dh halfkey <mod> <gen> [priv_a] | /dh secret <mod> <gen> <priv_a> <gB>")
            return
        sub = args[0].lower()

        if sub == "generate":
            max_mod = None
            if len(args) > 1:
                try:
                    max_mod = int(args[1])
                except ValueError:
                    print("max_mod doit être un entier.")
                    return
            p, g = self.cmd.dh_generate(max_mod)
            print(f"DH Parameters:")
            print(f"  Modulus (p) = {p}")
            print(f"  Generator (g) = {g}")

        elif sub == "halfkey":
            if len(args) < 3:
                print("Usage: /dh halfkey <mod> <gen> [priv_a]")
                return
            try:
                mod = int(args[1])
                gen = int(args[2])
                priv_a = int(args[3]) if len(args) > 3 else None
            except ValueError:
                print("Les paramètres doivent être des entiers.")
                return
            half_key, priv_a = self.cmd.dh_halfkey(mod, gen, priv_a)
            print(f"DH Half Key:")
            print(f"  A (half key) = {half_key}")
            print(f"  a (private)  = {priv_a}")
            
        elif sub == "secret":
            if len(args) < 5:
                print("Usage: /dh secret <mod> <gen> <priv_a> <gB>")
                return
            try:
                mod = int(args[1])
                gen = int(args[2])
                priv_a = int(args[3])
                gB = int(args[4])
            except ValueError:
                print("Les paramètres doivent être des entiers.")
                return
            secret = self.cmd.dh_secret(mod, gen, priv_a, gB)
            print(f"DH Shared Secret = {secret}")

        else:
            print("Usage: /dh generate | /dh halfkey | /dh secret")
#resolution probleme cli 
if __name__ == "__main__":
    cli = CLI()
    cli.run()

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