"""MRM-000 loading and semantic validation.

JSON Schema validation is useful at repository boundaries, but the engine keeps
its core validation dependency-free and checks invariants JSON Schema cannot
express, such as unique event IDs and valid group references.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any


_ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9._:-]{0,127}$")


class MRMValidationError(ValueError):
    """Raised when an MRM-000 document is structurally or semantically invalid."""


@dataclass(frozen=True, slots=True)
class TempoEvent:
    at_tick: int
    microseconds_per_quarter: int


@dataclass(frozen=True, slots=True)
class NoteEvent:
    id: str
    pitch: int
    onset_tick: int
    duration_tick: int
    velocity: int
    channel: int | None = None

    @property
    def end_tick(self) -> int:
        return self.onset_tick + self.duration_tick


@dataclass(frozen=True, slots=True)
class MusicalReferenceModel:
    id: str
    ticks_per_quarter: int
    tempo: tuple[TempoEvent, ...]
    duration_tick: int
    events: tuple[NoteEvent, ...]
    groups: tuple[dict[str, Any], ...]
    provenance: dict[str, Any]
    raw: dict[str, Any]

    @property
    def end_tick(self) -> int:
        return self.duration_tick


def _integer(value: Any, field: str, minimum: int, maximum: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise MRMValidationError(f"{field} must be an integer")
    if value < minimum or (maximum is not None and value > maximum):
        limit = f"..{maximum}" if maximum is not None else " or greater"
        raise MRMValidationError(f"{field} must be {minimum}{limit}")
    return value


def _stable_id(value: Any, field: str) -> str:
    if not isinstance(value, str) or not _ID_PATTERN.fullmatch(value):
        raise MRMValidationError(f"{field} is not a valid stable ID")
    return value


def parse_mrm(data: dict[str, Any]) -> MusicalReferenceModel:
    if not isinstance(data, dict):
        raise MRMValidationError("MRM document must be an object")
    if data.get("schema") != "MRM-000":
        raise MRMValidationError("schema must be MRM-000")

    model_id = _stable_id(data.get("id"), "id")
    timebase = data.get("timebase")
    if not isinstance(timebase, dict):
        raise MRMValidationError("timebase must be an object")
    ticks_per_quarter = _integer(
        timebase.get("ticks_per_quarter"), "timebase.ticks_per_quarter", 1
    )

    raw_tempo = data.get("tempo")
    if not isinstance(raw_tempo, list) or not raw_tempo:
        raise MRMValidationError("tempo must contain at least one event")
    tempo: list[TempoEvent] = []
    for index, item in enumerate(raw_tempo):
        if not isinstance(item, dict):
            raise MRMValidationError(f"tempo[{index}] must be an object")
        tempo.append(
            TempoEvent(
                _integer(item.get("at_tick"), f"tempo[{index}].at_tick", 0),
                _integer(
                    item.get("microseconds_per_quarter"),
                    f"tempo[{index}].microseconds_per_quarter",
                    1,
                ),
            )
        )
    tempo.sort(key=lambda event: event.at_tick)
    if tempo[0].at_tick != 0:
        raise MRMValidationError("the first tempo event must start at tick 0")
    if len({event.at_tick for event in tempo}) != len(tempo):
        raise MRMValidationError("tempo event ticks must be unique")

    raw_events = data.get("events")
    if not isinstance(raw_events, list):
        raise MRMValidationError("events must be an array")
    events: list[NoteEvent] = []
    event_ids: set[str] = set()
    for index, item in enumerate(raw_events):
        if not isinstance(item, dict) or item.get("type") != "note":
            raise MRMValidationError(f"events[{index}] must be a note object")
        event_id = _stable_id(item.get("id"), f"events[{index}].id")
        if event_id in event_ids:
            raise MRMValidationError(f"duplicate event ID: {event_id}")
        event_ids.add(event_id)
        channel = item.get("channel")
        events.append(
            NoteEvent(
                id=event_id,
                pitch=_integer(item.get("pitch"), f"events[{index}].pitch", 0, 127),
                onset_tick=_integer(
                    item.get("onset_tick"), f"events[{index}].onset_tick", 0
                ),
                duration_tick=_integer(
                    item.get("duration_tick"), f"events[{index}].duration_tick", 1
                ),
                velocity=_integer(
                    item.get("velocity"), f"events[{index}].velocity", 0, 127
                ),
                channel=(
                    None
                    if channel is None
                    else _integer(channel, f"events[{index}].channel", 0, 15)
                ),
            )
        )
    events.sort(key=lambda event: (event.onset_tick, event.pitch, event.id))
    duration_tick = _integer(data.get("duration_tick"), "duration_tick", 0)
    last_event_tick = max((event.end_tick for event in events), default=0)
    if duration_tick < last_event_tick:
        raise MRMValidationError(
            f"duration_tick {duration_tick} precedes the last event ending at {last_event_tick}"
        )

    raw_groups = data.get("groups", [])
    if not isinstance(raw_groups, list):
        raise MRMValidationError("groups must be an array")
    group_ids: set[str] = set()
    for index, group in enumerate(raw_groups):
        if not isinstance(group, dict):
            raise MRMValidationError(f"groups[{index}] must be an object")
        group_id = _stable_id(group.get("id"), f"groups[{index}].id")
        if group_id in group_ids:
            raise MRMValidationError(f"duplicate group ID: {group_id}")
        group_ids.add(group_id)
        members = group.get("members")
        if not isinstance(members, list) or not members:
            raise MRMValidationError(f"groups[{index}].members must not be empty")
        unknown = set(members) - event_ids
        if unknown:
            raise MRMValidationError(
                f"groups[{index}] references unknown events: {sorted(unknown)}"
            )

    provenance = data.get("provenance")
    if not isinstance(provenance, dict):
        raise MRMValidationError("provenance must be an object")
    for field in ("source_type", "source_id", "transformations"):
        if field not in provenance:
            raise MRMValidationError(f"provenance.{field} is required")

    return MusicalReferenceModel(
        id=model_id,
        ticks_per_quarter=ticks_per_quarter,
        tempo=tuple(tempo),
        duration_tick=duration_tick,
        events=tuple(events),
        groups=tuple(raw_groups),
        provenance=provenance,
        raw=data,
    )


def load_mrm(path: str | Path) -> MusicalReferenceModel:
    source = Path(path)
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MRMValidationError(f"cannot load {source}: {exc}") from exc
    return parse_mrm(data)
