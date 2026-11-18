"""The distribution pass's hook for map builders (design/DISTRIBUTION.md).

A builder that writes src/data/wild_encounters.json calls plan_hook.apply(entries) on the
encounter list just before it writes, so tools/ichor/wild_plan.py has the last word on
every planned table and a rerun keeps the distribution.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wild_plan import apply  # noqa: E402,F401
