---
applyTo: "tools/ichor/**,.github/workflows/**"
---

# Regression harness changes

Read [the engineering contract](../../design/ENGINEERING.md).
Keep suite selection explicit and conservative. Shared outputs require ordered,
serialized runs. Preserve existing gameplay assertions and suite interfaces.

Test the harness with failure fixtures, not just passing ROMs: nonzero exit even
after a completion marker, timeout, missing tools/completion, BUG, and crash.
Require real state evidence; never turn unavailable or skipped checks into PASS.
Do not publish ROMs, saves, states, or patches as workflow artifacts.
