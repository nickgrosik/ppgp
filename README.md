# PPGP — Pete’s Pretty Good Privacy

PPGP is a simple, beginner‑friendly Python tool that teaches the basics of public‑key cryptography. It supports RSA keypair generation, message encryption, and message decryption using secure modern padding schemes. The goal is to give learners a hands‑on way to understand how real cryptographic tools work under the hood.

This project is part of my cybersecurity portfolio and will continue to grow as I add more features and polish it.

## Features
- RSA keypair generation (private + public)
- RSA‑OAEP message encryption
- RSA‑OAEP message decryption
- Menu‑driven command‑line interface
- Automatic key storage in a user directory

## Planned Features
- Message signing and verification
- Key inspector (fingerprints, metadata)
- Key export/import
- Colorized CLI output
- Beginner “Learn Mode” improvements
- Packaging as a pip‑installable module

## Future AI Features
PPGP will eventually include optional AI-powered tools to make cryptography more accessible and beginner-friendly:
- **AI Key Inspector**  
  Explains key properties, detects weak configurations, and summarizes metadata in plain English.
- **AI Encryption Helper**  
  Provides guidance on what can be safely encrypted, warns about common mistakes, and explains errors.
- **AI Learning Mode**  
  An interactive assistant that teaches cryptography concepts, answers questions, and breaks down complex topics.  
- **AI File Classifier (optional)**  
  Identifies file types before encryption and recommends best practices, such as when to use hybrid encryption.

These features are planned as optional add-ons to enhance usability without replacing the core cryptographic functionality.


## How to Run
Clone the repository:

git clone https://github.com/nickgrosik/ppgp
cd ppgp

Run the program:

python -m pgpg.main

## Project Purpose
This project was built to strengthen my understanding of cryptography fundamentals, Python development, and secure key handling. It’s designed to be approachable for beginners while still following real cryptographic standards.

## Directory Structure
pgpg/
    main.py
    menu.py
    keygen.py
    encrypt.py
    decrypt.py
    beginner.py
    advanced.py

Keys and ciphertext are stored automatically in:

~/.ppgp/keys/

## License
MIT License
