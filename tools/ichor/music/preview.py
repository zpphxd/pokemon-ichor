#!/usr/bin/env python3
"""Render GBA-accurate audio previews of songs, through the built ROM and libmgba.

  python3 tools/ichor/music/preview.py [MUS_ICHOR_ELAIA ...]   (default: all Ichor songs
                                                                 plus three Emerald references)
A copy of pokeemerald.gba gets gSongTable[MUS_TITLE] pointed at the song, so the
title screen plays it (and never times out, since the song loops). WAVs land in
build/ichor_music/. Prints loudness, and how closely the second pass of the loop
matches the first (a hung note or a broken loop shows up as a low match).
"""
import os
import re
import subprocess
import sys
import wave

import numpy as np

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
OUT = os.path.join(ROOT, 'build', 'ichor_music')
RUNNER = os.path.join(ROOT, 'build', 'tools', 'ichor-render-audio')
SRC = os.path.join(ROOT, 'tools', 'ichor', 'music', 'render_audio.c')
PRESS, RATE = 500, 32768
REFS = ['MUS_LITTLEROOT', 'MUS_ROUTE101', 'MUS_VS_RIVAL']


def song_ids():
    ids = {}
    for line in open(os.path.join(ROOT, 'include', 'constants', 'songs.h')):
        m = re.match(r'#define\s+(MUS_\w+|PH_\w+|SE_\w+)\s+(\d+)', line)
        if m:
            ids[m.group(1)] = int(m.group(2))
    return ids


def build_runner():
    if os.path.exists(RUNNER) and os.path.getmtime(RUNNER) > os.path.getmtime(SRC):
        return
    prefix = subprocess.check_output(['brew', '--prefix', 'mgba'], text=True).strip()
    os.makedirs(os.path.dirname(RUNNER), exist_ok=True)
    subprocess.check_call(['cc', '-O2', f'-I{prefix}/include', SRC, f'-L{prefix}/lib', '-lmgba', '-o', RUNNER])


def render(name, sid, title_id, table, rom, seconds):
    data = bytearray(rom)
    data[table + 8 * title_id: table + 8 * title_id + 8] = rom[table + 8 * sid: table + 8 * sid + 8]
    path = os.path.join(OUT, name.lower() + '.gba')
    open(path, 'wb').write(data)
    wav = os.path.join(OUT, name.lower() + '.wav')
    subprocess.check_call([RUNNER, path, wav, str(int(PRESS + 300 + seconds * 60)), str(PRESS)])
    os.remove(path)
    w = wave.open(wav)
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2).astype(float) / 32768
    a = a[int((PRESS + 60) / 59.73 * RATE):]
    on = np.argmax(np.abs(a).max(axis=1) > 0.003)  # the song's first note
    return a[on:], wav


def main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import songs
    ids = song_ids()
    nm = subprocess.check_output(['/opt/devkitpro/devkitARM/bin/arm-none-eabi-nm',
                                  os.path.join(ROOT, 'pokeemerald.elf')], text=True)
    table = int(re.search(r'^(\w+) R gSongTable$', nm, re.M).group(1), 16) - 0x08000000
    rom = open(os.path.join(ROOT, 'pokeemerald.gba'), 'rb').read()
    os.makedirs(OUT, exist_ok=True)
    build_runner()
    by_name = {s.name.upper(): s for s in songs.SONGS}
    for name in sys.argv[1:] or [*by_name, *REFS]:
        s = by_name.get(name)
        if s:
            starts, end = s.section_starts()
            intro, loop = s.seconds(starts[s.loop_from]), s.seconds(end - starts[s.loop_from])
        else:
            intro, loop = 0, 30
        a, wav = render(name, ids[name], ids['MUS_TITLE'], table, rom, intro + 2 * loop + 2)
        rms = 20 * np.log10(np.sqrt((a ** 2).mean()) + 1e-9)
        peak = 20 * np.log10(np.abs(a).max() + 1e-9)
        line = f'{name:24s} rms {rms:6.1f} dBFS  peak {peak:5.1f} dBFS'
        if s:
            # Compare loop pass 2 with pass 1, aligning by cross-correlation of envelopes.
            env = np.abs(a).mean(axis=1)
            hop = RATE // 20
            e = env[:len(env) // hop * hop].reshape(-1, hop).mean(axis=1)
            i1, n = int(intro * 20), int((loop - 1) * 20)
            p1 = e[i1:i1 + n]
            best = max(range(int((intro + loop) * 20) - 10, int((intro + loop) * 20) + 10),
                       key=lambda j: np.dot(p1, e[j:j + n]) if j + n <= len(e) else -1)
            p2 = e[best:best + n]
            match = np.corrcoef(p1, p2)[0, 1]
            line += f'  loop {(best - i1) / 20:.2f}s (nominal {loop:.2f})  pass match {match:.3f}'
        print(line, '->', os.path.relpath(wav, ROOT))


if __name__ == '__main__':
    main()
