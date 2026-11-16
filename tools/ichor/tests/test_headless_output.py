#!/usr/bin/env python3
"""Verify that incomplete headless logs cannot report a successful run."""

import resource
import signal
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RUNNER = ROOT / "build/tools/ichor-mgba-headless"
ROM = ROOT / "pokeemerald.gba"


@unittest.skipUnless(RUNNER.is_file() and ROM.is_file(), "build the ROM and smoke runner first")
class HeadlessOutputTests(unittest.TestCase):
    def run_output(self, limited):
        with tempfile.TemporaryDirectory(prefix="headless-output-", dir=ROOT / "build") as directory:
            directory = Path(directory)
            script = directory / "output.lua"
            script.write_text(
                'for i = 1, 400 do console:log("OUTPUT CHECK line " .. i) end\n'
                'console:log("OUTPUT CHECK done")\n'
            )

            def limit_output():
                signal.signal(signal.SIGXFSZ, signal.SIG_IGN)
                resource.setrlimit(resource.RLIMIT_FSIZE, (4096, 4096))

            output = directory / "run.log"
            with output.open("w") as log:
                result = subprocess.run(
                    [str(RUNNER), "--script", str(script), "--frames", "2",
                     "--until", "OUTPUT CHECK done", str(ROM)],
                    cwd=ROOT, stdout=log, stderr=subprocess.PIPE, text=True,
                    preexec_fn=limit_output if limited else None, timeout=30,
                )
            return result, output.read_text()

    def test_complete_output(self):
        result, output = self.run_output(False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output.count("OUTPUT CHECK line "), 400)
        self.assertIn("OUTPUT CHECK done", output)
        self.assertIn("stopped after 0 frames (done)", output)

    def test_failed_write_is_not_success(self):
        result, output = self.run_output(True)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("could not write complete output", result.stderr)
        self.assertNotIn("OUTPUT CHECK done", output)


if __name__ == "__main__":
    unittest.main()
