from __future__ import annotations

import hashlib
from pathlib import Path
import shutil
import tempfile
import unittest

from iamp_engine.audio import render_wav
from iamp_engine.model import load_mrm
from iamp_engine.render import render_transmission
from iamp_engine.visual import VideoConfig


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples/reference-demo.mrm.json"
PROTOCOL = ROOT / "protocols/cp-000-baseline.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class RenderTests(unittest.TestCase):
    def test_audio_is_deterministic(self) -> None:
        model = load_mrm(FIXTURE)
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first.wav"
            second = Path(directory) / "second.wav"
            render_wav(model, first, sample_rate=8000, lead_seconds=0, tail_seconds=0)
            render_wav(model, second, sample_rate=8000, lead_seconds=0, tail_seconds=0)
            self.assertEqual(digest(first), digest(second))

    @unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg not installed")
    def test_end_to_end_smoke_render(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            manifest = render_transmission(
                mrm_path=FIXTURE,
                protocol_path=PROTOCOL,
                output_dir=output,
                transmission_id="T999",
                config=VideoConfig(
                    width=320,
                    height=180,
                    fps=4,
                    lead_seconds=0.25,
                    tail_seconds=0.25,
                ),
                sample_rate=8000,
            )
            self.assertEqual(manifest["status"], "generated")
            self.assertTrue((output / "T999.mp4").is_file())
            self.assertTrue((output / "T999.wav").is_file())
            self.assertTrue((output / "T999-thumbnail.png").is_file())
            self.assertTrue((output / "manifest.json").is_file())
            self.assertEqual(len(manifest["artifacts"]), 4)
            self.assertFalse(manifest["inputs"][0]["withheld"])
            self.assertIn("sha256", manifest["inputs"][0])

    @unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg not installed")
    def test_withheld_input_uses_commitment_not_raw_hash(self) -> None:
        commitment = "a" * 64
        with tempfile.TemporaryDirectory() as directory:
            manifest = render_transmission(
                mrm_path=FIXTURE,
                protocol_path=PROTOCOL,
                output_dir=Path(directory) / "output",
                transmission_id="T998",
                config=VideoConfig(width=320, height=180, fps=2, lead_seconds=0, tail_seconds=0),
                sample_rate=8000,
                ground_truth_commitment=commitment,
            )
            reference = manifest["inputs"][0]
            self.assertTrue(reference["withheld"])
            self.assertEqual(reference["commitment_sha256"], commitment)
            self.assertNotIn("sha256", reference)
            self.assertEqual(reference["path"], "withheld-ground-truth.mrm.json")


if __name__ == "__main__":
    unittest.main()
