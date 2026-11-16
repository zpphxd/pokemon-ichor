import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LAUNCHER = ROOT / "tools/ichor/tests/slice_playthrough.sh"


class SlicePolicyTests(unittest.TestCase):
    def setUp(self):
        (ROOT / "build").mkdir(exist_ok=True)
        directory = tempfile.TemporaryDirectory(prefix="slice-policy-", dir=ROOT / "build")
        self.addCleanup(directory.cleanup)
        self.out = Path(directory.name)
        self.receipts = []
        for folder, name in (("shots", "keep.png"), ("states", "keep.ss")):
            path = self.out / folder / name
            path.parent.mkdir()
            path.write_bytes(b"existing playthrough evidence")
            self.receipts.append(path)
        self.env = {key: value for key, value in os.environ.items()
                    if not key.startswith("SLICE_")}
        self.env["SLICE_OUT"] = str(self.out)

    def rejected(self, options, reason):
        result = subprocess.run(
            [str(LAUNCHER), str(self.out / "missing.gba")],
            cwd=ROOT, env=self.env | options, capture_output=True, text=True, timeout=10,
        )
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn(reason, output)
        self.assertNotIn("SLICE PASS", output)
        self.assertNotIn("SLICE PARTIAL PASS", output)
        for path in self.receipts:
            self.assertEqual(path.read_bytes(), b"existing playthrough evidence")

    def test_invalid_options_preserve_evidence(self):
        cases = (
            ({"SLICE_NATURAL": "invalid"}, "SLICE_NATURAL must be"),
            ({"SLICE_STARTER": "3"}, "SLICE_STARTER must be"),
            ({"SLICE_DIFFICULTY": "invalid"}, "unknown SLICE_DIFFICULTY"),
            ({"SLICE_GENDER": "invalid"}, "SLICE_GENDER must be"),
        )
        for options, reason in cases:
            with self.subTest(options=options):
                self.rejected(options, reason)

    def test_natural_rejects_assistance_before_touching_evidence(self):
        for options in ({"SLICE_FROM": "04_kleon"}, {"SLICE_WORKAROUNDS": "1"}):
            with self.subTest(options=options):
                self.rejected(options | {"SLICE_NATURAL": "1"}, "cannot resume")

    def test_invalid_beats_preserve_evidence(self):
        cases = (
            ({"SLICE_FROM": "missing"}, "unknown beat missing"),
            ({"SLICE_STOP_AFTER": "missing"}, "unknown beat missing"),
            ({"SLICE_FROM": "05_route1", "SLICE_STOP_AFTER": "04_kleon"},
             "requested beat range"),
        )
        for options, reason in cases:
            with self.subTest(options=options):
                self.rejected(options, reason)

    def test_all_declared_beats_are_accepted_by_preflight(self):
        script = LAUNCHER.with_suffix(".lua").read_text()
        beats = re.findall(r'^beat\("([^"]+)", function\(\)', script, re.MULTILINE)
        self.assertTrue(beats)
        for beat in beats:
            for option in ("SLICE_FROM", "SLICE_STOP_AFTER"):
                with self.subTest(option=option, beat=beat):
                    self.rejected({option: beat}, "missing (run make first)")

    def test_empty_optional_settings_use_defaults(self):
        self.rejected({"SLICE_NATURAL": "1", "SLICE_FROM": "", "SLICE_STOP_AFTER": ""},
                      "missing (run make first)")


if __name__ == "__main__":
    unittest.main()
