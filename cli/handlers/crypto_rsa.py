class RsaCmds:
    def __init__(self, cmd, buffers=None):
        self._cmd = cmd
        self._buffers = buffers

    def cmd_rsa(self, args):
        if not args or args[0].lower() != "generate":
            print("Usage: /rsa generate")
            return
        pub, priv, mod = self._cmd.rsa_generate()
        print(f"RSA Keys generated:")
        print(f"  Public Key  (e, n) = ({pub}, {mod})")
        print(f"  Private Key (d, n) = ({priv}, {mod})")

    def encode(self, args):
        if len(args) < 2:
            print("Usage: /encode rsa <pub> <mod>")
            return
        try:
            pub = int(args[0])
            mod = int(args[1])
        except ValueError:
            print("pub et mod doivent être des entiers.")
            return
        if not self._buffers.plain:
            print("Plain buffer est vide. Utilisez /set plain <text>")
            return
        self._buffers.encoded = self._cmd.encode_rsa(self._buffers.plain, pub, mod)
        print(f"Encoded buffer = {self._buffers.encoded}")

    def decode(self, args):
        if len(args) < 2:
            print("Usage: /decode rsa <priv> <mod>")
            return
        try:
            priv = int(args[0])
            mod = int(args[1])
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