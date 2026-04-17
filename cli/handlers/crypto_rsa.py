class RsaCmds:
    def __init__(self, cmd):
        self._cmd = cmd

    def cmd_rsa(self, args):
        if not args or args[0].lower() != "generate":
            print("Usage: /rsa generate")
            return
        pub, priv, mod = self._cmd.rsa_generate()
        print(f"RSA Keys generated:")
        print(f"  Public Key  (e, n) = ({pub}, {mod})")
        print(f"  Private Key (d, n) = ({priv}, {mod})")