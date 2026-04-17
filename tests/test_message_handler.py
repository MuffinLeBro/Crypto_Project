import unittest

from MessageHandler import MessageHandler


class MessageHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.handler = MessageHandler()

    def test_parse_hex_message_decodes_valid_isc_frame(self):
        decoded_message = self.handler.parse_hex_message("4953437300020000004800000069")

        self.assertEqual(decoded_message.msg_type, "s")
        self.assertEqual(decoded_message.char_count, 2)
        self.assertEqual(decoded_message.text, "Hi")

    def test_parse_hex_message_invalid_header_shows_expected_prefix(self):
        with self.assertRaisesRegex(
            ValueError,
            r"attendu 495343 \('ISC'\) au debut de la trame, recu 010203",
        ):
            self.handler.parse_hex_message("0102030405060708")


if __name__ == "__main__":
    unittest.main()