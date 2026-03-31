# ppgp/config.py
from pathlib import Path
from datetime import datetime

# Base project directory (ppgp/ is one level below)
BASE_DIR = Path(__file__).resolve().parent.parent

KEY_DIR = BASE_DIR / "keys"
ENCRYPTED_DIR = BASE_DIR / "encrypted"
SIGNATURE_DIR = BASE_DIR / "signatures"

# Ensure directories exist
for d in (KEY_DIR, ENCRYPTED_DIR, SIGNATURE_DIR):
    d.mkdir(exist_ok=True)

def _short_month(dt: datetime) -> str:
    return dt.strftime("%b") # Jan, Feb, Mar, ...

def _short_year(dt: datetime) -> str:
    return dt.strftime("%y") # 26 for 2026

def _time_string(dt: datetime) -> str:
    # Example: 3-49pm
    return dt.strftime("%#I-%M%p").lower() # Windows-friendly


def generate_timestamped_name(prefix: str, ext: str, directory: Path) -> Path:
    """
    prefix: 'encrypted' or 'signature'
    ext: '.bin' or '.sig'
    directory: where to save
    """
    now = datetime.now()
    month = _short_month(now)       # Mar
    day = now.day                   # 30
    year = _short_year(now)         # 26
    time_str = _time_string(now)    # 3-49pm

    base_name = f"{prefix}_{month}{day}_{time_str}_{year}"
    candidate = directory / f"{base_name}{ext}"

    if not candidate.exists():
        return candidate
    
    # If file exists, add _v2, _v3, ...
    version = 2
    while True:
        candidate = directory / f"{base_name}_v{version}{ext}"
        if not candidate.exists():
            return candidate
        version += 1