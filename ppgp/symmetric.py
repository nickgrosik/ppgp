from pathlib import Path
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt_file_aesgcm(input_path, output_path, key):
    """Encrypt a file with AES-GCM and write nonce + ciphertext."""
    in_path = Path(input_path)
    out_path = Path(output_path)

    if not in_path.exists():
        print(f"[PPGP] Input file not found: {in_path}")
        raise FileNotFoundError(f"Input file not found: {in_path}")

    if len(key) not in (16, 24, 32):
        raise ValueError("AES key must be 16, 24, or 32 bytes long.")

    data = in_path.read_bytes()
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, data, None)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(nonce + ciphertext)

    print(f"[PPGP] AES-GCM encryption complete: {out_path}")
    return out_path


def decrypt_file_aesgcm(input_path, output_path, key):
    """Decrypt a file containing nonce + ciphertext produced by encrypt_file_aesgcm."""
    in_path = Path(input_path)
    out_path = Path(output_path)

    if not in_path.exists():
        print(f"[PPGP] Input file not found: {in_path}")
        raise FileNotFoundError(f"Input file not found: {in_path}")

    if len(key) not in (16, 24, 32):
        raise ValueError("AES key must be 16, 24, or 32 bytes long.")

    blob = in_path.read_bytes()
    if len(blob) < 13:
        raise ValueError("Ciphertext file is too short to contain nonce + data.")

    nonce = blob[:12]
    ciphertext = blob[12:]

    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(plaintext)

    print(f"[PPGP] AES-GCM decryption complete: {out_path}")
    return out_path


if __name__ == "__main__":
    sample_input = Path("encrypted/demo_plaintext.txt")
    encrypted_output = Path("encrypted/demo_plaintext.aesgcm")
    decrypted_output = Path("encrypted/demo_plaintext.decrypted.txt")

    sample_input.parent.mkdir(parents=True, exist_ok=True)
    sample_input.write_text("hello from ppgp aes-gcm demo\n", encoding="utf-8")

    demo_key = AESGCM.generate_key(bit_length=256)

    print("[PPGP Demo] Running AES-GCM encrypt/decrypt demo...")
    encrypt_file_aesgcm(sample_input, encrypted_output, demo_key)
    decrypt_file_aesgcm(encrypted_output, decrypted_output, demo_key)
    print("[PPGP Demo] AES-GCM demo complete.")
