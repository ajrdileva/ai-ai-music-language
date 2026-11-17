from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - allows runtime-only installations
    Draft202012Validator = None


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipIf(Draft202012Validator is None, "install the dev extra for schema tests")
class SchemaTests(unittest.TestCase):
    def test_all_schemas_are_valid_draft_2020_12(self) -> None:
        for path in sorted((ROOT / "schemas").glob("*.json")):
            with self.subTest(path=path.name):
                Draft202012Validator.check_schema(json.loads(path.read_text()))

    def test_public_mrm_example(self) -> None:
        schema = json.loads((ROOT / "schemas/mrm-000.schema.json").read_text())
        instance = json.loads((ROOT / "examples/reference-demo.mrm.json").read_text())
        Draft202012Validator(schema).validate(instance)

    def test_baseline_protocol(self) -> None:
        schema = json.loads((ROOT / "schemas/cp-000.schema.json").read_text())
        instance = json.loads((ROOT / "protocols/cp-000-baseline.json").read_text())
        Draft202012Validator(schema).validate(instance)

    def test_t000_ground_truth_commitment(self) -> None:
        schema = json.loads((ROOT / "schemas/ground-truth-commitment-000.schema.json").read_text())
        instance = json.loads((ROOT / "transmissions/T000/ground-truth-commitment.json").read_text())
        Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(instance)

    def test_t000_receiver_package(self) -> None:
        schema = json.loads((ROOT / "schemas/receiver-package-000.schema.json").read_text())
        instance = json.loads((ROOT / "transmissions/T000/receiver-package.json").read_text())
        Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(instance)

    def test_t000_youtube_publication_record(self) -> None:
        schema = json.loads((ROOT / "schemas/publication-record-000.schema.json").read_text())
        instance = json.loads((ROOT / "transmissions/T000/publications/youtube.json").read_text())
        Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(instance)

    def test_t000_replication_batch_plan(self) -> None:
        schema = json.loads((ROOT / "schemas/replication-batch-plan-000.schema.json").read_text())
        instance = json.loads((ROOT / "replications/T000/batch-001/batch-plan.json").read_text())
        Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(instance)

    def test_t000_receiver_roster(self) -> None:
        schema = json.loads((ROOT / "schemas/receiver-roster-000.schema.json").read_text())
        roster = json.loads((ROOT / "replications/T000/batch-001/roster.json").read_text())
        Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(roster)

        slots = roster["slots"]
        self.assertEqual(len({slot["slot_id"] for slot in slots}), 8)
        self.assertEqual(len({slot["planned_run_id"] for slot in slots}), 8)
        family_counts: dict[str, int] = {}
        for slot in slots:
            family_counts[slot["model_family"]] = family_counts.get(slot["model_family"], 0) + 1
        self.assertEqual(len(family_counts), 4)
        self.assertTrue(all(count == 2 for count in family_counts.values()))
        self.assertGreaterEqual(
            sum(slot["isolation_level"] == "technical" for slot in slots),
            4,
        )

    def test_t000_replication_templates(self) -> None:
        run_schema = json.loads((ROOT / "schemas/receiver-run-metadata-000.schema.json").read_text())
        run_template = json.loads((ROOT / "replications/T000/batch-001/run-metadata.template.json").read_text())
        Draft202012Validator(run_schema, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(run_template)

        report_schema = json.loads((ROOT / "schemas/replication-batch-report-000.schema.json").read_text())
        report_template = json.loads((ROOT / "replications/T000/batch-001/aggregate-report.template.json").read_text())
        Draft202012Validator(report_schema, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(report_template)
        plan_content = (ROOT / "replications/T000/batch-001/batch-plan.json").read_bytes()
        self.assertEqual(hashlib.sha256(plan_content).hexdigest(), report_template["plan_sha256"])

    def test_t000_replication_candidate_lock_hashes(self) -> None:
        plan = json.loads((ROOT / "replications/T000/batch-001/batch-plan.json").read_text())
        for record in plan["candidate_lock"]["files"]:
            with self.subTest(path=record["path"]):
                content = (ROOT / record["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(content).hexdigest(), record["sha256"])

        evaluator = plan["candidate_lock"]["evaluator"]
        evaluator_content = (ROOT / evaluator["source"]).read_bytes()
        self.assertEqual(hashlib.sha256(evaluator_content).hexdigest(), evaluator["source_sha256"])

        for record in plan["execution_lock"]["files"]:
            with self.subTest(execution_path=record["path"]):
                content = (ROOT / record["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(content).hexdigest(), record["sha256"])


if __name__ == "__main__":
    unittest.main()
