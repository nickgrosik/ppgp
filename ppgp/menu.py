from .beginner import show_beginner_page
from .advanced import show_advanced_page
from .keygen import generate_keypair
from .encrypt import encrypt_message
from .decrypt import decrypt_message
from .keyinspector import inspect_key
from .sign import sign_message
from .verify import verify_signature

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
        print("9. Exit")

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
            print("\nI'll be here when you need me again. Deuces!\n")
            break
        else:
            print("\nWhy do you torment me?\n")