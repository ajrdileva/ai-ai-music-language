"""Content hashing and manifest helpers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


MEDIA_TYPES = {
    ".json": "application/json",
    ".mp4": "video/mp4",
    ".png": "image/png",
    ".wav": "audio/wav",
}


def sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_record(path: str | Path, *, role: str, relative_to: str | Path) -> dict[str, Any]:
    file_path = Path(path)
    return {
        "path": file_path.relative_to(relative_to).as_posix(),
        "media_type": MEDIA_TYPES.get(file_path.suffix.lower(), "application/octet-stream"),
        "bytes": file_path.stat().st_size,
        "sha256": sha256(file_path),
        "role": role,
    }


def write_json(path: str | Path, data: Any) -> None:
    Path(path).write_text(
        json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
