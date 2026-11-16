"""Command-line interface for the transmission engine."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .model import load_mrm
from .render import render_transmission
from .visual import VideoConfig


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="iamp", description="Render reproducible AI-to-AI musical transmissions")
    subcommands = parser.add_subparsers(dest="command", required=True)

    validate = subcommands.add_parser("validate", help="validate an MRM-000 document")
    validate.add_argument("mrm", type=Path)

    render = subcommands.add_parser("render", help="render WAV, MP4, thumbnail, report, and manifest")
    render.add_argument("--mrm", required=True, type=Path)
    render.add_argument("--protocol", required=True, type=Path)
    render.add_argument("--output", required=True, type=Path)
    render.add_argument("--transmission-id", default="T000")
    render.add_argument("--width", type=int, default=1280)
    render.add_argument("--height", type=int, default=720)
    render.add_argument("--fps", type=int, default=30)
    render.add_argument("--lead-seconds", type=float, default=2.0)
    render.add_argument("--tail-seconds", type=float, default=1.0)
    render.add_argument("--sample-rate", type=int, default=48_000)
    render.add_argument("--ffmpeg")
    render.add_argument(
        "--ground-truth-commitment",
        help="publish this salted SHA-256 commitment instead of the raw MRM hash",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "validate":
        model = load_mrm(args.mrm)
        print(json.dumps({"status": "valid", "schema": "MRM-000", "id": model.id, "events": len(model.events)}, sort_keys=True))
        return 0

    config = VideoConfig(
        width=args.width,
        height=args.height,
        fps=args.fps,
        lead_seconds=args.lead_seconds,
        tail_seconds=args.tail_seconds,
    )
    manifest = render_transmission(
        mrm_path=args.mrm,
        protocol_path=args.protocol,
        output_dir=args.output,
        transmission_id=args.transmission_id,
        config=config,
        sample_rate=args.sample_rate,
        ffmpeg=args.ffmpeg,
        ground_truth_commitment=args.ground_truth_commitment,
    )
    print(json.dumps({"status": manifest["status"], "transmission_id": manifest["transmission_id"], "output": str(args.output.resolve())}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
