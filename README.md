# PPGP — Pete’s Pretty Good Privacy

PPGP is a beginner friendly Python tool that teaches the basics of public key cryptography. It handles RSA keypair generation, message encryption, and message decryption using modern and secure padding schemes. The goal is to give learners a hands on way to understand how real cryptographic tools work under the hood without needing a PhD or a tolerance for academic PDFs.

This project is part of my cybersecurity portfolio and will continue to grow as I add more features, improve the user experience, and give the program more personality than a cryptography tool usually gets.

---

## Features
- RSA keypair generation (private + public)
- RSA‑OAEP message encryption
- RSA‑OAEP message decryption
- Menu‑driven command‑line interface that keeps things simple and readable
- Automatic key storage in a user directory
- Message signing and verification
- Key inspector (fingerprints, metadata)

---

## Planned Features
- Key export/import
- Colorized CLI output
- Beginner “Learn Mode” improvements
- Packaging as a pip‑installable module

---

## Future AI Features
Optional AI‑powered helpers to make cryptography less intimidating and more interactive:

### **AI Key Inspector**
Breaks down key properties, explains metadata, and warns about weak configurations in plain English.

### **AI Encryption Helper**
Guides users on what can be safely encrypted, explains errors, and prevents common mistakes.

### **AI Learning Mode**
An interactive assistant that teaches cryptography concepts and answers questions as you explore the tool.

### **AI File Classifier (optional)**
Identifies file types before encryption and recommends best practices (like when hybrid encryption makes sense).

These features will be optional add‑ons. The core cryptography will stay clean, simple, and fully manual.

---

## How to Run

Clone the repository:

```bash
git clone https://github.com/nickgrosik/ppgp
cd ppgp
```

Run the program:

```bash
python -m ppgp.main
```

---

## Project Purpose
This project strengthens my understanding of cryptography fundamentals, Python development, and secure key handling. It’s designed to be approachable for beginners while still following real cryptographic standards.

---

## Directory Structure

```text
ppgp/
    main.py
    menu.py
    keygen.py
    encrypt.py
    decrypt.py
    beginner.py
    advanced.py
```

---

## Key Storage

PPGP stores generated keys and encrypted files in a dedicated project directory.  
By default, this is:

```
D:/PPGP/keys/   (Windows example)
```

You can change this path in `config.py` if you want to use a different location.
