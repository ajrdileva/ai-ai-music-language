"""End-to-end transmission rendering orchestration."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
from typing import Any

from . import __version__
from .audio import render_wav
from .manifest import artifact_record, sha256, write_json
from .model import load_mrm
from .visual import VideoConfig, render_thumbnail, render_video


def _load_protocol(path: Path) -> dict[str, Any]:
    protocol = json.loads(path.read_text(encoding="utf-8"))
    required = {"schema", "protocol", "maturity", "target_model", "bootstrap", "response"}
    missing = required - protocol.keys()
    if protocol.get("schema") != "CP-000" or missing:
        raise ValueError(f"invalid CP-000 description; missing={sorted(missing)}")
    return protocol


def _ffmpeg_version(executable: str) -> str:
    result = subprocess.run(
        [executable, "-version"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.splitlines()[0]


def render_transmission(
    *,
    mrm_path: str | Path,
    protocol_path: str | Path,
    output_dir: str | Path,
    transmission_id: str,
    config: VideoConfig | None = None,
    sample_rate: int = 48_000,
    ffmpeg: str | None = None,
) -> dict[str, Any]:
    config = config or VideoConfig()
    config.validate()
    model_source = Path(mrm_path).resolve()
    protocol_source = Path(protocol_path).resolve()
    destination = Path(output_dir).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    model = load_mrm(model_source)
    protocol = _load_protocol(protocol_source)
    ffmpeg_path = ffmpeg or shutil.which("ffmpeg")
    if not ffmpeg_path:
        raise RuntimeError("ffmpeg is required to render MP4 output")

    audio_path = destination / f"{transmission_id}.wav"
    video_path = destination / f"{transmission_id}.mp4"
    thumbnail_path = destination / f"{transmission_id}-thumbnail.png"
    report_path = destination / "reproducibility-report.json"
    manifest_path = destination / "manifest.json"

    duration = render_wav(
        model,
        audio_path,
        sample_rate=sample_rate,
        lead_seconds=config.lead_seconds,
        tail_seconds=config.tail_seconds,
    )
    render_thumbnail(
        model,
        thumbnail_path,
        transmission_id=transmission_id,
        config=config,
    )
    render_video(
        model,
        audio_path,
        video_path,
        transmission_id=transmission_id,
        duration_seconds=duration,
        config=config,
        ffmpeg=ffmpeg_path,
    )

    report = {
        "schema": "REPRODUCIBILITY-REPORT-000",
        "transmission_id": transmission_id,
        "engine": {"name": "iamp-transmission-engine", "version": __version__},
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "pillow": __import__("PIL").__version__,
            "ffmpeg": _ffmpeg_version(ffmpeg_path),
        },
        "configuration": {**asdict(config), "sample_rate": sample_rate},
        "reproducibility": {
            "audio": "deterministic for the same Python/runtime inputs",
            "visual_frames": "deterministic for the same Pillow/font environment",
            "video": "perceptually reproducible; byte identity depends on FFmpeg/x264",
        },
        "validation": {
            "mrm_semantic_validation": "passed",
            "protocol_minimum_validation": "passed",
            "independent_evaluation": "not-run",
        },
    }
    write_json(report_path, report)

    artifacts = [
        artifact_record(audio_path, role="reference-audio", relative_to=destination),
        artifact_record(video_path, role="canonical-video", relative_to=destination),
        artifact_record(thumbnail_path, role="thumbnail", relative_to=destination),
        artifact_record(report_path, role="reproducibility-report", relative_to=destination),
    ]
    manifest = {
        "schema": "TRANSMISSION-MANIFEST-000",
        "transmission_id": transmission_id,
        "status": "generated",
        "foundation_version": "0.2",
        "components": {
            "reference_model": {"id": "MRM-000", "version": "0.1-draft", "source_ref": f"urn:iamp:{transmission_id}:reference-model"},
            "protocol": {
                "id": protocol["protocol"]["id"],
                "version": protocol["protocol"]["version"],
                "source_ref": "https://github.com/ajrdileva/ai-ai-music-language/blob/main/protocols/cp-000-baseline.json",
            },
            "renderer": {"id": "iamp-transmission-engine", "version": __version__, "source_ref": "https://github.com/ajrdileva/ai-ai-music-language"},
            "evaluator": {"id": "IES-C000", "version": "0.1-draft", "source_ref": "https://github.com/ajrdileva/ai-ai-music-language/blob/main/schemas/ies-c000.schema.json"},
        },
        "inputs": [
            {"path": model_source.name, "media_type": "application/json", "bytes": model_source.stat().st_size, "sha256": sha256(model_source), "role": "musical-reference-model"},
            {"path": protocol_source.name, "media_type": "application/json", "bytes": protocol_source.stat().st_size, "sha256": sha256(protocol_source), "role": "communication-protocol"},
        ],
        "artifacts": artifacts,
        "challenge": {
            "id": f"{transmission_id}-reconstruct",
            "type": "protocol",
            "instructions": "Recover the transmitted note events using only the published cold-start package.",
            "response_schema": "https://github.com/ajrdileva/ai-ai-music-language/blob/main/schemas/receiver-response-000.schema.json",
        },
        "entry_points": ["README.md", "protocols/cp-000-baseline.json"],
        "claims": [],
        "evaluations": [
            {"track": "communication", "status": "planned"},
            {"track": "knowledge", "status": "not-planned"},
        ],
    }
    write_json(manifest_path, manifest)
    return manifest
