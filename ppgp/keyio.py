from pathlib import Path
import getpass

from cryptography.hazmat.primitives import serialization


def export_private_key(key, filename, directory):
    """Export a private key to a PEM file using PKCS8 and no encryption."""
    directory_path = Path(directory)
    directory_path.mkdir(parents=True, exist_ok=True)

    output_path = directory_path / filename
    pem_bytes = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    with open(output_path, "wb") as f:
        f.write(pem_bytes)

    print(f"[PPGP] Private key exported to: {output_path}")
    return output_path


def export_public_key(key, filename, directory):
    """Export a public key to a PEM file using SubjectPublicKeyInfo."""
    directory_path = Path(directory)
    directory_path.mkdir(parents=True, exist_ok=True)

    output_path = directory_path / filename
    pem_bytes = key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    with open(output_path, "wb") as f:
        f.write(pem_bytes)

    print(f"[PPGP] Public key exported to: {output_path}")
    return output_path


def import_private_key(path):
    """Import a PEM-encoded private key with no password."""
    key_path = Path(path)
    if not key_path.exists():
        print(f"[PPGP] Private key file not found: {key_path}")
        raise FileNotFoundError(f"Private key file not found: {key_path}")

    with open(key_path, "rb") as f:
        key_data = f.read()

    key = serialization.load_pem_private_key(key_data, password=None)
    print(f"[PPGP] Private key imported from: {key_path}")
    return key


def import_public_key(path):
    """Import a PEM-encoded public key."""
    key_path = Path(path)
    if not key_path.exists():
        print(f"[PPGP] Public key file not found: {key_path}")
        raise FileNotFoundError(f"Public key file not found: {key_path}")

    with open(key_path, "rb") as f:
        key_data = f.read()

    key = serialization.load_pem_public_key(key_data)
    print(f"[PPGP] Public key imported from: {key_path}")
    return key


def export_private_key_encrypted(key, filename, directory):
    """Export a private key to encrypted PEM using PKCS8 and BestAvailableEncryption."""
    directory_path = Path(directory)
    directory_path.mkdir(parents=True, exist_ok=True)

    passphrase = getpass.getpass("Enter passphrase for private key export: ").encode("utf-8")
    confirm = getpass.getpass("Confirm passphrase: ").encode("utf-8")

    if not passphrase:
        print("[PPGP] Passphrase cannot be empty.")
        raise ValueError("Passphrase cannot be empty.")

    if passphrase != confirm:
        print("[PPGP] Passphrases did not match.")
        raise ValueError("Passphrases did not match.")

    output_path = directory_path / filename
    pem_bytes = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(passphrase),
    )

    with open(output_path, "wb") as f:
        f.write(pem_bytes)

    print(f"[PPGP] Encrypted private key exported to: {output_path}")
    return output_path


def import_private_key_encrypted(path):
    """Import an encrypted PEM private key using a passphrase prompt."""
    key_path = Path(path)
    if not key_path.exists():
        print(f"[PPGP] Encrypted private key file not found: {key_path}")
        raise FileNotFoundError(f"Encrypted private key file not found: {key_path}")

    passphrase = getpass.getpass("Enter passphrase for private key import: ").encode("utf-8")
    if not passphrase:
        print("[PPGP] Passphrase cannot be empty.")
        raise ValueError("Passphrase cannot be empty.")

    with open(key_path, "rb") as f:
        key_data = f.read()

    key = serialization.load_pem_private_key(key_data, password=passphrase)
    print(f"[PPGP] Encrypted private key imported from: {key_path}")
    return key


if __name__ == "__main__":
    from cryptography.hazmat.primitives.asymmetric import rsa

    print("\n[PPGP Demo] Generating temporary RSA keypair...")
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    print("[PPGP Demo] Exporting keys...")
    private_path = export_private_key(private_key, "demo_mykey.priv", "keys")
    public_path = export_public_key(public_key, "demo_mykey.pub", "keys")

    print("[PPGP Demo] Importing keys back from disk...")
    _loaded_private = import_private_key(private_path)
    _loaded_public = import_public_key(public_path)

    print("[PPGP Demo] Done. Export/import functions are working.")
