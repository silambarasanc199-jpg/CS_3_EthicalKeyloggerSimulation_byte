
import tkinter as tk
from pathlib import Path

from crypto_utils import encrypt_log, best_effort_secure_delete


PROJECT_DIR = Path(__file__).parent
LOG_DIR = PROJECT_DIR / "logs"

PLAINTEXT_LOG = LOG_DIR / "keystrokes.txt"
ENCRYPTED_LOG = LOG_DIR / "keystrokes.enc"

ABORT_SEQUENCE = "ABORT"


class EthicalKeyloggerSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Ghost Protocol - Ethical Keylogger Simulator")
        self.root.geometry("650x450")

        self.captured_keys = []
        self.abort_buffer = ""

        self.build_interface()

        # Capture keys ONLY inside this application's window.
        self.root.bind("<KeyPress>", self.handle_keypress)

    def build_interface(self):
        title = tk.Label(
            self.root,
            text="GHOST PROTOCOL",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=15)

        warning = tk.Label(
            self.root,
            text=(
                "AUTHORIZED LOCAL SIMULATION ONLY\n"
                "Keystrokes are captured only while this application is active."
            ),
            font=("Arial", 11),
            justify="center"
        )
        warning.pack(pady=10)

        self.status = tk.Label(
            self.root,
            text="Status: READY",
            font=("Arial", 12, "bold")
        )
        self.status.pack(pady=10)

        self.display = tk.Text(
            self.root,
            height=10,
            width=65
        )
        self.display.pack(padx=20, pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        encrypt_button = tk.Button(
            button_frame,
            text="Encrypt Log",
            command=self.encrypt_current_log,
            width=15
        )
        encrypt_button.pack(side="left", padx=5)

        purge_button = tk.Button(
            button_frame,
            text="Purge Logs",
            command=self.purge_logs,
            width=15
        )
        purge_button.pack(side="left", padx=5)

        close_button = tk.Button(
            button_frame,
            text="Close",
            command=self.root.destroy,
            width=15
        )
        close_button.pack(side="left", padx=5)

    def handle_keypress(self, event):
        """Handle only key events received by this application."""

        key = event.char

        if not key:
            return

        self.captured_keys.append(key)

        self.display.insert(tk.END, key)
        self.display.see(tk.END)

        # Track characters for the ABORT kill-switch.
        self.abort_buffer = (self.abort_buffer + key.upper())[-len(ABORT_SEQUENCE):]

        if self.abort_buffer == ABORT_SEQUENCE:
            self.panic_shutdown()

    def write_plaintext_log(self):
        LOG_DIR.mkdir(exist_ok=True)

        data = "".join(self.captured_keys)

        PLAINTEXT_LOG.write_text(
            data,
            encoding="utf-8"
        )

    def encrypt_current_log(self):
        if not self.captured_keys:
            self.status.config(text="Status: No data to encrypt")
            return

        self.write_plaintext_log()

        encrypt_log(
            PLAINTEXT_LOG,
            ENCRYPTED_LOG
        )

        best_effort_secure_delete(PLAINTEXT_LOG)

        self.status.config(
            text="Status: Log encrypted and plaintext removed"
        )

    def purge_logs(self):
        if PLAINTEXT_LOG.exists():
            best_effort_secure_delete(PLAINTEXT_LOG)

        if ENCRYPTED_LOG.exists():
            ENCRYPTED_LOG.unlink()

        self.captured_keys.clear()
        self.abort_buffer = ""

        self.display.delete("1.0", tk.END)

        self.status.config(
            text="Status: Logs purged"
        )

    def panic_shutdown(self):
        """ABORT sequence: encrypt, remove plaintext, and exit."""

        self.status.config(
            text="Status: ABORT detected — shutting down"
        )

        if self.captured_keys:
            self.write_plaintext_log()

            encrypt_log(
                PLAINTEXT_LOG,
                ENCRYPTED_LOG
            )

            best_effort_secure_delete(PLAINTEXT_LOG)

        self.root.after(500, self.root.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    app = EthicalKeyloggerSimulator(root)
    root.mainloop()
