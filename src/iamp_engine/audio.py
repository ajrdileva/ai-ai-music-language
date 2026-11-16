"""Deterministic neutral-tone audio rendering."""

from __future__ import annotations

from array import array
import math
from pathlib import Path
import wave

from .model import MusicalReferenceModel
from .timing import TempoMap


def midi_frequency(pitch: int) -> float:
    return 440.0 * 2.0 ** ((pitch - 69) / 12.0)


def render_wav(
    model: MusicalReferenceModel,
    path: str | Path,
    *,
    sample_rate: int = 48_000,
    lead_seconds: float = 2.0,
    tail_seconds: float = 1.0,
) -> float:
    """Render a mono-compatible stereo WAV and return its duration."""
    if sample_rate < 8_000:
        raise ValueError("sample_rate must be at least 8000")
    tempo = TempoMap(model)
    music_duration = tempo.tick_to_seconds(model.end_tick)
    duration = lead_seconds + music_duration + tail_seconds
    sample_count = max(1, math.ceil(duration * sample_rate))
    mix = array("f", [0.0]) * sample_count
    attack = max(1, round(0.008 * sample_rate))
    release = max(1, round(0.025 * sample_rate))

    for event in model.events:
        start_seconds = lead_seconds + tempo.tick_to_seconds(event.onset_tick)
        end_seconds = lead_seconds + tempo.tick_to_seconds(event.end_tick)
        start = max(0, round(start_seconds * sample_rate))
        end = min(sample_count, round(end_seconds * sample_rate))
        frequency = midi_frequency(event.pitch)
        amplitude = 0.24 * event.velocity / 127.0
        for index in range(start, end):
            age = index - start
            remaining = end - index
            envelope = min(1.0, age / attack, remaining / release)
            time = (index - start) / sample_rate
            fundamental = math.sin(2.0 * math.pi * frequency * time)
            overtone = 0.12 * math.sin(4.0 * math.pi * frequency * time)
            mix[index] += amplitude * envelope * (fundamental + overtone)

    peak = max((abs(value) for value in mix), default=0.0)
    scale = min(1.0, 0.92 / peak) if peak else 1.0
    pcm = array("h")
    for value in mix:
        sample = max(-32768, min(32767, round(value * scale * 32767)))
        pcm.extend((sample, sample))

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(destination), "wb") as output:
        output.setnchannels(2)
        output.setsampwidth(2)
        output.setframerate(sample_rate)
        output.writeframes(pcm.tobytes())
    return sample_count / sample_rate
