class HashCmds:
    def __init__(self, cmd, buffers):
        self._cmd = cmd
        self._buffers = buffers

    def cmd_hash(self):
        if not self._buffers.plain:
            print("Plain buffer est vide. Utilisez /set plain <text>")
            return
        self._buffers.encoded = self._cmd.sha256(self._buffers.plain)
        print(f"SHA-256: {self._buffers.encoded}")
        print(f"Encoded buffer = \"{self._buffers.encoded}\"")
