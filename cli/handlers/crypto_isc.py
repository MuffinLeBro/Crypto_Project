class IscCmds:
    def __init__(self, buffers, handler):
        self._buffers = buffers
        self._handler = handler

    def decode(self, args):
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
