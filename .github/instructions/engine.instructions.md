---
applyTo: "src/**/*.c,include/**/*.h,test/**/*.c"
---

# Engine and state changes

Read [the engine API](../../design/ENGINE_API.md) and the relevant system spec.
Trace defaults, callers, state ownership, bounds, and persistence before editing.
Claim named bank flags/vars through `tools/ichor/claim.py`; do not guess offsets
or reuse an allocated id. Preserve layout assertions and migration behavior.

Use the shared engine Lua helpers and existing expansion test patterns.
Cover relevant boundary/invalid inputs, save/reset/CONTINUE, and legacy defaults.
See [the validation matrix](../../design/ENGINEERING.md) for required suites.
