from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


class ReceiverMediaAdapterTests(unittest.TestCase):
    @unittest.skipIf(shutil.which("ffmpeg") is None, "ffmpeg is required")
    def test_t000_adapter_produces_neutral_views(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "adapter"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools/prepare_receiver_media.py"),
                    "--video",
                    str(ROOT / "transmissions/T000/artifacts/T000.mp4"),
                    "--audio",
                    str(ROOT / "transmissions/T000/artifacts/T000.wav"),
                    "--output-dir",
                    str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(json.loads(result.stdout)["outputs"], 24)
            manifest = json.loads((output / "adapter-manifest.json").read_text())
            schema = json.loads(
                (ROOT / "schemas/receiver-media-adapter-manifest-000.schema.json").read_text()
            )
            Draft202012Validator(schema).validate(manifest)
            self.assertEqual(manifest["schema"], "RMA-000")
            self.assertTrue(manifest["derived_not_candidate"])
            self.assertEqual(len(list(output.glob("video-frame-*.png"))), 22)
            self.assertEqual(len(manifest["outputs"]), 24)
            self.assertIn("pitch detection", manifest["forbidden_operations"])
            self.assertFalse(
                any(
                    argument.startswith("/")
                    for command in manifest["commands"]
                    for argument in command
                )
            )

            repeated_output = Path(temp_dir) / "adapter-repeated"
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools/prepare_receiver_media.py"),
                    "--video",
                    str(ROOT / "transmissions/T000/artifacts/T000.mp4"),
                    "--audio",
                    str(ROOT / "transmissions/T000/artifacts/T000.wav"),
                    "--output-dir",
                    str(repeated_output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            repeated_manifest = json.loads(
                (repeated_output / "adapter-manifest.json").read_text()
            )
            self.assertEqual(
                [record["sha256"] for record in manifest["outputs"]],
                [record["sha256"] for record in repeated_manifest["outputs"]],
            )


class ReceiverCaptureTests(unittest.TestCase):
    def test_capture_is_byte_preserving_and_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temporary = Path(temp_dir)
            source = temporary / "answer.txt"
            source.write_bytes(b'{"not": "schema-valid"}\n')
            run_dir = temporary / "run"
            command = [
                sys.executable,
                str(ROOT / "tools/capture_receiver_output.py"),
                "--source",
                str(source),
                "--run-dir",
                str(run_dir),
                "--run-id",
                "T000-RUN-002",
                "--slot-id",
                "T000-SLOT-001",
                "--receiver-model-id",
                "test-model",
                "--response-schema",
                str(ROOT / "schemas/receiver-response-000.schema.json"),
            ]
            first = subprocess.run(command, check=True, capture_output=True, text=True)
            self.assertEqual(json.loads(first.stdout)["status"], "captured")
            self.assertEqual((run_dir / "raw-response.txt").read_bytes(), source.read_bytes())
            manifest = json.loads((run_dir / "capture-manifest.json").read_text())
            schema = json.loads(
                (ROOT / "schemas/receiver-output-capture-000.schema.json").read_text()
            )
            Draft202012Validator(
                schema,
                format_checker=Draft202012Validator.FORMAT_CHECKER,
            ).validate(manifest)
            self.assertTrue(manifest["raw_response"]["byte_preserved"])
            self.assertFalse(manifest["checks"]["receiver_schema_valid"])
            self.assertFalse(manifest["scored"])

            second = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(second.returncode, 1)
            self.assertIn("refusing to overwrite", second.stderr)
