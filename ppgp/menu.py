from .beginner import show_beginner_page
from .advanced import show_advanced_page
from .keygen import generate_keypair
from .encrypt import encrypt_message
from .decrypt import decrypt_message

def show_menu():
    while True:
        print("\n=== PPGP Menu ===")
        print("1. Learn the Basics")
        print("2. Advanced Tools")
        print("3. Generate a Keypair")
        print("4. Encrypt a Message")
        print("5. Decrypt a Message")
        print("6. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            show_beginner_page()
        elif choice == "2":
            show_advanced_page()
        elif choice == "3":
            generate_keypair()
        elif choice == "4":
            encrypt_message()
        elif choice == "5":
            decrypt_message()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")