from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from iamp_engine.model import MRMValidationError, parse_mrm
from iamp_engine.timing import TempoMap


ROOT = Path(__file__).resolve().parents[1]


def fixture() -> dict:
    return json.loads((ROOT / "examples/reference-demo.mrm.json").read_text())


class ModelTests(unittest.TestCase):
    def test_valid_polyphonic_reference(self) -> None:
        model = parse_mrm(fixture())
        self.assertEqual(len(model.events), 4)
        self.assertEqual(model.end_tick, 2880)
        self.assertEqual(model.groups[0]["members"], ["demo-n002", "demo-n003"])

    def test_pitch_must_be_scalar(self) -> None:
        data = fixture()
        data["events"][0]["pitch"] = [57, 60]
        with self.assertRaisesRegex(MRMValidationError, "pitch must be an integer"):
            parse_mrm(data)

    def test_event_ids_must_be_unique(self) -> None:
        data = fixture()
        data["events"][1]["id"] = data["events"][0]["id"]
        with self.assertRaisesRegex(MRMValidationError, "duplicate event ID"):
            parse_mrm(data)

    def test_group_references_must_exist(self) -> None:
        data = fixture()
        data["groups"][0]["members"].append("missing-note")
        with self.assertRaisesRegex(MRMValidationError, "unknown events"):
            parse_mrm(data)

    def test_duration_must_contain_all_events(self) -> None:
        data = fixture()
        data["duration_tick"] = 2000
        with self.assertRaisesRegex(MRMValidationError, "precedes the last event"):
            parse_mrm(data)

    def test_tempo_changes_integrate(self) -> None:
        data = copy.deepcopy(fixture())
        data["tempo"].append({"at_tick": 480, "microseconds_per_quarter": 1000000})
        model = parse_mrm(data)
        tempo = TempoMap(model)
        self.assertAlmostEqual(tempo.tick_to_seconds(480), 0.5)
        self.assertAlmostEqual(tempo.tick_to_seconds(960), 1.5)


if __name__ == "__main__":
    unittest.main()
