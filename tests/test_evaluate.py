from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from jsonschema import Draft202012Validator

from iamp_engine.evaluate import evaluate_response


ROOT = Path(__file__).resolve().parents[1]
GROUND_TRUTH = ROOT / "examples/reference-demo.mrm.json"
RESPONSE_SCHEMA = ROOT / "schemas/receiver-response-000.schema.json"
IES_SCHEMA = ROOT / "schemas/ies-c000.schema.json"


def perfect_response() -> dict:
    truth = json.loads(GROUND_TRUTH.read_text())
    return {
        "schema": "RECEIVER-RESPONSE-000",
        "transmission_id": "T000",
        "protocol": {
            "id": "IAMP-CP-BASELINE",
            "version": "0.1.0",
            "recovered_without_extra_context": True,
        },
        "reconstructed_events": [
            {
                "id": f"rx-{index + 1:03d}",
                "pitch": event["pitch"],
                "onset_tick": event["onset_tick"],
                "duration_tick": event["duration_tick"],
                "velocity": event["velocity"],
                "confidence": 1.0,
            }
            for index, event in enumerate(truth["events"])
        ],
        "uncertainty": [],
        "context_used": ["frozen-test-package"],
    }


class EvaluationTests(unittest.TestCase):
    def _evaluate(self, response: dict) -> dict:
        with tempfile.TemporaryDirectory() as directory:
            response_path = Path(directory) / "response.json"
            report_path = Path(directory) / "report.json"
            response_path.write_text(json.dumps(response))
            report = evaluate_response(
                ground_truth_path=GROUND_TRUTH,
                response_path=response_path,
                response_schema_path=RESPONSE_SCHEMA,
                output_path=report_path,
                receiver_id="test-receiver",
                receiver_version="test-version",
            )
            self.assertTrue(report_path.is_file())
            schema = json.loads(IES_SCHEMA.read_text())
            Draft202012Validator(schema).validate(report)
            return report

    def test_perfect_response_passes(self) -> None:
        report = self._evaluate(perfect_response())
        self.assertEqual(report["verdict"]["status"], "pass")
        self.assertEqual(report["runs"][0]["metrics"]["event_f1"], 1.0)
        self.assertTrue(report["runs"][0]["metrics"]["overlap_relations_exact"])

    def test_omitted_event_fails(self) -> None:
        response = perfect_response()
        response["reconstructed_events"].pop()
        report = self._evaluate(response)
        self.assertEqual(report["verdict"]["status"], "fail")
        self.assertLess(report["runs"][0]["metrics"]["event_recall"], 1.0)

    def test_forbidden_context_fails(self) -> None:
        response = perfect_response()
        response["context_used"].append("withheld ground truth")
        report = self._evaluate(response)
        self.assertEqual(report["verdict"]["status"], "fail")
        self.assertTrue(report["runs"][0]["metrics"]["forbidden_context_used"])


if __name__ == "__main__":
    unittest.main()
