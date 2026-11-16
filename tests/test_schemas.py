from __future__ import annotations

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


if __name__ == "__main__":
    unittest.main()
