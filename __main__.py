"""Package entry point (`python3 ks_patcher.py` or `python3 -m <pkg>`)."""

from __future__ import annotations

from .ks_patcher import main

if __name__ == "__main__":
    raise SystemExit(main())
