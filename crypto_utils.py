
from pathlib import Path
from cryptography.fernet import Fernet

KEY_FILE = Path("secret.key")


def get_or_create_key():
    """Create an encryption key if one does not already exist."""
    if KEY_FILE.exists():
        return KEY_FILE.read_bytes()

    key = Fernet.generate_key()
    KEY_FILE.write_bytes(key)
    return key


def encrypt_log(input_file, output_file):
    """Encrypt a local log file using Fernet encryption."""
    key = get_or_create_key()
    cipher = Fernet(key)

    data = Path(input_file).read_bytes()
    encrypted = cipher.encrypt(data)

    Path(output_file).write_bytes(encrypted)


def decrypt_log(encrypted_file, output_file):
    """Decrypt an encrypted log file."""
    key = get_or_create_key()
    cipher = Fernet(key)

    encrypted = Path(encrypted_file).read_bytes()
    decrypted = cipher.decrypt(encrypted)

    Path(output_file).write_bytes(decrypted)


def best_effort_secure_delete(file_path):
    """
    Best-effort plaintext cleanup:
    overwrite with zeros, then remove the file.

    Note:
    This is not guaranteed forensic erasure on SSDs,
    journaling filesystems, or cloud storage.
    """
    path = Path(file_path)

    if path.exists():
        size = path.stat().st_size

        if size > 0:
            path.write_bytes(b"\x00" * size)

        path.unlink()
