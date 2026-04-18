from DiffieHellman import DiffieHellman


class DhCmds:
    def __init__(self, cmd=None):
        self._dh = DiffieHellman()

    def cmd_dh(self, args):
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
            p, g = self._dh.generate(max_mod)
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
            half_key, priv_a = self._dh.halfkey(mod, gen, priv_a)
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
            secret = self._dh.secret(mod, gen, priv_a, gB)
            print(f"DH Shared Secret = {secret}")

        else:
            print("Usage: /dh generate | /dh halfkey | /dh secret")