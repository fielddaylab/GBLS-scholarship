"""
Shared environment loader for GBLS tools.

Reads secrets from the project-root .env file (local development) or from
the process environment (Render and other hosting platforms).  The .env file
takes precedence for any key it defines; the process environment is used as
a fallback for keys that are absent from the file.

No third-party dependencies — uses only the standard library.
"""

import os
import re
from pathlib import Path


def _load_env_file(path: Path) -> dict:
    """Parse a .env file and return a dict of key→value pairs."""
    env: dict = {}
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return env

    for line in text.splitlines():
        line = line.strip()
        # Skip blank lines and comments
        if not line or line.startswith("#"):
            continue
        # KEY=VALUE  (value may be quoted)
        match = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)', line)
        if not match:
            continue
        key, value = match.group(1), match.group(2)
        # Strip surrounding quotes
        if len(value) >= 2 and value[0] in ('"', "'") and value[-1] == value[0]:
            value = value[1:-1]
        env[key] = value
    return env


# Search for .env starting from this file's location up to the repo root.
_here = Path(__file__).resolve().parent          # tools/
_candidates = [
    _here.parent / ".env",   # project root  ← preferred
    _here / ".env",          # tools/
]

_file_env: dict = {}
for _p in _candidates:
    _file_env = _load_env_file(_p)
    if _file_env:
        break


def get(key: str, default: str | None = None) -> str | None:
    """
    Return the value for *key*, or *default* if not found.

    Resolution order:
      1. .env file (local development)
      2. Process environment (Render secrets / Docker env)
      3. *default*
    """
    return _file_env.get(key) or os.environ.get(key) or default


def require(key: str) -> str:
    """Return the value for *key* or raise RuntimeError if it is missing."""
    value = get(key)
    if not value:
        raise RuntimeError(
            f"Missing required secret '{key}'. "
            f"Add it to your .env file or set it as an environment variable."
        )
    return value
