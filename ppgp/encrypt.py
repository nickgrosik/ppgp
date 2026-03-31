from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from .config import KEY_DIR, ENCRYPTED_DIR, generate_timestamped_name

def encrypt_message():
    # Ask user for message
    message = input("\nAlright, what message are we locking up today?\n> ").encode()

    # Load the public key
    public_path = KEY_DIR / "mykey.pub"

    if not public_path.exists():
        print("\nI looked everywhere, but there's no public key. Try generating a keypair first.\n")
        return
    
    with open(public_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    # Encrypt the message
    try:
        ciphertext = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception:
        print("\nEncryption didn't work. I don't think this key and that message are on speaking terms.\n")
        return

    # Generate nice filename
    output_path = generate_timestamped_name("encrypted", ".bin", ENCRYPTED_DIR)
    
    with open(output_path, "wb") as f:
        f.write(ciphertext)
        
    print("\nPrivacy secured - your message is now encrypted!")
    print(f"The ciphertext was saved to: {output_path}\n")