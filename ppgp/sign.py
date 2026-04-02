from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from .config import KEY_DIR, ENCRYPTED_DIR, SIGNATURE_DIR, generate_timestamped_name

def _list_encrypted_files():
        files = [f for f in ENCRYPTED_DIR.iterdir() if f.is_file() and f.suffix == ".bin"]
        files.sort()
        return files


def sign_message():
    # Load private key
    priv_path = KEY_DIR / "mykey.priv"
    if not priv_path.exists():
        print("\nNo private key found. Generate a keypair first.\n")
        return
    
    with open(priv_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    files = _list_encrypted_files()
    if not files:
        print("\nNo encrypted files found to sign\n")
        return
    
    print("\nAvailable encrypted files to sign:")
    for idx, path in enumerate(files, start=1):
        print(f"{idx}. {path.name}")

    choice = input("\nChoose a file to sign (number):\n> ").strip()
    if not choice.isdigit():
        print("\nInvalid choice.\n")
        return
    
    idx = int(choice)
    if idx < 1 or idx > len(files):
        print("\nChoice out of range.\n")
        return
    
    target_path = files[idx -1]

    with open(target_path, "rb") as f:
        data = f.read()

    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    sig_path = generate_timestamped_name("signature", ".sig", SIGNATURE_DIR)

    with open(sig_path, "wb") as f:
        f.write(signature)

    print("\nSignature created successfully!")
    print(f"Signature saved to {sig_path}\n")
