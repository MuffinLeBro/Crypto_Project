import os

from Command import Command
from Client import Client
from MessageHandler import MessageHandler

from cli.constants import ADDRSERVER, PORT, BANNER
from cli.buffers import CLIBuffers
from cli.history import CLIHistory
from cli.handlers.buffer_cmds import BufferCommands
from cli.handlers.crypto_cmds import CryptoCmds
from cli.handlers.crypto_rsa import RsaCmds
from cli.handlers.crypto_dh import DhCmds
from cli.handlers.misc_cmds import MiscCmds


class CLI:
    def __init__(self):
        self.client = Client()
        self.handler = MessageHandler()
        self.cmd = Command()
        self.buffers = CLIBuffers()
        self.history = CLIHistory()
        self.last_decoded_isc = None

        self._buf    = BufferCommands(self.buffers)
        self._crypto = CryptoCmds(self.cmd, self.buffers, self.handler)
        self._rsa    = RsaCmds(self.cmd)
        self._dh     = DhCmds(self.cmd)
        self._misc   = MiscCmds(self.client, self.cmd, self.buffers, self.history, self.send_to_server)

    def show_banner(self):
        print(BANNER)
        print("Type a message and press ENTER to send.")
        print("Type /help to see available commands.\n")

    def on_message_received(self, raw_data):
        try:
            decoded_message = self.handler.parse_message(raw_data)
        except (TypeError, ValueError, UnicodeDecodeError) as exc:
            print(f"\n[Serveur] Trame ISC invalide: {exc}")
            print("> ", end="", flush=True)
            return

        self.last_decoded_isc = decoded_message
        self.history.append("recv", decoded_message.msg_type, decoded_message.text)
        print(f"\n[Serveur] ({decoded_message.msg_type}): {decoded_message.text}")
        print("> ", end="", flush=True)

    def send_to_server(self, msg_type, text, silent=False):
        try:
            payload = self.handler.build_message(msg_type, text)
        except (TypeError, ValueError) as exc:
            print(f"Impossible d'encoder la trame ISC: {exc}")
            return

        self.client.send(payload)
        self.history.append("sent", msg_type, text)
        if not silent:
            print(f"Message envoyé: {text}")

    def run(self):
        self.client.connect(ADDRSERVER, PORT)
        if not self.client.connected:
            print("Impossible de se connecter au serveur. Arrêt.")
            return

        self.client.start_receiving(self.on_message_received)
        self.show_banner()

        try:
            while self.client.running:
                try:
                    user_input = input("> ")
                except EOFError:
                    break

                if not user_input.strip():
                    continue

                if user_input.startswith("/"):
                    self.handle_command(user_input.strip())
                else:
                    self.send_to_server("s", user_input)
        except KeyboardInterrupt:
            print("\nInterruption.")
        finally:
            self.client.close()

    def handle_command(self, input_str):
        parts = input_str.split()
        command = parts[0].lower()
        args = parts[1:]

        if command == "/help":
            print(BANNER)

        elif command in ("/quit", "/exit"):
            print("Déconnexion...")
            self.client.running = False

        elif command == "/clear":
            os.system("clear" if os.name != "nt" else "cls")

        elif command == "/health":
            self._misc.cmd_health()

        elif command == "/clearbuf":
            self._buf.cmd_clearbuf(args)

        elif command == "/set":
            self._buf.cmd_set(args)

        elif command == "/show":
            self._buf.cmd_show()

        elif command == "/list":
            self._misc.cmd_list(args)

        elif command == "/select":
            self._misc.cmd_select(args)

        elif command == "/send":
            self._misc.cmd_send(args)

        elif command == "/encode":
            self._crypto.cmd_encode(args)

        elif command == "/decode":
            self._crypto.cmd_decode(args)

        elif command == "/rsa":
            self._rsa.cmd_rsa(args)

        elif command == "/hash":
            self._misc.cmd_hash()

        elif command == "/dh":
            self._dh.cmd_dh(args)

        else:
            print(f"Commande inconnue : {command}. Tapez /help pour l'aide.")