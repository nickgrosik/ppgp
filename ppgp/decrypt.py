import os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

from .config import KEY_DIR, ENCRYPTED_DIR

def _list_encrypted_files():
    files = [f for f in ENCRYPTED_DIR.iterdir() if f.is_file() and f.suffix == ".bin"]
    files.sort()
    return files


def decrypt_message():
    # Load ciphertext
    priv_path = KEY_DIR / "mykey.priv"
    if not priv_path.exists():
        print("\nWe didn't find anything. Try generating a keypair first.\n")
        return
    
    with open(priv_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    files = _list_encrypted_files()
    if not files:
        print("\nWe couldn't find any files to work with.\n")
        return
    
    print("\nHere's what we found:")
    for idx, path in enumerate(files, start=1):
        print(f"{idx}. {path.name}")

    choice = input("\nWhich one do you want to decrypt? Pick whichever looks right:\n> ").strip()
    if not choice.isdigit():
        print("\nThat doesn't look like a number.\n")
        return
    
    idx = int(choice)
    if idx < 1 or idx > len(files):
        print("\nI like the enthusiasm, but that number's out of range.\n")
        return
    
    ciphertext_path = files[idx -1]

    with open(ciphertext_path, "rb") as f:
        ciphertext = f.read()

    try:
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception:
        print("\nDecryption failed. I don't think this key matches up that file.\n")
        return
    
    print("\nHere's your decrypted message:")
    print(plaintext.decode(errors="replace"))
    print()