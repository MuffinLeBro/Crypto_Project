class CryptoCmds:
    def __init__(self, cmd, buffers, handler):
        self._cmd = cmd
        self._buffers = buffers
        self._handler = handler

    def cmd_encode(self, args):
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
            if not self._buffers.plain:
                print("Plain buffer est vide. Utilisez /set plain <text>")
                return
            self._buffers.encoded = self._cmd.encode_shift(self._buffers.plain, k)
            print(f"Encoded buffer = \"{self._buffers.encoded}\"")

        elif method == "vigenere":
            if len(args) < 2:
                print("Usage: /encode vigenere <key>")
                return
            key = args[1]
            if not self._buffers.plain:
                print("Plain buffer est vide. Utilisez /set plain <text>")
                return
            try:
                self._buffers.encoded = self._cmd.encode_vigenere(self._buffers.plain, key)
            except ValueError as exc:
                print(exc)
                return
            print(f"Encoded buffer = \"{self._buffers.encoded}\"")

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
            if not self._buffers.plain:
                print("Plain buffer est vide. Utilisez /set plain <text>")
                return
            self._buffers.encoded = self._cmd.encode_rsa(self._buffers.plain, pub, mod)
            print(f"Encoded buffer = {self._buffers.encoded}")

        else:
            print("Méthode inconnue. Utilisez: shift, vigenere, rsa")

    def cmd_decode(self, args):
        if not args:
            print("Usage: /decode shift <k> | /decode isc [hex_message] | /decode vigenere <key> | /decode rsa <priv> <mod>")
            return
        method = args[0].lower()

        if method == "isc":
            self._decode_isc(args[1:])

        elif method == "shift":
            if len(args) < 2:
                print("Usage: /decode shift <k>")
                return
            try:
                k = int(args[1])
            except ValueError:
                print("La clé doit être un entier.")
                return
            if not self._buffers.encoded:
                print("Encoded buffer est vide.")
                return
            self._buffers.plain = self._cmd.decode_shift(self._buffers.encoded, k)
            print(f"Plain buffer = \"{self._buffers.plain}\"")

        elif method == "vigenere":
            if len(args) < 2:
                print("Usage: /decode vigenere <key>")
                return
            key = args[1]
            if not self._buffers.encoded:
                print("Encoded buffer est vide.")
                return
            try:
                self._buffers.plain = self._cmd.decode_vigenere(self._buffers.encoded, key)
            except ValueError as exc:
                print(exc)
                return
            print(f"Plain buffer = \"{self._buffers.plain}\"")

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
            if not self._buffers.encoded:
                print("Encoded buffer est vide.")
                return
            if not isinstance(self._buffers.encoded, list):
                print("Encoded buffer n'est pas au format RSA (liste d'entiers). Encodez d'abord avec /encode rsa.")
                return
            self._buffers.plain = self._cmd.decode_rsa(self._buffers.encoded, priv, mod)
            print(f"Plain buffer = \"{self._buffers.plain}\"")

        else:
            print("Méthode inconnue. Utilisez: isc, shift, vigenere, rsa")

    def _decode_isc(self, args):
        if args:
            raw_hex_message = " ".join(args)
            self._buffers.encoded = raw_hex_message
        else:
            if not self._buffers.encoded:
                print("Usage: /decode isc [hex_message]")
                return
            if isinstance(self._buffers.encoded, list):
                print("Encoded buffer n'est pas une trame ISC hexadecimale.")
                return
            raw_hex_message = self._buffers.encoded

        try:
            decoded_message = self._handler.parse_hex_message(raw_hex_message)
        except (TypeError, ValueError, UnicodeDecodeError) as exc:
            print(f"Impossible de decoder la trame ISC: {exc}")
            if str(exc).startswith("En-tete ISC invalide"):
                example_hex_message = self._handler.build_message("s", "Hi").hex().upper()
                print(f"Exemple de trame ISC valide : {example_hex_message}")
                print(f"Exemple de commande         : /decode isc {example_hex_message}")
            return

        self._buffers.plain = decoded_message.text
        print("Message ISC decode:")
        print(f"  Type     : {decoded_message.msg_type}")
        print(f"  Longueur : {decoded_message.char_count}")
        print(f"  Texte    : {decoded_message.text}")
        print(f"Plain buffer = \"{self._buffers.plain}\"")