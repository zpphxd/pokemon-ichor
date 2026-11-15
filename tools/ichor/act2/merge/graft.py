#!/usr/bin/env python3
"""For files where theirs only added lines since the merge base: start from ours and
insert each of theirs' added blocks after the same base context lines (up to 40 lines of
preceding context, matched uniquely in ours)."""
import re, subprocess, sys
base, theirs = sys.argv[1], sys.argv[2]
for f in sys.argv[3:]:
    ours = subprocess.run(['git', 'show', f'HEAD:{f}'], capture_output=True, text=True, check=True).stdout.split('\n')
    b = subprocess.run(['git', 'show', f'{base}:{f}'], capture_output=True, text=True, check=True).stdout.split('\n')
    d = subprocess.run(['git', 'diff', '-U0', base, theirs, '--', f], capture_output=True, text=True, check=True).stdout.split('\n')
    hunks, cur = [], None
    for line in d:
        m = re.match(r'^@@ -(\d+)(?:,(\d+))? \+\d+(?:,\d+)? @@', line)
        if m:
            a, cnt = int(m.group(1)), int(m.group(2) or 1)
            assert cnt == 0, f'{f}: theirs changed existing lines'
            cur = [a, []]; hunks.append(cur)
        elif cur is not None and line.startswith('+') and not line.startswith('+++'):
            cur[1].append(line[1:])
    for a, added in hunks:
        for k in range(40, 0, -1):
            ctx = b[max(0, a - k):a]
            hits = [i for i in range(len(ours) - len(ctx) + 1) if ours[i:i + len(ctx)] == ctx]
            if len(hits) == 1:
                at = hits[0] + len(ctx); break
        else:
            sys.exit(f'{f}: no unique anchor for hunk at base line {a}')
        ours[at:at] = added
    open(f, 'w').write('\n'.join(ours))
    print(f, len(hunks), 'hunks grafted')
