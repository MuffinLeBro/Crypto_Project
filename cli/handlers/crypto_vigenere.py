class VigenereCmds:
    def __init__(self, cmd, buffers):
        self._cmd = cmd
        self._buffers = buffers

    def encode(self, args):
        if len(args) < 1:
            print("Usage: /encode vigenere <key>")
            return
        key = args[0]
        if not self._buffers.plain:
            print("Plain buffer est vide. Utilisez /set plain <text>")
            return
        try:
            self._buffers.encoded = self._cmd.encode_vigenere(self._buffers.plain, key)
        except ValueError as exc:
            print(exc)
            return
        print(f"Encoded buffer = \"{self._buffers.encoded}\"")

    def decode(self, args):
        if len(args) < 1:
            print("Usage: /decode vigenere <key>")
            return
        key = args[0]
        if not self._buffers.encoded:
            print("Encoded buffer est vide.")
            return
        try:
            self._buffers.plain = self._cmd.decode_vigenere(self._buffers.encoded, key)
        except ValueError as exc:
            print(exc)
            return
        print(f"Plain buffer = \"{self._buffers.plain}\"")
