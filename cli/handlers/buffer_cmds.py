from cli.buffers import CLIBuffers


class BufferCommands:
    def __init__(self, buffers: CLIBuffers):
        self._buffers = buffers

    def cmd_clearbuf(self, args):
        if not args:
            self._buffers.plain = ""
            self._buffers.encoded = ""
            print("Buffers vidés.")
        elif args[0] == "plain":
            self._buffers.plain = ""
            print("Plain buffer vidé.")
        elif args[0] == "encoded":
            self._buffers.encoded = ""
            print("Encoded buffer vidé.")
        else:
            print("Usage: /clearbuf [plain|encoded]")

    def cmd_set(self, args):
        if len(args) < 2:
            print("Usage: /set <plain|encoded> <text>")
            return
        buf_type = args[0]
        text = " ".join(args[1:])
        if buf_type == "plain":
            self._buffers.plain = text
            print(f"Plain buffer = \"{self._buffers.plain}\"")
        elif buf_type == "encoded":
            self._buffers.encoded = text
            print(f"Encoded buffer = \"{self._buffers.encoded}\"")
        else:
            print("Usage: /set <plain|encoded> <text>")

    def cmd_show(self):
        print(f"Plain buffer   : \"{self._buffers.plain}\"")
        if isinstance(self._buffers.encoded, list):
            print(f"Encoded buffer : {self._buffers.encoded}  (RSA int list)")
        else:
            print(f"Encoded buffer : \"{self._buffers.encoded}\"")