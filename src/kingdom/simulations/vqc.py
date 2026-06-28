"""VQC pipeline stub — integrate from vqc_sims_public."""

from __future__ import annotations

from kingdom.core.quaternion import Quaternion


def encode_demo_payload(text: str) -> Quaternion:
    """Map a short text payload to a unit quaternion (demo encoding)."""
    raw = text.encode("utf-8")[:16]
    import numpy as np

    arr = np.frombuffer(raw.ljust(16, b"\x00"), dtype=np.uint8).astype(float)
    vec = arr[:4]
    vec = vec / (np.linalg.norm(vec) + 1e-12)
    return Quaternion(vec[0], vec[1], vec[2], vec[3])