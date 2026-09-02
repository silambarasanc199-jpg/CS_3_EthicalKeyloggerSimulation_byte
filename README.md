
# Ghost Protocol — Ethical Keylogger Simulation

## AVIP 2026 CyberSecurity — Task 3

A safe, application-local keylogger simulation demonstrating:

- Local key-event capture
- `ABORT` kill-switch detection
- Fernet-based encryption
- Plaintext log cleanup
- Automated security tests
- Explicit consent and authorized-use controls

---

## ⚠️ Ethics & Consent

This project is designed strictly for **authorized educational testing**.

The simulator:

- Captures keystrokes only while its own application window is active.
- Does NOT install a global keyboard hook.
- Does NOT monitor other applications.
- Does NOT attempt to hide its process.
- Does NOT collect credentials intentionally.
- Does NOT bypass operating-system security controls.
- Does NOT transmit captured data to a remote server.

Use is limited to:

1. The developer's own device, or
2. A device for which the developer has explicit permission from the owner.

Unauthorized monitoring of another person's keystrokes is prohibited.

---

## Kill-Switch

The simulator recognizes the sequence:

`ABORT`

When the sequence is detected:

1. The current local simulation log is written.
2. The log is encrypted.
3. The plaintext log is removed.
4. The application shuts down.

The kill-switch is intentionally implemented as a safety mechanism.

---

## Secure Storage

Simulation logs are encrypted using the Python `cryptography`
library and Fernet authenticated encryption.

Plaintext logs are removed after encryption.

The project uses best-effort plaintext cleanup. File overwriting
followed by deletion is **not guaranteed forensic erasure**, especially
on SSDs, journaling filesystems, or cloud-backed storage.

---

## Data Handling

This project is intentionally local-only.

No keystroke data is uploaded to a server or third-party service.

Sample data used in demonstrations is synthetic and contains no
real passwords, credentials, or private information.

---

## Testing

Automated tests verify:

- Encryption and decryption
- Plaintext cleanup

Run:

```bash
python test_keylogger.py
