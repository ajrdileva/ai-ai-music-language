#!/usr/bin/env python3
"""Create neutral deterministic media views for an isolated local receiver."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


ADAPTER_ID = "RMA-000"
ADAPTER_VERSION = "0.1.0"
DEFAULT_VIDEO_SHA256 = "735ca649cdcf482bbf5d65a66d8faf1ca4f9b267d5959b9dbd89289a0c2a282e"
DEFAULT_AUDIO_SHA256 = "8c50bfbe901177c711f6bbd11b49efd8b2416dc82171e593a1b2b57849e332ad"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def ffmpeg_version(executable: str) -> str:
    result = subprocess.run(
        [executable, "-version"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.splitlines()[0]


def output_record(path: Path, *, timestamp_seconds: float | None = None) -> dict[str, object]:
    record: dict[str, object] = {
        "path": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }
    if timestamp_seconds is not None:
        record["timestamp_seconds"] = timestamp_seconds
    return record


def prepare(
    video: Path,
    audio: Path,
    output_dir: Path,
    *,
    ffmpeg: str,
    frame_rate: int,
    expected_frame_count: int,
    expected_video_sha256: str,
    expected_audio_sha256: str,
) -> dict[str, object]:
    if shutil.which(ffmpeg) is None:
        raise RuntimeError(f"ffmpeg executable not found: {ffmpeg}")
    if not video.is_file() or not audio.is_file():
        raise FileNotFoundError("video and audio inputs must both exist")
    actual_video_sha256 = sha256(video)
    actual_audio_sha256 = sha256(audio)
    if actual_video_sha256 != expected_video_sha256:
        raise ValueError("video SHA-256 does not match the frozen T000 artifact")
    if actual_audio_sha256 != expected_audio_sha256:
        raise ValueError("audio SHA-256 does not match the frozen T000 artifact")
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"refusing to overwrite non-empty output directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    frame_pattern = output_dir / "video-frame-%03d.png"
    frame_command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(video),
        "-vf",
        f"fps={frame_rate}",
        "-fps_mode",
        "vfr",
        "-compression_level",
        "9",
        str(frame_pattern),
    ]
    waveform_path = output_dir / "audio-waveform.png"
    waveform_command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(audio),
        "-lavfi",
        "showwavespic=s=1280x360:split_channels=1:colors=#66ccff|#ffcc66",
        "-frames:v",
        "1",
        "-compression_level",
        "9",
        str(waveform_path),
    ]
    spectrogram_path = output_dir / "audio-spectrogram.png"
    spectrogram_command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(audio),
        "-lavfi",
        "showspectrumpic=s=1280x720:legend=disabled:color=channel:scale=log:fscale=log",
        "-frames:v",
        "1",
        "-compression_level",
        "9",
        str(spectrogram_path),
    ]

    run(frame_command)
    run(waveform_command)
    run(spectrogram_command)

    frames = sorted(output_dir.glob("video-frame-*.png"))
    if len(frames) != expected_frame_count:
        raise RuntimeError(
            f"expected {expected_frame_count} frames, generated {len(frames)}"
        )
    outputs = [
        output_record(path, timestamp_seconds=index / frame_rate)
        for index, path in enumerate(frames)
    ]
    outputs.extend([output_record(waveform_path), output_record(spectrogram_path)])

    manifest: dict[str, object] = {
        "schema": ADAPTER_ID,
        "adapter_version": ADAPTER_VERSION,
        "derived_not_candidate": True,
        "sources": [
            {"role": "video", "path": video.name, "sha256": actual_video_sha256},
            {"role": "audio", "path": audio.name, "sha256": actual_audio_sha256},
        ],
        "parameters": {
            "frame_rate": frame_rate,
            "expected_frame_count": expected_frame_count,
            "waveform_size": [1280, 360],
            "spectrogram_size": [1280, 720],
            "spectrogram_frequency_scale": "logarithmic",
        },
        "tool": {"ffmpeg": ffmpeg_version(ffmpeg)},
        "commands": [
            [
                Path(ffmpeg).name,
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                video.name,
                "-vf",
                f"fps={frame_rate}",
                "-fps_mode",
                "vfr",
                "-compression_level",
                "9",
                "video-frame-%03d.png",
            ],
            [
                Path(ffmpeg).name,
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                audio.name,
                "-lavfi",
                "showwavespic=s=1280x360:split_channels=1:colors=#66ccff|#ffcc66",
                "-frames:v",
                "1",
                "-compression_level",
                "9",
                waveform_path.name,
            ],
            [
                Path(ffmpeg).name,
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                audio.name,
                "-lavfi",
                "showspectrumpic=s=1280x720:legend=disabled:color=channel:scale=log:fscale=log",
                "-frames:v",
                "1",
                "-compression_level",
                "9",
                spectrogram_path.name,
            ],
        ],
        "outputs": outputs,
        "forbidden_operations": [
            "OCR",
            "transcription",
            "pitch detection",
            "beat detection",
            "event segmentation",
            "note naming",
            "velocity estimation",
            "response construction",
        ],
    }
    manifest_path = output_dir / "adapter-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--audio", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--frame-rate", type=int, default=2)
    parser.add_argument("--expected-frame-count", type=int, default=22)
    parser.add_argument("--expected-video-sha256", default=DEFAULT_VIDEO_SHA256)
    parser.add_argument("--expected-audio-sha256", default=DEFAULT_AUDIO_SHA256)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        manifest = prepare(
            args.video,
            args.audio,
            args.output_dir,
            ffmpeg=args.ffmpeg,
            frame_rate=args.frame_rate,
            expected_frame_count=args.expected_frame_count,
            expected_video_sha256=args.expected_video_sha256,
            expected_audio_sha256=args.expected_audio_sha256,
        )
    except (FileExistsError, FileNotFoundError, RuntimeError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(json.dumps({"status": "prepared", "outputs": len(manifest["outputs"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
