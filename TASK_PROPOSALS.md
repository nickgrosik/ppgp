# Codebase Task Proposals

## 1) Typo fix task
**Title:** Fix user-facing typos in beginner/signing flows

**Why this matters:** Several CLI strings contain misspellings that reduce polish and can confuse beginners.

**Evidence:**
- `"To docode something..."` should be `"decode"`.
- `"digit fingerprint"` should be `"digital fingerprint"`.
- `"Available encrypted fils to sign:"` should be `"files"`.
- `"Signature saved tp"` should be `"to"`.

**Definition of done:**
- Correct all user-facing typos in `ppgp/beginner.py` and `ppgp/sign.py`.
- Re-run a quick CLI smoke test to ensure the changed text appears correctly.

---

## 2) Bug fix task
**Title:** Make timestamp filename generation cross-platform (Linux/macOS + Windows)

**Why this matters:** `config._time_string` uses `"%#I"`, which is Windows-specific. On Linux/macOS, this may produce malformed names (or fail to strip leading zero), causing inconsistent file naming.

**Evidence:**
- Current implementation: `return dt.strftime("%#I-%M%p").lower()  # Windows-friendly`

**Definition of done:**
- Replace `%#I` usage with portable logic (e.g., `%I` + leading-zero normalization, or platform-conditional format codes).
- Add tests for representative timestamps (e.g., `03:49 PM` -> `3-49pm`) and verify generated paths do not collide unexpectedly.

---

## 3) Documentation/comment discrepancy task
**Title:** Align README key-storage docs with actual implementation

**Why this matters:** README says default key storage is `D:/PPGP/keys/`, but code stores keys under the repository root (`BASE_DIR / "keys"`). This discrepancy can mislead users trying to locate artifacts.

**Evidence:**
- README key storage section claims a Windows path default.
- `ppgp/config.py` sets `BASE_DIR = Path(__file__).resolve().parent.parent` and `KEY_DIR = BASE_DIR / "keys"`.

**Definition of done:**
- Update README “Key Storage” text to describe the real default path behavior (repo-local directories).
- Optionally add a note showing where `encrypted/` and `signatures/` are also stored.

---

## 4) Test improvement task
**Title:** Add unit tests for encryption/signature file selection helpers and input validation

**Why this matters:** Core CLI flows (`decrypt_message`, `sign_message`, `verify_signature`) rely on directory listing + numeric selection with edge-case handling, but there are no tests. Regressions are likely as features grow.

**Evidence:**
- No test files currently exist in the repository.
- Selection/input handling logic is repeated across `decrypt.py`, `sign.py`, and `verify.py`.

**Definition of done:**
- Introduce a test suite (e.g., `pytest`) with temp directories and monkeypatched input.
- Cover:
  - empty-directory cases,
  - non-numeric input,
  - out-of-range input,
  - happy-path selection for encrypted/signature files.
- Ensure tests run in CI/local via a documented command.
