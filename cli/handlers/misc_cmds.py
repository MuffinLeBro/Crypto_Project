class MiscCmds:
    def __init__(self, client, cmd, buffers, history, send_fn):
        self._client  = client
        self._cmd     = cmd
        self._buffers = buffers
        self._history = history
        self._send    = send_fn   # référence vers CLI.send_to_server

    def cmd_send(self, args):
        if not args:
            print("Usage: /send <text>|plain|encoded [-s]")
            return
        silent = "-s" in args
        send_args = [a for a in args if a != "-s"]
        keyword = send_args[0] if send_args else ""
        if keyword == "plain":
            if not self._buffers.plain:
                print("Plain buffer est vide.")
                return
            self._send("s", self._buffers.plain, silent)
        elif keyword == "encoded":
            if not self._buffers.encoded:
                print("Encoded buffer est vide.")
                return
            self._send("s", self._buffers.encoded, silent)
        else:
            self._send("s", " ".join(send_args), silent)

    def cmd_health(self):
        if self._client.health():
            print("Connexion au serveur : OK")
        else:
            print("Connexion au serveur : PERDUE")

    def cmd_list(self, args):
        n = 10
        if args:
            try:
                n = int(args[0])
            except ValueError:
                print("Usage: /list [n]")
                return
        recent = self._history.get_last(n)
        if not recent:
            print("Aucun message.")
            return
        start_idx = max(0, len(self._history) - n)
        for i, (direction, msg_type, text) in enumerate(recent):
            arrow = "<-" if direction == "recv" else "->"
            print(f"  [{start_idx + i}] {arrow} ({msg_type}) {text}")

    def cmd_select(self, args):
        if not args:
            print("Usage: /select <i> [e|c]")
            return
        try:
            idx = int(args[0])
        except ValueError:
            print("Usage: /select <i> [e|c]")
            return
        entry = self._history.get(idx)
        if entry is None:
            print(f"Index invalide. Messages disponibles : 0-{len(self._history) - 1}")
            return
        _, _, text = entry
        target = args[1].lower() if len(args) > 1 else "c"
        if target == "e":
            self._buffers.encoded = text
            print(f"Encoded buffer = \"{text}\"")
        else:
            self._buffers.plain = text
            print(f"Plain buffer = \"{text}\"")