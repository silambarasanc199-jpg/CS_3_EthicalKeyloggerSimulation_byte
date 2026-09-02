
import tempfile
import unittest
from pathlib import Path

from crypto_utils import (
    encrypt_log,
    decrypt_log,
    best_effort_secure_delete
)


class TestEthicalKeylogger(unittest.TestCase):

    def test_encryption_and_decryption(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)

            original = folder / "original.txt"
            encrypted = folder / "encrypted.enc"
            decrypted = folder / "decrypted.txt"

            original.write_text(
                "AUTHORIZED TEST DATA",
                encoding="utf-8"
            )

            encrypt_log(original, encrypted)

            self.assertTrue(encrypted.exists())

            decrypt_log(encrypted, decrypted)

            self.assertEqual(
                decrypted.read_text(encoding="utf-8"),
                "AUTHORIZED TEST DATA"
            )

    def test_plaintext_cleanup(self):
        with tempfile.TemporaryDirectory() as temp:
            file = Path(temp) / "test.txt"

            file.write_text(
                "TEMPORARY AUTHORIZED DATA",
                encoding="utf-8"
            )

            best_effort_secure_delete(file)

            self.assertFalse(file.exists())


if __name__ == "__main__":
    unittest.main()
