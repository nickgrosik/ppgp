import os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

KEYS_DIR = os.path.expanduser("~/.ppgp/keys")

def decrypt_message():
    # Load ciphertext
    ciphertext_path = os.path.join(KEYS_DIR, "ciphertext.bin")

    if not os.path.exists(ciphertext_path):
        print("\nNo ciphertext found. Encrypt a message first.\n")
        return
    
    with open(ciphertext_path, "rb") as f:
        ciphertext = f.read()

    # Load private key
    private_path = os.path.join(KEYS_DIR, "mykey.priv")

    if not os.path.exists(private_path):
        print("\nNo private key found. Generate a keypair first.\n")
        return
    
    with open(private_path, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
        )


    # Decrypt the message
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
        print("\nDecryption failed. Wrong key or corrupted ciphertext.\n")
        return
    
    print("\nDecrypted message:")
    print(plaintext.decode() + "\n")