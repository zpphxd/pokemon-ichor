#!/usr/bin/env python3
"""Render GBA-accurate audio previews of songs, through the built ROM and libmgba.

  python3 tools/ichor/music/preview.py [MUS_ICHOR_ELAIA ...]   (default: all Ichor songs
                                                                 plus three Emerald references)
  python3 tools/ichor/music/preview.py MUS_VS_WILD MUS_HEAL:2.3   (references; NAME:seconds
                                                                 measures a one-shot's span)
A copy of pokeemerald.gba gets gSongTable[MUS_TITLE] pointed at the song, so the
title screen plays it. WAVs land in build/ichor_music/. Prints loudness and clipping;
for loops, how closely the second pass matches the first (a hung note or a broken loop
shows up as a low match) and how low the level dips at the seam.
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


def render(name, entry, ids, table, rom, seconds):
    """-> interleaved stereo int16 samples from the song's first note, and the WAV path.

    The song under test takes gSongTable[MUS_TITLE] and is forced onto the BGM player
    (fanfares normally use SE2; the title screen watches the BGM player and leaves when
    it stops). MUS_INTRO is silenced so nothing plays before the title, and the first
    sound after START is the song's first note. The intro itself is recorded from boot.
    """
    data = bytearray(rom)
    slot = lambda n: slice(table + 8 * ids[n], table + 8 * ids[n] + 8)
    press = PRESS
    if name == 'MUS_INTRO':
        press = None
    else:
        data[slot('MUS_TITLE')] = entry[:4] + bytes(4)
        data[slot('MUS_INTRO')] = rom[slot('MUS_DUMMY')]
    path = os.path.join(OUT, name.lower() + '.gba')
    open(path, 'wb').write(data)
    wav = os.path.join(OUT, name.lower() + '.wav')
    frames = int((press or 0) + 300 + seconds * 60)
    subprocess.check_call([RUNNER, path, wav, str(frames)] + ([str(press)] if press else []),
                          stdout=subprocess.DEVNULL)
    os.remove(path)
    w = wave.open(wav)
    a = array('h')
    a.frombytes(w.readframes(w.getnframes()))
    if sys.byteorder == 'big':
        a.byteswap()
    skip = 2 * int((press or 0) / 59.73 * RATE)
    threshold = int(0.003 * 32768)
    on = next(i for i in range(skip, len(a)) if abs(a[i]) > threshold) & ~1  # the song's first note
    return a[on:], wav


def db(v):
    return 20 * math.log10(v / 32768 + 1e-9)


def rms(a):
    return math.sqrt(sum(v * v for v in a) / max(1, len(a)))


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
    for arg in sys.argv[1:] or [*by_name, *REFS]:
        name, _, secs = arg.partition(':')  # NAME:seconds measures a reference over that span
        s = by_name.get(name)
        sid = s.song_id if s else name
        entry = rom[table + 8 * ids[sid]: table + 8 * ids[sid] + 8]
        if s and s.loop_from:
            starts, end = s.section_starts()
            intro, loop = s.seconds(starts[s.loop_from]), s.seconds(end - starts[s.loop_from])
            length = intro + 2 * loop + 2
        elif s:
            intro, loop = 0, None
            length = s.seconds(s.section_starts()[1])
        else:
            intro, loop = 0, None
            length = float(secs or 30)
        a, wav = render(sid if sid == 'MUS_INTRO' else name, entry, ids, table, rom, length + 1)
        if loop is None:
            a = a[:2 * int(length * RATE)]  # a one-shot: measure its own span only
        level = db(rms(a))
        peak = db(max(max(a), -min(a)))
        clipped = sum(1 for v in a if v >= 32767 or v <= -32768)
        line = f'{name:26s} rms {level:6.1f} dBFS  peak {peak:5.1f} dBFS  clip {clipped}'
        if s and s.ref:
            line += f'  (replaces {s.ref[0]} at {s.ref[1]:.1f})'
        if s and loop is None:
            line += f'  one-shot {length:.2f}s'
        if s and loop:
            # Compare loop pass 2 with pass 1, aligning by cross-correlation of envelopes.
            e = envelope(a)
            i1, n = int(intro * ENV_HZ), int((loop - 1) * ENV_HZ)
            p1 = e[i1:i1 + n]
            nominal = int((intro + loop) * ENV_HZ)
            cands = [j for j in range(nominal - 10, nominal + 10) if j + n <= len(e)]
            best = max(cands, key=lambda j: correlation(p1, e[j:j + n]))
            match = correlation(p1, e[best:best + n])
            # The correlation reads low on flat, sustained textures, so also give the
            # largest level difference between the passes over any 1 s window. A hung or
            # dropped note shows up here as several dB; a clean loop stays near 1 dB.
            p2 = e[best:best + n]
            diff = [abs(20 * math.log10((sum(p2[k:k + ENV_HZ]) + 1) / (sum(p1[k:k + ENV_HZ]) + 1)))
                    for k in range(0, n - ENV_HZ, ENV_HZ // 2)]
            # Seam: the quietest 100 ms within half a second of the loop point, against the song.
            seam = 2 * int(best / ENV_HZ * RATE)
            w = 2 * (RATE // 10)
            gap = min(db(rms(a[k:k + w])) for k in range(seam - 5 * w, seam + 4 * w, w // 2)) - level
            line += (f'  loop {(best - i1) / ENV_HZ:.2f}s (nominal {loop:.2f})  pass match {match:.3f}'
                     f'  worst 1s {max(diff):.1f} dB  seam low {gap:+.1f} dB')
        print(line, '->', os.path.relpath(wav, ROOT))


if __name__ == '__main__':
    main()
