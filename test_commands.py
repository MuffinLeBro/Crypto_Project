from Command import Command
from MessageHandler import MessageHandler
from DiffieHellman import DiffieHellman
from cli.buffers import CLIBuffers
from cli.handlers.crypto_shift import ShiftCmds
from cli.handlers.crypto_vigenere import VigenereCmds
from cli.handlers.crypto_rsa import RsaCmds
from cli.handlers.crypto_isc import IscCmds
from cli.handlers.crypto_hash import HashCmds
from cli.handlers.crypto_dh import DhCmds
from cli.handlers.buffer_cmds import BufferCommands

cmd = Command()
handler = MessageHandler()
buffers = CLIBuffers()

shift    = ShiftCmds(cmd, buffers)
vigenere = VigenereCmds(cmd, buffers)
rsa      = RsaCmds(cmd, buffers)
isc      = IscCmds(buffers, handler)
hash_cmd = HashCmds(cmd, buffers)
dh_cmd   = DhCmds()
buf_cmd  = BufferCommands(buffers)

sep = lambda title: print(f"\n{'='*48}\n{title}\n{'='*48}")

sep("/set plain HelloWorld")
buf_cmd.cmd_set(["plain", "HelloWorld"])

sep("/show")
buf_cmd.cmd_show()

sep("/encode shift 3")
shift.encode(["3"])

sep("/decode shift 3")
shift.decode(["3"])

sep("/set plain HelloWorld  (reset)")
buf_cmd.cmd_set(["plain", "HelloWorld"])

sep("/encode vigenere KEY")
vigenere.encode(["KEY"])

sep("/decode vigenere KEY")
vigenere.decode(["KEY"])

sep("/hash")
buf_cmd.cmd_set(["plain", "HelloWorld"])
hash_cmd.cmd_hash()

sep("/rsa generate")
rsa_only = RsaCmds(cmd)
rsa_only.cmd_rsa(["generate"])

sep("/encode rsa 17 851  +  /decode rsa 413 851")
buf_cmd.cmd_set(["plain", "Hi"])
rsa.encode(["17", "851"])
rsa.decode(["413", "851"])

sep("/decode isc 4953437300020000004800000069")
isc.decode(["4953437300020000004800000069"])

sep("/dh generate 100")
dh_cmd.cmd_dh(["generate", "100"])

sep("/dh halfkey 97 5")
dh_cmd.cmd_dh(["halfkey", "97", "5"])

sep("/dh secret 97 5 2 23")
dh_cmd.cmd_dh(["secret", "97", "5", "2", "23"])

sep("/clearbuf plain")
buf_cmd.cmd_clearbuf(["plain"])
buf_cmd.cmd_show()

sep("/clearbuf encoded")
buf_cmd.cmd_clearbuf(["encoded"])
buf_cmd.cmd_show()

print("\n\nTOUS LES TESTS OK")
