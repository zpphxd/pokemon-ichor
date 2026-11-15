#!/usr/bin/env python3
"""After a merge: list flags.h names defined twice, two names on one value, and #if balance.
  python3 tools/ichor/act2/merge/checkflags.py   (from the repo root)"""
import re, collections
s = open('include/constants/flags.h').read()
names = collections.Counter(re.findall(r'^\s*#define\s+(\w+)', s, re.M))
dup = [n for n, c in names.items() if c > 1]
ex = collections.defaultdict(list)
for n, e in re.findall(r'^#define\s+(FLAG_\w+)\s+(.+?)\s*(?://.*)?$', s, re.M):
    e = re.sub(r'\s', '', e)
    if re.fullmatch(r'0x[0-9A-Fa-f]+', e) and n.startswith('FLAG_UNUSED'): continue
    ex[e].append(n)
# 0x1F4 is FLAG_HIDDEN_ITEMS_START's own value; 0 is the FRLG flags' when not FRLG; the daily
# bank's first flag shares its block start.
dv = {k: v for k, v in ex.items() if len(v) > 1 and k not in ('0x1F4', '0', '(ICHOR_DAILY_FLAGS_START+0x00)')}
print('dup names:', dup)
print('dup values:', dv)
print('#if/#endif', len(re.findall(r'^\s*#if', s, re.M)), len(re.findall(r'^\s*#endif', s, re.M)))
