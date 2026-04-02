from .beginner import show_beginner_page
from .advanced import show_advanced_page
from .keygen import generate_keypair
from .encrypt import encrypt_message
from .decrypt import decrypt_message
from .keyinspector import inspect_key
from .sign import sign_message
from .verify import verify_signature
from .config import KEY_DIR
from .keyio import import_private_key, import_public_key, export_private_key_encrypted, import_private_key_encrypted
from .symmetric import encrypt_file_aesgcm, decrypt_file_aesgcm
from .fingerprint import public_key_fingerprint


def _prompt_aes_key_bytes():
    key_hex = input("\nEnter AES key as hex (32, 48, or 64 hex chars):\n> ").strip()
    try:
        key = bytes.fromhex(key_hex)
    except ValueError:
        print("\nThat isn't valid hex.\n")
        return None

    if len(key) not in (16, 24, 32):
        print("\nAES key must be 16, 24, or 32 bytes.\n")
        return None

    return key


def show_menu():
    while True:
        print("\n==============================")
        print("        PPGP MAIN MENU        ")
        print("==============================")
        print("How can I help?\n")
        print("1. Learn the Basics")
        print("2. Advanced Tools")
        print("3. Generate Keypair")
        print("4. Encrypt Message")
        print("5. Decrypt Message")
        print("6. Inspect Key")
        print("7. Sign Message")
        print("8. Verify Signature")
        print("9. Export Private Key (Passphrase)")
        print("10. Import Private Key (Passphrase)")
        print("11. AES-GCM Encrypt File")
        print("12. AES-GCM Decrypt File")
        print("13. Show Public Key Fingerprint")
        print("14. Exit")

        choice = input("\nHit me with something (a number please):").strip()

        if choice == "1":
            print("\nAwesome, let's start with the basics.\n")
            show_beginner_page()

        elif choice == "2":
            print("\nBrainscan complete! I'm just joking... or AM i?\n")
            show_advanced_page()

        elif choice == "3":
            print("\nHere's some fresh keys, hot off the press.\n")
            generate_keypair()

        elif choice == "4":
            print("\nWe need to protect your privacy, let's get something encrypted.\n")
            encrypt_message()

        elif choice == "5":
            print("\nDon't worry, dynamite is on stand-by if this key doesn't crack the code.\n")
            decrypt_message()

        elif choice == "6":
            path = input("\nPerfect, type the path to your public key below:\n")
            inspect_key(path)

        elif choice == "7":
            print("\nIs it more of a digital fingerprint than a John Hancock? The world may never know.\n")
            sign_message()

        elif choice == "8":
            print("\nTemporarily lending you my Sherlock detective skills...\n")
            verify_signature()

        elif choice == "9":
            try:
                private_path = KEY_DIR / "mykey.priv"
                private_key = import_private_key(private_path)
                filename = input("\nOutput filename for encrypted private key [mykey_encrypted.priv]:\n> ").strip() or "mykey_encrypted.priv"
                export_private_key_encrypted(private_key, filename, KEY_DIR)
            except Exception as e:
                print(f"\nCouldn't export encrypted private key: {e}\n")

        elif choice == "10":
            try:
                path = input("\nPath to encrypted private key [keys/mykey_encrypted.priv]:\n> ").strip() or str(KEY_DIR / "mykey_encrypted.priv")
                key = import_private_key_encrypted(path)
                print(f"\nEncrypted private key loaded successfully: {type(key).__name__}\n")
            except Exception as e:
                print(f"\nCouldn't import encrypted private key: {e}\n")

        elif choice == "11":
            try:
                key = _prompt_aes_key_bytes()
                if key is None:
                    continue
                input_path = input("\nInput file path to encrypt:\n> ").strip()
                output_path = input("Output file path [encrypted/output.aesgcm]:\n> ").strip() or "encrypted/output.aesgcm"
                encrypt_file_aesgcm(input_path, output_path, key)
            except Exception as e:
                print(f"\nAES-GCM encryption failed: {e}\n")

        elif choice == "12":
            try:
                key = _prompt_aes_key_bytes()
                if key is None:
                    continue
                input_path = input("\nInput file path to decrypt:\n> ").strip()
                output_path = input("Output file path [encrypted/output.decrypted]:\n> ").strip() or "encrypted/output.decrypted"
                decrypt_file_aesgcm(input_path, output_path, key)
            except Exception as e:
                print(f"\nAES-GCM decryption failed: {e}\n")

        elif choice == "13":
            try:
                public_key = import_public_key(KEY_DIR / "mykey.pub")
                fp = public_key_fingerprint(public_key)
                print(f"\nPublic key fingerprint (SHA256, first 40 hex): {fp}\n")
            except Exception as e:
                print(f"\nCouldn't compute fingerprint: {e}\n")

        elif choice == "14":
            print("\nI'll be here when you need me again. Deuces!\n")
            break
        else:
            print("\nWhy do you torment me?\n")
