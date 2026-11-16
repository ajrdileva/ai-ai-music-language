"""Tick/second conversion for an MRM tempo map."""

from __future__ import annotations

from dataclasses import dataclass

from .model import MusicalReferenceModel


@dataclass(frozen=True, slots=True)
class TempoSegment:
    start_tick: int
    start_seconds: float
    microseconds_per_quarter: int


class TempoMap:
    def __init__(self, model: MusicalReferenceModel):
        segments: list[TempoSegment] = []
        seconds = 0.0
        previous_tick = 0
        previous_tempo = model.tempo[0].microseconds_per_quarter
        for tempo in model.tempo:
            seconds += (
                (tempo.at_tick - previous_tick)
                / model.ticks_per_quarter
                * previous_tempo
                / 1_000_000
            )
            segments.append(
                TempoSegment(tempo.at_tick, seconds, tempo.microseconds_per_quarter)
            )
            previous_tick = tempo.at_tick
            previous_tempo = tempo.microseconds_per_quarter
        self.ticks_per_quarter = model.ticks_per_quarter
        self.segments = tuple(segments)

    def tick_to_seconds(self, tick: int) -> float:
        if tick < 0:
            raise ValueError("tick must be non-negative")
        segment = self.segments[0]
        for candidate in self.segments[1:]:
            if candidate.start_tick > tick:
                break
            segment = candidate
        return segment.start_seconds + (
            (tick - segment.start_tick)
            / self.ticks_per_quarter
            * segment.microseconds_per_quarter
            / 1_000_000
        )
