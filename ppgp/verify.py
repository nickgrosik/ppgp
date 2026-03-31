from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

from .config import KEY_DIR, ENCRYPTED_DIR, SIGNATURE_DIR


def _list_encrypted_files():
    files = [f for f in ENCRYPTED_DIR.iterdir() if f.is_file() and f.suffix == ".bin"]
    files.sort()
    return files

def _list_signature_files():
    files = [f for f in SIGNATURE_DIR.iterdir() if f.is_file() and f.suffix == ".sig"]
    files.sort()
    return files

def verify_signature():
    # Lead public key
    pub_path = KEY_DIR / "mykey.pub"
    if not pub_path.exists():
        print("\nNo public key found. You're asking me to work purely off vibes here. Try generating a keypair first.\n")
        return
    
    with open(pub_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    sig_files = _list_signature_files()
    if not sig_files:
        print("\nNo signature files found. There's nothing to be verified yet.\n")
        return
    
    print("\nHere's what we found:")
    for idx, path in enumerate(sig_files, start=1):
        print(f"{idx}. {path.name}")

    sig_choice = input("\nWhich signature would you like to check?\n> ").strip()
    if not sig_choice.isdigit():
        print("\nFriend... that is not a number.\n")
        return
    
    sig_idx = int(sig_choice)
    if sig_idx < 1 or sig_idx > len(sig_files):
        print("\nSold out! Pick something actually on the list.\n")
        return
    
    sig_path = sig_files[sig_idx - 1]

    enc_files = _list_encrypted_files()
    if not enc_files:
        print("\nNo encrypted files found. I need a little more than just vibes to verify something.\n")
        return
    
    print("\nHere's the encrypted files you can verify it with:")
    for idx, path in enumerate(enc_files, start=1):
        print(f"{idx}. {path.name}")

    enc_choice = input("\nWhich encrypted file are we comparing it to?\n> ").strip()
    if not enc_choice.isdigit():
        print("\nMy brother in Christ... please actually use a number.\n")
        return
    
    enc_idx = int(enc_choice)
    if enc_idx < 1 or enc_idx > len(enc_files):
        print("\nI admire the confidence, but that number is out of range.\n")
        return
    
    enc_path = enc_files[enc_idx - 1]

    with open(sig_path, "rb") as f:
        signature = f.read()

    with open(enc_path, "rb") as f:
        data = f.read()

    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("\n Signature checks out... it looks like everything matches up!\n")
    except Exception:
        print("\nNope! That signature does NOT belong to that file!\n")