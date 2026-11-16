#!/usr/bin/env python3
"""Conservative, serialized regression selection. See design/ENGINEERING.md."""
import argparse
from collections import Counter
import contextlib
import fcntl
import fnmatch
import json
import os
from pathlib import Path
import re
import shlex
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "tools/ichor/checks.json"
FAST = {"host", "invariants"}
CORE = FAST | {"bootstrap", "build", "budget", "smoke"}
ROM_LIMIT = 32 * 1024 * 1024
GENERAL_CONTENT = {"map-audit", "items-doors", "slice", "sidechecks"}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, stderr=subprocess.PIPE).decode()


def changed_paths(base):
    merge_base = git("merge-base", "--", base, "HEAD").strip()
    committed = git("diff", "--no-renames", "--name-only", "-z", merge_base, "HEAD", "--")
    local = git("diff", "--no-renames", "--name-only", "-z", "HEAD", "--")
    untracked = git("ls-files", "--others", "--exclude-standard", "-z")
    return sorted(set(filter(None, (committed + local + untracked).split("\0"))))


def load_suites(path=REGISTRY):
    rows = json.loads(path.read_text())["suites"]
    suites = {}
    for row in rows:
        if (not isinstance(row, dict)
                or set(row) != {"id", "command", "category", "deps", "paths"}
                or not isinstance(row["id"], str)
                or not isinstance(row["category"], str)
                or not re.fullmatch(r"[a-z][a-z0-9-]*", row["id"])
                or row["id"] in suites
                or not all(isinstance(row[k], list) for k in ("command", "deps", "paths"))
                or not all(isinstance(v, str) for k in ("command", "deps", "paths") for v in row[k])
                or not row["command"]):
            raise ValueError("invalid or duplicate suite entry")
        suites[row["id"]] = row
    ordered(suites, set(suites))
    return suites


def ordered(suites, selected):
    result, active, visited = [], set(), set()

    def visit(name):
        if name not in suites:
            raise ValueError(f"unknown suite/dependency: {name}")
        if name in active:
            raise ValueError(f"cyclic suite dependency: {name}")
        if name in visited:
            return
        active.add(name)
        for dep in suites[name]["deps"]:
            visit(dep)
        active.remove(name)
        visited.add(name)
        result.append(name)

    for name in suites:
        if name in selected:
            visit(name)
    for name in selected:
        if name not in suites:
            raise ValueError(f"unknown suite: {name}")
    return result


def select(suites, profile, paths):
    reasons = {name: "mandatory opening gate" for name in CORE}
    if profile == "fast":
        return {name: "fast harness/structural gate" for name in FAST}
    if profile == "full":
        return {name: "full profile" for name in suites}
    for path in paths:
        if path.endswith(".md") and not path.startswith("tools/"):
            continue
        matches = [name for name, row in suites.items()
                   if any(fnmatch.fnmatchcase(path, pattern) for pattern in row["paths"])]
        if not matches or not set(matches) - GENERAL_CONTENT:
            return {name: f"conservative fallback: {path}" for name in suites}
        for name in matches:
            reasons[name] = f"affected path: {path}"
    return reasons


def claims_errors(lines, marker, bases):
    start = f"// {marker}: claim.py"
    end = f"// {marker}: end"
    inside, found_start, found_end = False, False, False
    used, names, errors = set(), set(), []
    for number, line in enumerate(lines, 1):
        if line.startswith(start):
            inside, found_start = True, True
            continue
        if line == end:
            inside, found_end = False, True
            continue
        if not inside or not line.startswith("#define"):
            continue
        match = re.fullmatch(r"#define\s+(\w+)\s+\((\w+) \+ (0x[0-9A-Fa-f]+)\)\s*(?://.*)?", line)
        if not match or match[2] not in bases:
            errors.append(f"line {number}: malformed claim; use claim.py")
            continue
        name, base, offset = match[1], match[2], int(match[3], 16)
        if offset >= bases[base] or (base, offset) in used or name in names:
            errors.append(f"line {number}: duplicate/out-of-range claim {name}; use claim.py")
        used.add((base, offset))
        names.add(name)
    if not found_start or not found_end or inside:
        errors.append(f"missing claim block markers: {marker}")
    return errors


def invariants():
    # Read allocator capacities from the allocator itself, not a second bank map.
    from claim import BANKS
    errors = []
    for kind in ("bankflag", "dailyflag", "bankvar"):
        path, _, segments, marker = BANKS[kind]
        bases = {base: last - first + 1 for first, last, base in segments}
        errors.extend(f"{path.relative_to(ROOT)}: {e}"
                      for e in claims_errors(path.read_text().splitlines(), marker, bases))
    tracked = set(git("ls-files", "-z").split("\0"))
    for path in (ROOT / "data").rglob("*.pory"):
        output = path.with_suffix(".inc").relative_to(ROOT).as_posix()
        if output in tracked:
            errors.append(f"{output}: generated output is tracked; untrack it and add to .gitignore")
        ignored = subprocess.run(["git", "check-ignore", "-q", "--", output], cwd=ROOT).returncode
        if ignored != 0:
            errors.append(f"{output}: generated output must be listed in .gitignore")
    documents = [ROOT / "AGENTS.md", ROOT / "CLAUDE.md", ROOT / "design/ENGINEERING.md",
                 ROOT / ".github/copilot-instructions.md",
                 *sorted((ROOT / ".github/instructions").glob("*.md"))]
    for document in documents:
        for target in re.findall(r"\[[^]]*\]\(([^)\s]+)\)", document.read_text()):
            if "://" not in target and not target.startswith("#"):
                resolved = (document.parent / target.split("#")[0]).resolve()
                if not resolved.is_relative_to(ROOT) or not resolved.exists():
                    errors.append(f"{document.relative_to(ROOT)}: broken/local-external reference {target}")
    for error in errors:
        print(f"INVARIANT FAIL: {error}", file=sys.stderr)
    if not errors:
        print("INVARIANTS PASS: claim blocks, generated scripts, and engineering references")
    return int(bool(errors))


def budget(path=None):
    path = path or ROOT / "pokeemerald.gba"
    size = path.stat().st_size
    print(f"ROM: {size} bytes; {ROM_LIMIT - size} bytes remaining of {ROM_LIMIT}")
    if size <= 0 or size > ROM_LIMIT:
        print("BUDGET FAIL: missing/empty or over 32 MiB cartridge capacity", file=sys.stderr)
        return 1
    return 0


def map_regression(base, maps):
    baseline = git("merge-base", "--", base, "HEAD").strip()
    if baseline == git("rev-parse", "HEAD").strip() and not changed_paths(base):
        raise ValueError("map baseline must precede this revision, not be the revision under test")
    out = ROOT / "build/ichor-check"
    out.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, str(ROOT / "tools/ichor/map_audit.py"), "--json"]
    # Audit the whole map graph in both revisions: removed maps and adjacent seams
    # matter, and a new map need not exist in the baseline.
    reports = []
    for label, extra in (("current", []), ("baseline", ["--ref", baseline])):
        result = subprocess.run(command + ["--all-ichor"] + extra, cwd=ROOT,
                                capture_output=True, text=True, timeout=300)
        if result.returncode not in (0, 1):
            raise ValueError(f"map {label} audit failed: {result.stderr[-2000:]}")
        report = json.loads(result.stdout)
        (out / f"map-{label}.json").write_text(json.dumps(report, indent=2) + "\n")
        reports.append(report)
    current, old = reports
    def failures(report):
        return Counter((f["map"], f["message"]) for f in report["findings"] if f["level"] == "FAIL")
    new = failures(current) - failures(old)
    existing = failures(current) & failures(old)
    print(json.dumps({"baseline_revision": baseline, "affected_maps": maps,
                      "new_failures": [{"map": key[0], "message": key[1], "count": count}
                                       for key, count in new.items()],
                      "baseline_failures": [{"map": key[0], "message": key[1], "count": count}
                                            for key, count in existing.items()]}, indent=2))
    return int(bool(new))


def run_command(command, log, env, timeout=7200):
    with log.open("w") as output:
        try:
            process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=output,
                                       stderr=subprocess.STDOUT, start_new_session=True)
        except OSError as error:
            output.write(f"CHECK FAIL: {error}\n")
            return 127
        try:
            return process.wait(timeout=timeout)
        except (subprocess.TimeoutExpired, KeyboardInterrupt):
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            output.write("CHECK FAIL: orchestration timeout/interruption\n")
            return 124


def tool_versions(env):
    versions = {}
    for tool, arguments in {"python3": ["--version"], "arm-none-eabi-gcc": ["--version"],
                            "poryscript": ["-v"], "cc": ["--version"],
                            "timeout": ["--version"], "gtimeout": ["--version"]}.items():
        try:
            result = subprocess.run([tool, *arguments], env=env, capture_output=True,
                                    text=True, timeout=10)
            versions[tool] = {"exit_code": result.returncode,
                              "output": (result.stdout + result.stderr).strip()[:500]}
        except (OSError, subprocess.TimeoutExpired) as error:
            versions[tool] = {"unavailable": str(error)}
    prefix = env.get("MGBA_PREFIX")
    stamp = Path(prefix) / "versions.txt" if prefix else None
    versions["mGBA"] = {"required": "0.10.5", "prefix": prefix or "system/Homebrew",
                        "observed_build_stamp": stamp.read_text() if stamp and stamp.is_file() else None,
                        "verification": "actual runner compilation/execution is recorded by Lua suite status"}
    return versions


@contextlib.contextmanager
def workspace_lock(out):
    with (out / "check.lock").open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise ValueError("another regression runner is using this worktree") from error
        yield


def write_report(out, report):
    temporary = out / "report.json.tmp"
    temporary.write_text(json.dumps(report, indent=2) + "\n")
    temporary.replace(out / "report.json")


def execute(suites, names, reasons, paths, profile, base, jobs):
    out = ROOT / "build/ichor-check"
    out.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["PATH"] = (f"{env.get('DEVKITARM', '/opt/devkitpro/devkitARM')}/bin:"
                   f"{env['PATH']}:{Path.home()}/.local/bin:/opt/homebrew/bin")
    # A resumed/workaround run or a limited side-check list is not a full gate.
    for key in ("SLICE_FROM", "SLICE_WORKAROUNDS", "SLICE_OUT", "CHECKS_ONLY", "CHECKS_OUT"):
        env.pop(key, None)
    report = {"revision": git("rev-parse", "HEAD").strip(),
              "worktree_status": git("status", "--porcelain"),
              "base": base,
              "profile": profile, "paths": paths, "tool_versions": tool_versions(env),
              "coverage_limits": ["Assisted progression is not natural-level balance or human approval."],
              "suites": [], "status": "running"}
    status = {}
    with workspace_lock(out):
        write_report(out, report)
        for name in names:
            row = suites[name]
            command = [part.replace("{jobs}", str(jobs)) for part in row["command"]]
            if name == "map-audit" and profile == "changed":
                maps = sorted({p.split("/")[2] for p in paths if p.startswith("data/maps/")
                               and len(p.split("/")) > 3
                               and (ROOT / "data/maps" / p.split("/")[2] / "map.json").exists()})
            else:
                maps = []
            if name == "map-audit":
                command = [sys.executable, "tools/ichor/check.py", "--map-regression",
                           "--base", base, "--maps", *maps]
            entry = {"id": name, "category": row["category"], "command": command,
                     "reason": reasons.get(name, "suite prerequisite")}
            blocked = [dep for dep in row["deps"] if status.get(dep) != "passed"]
            if blocked:
                entry.update(status="blocked", blocked_by=blocked)
            else:
                log = out / f"{name}.log"
                print(f"CHECK {name}: {shlex.join(command)}", flush=True)
                started = time.monotonic()
                code = run_command(command, log, env)
                text = log.read_text(errors="replace")
                text_error = name in {"slice", "sidechecks"} and re.search(r"^(WIDE|TALL)\s", text, re.M)
                entry.update(status="passed" if code == 0 and not text_error else "failed",
                             exit_code=code, seconds=round(time.monotonic() - started, 2),
                             log=log.relative_to(ROOT).as_posix())
                if name == "map-audit" and code == 0:
                    map_report = json.loads(text)
                    entry["baseline_revision"] = map_report["baseline_revision"]
                    entry["baseline_failures"] = map_report["baseline_failures"]
                    if entry["baseline_failures"]:
                        entry["status"] = "baseline_failed"
                        print("MAP BASELINE FAILURES RETAINED: see map-audit.log", flush=True)
                if text_error:
                    entry["error"] = "measured dialogue exceeds the text box"
                if name == "expansion":
                    entry["native_counts"] = {key: int(value) for key, value in
                                              re.findall(r"^-\s+Tests\s+(\w+):\s+(\d+)", text, re.M)}
                if entry["status"] == "failed":
                    print(text[-4000:], file=sys.stderr)
            status[name] = entry["status"]
            report["suites"].append(entry)
            # Persist partial evidence after each suite, even if a later run is interrupted.
            write_report(out, report)
        for name, row in suites.items():
            if name not in names:
                report["suites"].append({"id": name, "category": row["category"],
                                         "status": "not_selected"})
        successful = all(v in {"passed", "baseline_failed"} for v in status.values())
        report["status"] = ("passed_with_baseline_failures" if "baseline_failed" in status.values()
                            else "passed") if successful else "failed"
        write_report(out, report)
    print(f"CHECK {report['status'].upper()}: build/ichor-check/report.json")
    return int(not successful)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("fast", "changed", "full"), default="changed")
    parser.add_argument("--base", default="main", help="explicit PR base ref; never guessed on failure")
    parser.add_argument("--jobs", type=int, default=min(os.cpu_count() or 1, 8))
    parser.add_argument("--dry-run", action="store_true")
    internal = parser.add_mutually_exclusive_group()
    internal.add_argument("--invariants", action="store_true")
    internal.add_argument("--budget", action="store_true")
    internal.add_argument("--map-regression", action="store_true")
    parser.add_argument("--maps", nargs="*", default=[])
    args = parser.parse_args()
    try:
        if args.invariants:
            return invariants()
        if args.budget:
            return budget()
        if args.map_regression:
            return map_regression(args.base, args.maps)
        if args.jobs < 1:
            raise ValueError("--jobs must be positive")
        suites = load_suites()
        paths = changed_paths(args.base) if args.profile == "changed" else []
        reasons = select(suites, args.profile, paths)
        names = ordered(suites, set(reasons))
        if args.dry_run:
            print(json.dumps([{"id": name, "reason": reasons.get(name, "suite prerequisite"),
                               "category": suites[name]["category"]} for name in names], indent=2))
            return 0
        return execute(suites, names, reasons, paths, args.profile, args.base, args.jobs)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError,
            subprocess.TimeoutExpired) as error:
        print(f"CHECK FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
