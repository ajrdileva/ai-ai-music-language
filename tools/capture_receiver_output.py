#!/usr/bin/env python3
"""Preserve one receiver's first response byte-for-byte without scoring it."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - runtime reports validation unavailable
    Draft202012Validator = None


RUN_ID = re.compile(r"^T[0-9]{3,}-RUN-[0-9]{3,}$")
SLOT_ID = re.compile(r"^T[0-9]{3,}-SLOT-[0-9]{3,}$")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def capture(
    source: Path,
    run_dir: Path,
    *,
    run_id: str,
    slot_id: str,
    receiver_model_id: str,
    response_schema: Path,
) -> dict[str, object]:
    if not RUN_ID.fullmatch(run_id):
        raise ValueError(f"invalid run ID: {run_id}")
    if not SLOT_ID.fullmatch(slot_id):
        raise ValueError(f"invalid slot ID: {slot_id}")
    if not source.is_file():
        raise FileNotFoundError(source)
    if run_dir.exists() and any(run_dir.iterdir()):
        raise FileExistsError(f"refusing to overwrite non-empty run directory: {run_dir}")
    run_dir.mkdir(parents=True, exist_ok=True)
    destination = run_dir / "raw-response.txt"
    shutil.copyfile(source, destination)

    parse_valid = False
    schema_valid: bool | None = None
    parse_error: str | None = None
    try:
        response = json.loads(destination.read_text(encoding="utf-8"))
        parse_valid = True
        if Draft202012Validator is not None:
            schema = json.loads(response_schema.read_text(encoding="utf-8"))
            Draft202012Validator(schema).validate(response)
            schema_valid = True
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        parse_error = type(error).__name__
    except Exception as error:  # validation failure is evidence, never repaired
        if Draft202012Validator is not None and error.__class__.__module__.startswith("jsonschema"):
            schema_valid = False
            parse_error = type(error).__name__
        else:
            raise

    manifest: dict[str, object] = {
        "schema": "RECEIVER-OUTPUT-CAPTURE-000",
        "run_id": run_id,
        "slot_id": slot_id,
        "receiver_model_id": receiver_model_id,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "raw_response": {
            "path": destination.name,
            "bytes": destination.stat().st_size,
            "sha256": sha256(destination),
            "byte_preserved": destination.read_bytes() == source.read_bytes(),
        },
        "checks": {
            "json_parse_valid": parse_valid,
            "receiver_schema_valid": schema_valid,
            "error_class": parse_error,
        },
        "scored": False,
        "normalized": False,
        "repaired": False,
    }
    manifest_path = run_dir / "capture-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--slot-id", required=True)
    parser.add_argument("--receiver-model-id", required=True)
    parser.add_argument("--response-schema", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        manifest = capture(
            args.source,
            args.run_dir,
            run_id=args.run_id,
            slot_id=args.slot_id,
            receiver_model_id=args.receiver_model_id,
            response_schema=args.response_schema,
        )
    except (FileExistsError, FileNotFoundError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(json.dumps({"status": "captured", "sha256": manifest["raw_response"]["sha256"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
