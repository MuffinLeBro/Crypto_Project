from cli.handlers.crypto_shift import ShiftCmds
from cli.handlers.crypto_vigenere import VigenereCmds
from cli.handlers.crypto_rsa import RsaCmds
from cli.handlers.crypto_isc import IscCmds


class CryptoCmds:
    def __init__(self, cmd, buffers, handler):
        self._shift    = ShiftCmds(cmd, buffers)
        self._vigenere = VigenereCmds(cmd, buffers)
        self._rsa      = RsaCmds(cmd, buffers)
        self._isc      = IscCmds(buffers, handler)

    def cmd_encode(self, args):
        if not args:
            print("Usage: /encode shift <k> | /encode vigenere <key> | /encode rsa <pub> <mod>")
            return
        method = args[0].lower()
        rest = args[1:]

        if method == "shift":
            self._shift.encode(rest)
        elif method == "vigenere":
            self._vigenere.encode(rest)
        elif method == "rsa":
            self._rsa.encode(rest)
        else:
            print("Méthode inconnue. Utilisez: shift, vigenere, rsa")

    def cmd_decode(self, args):
        if not args:
            print("Usage: /decode shift <k> | /decode isc [hex_message] | /decode vigenere <key> | /decode rsa <priv> <mod>")
            return
        method = args[0].lower()
        rest = args[1:]

        if method == "isc":
            self._isc.decode(rest)
        elif method == "shift":
            self._shift.decode(rest)
        elif method == "vigenere":
            self._vigenere.decode(rest)
        elif method == "rsa":
            self._rsa.decode(rest)
        else:
            print("Méthode inconnue. Utilisez: isc, shift, vigenere, rsa")