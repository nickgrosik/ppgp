import os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

KEYS_DIR = os.path.expanduser("~/.ppgp/keys")

def encrypt_message():
    # Ask user for message
    message = input("\nEnter the message you want to encrpyt:\n> ").encode()

    # Load the public key
    public_path = os.path.join(KEYS_DIR, "mykey.pub")

    if not os.path.exists(public_path):
        print("\nNo public key found. Generate a keypair first.\n")
        return
    
    with open(public_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    # Encrypt the message
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Save ciphertext
    output_path = os.path.join(KEYS_DIR, "ciphertext.bin")
    with open(output_path, "wb") as f:
        f.write(ciphertext)
        
    print("\nMessage encrypted successfully!")
    print(f"Ciphertext saved to: {output_path}\n")