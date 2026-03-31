from cryptography.hazmat.primitives import serialization, hashes

def inspect_key(path):
    try:
        with open(path, "rb") as f:
            key_data = f.read()

        # Correct variable name
        public_key = serialization.load_pem_public_key(key_data)

        # Extract key size
        key_size = public_key.key_size

        # fingerprint
        digest = hashes.Hash(hashes.SHA256())
        digest.update(key_data)
        fingerprint = digest.finalize().hex()

        print("\nKey Inspector")
        print("-------------")
        print(f"Algorithm: RSA")
        print(f"Key Size: {key_size} bits")
        print(f"Fingerprint: {fingerprint[:32]}...")
        print("Status: Valid\n")

    except Exception as e:
        print(f"Error: {e}")