#!/usr/bin/env python3
"""Render GBA-accurate audio previews of songs, through the built ROM and libmgba.

  python3 tools/ichor/music/preview.py [MUS_ICHOR_ELAIA ...]   (default: all Ichor songs
                                                                 plus three Emerald references)
A copy of pokeemerald.gba gets gSongTable[MUS_TITLE] pointed at the song, so the
title screen plays it (and never times out, since the song loops). WAVs land in
build/ichor_music/. Prints loudness, and how closely the second pass of the loop
matches the first (a hung note or a broken loop shows up as a low match).
Needs only the Python standard library, plus Homebrew mgba for the renderer.
"""
import math
import os
import re
import subprocess
import sys
import wave
from array import array

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
OUT = os.path.join(ROOT, 'build', 'ichor_music')
RUNNER = os.path.join(ROOT, 'build', 'tools', 'ichor-render-audio')
SRC = os.path.join(ROOT, 'tools', 'ichor', 'music', 'render_audio.c')
PRESS, RATE = 500, 32768
ENV_HZ = 20
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
    """-> interleaved stereo int16 samples from the song's first note, and the WAV path."""
    data = bytearray(rom)
    data[table + 8 * title_id: table + 8 * title_id + 8] = rom[table + 8 * sid: table + 8 * sid + 8]
    path = os.path.join(OUT, name.lower() + '.gba')
    open(path, 'wb').write(data)
    wav = os.path.join(OUT, name.lower() + '.wav')
    subprocess.check_call([RUNNER, path, wav, str(int(PRESS + 300 + seconds * 60)), str(PRESS)],
                          stdout=subprocess.DEVNULL)
    os.remove(path)
    w = wave.open(wav)
    a = array('h')
    a.frombytes(w.readframes(w.getnframes()))
    if sys.byteorder == 'big':
        a.byteswap()
    skip = 2 * int((PRESS + 60) / 59.73 * RATE)
    threshold = int(0.003 * 32768)
    on = next(i for i in range(skip, len(a)) if abs(a[i]) > threshold) & ~1  # the song's first note
    return a[on:], wav


def envelope(a):
    hop = 2 * (RATE // ENV_HZ)
    return [sum(map(abs, a[i:i + hop])) / hop for i in range(0, len(a) - hop + 1, hop)]


def correlation(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((p - mx) * (q - my) for p, q in zip(x, y))
    sxx = sum((p - mx) ** 2 for p in x)
    syy = sum((q - my) ** 2 for q in y)
    return sxy / math.sqrt(sxx * syy) if sxx and syy else 0.0


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
        rms = 20 * math.log10(math.sqrt(sum(map(lambda v: v * v, a)) / len(a)) / 32768 + 1e-9)
        peak = 20 * math.log10(max(max(a), -min(a)) / 32768 + 1e-9)
        line = f'{name:24s} rms {rms:6.1f} dBFS  peak {peak:5.1f} dBFS'
        if s:
            # Compare loop pass 2 with pass 1, aligning by cross-correlation of envelopes.
            e = envelope(a)
            i1, n = int(intro * ENV_HZ), int((loop - 1) * ENV_HZ)
            p1 = e[i1:i1 + n]
            nominal = int((intro + loop) * ENV_HZ)
            cands = [j for j in range(nominal - 10, nominal + 10) if j + n <= len(e)]
            best = max(cands, key=lambda j: correlation(p1, e[j:j + n]))
            match = correlation(p1, e[best:best + n])
            line += f'  loop {(best - i1) / ENV_HZ:.2f}s (nominal {loop:.2f})  pass match {match:.3f}'
        print(line, '->', os.path.relpath(wav, ROOT))


if __name__ == '__main__':
    main()
