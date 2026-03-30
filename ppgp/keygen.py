import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

KEYS_DIR = os.path.expanduser("~/.ppgp/keys")

def generate_keypair():
    # Make sure the keys directory exists
    os.makedirs(KEYS_DIR, exist_ok=True)

    # Generate a private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Extract the public key
    public_key = private_key.public_key()

    # Convert private key to PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Convert public key to PEM format
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Save the keys
    private_path = os.path.join(KEYS_DIR, "mykey.priv")
    public_path = os.path.join(KEYS_DIR, "mykey.pub")

    with open(public_path, "wb") as f:
        f.write(public_pem)

    with open(private_path, "wb") as f:
        f.write(private_pem)
    
    print("\nYour keys have been created!")
    print(f"Public key:   {public_path}")
    print(f"Private key:  {private_path}")
    print("Keep your private key safe.\n")