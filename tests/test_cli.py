import io
import unittest
from contextlib import redirect_stdout

from CLI import CLI


class CLITestCase(unittest.TestCase):
    def test_decode_isc_invalid_header_prints_example(self):
        cli = CLI()
        self.addCleanup(cli.client.sock.close)
        output = io.StringIO()

        with redirect_stdout(output):
            cli._cmd_decode_isc(["0102030405060708"])

        rendered_output = output.getvalue()
        self.assertIn("Impossible de decoder la trame ISC:", rendered_output)
        self.assertIn("Exemple de trame ISC valide : 4953437300020000004800000069", rendered_output)
        self.assertIn("Exemple de commande         : /decode isc 4953437300020000004800000069", rendered_output)


if __name__ == "__main__":
    unittest.main()