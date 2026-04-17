ADDRSERVER = "vlbelintrocrypto.hevs.ch"
PORT = 6000

BANNER = """
================================================
            AVAILABLE COMMANDS
================================================
/help                       - Show this message
/health                     - Check server connection
/quit, /exit                - Disconnect and exit
/send <text>|plain|encoded [-s] - Send text or buffer
/clear                      - Clear the screen
/clearbuf [plain|encoded]   - Clear buffers
/set <plain|encoded> <text> - Set buffer
/show                       - Show current buffers
/list [n]                   - Show last n messages (default 10)
/select <i> [e|c]           - Select message for encoded/plain buffer
/encode shift <k>           - Encode plain buffer with shift
/decode shift <k>           - Decode encoded buffer with shift

/decode isc [hex_message]   - Decode ISC frame from hex or encoded buffer
/encode vigenere <key>
/decode vigenere <key>
/encode rsa <pub> <mod>
/decode rsa <priv> <mod>
/rsa generate               - Generate RSA keys
/hash                       - SHA-256 of plain buffer
/dh generate [max_mod]
/dh halfkey <mod> <gen> [priv_a]
/dh secret <mod> <gen> <priv_a> <gB>
<text>                      - Send clear message to other clients
================================================
"""