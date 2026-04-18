class ShiftCmds:
    def __init__(self, cmd, buffers):
        self._cmd = cmd
        self._buffers = buffers

    def encode(self, args):
        if len(args) < 1:
            print("Usage: /encode shift <k>")
            return
        try:
            k = int(args[0])
        except ValueError:
            print("La clé doit être un entier.")
            return
        if not self._buffers.plain:
            print("Plain buffer est vide. Utilisez /set plain <text>")
            return
        self._buffers.encoded = self._cmd.encode_shift(self._buffers.plain, k)
        print(f"Encoded buffer = \"{self._buffers.encoded}\"")

    def decode(self, args):
        if len(args) < 1:
            print("Usage: /decode shift <k>")
            return
        try:
            k = int(args[0])
        except ValueError:
            print("La clé doit être un entier.")
            return
        if not self._buffers.encoded:
            print("Encoded buffer est vide.")
            return
        self._buffers.plain = self._cmd.decode_shift(self._buffers.encoded, k)
        print(f"Plain buffer = \"{self._buffers.plain}\"")
