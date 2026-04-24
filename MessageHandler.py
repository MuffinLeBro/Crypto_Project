import struct
from dataclasses import dataclass


@dataclass(frozen=True)
class ISCMessage:
    msg_type: str
    text: str
    char_count: int
    raw_bytes: bytes

class MessageHandler:
    def __init__(self, bytesPerChar=4):
        self.header = b'ISC'
        self.bytesPerChar = bytesPerChar
        self.binaryMessage = b''

    def _format_hex_prefix(self, raw_bytes, length):
        prefix = raw_bytes[:length].hex().upper()
        return prefix or "(vide)"

    def _read_header(self, raw_bytes):
        header = raw_bytes[0:3]
        if header != self.header:
            raise ValueError(
                "En-tete ISC invalide: "
                f"attendu {self.header.hex().upper()} ('ISC') au debut de la trame, "
                f"recu {self._format_hex_prefix(raw_bytes, 3)}."
            )
        return header

    def _read_type(self, raw_bytes):
        try:
            return raw_bytes[3:4].decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError("Type de message ISC invalide.") from exc

    def _read_length(self, raw_bytes):
        return struct.unpack('>H', raw_bytes[4:6])[0]

    def _extract_text(self, body_bytes, char_count):
        expected_body_length = char_count * self.bytesPerChar
        if len(body_bytes) != expected_body_length:
            raise ValueError(
                "Longueur du corps ISC invalide: "
                f"{len(body_bytes)} octets recus, {expected_body_length} attendus."
            )

        message = ""
        for index in range(char_count):
            start = index * self.bytesPerChar
            end = start + self.bytesPerChar
            char_block = body_bytes[start:end]
            message += self._decode_char_block(char_block)
        return message

    def build_message(self, msg_type, text):
        if not isinstance(text, str):
            raise TypeError("Le texte ISC doit etre une chaine.")
        if not isinstance(msg_type, str) or len(msg_type) != 1:
            raise ValueError("Le type ISC doit contenir exactement un caractere.")

        typeByte = msg_type.encode('utf-8')

        nChar = len(text)
        lengthByte = struct.pack('>H', nChar)
        bodyBytes = text.encode("utf-32-be")

        return self.header + typeByte + lengthByte + bodyBytes

    def add_data(self, msg_type, text):
        self.binaryMessage = self.build_message(msg_type, text)

    def get_message(self):
        return self.binaryMessage

    def _decode_char_block(self, char_block):
        charBytes = char_block.lstrip(b'\x00')
        if not charBytes:
            return ""
        return charBytes.decode('utf-8')

    def parse_message(self, raw_bytes):
        if isinstance(raw_bytes, bytearray):
            raw_bytes = bytes(raw_bytes)
        if not isinstance(raw_bytes, bytes):
            raise TypeError("Une trame ISC doit etre fournie en octets.")
        if len(raw_bytes) < 6:
            raise ValueError("Trame ISC trop courte.")

        self._read_header(raw_bytes)
        msg_type = self._read_type(raw_bytes)
        n_chars = self._read_length(raw_bytes)
        body_bytes = raw_bytes[6:]
        message = self._extract_text(body_bytes, n_chars)

        return ISCMessage(
            msg_type=msg_type,
            text=message,
            char_count=n_chars,
            raw_bytes=raw_bytes,
        )

    def parse_hex_message(self, raw_hex_message):
        if not isinstance(raw_hex_message, str):
            raise TypeError("La trame ISC hexadecimale doit etre une chaine.")

        normalized_hex = raw_hex_message.replace('0x', ' ').replace('0X', ' ')
        normalized_hex = "".join(normalized_hex.split())
        if not normalized_hex:
            raise ValueError("Aucune trame ISC a decoder.")

        try:
            raw_bytes = bytes.fromhex(normalized_hex)
        except ValueError as exc:
            raise ValueError("La trame ISC doit etre une chaine hexadecimale valide.") from exc

        return self.parse_message(raw_bytes)
    
    def decode_message(self, raw_bytes):
        try:
            decoded_message = self.parse_message(raw_bytes)
        except (TypeError, ValueError, UnicodeDecodeError):
            return None, None

        return decoded_message.msg_type, decoded_message.text