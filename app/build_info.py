"""Build metadata for Kingdom Come Space."""

from __future__ import annotations

import os

VERSION = "0.2.1"
GITHUB_URL = "https://github.com/kinaar8340/kingdom_come"
HF_SPACE_URL = "https://huggingface.co/spaces/kinaar111/kingdom"
HF_PROFILE_URL = "https://huggingface.co/kinaar111"


def get_build_label() -> str:
    space = os.environ.get("SPACE_ID", "")
    suffix = f" · {space}" if space else " · local"
    return f"Kingdom Come v{VERSION}{suffix}"