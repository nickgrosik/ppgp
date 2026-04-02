from cryptography.hazmat.primitives import hashes, serialization


def public_key_fingerprint(public_key):
    """Return the first 40 hex chars of SHA256 over DER-encoded public key."""
    der = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    digest = hashes.Hash(hashes.SHA256())
    digest.update(der)
    return digest.finalize().hex()[:40]


if __name__ == "__main__":
    from cryptography.hazmat.primitives.asymmetric import rsa

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    fp = public_key_fingerprint(public_key)
    print(f"[PPGP Demo] Public key fingerprint (first 40 hex): {fp}")
