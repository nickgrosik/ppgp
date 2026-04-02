import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import importlib.util

if importlib.util.find_spec("cryptography") is None:
    raise unittest.SkipTest("cryptography is not installed in this environment")

from ppgp import decrypt, sign, verify


class FakePrivateKey:
    def decrypt(self, ciphertext, pad):
        return b"hello"

    def sign(self, data, pad, algo):
        return b"fake-signature"


class FakePublicKey:
    def verify(self, signature, data, pad, algo):
        return None


class CliFlowTests(unittest.TestCase):
    def test_decrypt_rejects_non_numeric_choice(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            key_dir = base / "keys"
            enc_dir = base / "encrypted"
            key_dir.mkdir()
            enc_dir.mkdir()
            (key_dir / "mykey.priv").write_bytes(b"priv")
            (enc_dir / "sample.bin").write_bytes(b"cipher")

            with patch.object(decrypt, "KEY_DIR", key_dir), \
                patch.object(decrypt, "ENCRYPTED_DIR", enc_dir), \
                patch("ppgp.decrypt.serialization.load_pem_private_key", return_value=FakePrivateKey()), \
                patch("builtins.input", return_value="abc"), \
                patch("sys.stdout", new_callable=io.StringIO) as out:
                decrypt.decrypt_message()

            self.assertIn("doesn't look like a number", out.getvalue())

    def test_decrypt_rejects_out_of_range_choice(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            key_dir = base / "keys"
            enc_dir = base / "encrypted"
            key_dir.mkdir()
            enc_dir.mkdir()
            (key_dir / "mykey.priv").write_bytes(b"priv")
            (enc_dir / "sample.bin").write_bytes(b"cipher")

            with patch.object(decrypt, "KEY_DIR", key_dir), \
                patch.object(decrypt, "ENCRYPTED_DIR", enc_dir), \
                patch("ppgp.decrypt.serialization.load_pem_private_key", return_value=FakePrivateKey()), \
                patch("builtins.input", return_value="9"), \
                patch("sys.stdout", new_callable=io.StringIO) as out:
                decrypt.decrypt_message()

            self.assertIn("out of range", out.getvalue())

    def test_sign_handles_empty_encrypted_directory(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            key_dir = base / "keys"
            enc_dir = base / "encrypted"
            sig_dir = base / "signatures"
            key_dir.mkdir()
            enc_dir.mkdir()
            sig_dir.mkdir()
            (key_dir / "mykey.priv").write_bytes(b"priv")

            with patch.object(sign, "KEY_DIR", key_dir), \
                patch.object(sign, "ENCRYPTED_DIR", enc_dir), \
                patch.object(sign, "SIGNATURE_DIR", sig_dir), \
                patch("ppgp.sign.serialization.load_pem_private_key", return_value=FakePrivateKey()), \
                patch("sys.stdout", new_callable=io.StringIO) as out:
                sign.sign_message()

            self.assertIn("No encrypted files found to sign", out.getvalue())

    def test_sign_happy_path_writes_signature(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            key_dir = base / "keys"
            enc_dir = base / "encrypted"
            sig_dir = base / "signatures"
            key_dir.mkdir()
            enc_dir.mkdir()
            sig_dir.mkdir()
            (key_dir / "mykey.priv").write_bytes(b"priv")
            (enc_dir / "sample.bin").write_bytes(b"cipher")

            out_file = sig_dir / "signature_test.sig"
            with patch.object(sign, "KEY_DIR", key_dir), \
                patch.object(sign, "ENCRYPTED_DIR", enc_dir), \
                patch.object(sign, "SIGNATURE_DIR", sig_dir), \
                patch("ppgp.sign.serialization.load_pem_private_key", return_value=FakePrivateKey()), \
                patch("ppgp.sign.generate_timestamped_name", return_value=out_file), \
                patch("builtins.input", return_value="1"):
                sign.sign_message()

            self.assertTrue(out_file.exists())
            self.assertEqual(out_file.read_bytes(), b"fake-signature")

    def test_verify_rejects_non_numeric_signature_choice(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            key_dir = base / "keys"
            enc_dir = base / "encrypted"
            sig_dir = base / "signatures"
            key_dir.mkdir()
            enc_dir.mkdir()
            sig_dir.mkdir()
            (key_dir / "mykey.pub").write_bytes(b"pub")
            (sig_dir / "a.sig").write_bytes(b"sig")
            (enc_dir / "a.bin").write_bytes(b"data")

            with patch.object(verify, "KEY_DIR", key_dir), \
                patch.object(verify, "ENCRYPTED_DIR", enc_dir), \
                patch.object(verify, "SIGNATURE_DIR", sig_dir), \
                patch("ppgp.verify.serialization.load_pem_public_key", return_value=FakePublicKey()), \
                patch("builtins.input", side_effect=["hello"]), \
                patch("sys.stdout", new_callable=io.StringIO) as out:
                verify.verify_signature()

            self.assertIn("not a number", out.getvalue())

    def test_verify_happy_path(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            key_dir = base / "keys"
            enc_dir = base / "encrypted"
            sig_dir = base / "signatures"
            key_dir.mkdir()
            enc_dir.mkdir()
            sig_dir.mkdir()
            (key_dir / "mykey.pub").write_bytes(b"pub")
            (sig_dir / "a.sig").write_bytes(b"sig")
            (enc_dir / "a.bin").write_bytes(b"data")

            with patch.object(verify, "KEY_DIR", key_dir), \
                patch.object(verify, "ENCRYPTED_DIR", enc_dir), \
                patch.object(verify, "SIGNATURE_DIR", sig_dir), \
                patch("ppgp.verify.serialization.load_pem_public_key", return_value=FakePublicKey()), \
                patch("builtins.input", side_effect=["1", "1"]), \
                patch("sys.stdout", new_callable=io.StringIO) as out:
                verify.verify_signature()

            self.assertIn("Signature checks out", out.getvalue())


if __name__ == "__main__":
    unittest.main()
