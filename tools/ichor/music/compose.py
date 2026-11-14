#!/usr/bin/env python3
"""Compose Pokemon Ichor's original songs into MIDI files for mid2agb.

  python3 tools/ichor/music/compose.py           # write sound/songs/midi/mus_ichor_*.mid
  python3 tools/ichor/music/compose.py --check   # validate, and confirm the .mid files are current
  python3 tools/ichor/music/compose.py --summary # print form, timing and ranges

The notes live in songs.py as plain text; see the notation notes there.
Output is deterministic: the same data always gives byte-identical .mid files.
"""
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)

TPQ = 24        # ticks per quarter: the GBA's own resolution, so mid2agb copies timing 1:1
EIGHTH = 12
PLACEHOLDER = 'voice_square_1 60, 0, 0, 2, 0, 0, 15, 0'
CGB_LOWEST = 36  # m4a clamps square/wave keys below MIDI 36 (see MidiKeyToCgbFreq)

NOTE_RE = re.compile(r'^([A-G])([#b]?)(\d)$')
SEMI = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}


def pitch(name):
    m = NOTE_RE.match(name)
    if not m:
        raise ValueError(f'bad pitch {name!r}')
    acc = {'#': 1, 'b': -1, '': 0}[m.group(2)]
    return 12 * (int(m.group(3)) + 1) + SEMI[m.group(1)] + acc


def pname(n):
    return ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B'][n % 12] + str(n // 12 - 1)


TOKEN_RE = re.compile(r'^(?P<p>r|[A-G][#b]?\d(?:\+[A-G][#b]?\d)*|[a-z][a-z0-9]*(?:\+[a-z][a-z0-9]*)*)'
                      r'(?::(?P<d>\d+(?:\.\d+)?(?:/\d+)?))?(?P<m>[\^_.\-]*)$')


def parse_dur(text):
    if '/' in text:
        a, b = text.split('/')
        val = float(a) / float(b)
    else:
        val = float(text)
    ticks = val * EIGHTH
    if abs(ticks - round(ticks)) > 1e-6:
        raise ValueError(f'duration {text} is not a whole number of ticks')
    return int(round(ticks))


def parse_part(text, bar_ticks, kit, where):
    """Parse 'tok tok | tok ...' into notes [(start, dur, [keys], vel_delta, gate_scale)], bar count."""
    bars = [b for b in text.split('|')]
    if bars and not bars[0].strip():
        bars = bars[1:]
    if bars and not bars[-1].strip():
        bars = bars[:-1]
    notes, t, dur = [], 0, EIGHTH
    tie = None
    for bi, bar in enumerate(bars):
        start_bar = t
        for tok in bar.split():
            m = TOKEN_RE.match(tok)
            if not m:
                raise ValueError(f'{where} bar {bi + 1}: bad token {tok!r}')
            if m.group('d'):
                dur = parse_dur(m.group('d'))
            mods = m.group('m')
            p = m.group('p')
            if p != 'r':
                keys = [kit[k] if k in kit else pitch(k) for k in p.split('+')]
                if tie is not None:
                    if tie[2] != keys:
                        raise ValueError(f'{where} bar {bi + 1}: tie to a different pitch')
                    tie[1] += dur
                    note = tie
                else:
                    vel = 16 if '^' in mods else (-24 if '_' in mods else 0)
                    note = [t, dur, keys, vel, 0.5 if '.' in mods else 1.0]
                    notes.append(note)
                tie = note if '-' in mods else None
            elif tie is not None:
                raise ValueError(f'{where} bar {bi + 1}: tie into a rest')
            t += dur
        if t - start_bar != bar_ticks:
            raise ValueError(f'{where} bar {bi + 1}: {(t - start_bar) / EIGHTH} eighths, '
                             f'expected {bar_ticks / EIGHTH}')
    return notes, len(bars)


class Track:
    def __init__(self, name, program, volume, pan=0, velocity=96, gate=1.0, lo='C2', hi='C7',
                 kit=None, vibrato=None, parts=None):
        self.name, self.program, self.volume, self.pan = name, program, volume, pan
        self.velocity, self.gate = velocity, gate
        self.lo, self.hi = pitch(lo), pitch(hi)
        self.kit = kit or {}
        self.vibrato = vibrato  # (depth, lfo speed, delay in ticks)
        self.parts = parts or {}


class Song:
    def __init__(self, name, title, meter, grouping, tempo, voicegroup, volume, reverb, priority,
                 sections, loop_from, modes, tracks, target, chords):
        assert tempo % 2 == 0, 'm4a stores tempo/2, so use an even BPM'
        self.__dict__.update(locals())
        del self.__dict__['self']
        self.bar_ticks = meter[0] * (TPQ * 4 // meter[1])

    def section_starts(self):
        starts, t = {}, 0
        for name, bars in self.sections:
            starts[name] = t
            t += bars * self.bar_ticks
        return starts, t

    def seconds(self, ticks):
        return ticks / TPQ * 60.0 / self.tempo

    def build(self):
        """Return {track: [(start, dur, key, vel)]} with absolute ticks."""
        starts, _ = self.section_starts()
        out = {}
        for tr in self.tracks:
            evs = []
            for sec, bars in self.sections:
                if sec not in tr.parts:
                    continue
                notes, n = parse_part(tr.parts[sec], self.bar_ticks, tr.kit, f'{self.name}/{tr.name}/{sec}')
                if n != bars:
                    raise ValueError(f'{self.name}/{tr.name}/{sec}: {n} bars, expected {bars}')
                for start, dur, keys, dv, gs in notes:
                    sound = max(1, int(round(dur * tr.gate * gs)))
                    vel = max(1, min(127, tr.velocity + dv))
                    for k in keys:
                        evs.append((starts[sec] + start, sound, k, vel, sec))
            out[tr] = evs
        return out


# ---------------------------------------------------------------- MIDI writer

def vlq(n):
    b = [n & 0x7F]
    n >>= 7
    while n:
        b.append(0x80 | (n & 0x7F))
        n >>= 7
    return bytes(reversed(b))


def track_chunk(events):
    """events: [(tick, order, bytes)] -> MTrk chunk."""
    events.sort(key=lambda e: (e[0], e[1]))
    data, last = b'', 0
    for tick, _, msg in events:
        data += vlq(tick - last) + msg
        last = tick
    data += vlq(0) + b'\xff\x2f\x00'
    return b'MTrk' + struct.pack('>I', len(data)) + data


def meta(kind, payload):
    return bytes([0xFF, kind]) + vlq(len(payload)) + payload


def to_midi(song):
    built = song.build()
    starts, end = song.section_starts()
    loop = starts[song.loop_from]
    num, den = song.meter
    cond = [(0, 0, meta(0x03, song.title.encode())),
            (0, 1, meta(0x58, bytes([num, den.bit_length() - 1, 24, 8]))),
            (0, 2, meta(0x51, struct.pack('>I', 60000000 // song.tempo)[1:]))]
    for sec, _ in song.sections:  # long marker names are ignored by mid2agb
        cond.append((starts[sec], 3, meta(0x06, f'Section {sec}'.encode())))
    cond.append((loop, 4, meta(0x06, b'[')))
    cond.append((end, 4, meta(0x06, b']')))
    chunks = [track_chunk(cond)]
    chan = 0
    for tr in song.tracks:
        ch = 9 if tr.program == 0 else chan
        if tr.program != 0:
            chan += 1 + (chan == 8)
        evs = [(0, 0, meta(0x03, tr.name.encode())),
               (0, 1, bytes([0xC0 | ch, tr.program])),
               (0, 2, bytes([0xB0 | ch, 7, tr.volume])),
               (0, 3, bytes([0xB0 | ch, 10, tr.pan + 64]))]
        if tr.vibrato:
            depth, speed, delay = tr.vibrato
            evs += [(0, 4, bytes([0xB0 | ch, 21, speed])), (0, 5, bytes([0xB0 | ch, 26, delay])),
                    (0, 6, bytes([0xB0 | ch, 1, depth]))]
        for start, dur, key, vel, _ in built[tr]:
            evs.append((start, 20, bytes([0x90 | ch, key, vel])))
            evs.append((start + dur, 10, bytes([0x80 | ch, key, 0])))
        chunks.append(track_chunk(evs))
    return b'MThd' + struct.pack('>IHHH', 6, 1, len(chunks), TPQ) + b''.join(chunks)


# ---------------------------------------------------------------- checks

def voicegroup_entries(name, base=0):
    path = os.path.join(ROOT, 'sound', 'voicegroups', name + '.inc')
    lines = [l.strip() for l in open(path) if l.strip() and not l.strip().startswith('@')]
    m = re.match(r'voice_group\s+\w+(?:,\s*(\d+))?', lines[0])
    off = int(m.group(1)) if m.group(1) else 0
    return {off + i: l for i, l in enumerate(lines[1:]) if not l.startswith('voice_group')}


def check(song):
    errs, warns = [], []
    built = song.build()
    starts, end = song.section_starts()
    loop = starts[song.loop_from]
    vg = voicegroup_entries(song.voicegroup)
    kit_entries = None
    if 0 in vg:
        m = re.search(r'voicegroup_(\w+)', vg[0])
        for f in os.listdir(os.path.join(ROOT, 'sound', 'voicegroups', 'drumsets')):
            first = open(os.path.join(ROOT, 'sound', 'voicegroups', 'drumsets', f)).readline()
            if re.match(rf'voice_group\s+{m.group(1)}\b', first):
                kit_entries = voicegroup_entries('drumsets/' + f[:-4])
    if len(song.tracks) > 10:
        errs.append('more than 10 tracks (NUM_TRACKS_BGM)')
    for tr, evs in built.items():
        entry = vg.get(tr.program, PLACEHOLDER)
        if entry == PLACEHOLDER:
            errs.append(f'{tr.name}: program {tr.program} is empty in voicegroup {song.voicegroup}')
        cgb = 'square' in entry or 'programmable_wave' in entry or 'noise' in entry
        if not evs:
            errs.append(f'{tr.name}: no notes (mid2agb would drop the track)')
        for start, dur, key, vel, sec in evs:
            at = f'{tr.name} {sec} bar {(start - starts[sec]) // song.bar_ticks + 1}'
            if start < loop < start + dur:
                errs.append(f'{at}: note crosses the loop start')
            if start + dur > end:
                errs.append(f'{at}: note hangs past the loop end')
            if tr.program == 0:
                if kit_entries is None or kit_entries.get(key, PLACEHOLDER) == PLACEHOLDER:
                    errs.append(f'{at}: drum key {key} is empty in the drumset')
                continue
            if not tr.lo <= key <= tr.hi:
                errs.append(f'{at}: {pname(key)} outside {pname(tr.lo)}-{pname(tr.hi)}')
            if cgb and key < CGB_LOWEST:
                errs.append(f'{at}: {pname(key)} is below the CGB floor C2')
            mode = song.modes.get(sec, song.modes['*'])
            if key % 12 not in mode:
                errs.append(f'{at}: {pname(key)} is outside the mode')
    # CGB channels are single hardware voices: no overlaps between tracks on one channel.
    hw = {}
    for tr, evs in built.items():
        entry = vg.get(tr.program, '')
        for kind in ('square_1', 'square_2', 'programmable_wave', 'noise'):
            if f'voice_{kind}' in entry:
                hw.setdefault(kind, []).append((tr, evs))
    for kind, users in hw.items():
        spans = sorted((s, s + d, tr.name) for tr, evs in users for s, d, *_ in evs)
        for a, b in zip(spans, spans[1:]):
            if b[0] < a[1] and a[2] != b[2]:
                errs.append(f'{kind}: {a[2]} and {b[2]} overlap at tick {b[0]}')
                break
    # Loop seam: something sounds in the last and first loop bars.
    for edge, (lo, hi) in (('last', (end - song.bar_ticks, end)), ('first', (loop, loop + song.bar_ticks))):
        if not any(lo <= s < hi for evs in built.values() for s, *_ in evs):
            errs.append(f'nothing plays in the {edge} bar of the loop')
    # DirectSound polyphony (5 mixer channels), counting gated notes only.
    ds = [(s, d) for tr, evs in built.items() if not any(
        k in vg.get(tr.program, '') for k in ('square', 'programmable_wave', 'noise')) for s, d, *_ in evs]
    marks = sorted([(s, 1) for s, d in ds] + [(s + d, -1) for s, d in ds], key=lambda x: (x[0], x[1]))
    cur = peak = 0
    for _, step in marks:
        cur += step
        peak = max(peak, cur)
    if peak > 6:
        warns.append(f'up to {peak} DirectSound notes at once (mixer has 5)')
    secs = song.seconds(end - loop)
    if not song.target[0] <= secs <= song.target[1]:
        errs.append(f'loop is {secs:.1f}s, target {song.target}')
    # midi.cfg must carry the voicegroup, volume, reverb and priority recorded in songs.py.
    cfg = {}
    for line in open(os.path.join(ROOT, 'sound', 'songs', 'midi', 'midi.cfg')):
        mid, _, opts = line.partition(':')
        cfg[mid.strip()] = ' '.join(opts.split())
    want = f'-E -R{song.reverb} -G_{song.voicegroup} -V{song.volume:03d}'
    if song.priority:
        want += f' -P{song.priority}'
    if cfg.get(song.name + '.mid') != want:
        errs.append(f'midi.cfg has {cfg.get(song.name + ".mid")!r}; songs.py wants {want!r}')
    return errs, warns, peak


def mid_path(song):
    return os.path.join(ROOT, 'sound', 'songs', 'midi', song.name + '.mid')


def summary(song):
    starts, end = song.section_starts()
    loop = starts[song.loop_from]
    form = ' '.join(f'{n}({b})' for n, b in song.sections)
    print(f'{song.name}: {song.meter[0]}/{song.meter[1]} {"+".join(map(str, song.grouping))} '
          f'q={song.tempo} vg={song.voicegroup}  form {form}')
    print(f'  intro {song.seconds(loop):.1f}s, loop {song.seconds(end - loop):.1f}s')
    for tr, evs in song.build().items():
        keys = [k for _, _, k, *_ in evs]
        print(f'  {tr.name:10s} prog {tr.program:3d} vol {tr.volume:3d} pan {tr.pan:+3d} '
              f'{pname(min(keys))}-{pname(max(keys))} notes {len(evs)}')


def main():
    import songs
    ok = True
    for song in songs.SONGS:
        data = to_midi(song)
        if '--check' in sys.argv:
            errs, warns, peak = check(song)
            current = os.path.exists(mid_path(song)) and open(mid_path(song), 'rb').read() == data
            if not current:
                errs.append(f'{mid_path(song)} is stale; run compose.py')
            for w in warns:
                print(f'{song.name}: warning: {w}')
            for e in errs:
                print(f'{song.name}: ERROR: {e}')
            print(f'{song.name}: {"OK" if not errs else "FAIL"} (peak {peak} DirectSound notes)')
            ok &= not errs
        elif '--summary' in sys.argv:
            summary(song)
        else:
            with open(mid_path(song), 'wb') as f:
                f.write(data)
            print('wrote', os.path.relpath(mid_path(song), ROOT))
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
