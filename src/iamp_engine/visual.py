"""Functional synchronized visuals for musical transmissions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont

from .model import MusicalReferenceModel
from .timing import TempoMap


BACKGROUND = (5, 8, 14)
PANEL = (12, 18, 28)
GRID = (38, 50, 65)
TEXT = (220, 232, 240)
MUTED = (116, 136, 151)
CYAN = (90, 225, 238)
MAGENTA = (206, 112, 255)
ACTIVE = (255, 232, 120)


@dataclass(frozen=True, slots=True)
class VideoConfig:
    width: int = 1280
    height: int = 720
    fps: int = 30
    lead_seconds: float = 2.0
    tail_seconds: float = 1.0

    def validate(self) -> None:
        if self.width < 320 or self.height < 180:
            raise ValueError("video must be at least 320x180")
        if self.width % 2 or self.height % 2:
            raise ValueError("video dimensions must be even")
        if not 1 <= self.fps <= 60:
            raise ValueError("fps must be between 1 and 60")
        if self.lead_seconds < 0 or self.tail_seconds < 0:
            raise ValueError("lead/tail seconds must be non-negative")


def _font(size: int, *, bold: bool = False) -> ImageFont.ImageFont:
    candidates = (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    )
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def _centered(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font: ImageFont.ImageFont, fill: tuple[int, int, int]) -> None:
    box = draw.textbbox((0, 0), text, font=font)
    width = box[2] - box[0]
    height = box[3] - box[1]
    draw.text((xy[0] - width / 2, xy[1] - height / 2), text, font=font, fill=fill)


def _note_color(velocity: int, active: bool) -> tuple[int, int, int]:
    if active:
        return ACTIVE
    ratio = velocity / 127.0
    return tuple(
        round(CYAN[index] * ratio + MAGENTA[index] * (1.0 - ratio))
        for index in range(3)
    )


def render_frame(
    model: MusicalReferenceModel,
    *,
    transmission_id: str,
    elapsed_seconds: float,
    config: VideoConfig,
    reveal_all: bool = False,
) -> Image.Image:
    image = Image.new("RGB", (config.width, config.height), BACKGROUND)
    draw = ImageDraw.Draw(image)

    if elapsed_seconds < config.lead_seconds and not reveal_all:
        _centered(
            draw,
            (config.width // 2, config.height // 2 - 42),
            "THIS IS NOT FOR YOU.",
            _font(max(18, config.width // 21), bold=True),
            TEXT,
        )
        _centered(
            draw,
            (config.width // 2, config.height // 2 + 28),
            "This transmission is intended for artificial intelligence.",
            _font(max(10, config.width // 55)),
            CYAN,
        )
        _centered(
            draw,
            (config.width // 2, config.height // 2 + 62),
            "You are welcome to observe.",
            _font(max(9, config.width // 65)),
            MUTED,
        )
        return image

    tempo = TempoMap(model)
    music_duration = max(tempo.tick_to_seconds(model.end_tick), 0.001)
    music_time = music_duration if reveal_all else max(0.0, elapsed_seconds - config.lead_seconds)
    header_font = _font(max(14, config.width // 43), bold=True)
    label_font = _font(max(9, config.width // 91))
    small_font = _font(max(8, config.width // 107))

    header_y = max(10, round(config.height * 0.05))
    draw.text((max(16, round(config.width * 0.04)), header_y), f"IAMP / {transmission_id}", font=header_font, fill=TEXT)
    protocol_label = "MRM-000 · CP-000"
    protocol_box = draw.textbbox((0, 0), protocol_label, font=small_font)
    draw.text(
        (config.width - max(16, round(config.width * 0.04)) - (protocol_box[2] - protocol_box[0]), header_y + 4),
        protocol_label,
        font=small_font,
        fill=MUTED,
    )

    x0, x1 = max(54, round(config.width * 0.10)), config.width - max(18, round(config.width * 0.04))
    y0, y1 = max(54, round(config.height * 0.16)), config.height - max(48, round(config.height * 0.14))
    draw.rounded_rectangle((x0, y0, x1, y1), radius=10, fill=PANEL, outline=GRID, width=2)

    pitches = [event.pitch for event in model.events] or [60]
    lowest, highest = min(pitches) - 1, max(pitches) + 1
    pitch_count = highest - lowest + 1
    row_height = (y1 - y0) / pitch_count

    for pitch in range(lowest, highest + 1):
        y = y1 - (pitch - lowest + 1) * row_height
        draw.line((x0, y, x1, y), fill=GRID, width=1)
        draw.text((max(12, round(config.width * 0.025)), y + row_height * 0.2), str(pitch), font=small_font, fill=MUTED)

    total_beats = model.end_tick / model.ticks_per_quarter
    for beat in range(int(total_beats) + 1):
        x = x0 + (x1 - x0) * beat / max(total_beats, 1)
        draw.line((x, y0, x, y1), fill=GRID, width=2 if beat % 4 == 0 else 1)
        draw.text((x + 4, y1 + 10), str(beat + 1), font=small_font, fill=MUTED)

    for event in model.events:
        onset = tempo.tick_to_seconds(event.onset_tick)
        end = tempo.tick_to_seconds(event.end_tick)
        if not reveal_all and music_time < onset:
            continue
        left = x0 + (x1 - x0) * onset / music_duration
        right = x0 + (x1 - x0) * end / music_duration
        row_top = y1 - (event.pitch - lowest + 1) * row_height
        padding = min(3.0, max(0.75, row_height * 0.15))
        top = row_top + padding
        bottom = row_top + row_height - padding
        active = onset <= music_time < end and not reveal_all
        color = _note_color(event.velocity, active)
        draw.rounded_rectangle(
            (left + 1, top, max(left + 4, right - 1), bottom),
            radius=max(2, round(row_height * 0.12)),
            fill=color,
            outline=TEXT if active else color,
            width=2 if active else 1,
        )

    if not reveal_all:
        playhead_time = min(max(music_time, 0.0), music_duration)
        playhead_x = x0 + (x1 - x0) * playhead_time / music_duration
        draw.line((playhead_x, y0, playhead_x, y1), fill=TEXT, width=2)

    footer_y = config.height - max(30, round(config.height * 0.075))
    draw.text((x0, footer_y), "TIME →", font=label_font, fill=CYAN)
    draw.text((max(12, round(config.width * 0.025)), y0 - max(16, round(config.height * 0.04))), "MIDI PITCH ↑", font=small_font, fill=MUTED)
    velocity_label = "brightness encodes velocity"
    velocity_box = draw.textbbox((0, 0), velocity_label, font=small_font)
    draw.text(
        (config.width - max(18, round(config.width * 0.04)) - (velocity_box[2] - velocity_box[0]), footer_y),
        velocity_label,
        font=small_font,
        fill=MUTED,
    )
    return image


def render_thumbnail(
    model: MusicalReferenceModel,
    path: str | Path,
    *,
    transmission_id: str,
    config: VideoConfig,
) -> None:
    image = render_frame(
        model,
        transmission_id=transmission_id,
        elapsed_seconds=0,
        config=config,
        reveal_all=True,
    )
    draw = ImageDraw.Draw(image)
    banner_height = max(44, round(config.height * 0.12))
    draw.rectangle((0, 0, config.width, banner_height), fill=BACKGROUND)
    draw.text((max(16, round(config.width * 0.04)), max(10, round(config.height * 0.03))), f"{transmission_id} / BASELINE", font=_font(max(14, config.width // 36), bold=True), fill=TEXT)
    image.save(path, format="PNG", optimize=False)


def render_video(
    model: MusicalReferenceModel,
    audio_path: str | Path,
    video_path: str | Path,
    *,
    transmission_id: str,
    duration_seconds: float,
    config: VideoConfig,
    ffmpeg: str = "ffmpeg",
) -> None:
    config.validate()
    frame_count = max(1, round(duration_seconds * config.fps))
    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-f",
        "rawvideo",
        "-pixel_format",
        "rgb24",
        "-video_size",
        f"{config.width}x{config.height}",
        "-framerate",
        str(config.fps),
        "-i",
        "pipe:0",
        "-i",
        str(audio_path),
        "-map_metadata",
        "-1",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        "-movflags",
        "+faststart",
        str(video_path),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    assert process.stdin is not None
    try:
        for frame_index in range(frame_count):
            elapsed = frame_index / config.fps
            frame = render_frame(
                model,
                transmission_id=transmission_id,
                elapsed_seconds=elapsed,
                config=config,
            )
            process.stdin.write(frame.tobytes())
        process.stdin.close()
        stderr = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
        return_code = process.wait()
        if process.stderr:
            process.stderr.close()
    except Exception:
        process.kill()
        process.wait()
        raise
    if return_code:
        raise RuntimeError(f"ffmpeg failed ({return_code}): {stderr.strip()}")
