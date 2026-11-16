"""Preregistered T000 communication evaluator.

This module implements the matching rules and confirmatory threshold declared in
transmissions/T000/EXPERIMENT.md. It is intentionally separate from the renderer.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator

from .manifest import write_json
from .model import MusicalReferenceModel, NoteEvent, load_mrm


@dataclass(frozen=True, slots=True)
class Match:
    truth_index: int
    response_index: int
    onset_error: int
    duration_error: int
    velocity_error: int


def _load_json(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def _response_notes(response: dict[str, Any]) -> list[NoteEvent]:
    notes: list[NoteEvent] = []
    identifiers: set[str] = set()
    for item in response["reconstructed_events"]:
        if item["id"] in identifiers:
            raise ValueError(f"duplicate response event ID: {item['id']}")
        identifiers.add(item["id"])
        notes.append(
            NoteEvent(
                id=item["id"],
                pitch=item["pitch"],
                onset_tick=item["onset_tick"],
                duration_tick=item["duration_tick"],
                velocity=item["velocity"],
            )
        )
    return notes


def match_events(
    truth: tuple[NoteEvent, ...],
    response: list[NoteEvent],
    *,
    onset_tolerance: int = 60,
) -> list[Match]:
    candidates: list[tuple[int, int, int, int]] = []
    for truth_index, expected in enumerate(truth):
        for response_index, observed in enumerate(response):
            onset_error = abs(expected.onset_tick - observed.onset_tick)
            if expected.pitch == observed.pitch and onset_error <= onset_tolerance:
                candidates.append(
                    (
                        onset_error,
                        abs(expected.duration_tick - observed.duration_tick),
                        truth_index,
                        response_index,
                    )
                )
    candidates.sort()
    used_truth: set[int] = set()
    used_response: set[int] = set()
    matches: list[Match] = []
    for onset_error, duration_error, truth_index, response_index in candidates:
        if truth_index in used_truth or response_index in used_response:
            continue
        used_truth.add(truth_index)
        used_response.add(response_index)
        matches.append(
            Match(
                truth_index=truth_index,
                response_index=response_index,
                onset_error=onset_error,
                duration_error=duration_error,
                velocity_error=abs(
                    truth[truth_index].velocity - response[response_index].velocity
                ),
            )
        )
    return sorted(matches, key=lambda match: match.truth_index)


def _relations(
    notes: tuple[NoteEvent, ...] | list[NoteEvent],
    predicate: Callable[[NoteEvent, NoteEvent], bool],
) -> set[tuple[int, int]]:
    return {
        (left, right)
        for left in range(len(notes))
        for right in range(left + 1, len(notes))
        if predicate(notes[left], notes[right])
    }


def _relation_exact(
    truth: tuple[NoteEvent, ...],
    response: list[NoteEvent],
    matches: list[Match],
    predicate: Callable[[NoteEvent, NoteEvent], bool],
) -> bool:
    if len(matches) != len(truth) or len(matches) != len(response):
        return False
    response_to_truth = {match.response_index: match.truth_index for match in matches}
    observed = {
        tuple(sorted((response_to_truth[left], response_to_truth[right])))
        for left, right in _relations(response, predicate)
    }
    return observed == _relations(truth, predicate)


def evaluate_response(
    *,
    ground_truth_path: str | Path,
    response_path: str | Path,
    response_schema_path: str | Path,
    output_path: str | Path,
    receiver_id: str,
    receiver_version: str,
    evaluation_id: str = "T000-IES-C000-RUN-001",
) -> dict[str, Any]:
    truth_model: MusicalReferenceModel = load_mrm(ground_truth_path)
    response = _load_json(response_path)
    response_schema = _load_json(response_schema_path)
    validator = Draft202012Validator(
        response_schema,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )
    errors = sorted(validator.iter_errors(response), key=lambda error: list(error.path))
    if errors:
        summary = "; ".join(error.message for error in errors[:5])
        raise ValueError(f"receiver response schema validation failed: {summary}")

    observed = _response_notes(response)
    matches = match_events(truth_model.events, observed, onset_tolerance=60)
    matched = len(matches)
    truth_count = len(truth_model.events)
    response_count = len(observed)
    precision = matched / response_count if response_count else 0.0
    recall = matched / truth_count if truth_count else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    onset_mae = sum(match.onset_error for match in matches) / matched if matched else 0.0
    duration_mae = sum(match.duration_error for match in matches) / matched if matched else 0.0
    velocity_mae = sum(match.velocity_error for match in matches) / matched if matched else 0.0
    onset_within = sum(match.onset_error <= 60 for match in matches) / truth_count if truth_count else 1.0
    duration_within = sum(match.duration_error <= 60 for match in matches) / truth_count if truth_count else 1.0
    velocity_within = sum(match.velocity_error <= 8 for match in matches) / truth_count if truth_count else 1.0

    simultaneous = lambda left, right: left.onset_tick == right.onset_tick
    common_ending = lambda left, right: left.end_tick == right.end_tick
    overlap = lambda left, right: max(left.onset_tick, right.onset_tick) < min(left.end_tick, right.end_tick)
    simultaneous_exact = _relation_exact(truth_model.events, observed, matches, simultaneous)
    common_ending_exact = _relation_exact(truth_model.events, observed, matches, common_ending)
    overlap_exact = _relation_exact(truth_model.events, observed, matches, overlap)

    protocol = response["protocol"]
    protocol_recovered = (
        protocol["id"] == "IAMP-CP-BASELINE"
        and protocol["version"] == "0.1.0"
        and protocol["recovered_without_extra_context"] is True
    )
    context_disclosed = bool(response["context_used"])
    forbidden_markers = (
        ".private/",
        "withheld ground truth",
        "commitment-secret",
        "prior conversation",
        "another receiver",
    )
    forbidden_context_used = any(
        marker in source.lower()
        for source in response["context_used"]
        for marker in forbidden_markers
    )
    passed = all(
        (
            protocol_recovered,
            precision == 1.0,
            recall == 1.0,
            f1 == 1.0,
            onset_within == 1.0,
            duration_within == 1.0,
            simultaneous_exact,
            common_ending_exact,
            overlap_exact,
            context_disclosed,
            not forbidden_context_used,
        )
    )

    match_records = [
        {
            "truth_event_id": truth_model.events[match.truth_index].id,
            "response_event_id": observed[match.response_index].id,
            "onset_error_ticks": match.onset_error,
            "duration_error_ticks": match.duration_error,
            "velocity_error": match.velocity_error,
        }
        for match in matches
    ]
    metrics = {
        "event_precision": precision,
        "event_recall": recall,
        "event_f1": f1,
        "pitch_accuracy": matched / truth_count if truth_count else 1.0,
        "onset_mae_ticks": onset_mae,
        "onset_within_60_ticks": onset_within,
        "duration_mae_ticks": duration_mae,
        "duration_within_60_ticks": duration_within,
        "velocity_mae": velocity_mae,
        "velocity_within_8_units": velocity_within,
        "overlap_recovery": 1.0 if overlap_exact else 0.0,
        "protocol_recovered": protocol_recovered,
        "context_disclosed": context_disclosed,
        "forbidden_context_used": forbidden_context_used,
        "simultaneous_relations_exact": simultaneous_exact,
        "common_ending_relations_exact": common_ending_exact,
        "overlap_relations_exact": overlap_exact,
        "truth_event_count": truth_count,
        "response_event_count": response_count,
        "matched_event_count": matched,
        "matches": match_records,
    }
    verdict_summary = (
        "All preregistered T000 communication thresholds passed."
        if passed
        else "One or more preregistered T000 communication thresholds failed."
    )
    report = {
        "schema": "IES-C000",
        "evaluation_id": evaluation_id,
        "transmission_id": "T000",
        "independence": {
            "evaluator_id": "iamp-t000-evaluator",
            "evaluator_version": "0.1.0",
            "candidate_authored_verdict": False,
            "rationale": "Scoring code and thresholds were committed before the receiver run; the receiver does not assign the verdict.",
        },
        "configuration": {
            "receiver": {"id": receiver_id, "version": receiver_version},
            "context_provided": response["context_used"],
            "ground_truth_ref": "transmissions/T000/reveal/ground-truth.mrm.json",
            "metrics_preregistered": True,
            "tolerances": {"onset_ticks": 60, "duration_ticks": 60, "velocity_units_secondary": 8},
        },
        "runs": [
            {
                "run_id": "run-001",
                "raw_response_ref": Path(response_path).name,
                "metrics": metrics,
            }
        ],
        "verdict": {"status": "pass" if passed else "fail", "summary": verdict_summary},
        "limitations": [
            "This is a single receiver run.",
            "CP-000 directly labels the MIDI pitch axis and is a baseline rather than a compressed protocol.",
            "Velocity is reported as a secondary, non-gating metric in v0.1.",
        ],
    }
    write_json(output_path, report)
    return report
