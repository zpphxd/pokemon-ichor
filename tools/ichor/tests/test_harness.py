"""Host-only regression tests; no ROM, compiler, or mGBA installation required."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location("ichor_check", ROOT / "tools/ichor/check.py")
check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check)
HELPER = ROOT / "tools/ichor/tests/harness.sh"


class VerdictTests(unittest.TestCase):
    def result(self, text, code=0, marker="SAVE done"):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "run.log"
            log.write_text(text)
            return subprocess.run(
                ["bash", "-c", '. "$1"; harness_result SAVE "$2" "$3" "$4"',
                 "test", str(HELPER), str(log), str(code), marker],
                capture_output=True, text=True)

    def test_success(self):
        self.assertEqual(self.result("[Scripting] SAVE ok state\n[Scripting] SAVE done\n").returncode, 0)

    def test_completion_never_overrides_exit_failure(self):
        for code in (1, 2, 124, 137):
            with self.subTest(code=code):
                self.assertNotEqual(self.result("SAVE done\n", code).returncode, 0)

    def test_failure_markers(self):
        for text in ("SAVE FAIL: state", "SAVE BUG missing reward", "Assertion failed",
                     "invalid address", "Illegal opcode", "undefined instruction",
                     "bad write", "abort"):
            with self.subTest(text=text):
                self.assertNotEqual(self.result(text + "\nSAVE done\n").returncode, 0)

    def test_missing_completion(self):
        self.assertNotEqual(self.result("SAVE ok state\n").returncode, 0)

    def test_custom_completion(self):
        self.assertEqual(self.result("SAVE SUMMARY\n", marker="SAVE SUMMARY").returncode, 0)

    def test_missing_log(self):
        result = subprocess.run(
            ["bash", "-c", '. "$1"; harness_result SAVE "$2" 0', "test",
             str(HELPER), "/no/such/ichor-fixture.log"], capture_output=True)
        self.assertNotEqual(result.returncode, 0)

    def test_missing_prerequisite_is_explicit(self):
        result = subprocess.run(
            ["bash", "-c", '. "$1"; harness_require ichor-nonexistent-tool "install tool"',
             "test", str(HELPER)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing ichor-nonexistent-tool", result.stderr)

    def test_explicit_python_environment_precedes_fallback_tools(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            for subdir in ("selected", ".local/bin"):
                executable = home / subdir / "python3"
                executable.parent.mkdir(parents=True)
                executable.write_text("#!/bin/bash\nexit 0\n")
                executable.chmod(0o755)
            result = subprocess.run(
                ["bash", "-c", 'HOME="$2"; PATH="$2/selected:$PATH"; . "$1"; command -v python3',
                 "test", str(HELPER), str(home)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.strip(), str(home / "selected/python3"))

    def test_wrappers_do_not_bypass_the_python_environment(self):
        for wrapper in (ROOT / "tools/ichor").rglob("*.sh"):
            with self.subTest(wrapper=wrapper.relative_to(ROOT)):
                self.assertNotIn("/usr/bin/python3", wrapper.read_text())

    def test_no_unbounded_fallback(self):
        result = subprocess.run(
            ["bash", "-c", '. "$1"; PATH=/no-tools; harness_timeout', "test", str(HELPER)],
            capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("coreutils", result.stderr)

    def test_cached_runner_cannot_hide_compile_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runner = root / "build/tools/ichor-mgba-headless"
            runner.parent.mkdir(parents=True)
            runner.write_text("#!/bin/bash\nexit 0\n")
            runner.chmod(0o755)
            for name, code in (("cc", 13), ("timeout", 0)):
                script = root / name
                script.write_text(f"#!/bin/bash\nexit {code}\n")
                script.chmod(0o755)
            env = os.environ.copy()
            env["MGBA_PREFIX"] = str(root)
            result = subprocess.run(
                ["bash", "-c", '. "$1"; PATH="$2:$PATH"; harness_prepare',
                 "test", str(HELPER), str(root)], cwd=root, env=env,
                capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Lua-capable mGBA", result.stderr)

    def test_failed_setup_pipeline(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            preproc = root / "tools/preproc/preproc"
            preproc.parent.mkdir(parents=True)
            preproc.write_text('#!/bin/bash\nif [ "$1" = -s ]; then exit 17; fi\n/bin/cat\n')
            preproc.chmod(0o755)
            for tool in ("arm-none-eabi-cpp", "arm-none-eabi-as"):
                script = root / tool
                script.write_text("#!/bin/bash\n/bin/cat\n")
                script.chmod(0o755)
            result = subprocess.run(
                ["bash", "-c", '. "$1"; PATH="$2:$PATH"; harness_assemble setup.s setup.o',
                 "test", str(HELPER), str(root)], cwd=root, capture_output=True)
            self.assertEqual(result.returncode, 17)


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.suites = check.load_suites()

    def test_fast_needs_no_rom(self):
        self.assertEqual(set(check.select(self.suites, "fast", [])), check.FAST)

    def test_shared_engine_falls_back_to_full(self):
        for path in ("src/event_data.c", "include/ichor_save.h", "data/scripts/ichor.pory",
                     "graphics/fonts/normal.png", "tools/ichor/tests/harness.sh",
                     "src/data/wild_encounters.json", "unknown-gameplay-file.c",
                     "data/maps/UncoveredChapter/scripts.pory"):
            with self.subTest(path=path):
                self.assertEqual(set(check.select(self.suites, "changed", [path])), set(self.suites))

    def test_owning_area_and_neighbors(self):
        selected = check.select(self.suites, "changed", ["data/maps/KallisteRoute1/scripts.pory"])
        self.assertTrue({"opening"}.isdisjoint(selected))
        self.assertTrue({"route1", "seam", "slice", "sidechecks"} <= selected.keys())
        self.assertTrue(check.CORE <= selected.keys())

    def test_sidechecks_require_current_slice(self):
        ordered = check.ordered(self.suites, {"sidechecks"})
        self.assertLess(ordered.index("slice"), ordered.index("sidechecks"))
        self.assertLess(ordered.index("build"), ordered.index("slice"))

    def test_full_contains_every_suite(self):
        self.assertEqual(set(check.ordered(self.suites, set(self.suites))), set(self.suites))

    def test_unknown_selector_fails(self):
        with self.assertRaises(ValueError):
            check.ordered(self.suites, {"typo"})

    def test_missing_and_cyclic_dependencies_fail(self):
        for deps in (["missing"], ["one"]):
            with self.subTest(deps=deps), self.assertRaises(ValueError):
                check.ordered({"one": {"deps": deps}}, {"one"})

    def test_invalid_base_never_means_empty_diff(self):
        with self.assertRaises(subprocess.CalledProcessError):
            check.changed_paths("ichor-no-such-ref")

    def test_diff_includes_commits_staged_unstaged_untracked(self):
        with mock.patch.object(check, "git", side_effect=["base\n", "committed\0old\0",
                                                        "staged\0unstaged\0", "new\0"]):
            self.assertEqual(check.changed_paths("main"),
                             ["committed", "new", "old", "staged", "unstaged"])

    def test_registry_has_all_emulator_wrappers(self):
        excluded = {"elaia_symbols.sh", "slice_symbols.sh", "engine_build.sh",
                    "harness.sh", "slice_gallery.sh"}
        registered = {Path(arg).name for row in self.suites.values()
                      for arg in row["command"] if arg.endswith(".sh")}
        existing = {p.name for p in (ROOT / "tools/ichor/tests").glob("*.sh")} - excluded
        self.assertTrue(existing <= registered, existing - registered)


class StructuralTests(unittest.TestCase):
    def test_map_regression_retains_baseline_and_rejects_new_findings(self):
        baseline = {"maps": 1, "findings": [{"map": "Old", "level": "FAIL", "message": "old"}]}
        for changed, expected in ((baseline, 0),
                                  ({"maps": 2, "findings": baseline["findings"] +
                                    [{"map": "New", "level": "FAIL", "message": "new"}]}, 1)):
            results = [subprocess.CompletedProcess([], 1, json.dumps(changed), ""),
                       subprocess.CompletedProcess([], 1, json.dumps(baseline), "")]
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as directory, \
                    mock.patch.object(check, "ROOT", Path(directory)), \
                    mock.patch.object(check, "git", side_effect=["base\n", "head\n"]), \
                    mock.patch.object(check.subprocess, "run", side_effect=results):
                self.assertEqual(check.map_regression("main", []), expected)

    def test_clean_revision_cannot_be_its_own_map_baseline(self):
        with mock.patch.object(check, "git", side_effect=["head\n", "head\n"]), \
                mock.patch.object(check, "changed_paths", return_value=[]), \
                self.assertRaises(ValueError):
            check.map_regression("main", [])

    def test_claim_bounds_and_duplicates(self):
        lines = ["// Ichor bank vars: claim.py bankvar adds lines here, in order.",
                 "#define VAR_ONE (ICHOR_VARS_START + 0x000) // one",
                 "#define VAR_TWO (ICHOR_VARS_START + 0x000) // duplicate",
                 "#define VAR_THREE (ICHOR_VARS_START + 0x020) // outside",
                 "// Ichor bank vars: end"]
        errors = check.claims_errors(lines, "Ichor bank vars", {"ICHOR_VARS_START": 32})
        self.assertEqual(len(errors), 2)

    def test_reserved_aliases_outside_claim_blocks_are_valid(self):
        lines = ["#define ALIAS START", "// Ichor bank vars: claim.py",
                 "#define VAR_ONE (ICHOR_VARS_START + 0x01F)",
                 "// Ichor bank vars: end"]
        self.assertEqual(check.claims_errors(lines, "Ichor bank vars", {"ICHOR_VARS_START": 32}), [])

    def test_missing_or_malformed_claim_block_fails(self):
        self.assertTrue(check.claims_errors([], "Ichor bank vars", {"ICHOR_VARS_START": 32}))

    def test_exact_rom_ceiling(self):
        with tempfile.TemporaryDirectory() as directory:
            rom = Path(directory) / "test.gba"
            with rom.open("wb") as output:
                output.truncate(check.ROM_LIMIT)
            self.assertEqual(check.budget(rom), 0)
            with rom.open("ab") as output:
                output.write(b"x")
            self.assertEqual(check.budget(rom), 1)
            rom.write_bytes(b"")
            self.assertEqual(check.budget(rom), 1)


class TextRendererTests(unittest.TestCase):
    def report(self, records):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "run.log"
            log.write_text(records)
            return subprocess.run(
                [sys.executable, str(ROOT / "tools/ichor/tests/slice_text_report.py"), str(log)],
                capture_output=True, text=True)

    def test_normal_field_three_lines_still_fail(self):
        result = self.report("SIDE TEXT 1 0,0 BBFEBCFEBD\n")
        self.assertEqual(result.returncode, 0)
        self.assertIn("TALL page 1 has 3 lines", result.stdout)

    def test_recovery_uses_measured_window(self):
        result = self.report("SIDE TEXT 1 0,0 BBFEBCFEBD 238,5\n")
        self.assertEqual(result.returncode, 0)
        self.assertIn("0 tall pages", result.stdout)

    def test_recovery_overflow_still_fails(self):
        result = self.report("SIDE TEXT 1 0,0 BBFEBCFEBD 238,2\n")
        self.assertIn("TALL page 1 has 3 lines", result.stdout)

    def test_same_text_in_different_renderers_is_not_deduplicated(self):
        result = self.report("SIDE TEXT 1 0,0 BBFEBCFEBD 238,5\nSIDE TEXT 1 0,0 BBFEBCFEBD\n")
        self.assertIn("2 messages", result.stdout)
        self.assertIn("1 tall pages", result.stdout)

    def test_width_is_checked_against_recorded_geometry(self):
        result = self.report("SIDE TEXT 1 0,0 BBBBBB 1,5\n")
        self.assertIn("WIDE ", result.stdout)

    def test_scrolling_still_fits_field_box(self):
        result = self.report("SIDE TEXT 1 0,0 BBFEBCFABD\n")
        self.assertIn("0 tall pages", result.stdout)

    def test_invalid_geometry_is_an_error(self):
        for bounds in ("0,5", "238,0", "wide,5"):
            with self.subTest(bounds=bounds):
                result = self.report(f"SIDE TEXT 1 0,0 BB {bounds}\n")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("recorded text", result.stderr)


class ExecutionTests(unittest.TestCase):
    def test_native_counts_preserve_colored_result_categories(self):
        counts = {"KNOWN_FAILING": 19, "TO_DO": 419, "EXPECT_FAILING": 9,
                  "PASSED": 5486, "TOTAL": 5933}
        output = "\n".join(f"- Tests \x1b[32m{key}\x1b[0m: {value}"
                           for key, value in counts.items())
        suites = {"expansion": {"command": [sys.executable, "-c", f"print({output!r})"],
                                "deps": [], "category": "engine"}}
        with tempfile.TemporaryDirectory() as directory, \
                mock.patch.object(check, "ROOT", Path(directory)), \
                mock.patch.object(check, "git", return_value="fixture\n"), \
                mock.patch.object(check, "tool_versions", return_value={}):
            self.assertEqual(check.execute(suites, ["expansion"], {}, [], "test", "main", 1), 0)
            report = json.loads((Path(directory) / "build/ichor-check/report.json").read_text())
            self.assertEqual(report["suites"][0]["native_counts"], counts)

    def test_fake_runner_and_nonzero_completion(self):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "run.log"
            code = check.run_command([sys.executable, "-c", "print('SAVE done'); raise SystemExit(2)"],
                                     log, os.environ.copy())
            self.assertEqual(code, 2)
            self.assertIn("SAVE done", log.read_text())

    def test_timeout_stops_process(self):
        with tempfile.TemporaryDirectory() as directory:
            code = check.run_command([sys.executable, "-c", "import time; time.sleep(30)"],
                                     Path(directory) / "run.log", os.environ.copy(), timeout=0.05)
            self.assertEqual(code, 124)

    def test_missing_command_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "run.log"
            self.assertEqual(check.run_command(["ichor-missing-command"], log, os.environ.copy()), 127)
            self.assertIn("CHECK FAIL", log.read_text())

    def test_execution_reports_blocked_and_unselected(self):
        suites = {"fail": {"command": ["missing-fixture"], "deps": [], "category": "test"},
                  "blocked": {"command": ["not-run"], "deps": ["fail"], "category": "test"},
                  "unselected": {"command": ["not-run"], "deps": [], "category": "test"}}
        with tempfile.TemporaryDirectory() as directory, \
                mock.patch.object(check, "ROOT", Path(directory)), \
                mock.patch.object(check, "git", return_value="fixture\n"), \
                mock.patch.object(check, "tool_versions", return_value={}):
            self.assertEqual(check.execute(suites, ["fail", "blocked"], {}, [], "test", "main", 1), 1)
            report = json.loads((Path(directory) / "build/ichor-check/report.json").read_text())
            self.assertEqual([s["status"] for s in report["suites"]],
                             ["failed", "blocked", "not_selected"])


if __name__ == "__main__":
    unittest.main()
