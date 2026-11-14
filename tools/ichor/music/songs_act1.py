"""Act I (Phase 2) music, and Elpis's lullaby. All original, all on the `ichor`
voicegroup. Notation is as in songs.py, which imports this module at its end (so import
songs, not this). The leitmotifs these songs quote are mapped in design/MUSIC.md.

Map music is the director's to assign; nothing here touches map.json. The one engine
pairing is sNightMusicTable in src/overworld.c, which swaps MUS_ICHOR_ROAD for
MUS_ICHOR_ROAD_NIGHT at night on any map that plays the road.
"""
import re

from compose import EIGHTH, Song, Track, parse_part, pname
from songs import (AEOLIAN, DORIAN, FRAME_KIT, IONIAN, LOCRIAN, LYDIAN, MIXOLYDIAN, PHRYGIAN, VG,
                   bar_chords, bars, diatonic, gen, notes, octave, pcs, step, triad)
from songs_engine import offbeats, roll, root_fifth


# ---------------------------------------------------------------- helpers

def remap(part, names):
    """Respell pitch classes, e.g. {'A': 'Ab'}: the day road's tune at night."""
    return re.sub(r'\b([A-G][#b]?)(\d)', lambda m: names.get(m.group(1), m.group(1)) + m.group(2), part)


def render(evs, bar_ticks, nbars):
    """[(start, dur, pitch name)] -> notation, splitting notes at bar lines with ties."""
    out = []
    for b in range(nbars):
        lo, hi, toks, t = b * bar_ticks, (b + 1) * bar_ticks, [], b * bar_ticks
        for s, d, k in sorted(evs):
            s, e = max(s, lo), min(s + d, hi)
            if e <= s or e <= t:
                continue
            if s > t:
                toks.append(f'r:{(s - t) / EIGHTH:g}')
            toks.append(f'{k}:{(e - s) / EIGHTH:g}' + ('-' if s + d > hi else ''))
            t = e
        if t < hi:
            toks.append(f'r:{(hi - t) / EIGHTH:g}')
        out.append(' '.join(toks))
    return ' | '.join(out)


def delay(part, eighths, bar_ticks):
    """The part played `eighths` later, cut at the section's end: a cave's echo."""
    evs, n = parse_part(part, bar_ticks, {}, 'delay')
    shift = int(eighths * EIGHTH)
    keep = []
    for s, d, ks, _, _ in evs:
        if s + shift < n * bar_ticks:
            keep.append((s + shift, min(d, n * bar_ticks - s - shift), pname(ks[0])))
    return render(keep, bar_ticks, n)


def hocket(line, keep, size=1):
    """Every other note of a line of equal values; the rest become rests."""
    out = []
    for bar in line.split('|'):
        toks = bar.split()
        out.append(' '.join(f'{t}:{size}' if i % 2 == keep else f'r:{size}' for i, t in enumerate(toks)))
    return ' | '.join(out)


def per_bar(fn):
    """Accompaniment from a chord spec of one chord, or two chords splitting the bar."""
    def g(spec):
        return fn(*bar_chords(spec))
    return g


# ============================================================ Elpis's lullaby
# The score's heart (MUSIC.md). D Dorian (D Greek Phrygian, Elaia's home mode), 3/4,
# eight bars. It is the Thread run backwards: the Thread climbs A-D-E-F, the lullaby
# falls F-E-D-A. Both of its phrases stop on A, the half cadence. Its eighth bar,
# where the tune would come home to D, is LB_LAST, and no arrangement plays it until
# Elpis finishes the song (STORY III-12). Until then that bar is the gap where she
# falls asleep, and the loop starts the song again instead of ending it.
D_DOR = pcs('D', DORIAN)
LB_TUNE = ('F5:2 E5:1 D5:1 A4:2 | B4:2 D5:1 E5:1 D5:2 | F5:2 E5:1 D5:1 A4:2 | C5:2 B4:1 G4:1 A4:2 | '
           'F5:2 A5:2 G5:1 F5:1 | E5:2 G5:1 E5:1 C5:2 | D5:2 B4:1 C5:1 A4:2')
LB_TAIL = LB_TUNE.split(' | ')[4:]  # bars 5-7, the second phrase
LB_LAST = 'D5:6'  # the withheld bar: A rises to D, the Thread's first step
LB_CH = ['Dm', 'G', 'Dm', 'Am', 'F', 'C', 'G Am', 'Am']


def lb_rock(a, b=None):
    """The cradle: up and back over the bar, or split 4 + 2 for two chords."""
    r, t, f = triad(a, 48)
    if b is None:
        return notes([(r, 1), (f, 1), (t + 12, 1), (r + 12, 1), (t + 12, 1), (f, 1)])
    r2, t2, f2 = triad(b, 48)
    return notes([(r, 1), (f, 1), (t + 12, 1), (f, 1), (r2, 1), (f2, 1)])


def lb_root(a, b=None):
    if b is None:
        return notes([(triad(a, 38)[0], 6)])
    return notes([(triad(a, 38)[0], 4), (triad(b, 38)[0], 2)])


def lb_pad(a, b=None):
    if b is None:
        return notes([(triad(a, 55)[1], 6)])
    return notes([(triad(a, 55)[1], 4), (triad(b, 55)[1], 2)])


# The hum: Elpis's room (Act II). She hums it while the lyre rocks the cradle, and
# falls asleep on the half cadence. Bar 8 is the lyre alone, rocking on A. In A2 her
# father's lyre takes the tune and she joins drowsily for the last phrase, a third
# under, and falls asleep again.
ELPIS_LULLABY = Song(
    name='mus_ichor_elpis_lullaby', title="Elpis's Lullaby", meter=(3, 4), grouping=(2, 2, 2), tempo=72,
    voicegroup=VG, volume=101, reverb=50, priority=0, sections=[('intro', 1), ('A', 8), ('A2', 8)],
    loop_from='A', modes={'*': D_DOR}, target=(36, 44),
    chords={'intro': ['Dm'], 'A': LB_CH, 'A2': LB_CH}, ref=('MUS_SOOTOPOLIS', -24.4), tracks=[
        Track('hum', 53, 110, pan=-6, velocity=100, lo='F4', hi='A5', vibrato=(3, 30, 20), parts={
            'A': LB_TUNE + ' | r:6',
            'A2': 'r:6 | r:6 | r:6 | r:6 | ' + diatonic(' | '.join(LB_TAIL), D_DOR, -2) + ' | r:6'}),
        Track('lyre', 46, 110, pan=12, velocity=100, lo='G4', hi='A5', parts={'A2': LB_TUNE + ' | r:6'}),
        Track('kithara', 46, 84, pan=20, velocity=84, lo='C3', hi='C5',
              parts={'intro': lb_rock('Dm'), 'A': gen(LB_CH, per_bar(lb_rock)), 'A2': gen(LB_CH, per_bar(lb_rock))}),
        Track('strings', 48, 50, pan=-24, velocity=72, lo='A3', hi='A4', parts={'A2': gen(LB_CH, per_bar(lb_pad))}),
        Track('bass', 92, 50, velocity=90, lo='C2', hi='C4',
              parts={'A': gen(LB_CH, per_bar(lb_root)), 'A2': gen(LB_CH, per_bar(lb_root))}),
    ])


def box_teeth(a, b=None):
    """The comb's lower teeth: a waltz arpeggio, root-fifth-tenth."""
    r, t, f = triad(a, 57)
    if b is None:
        return notes([(r, 2), (f, 2), (t + 12, 2)])
    return notes([(r, 2), (f, 2), (triad(b, 57)[0], 2)])


# The music box: Daedalus's prototype in his workshop, Elpis's box on her shelf, and
# the whole Frozen Hour, where it is the only music (STORY §6.12). The comb plays the
# tune an octave up over its own lower teeth. The escapement ticks once a second
# (crotchet = 60), tick-tock-tock, and in the eighth bar the comb is silent and only
# the ticking goes on: the box is missing its last bar.
BOX_TICK = 'C6:0.5 r:1.5 G5:0.5 r:1.5 G5:0.5 r:1.5'
ELPIS_LULLABY_BOX = Song(
    name='mus_ichor_elpis_lullaby_box', title='The Music Box', meter=(3, 4), grouping=(2, 2, 2), tempo=60,
    voicegroup=VG, volume=127, reverb=50, priority=0, sections=[('intro', 1), ('A', 8)], loop_from='A',
    modes={'*': D_DOR}, target=(22, 26), chords={'intro': ['Dm'], 'A': LB_CH},
    ref=('MUS_SEALED_CHAMBER', -23.7), tracks=[
        Track('comb', 10, 127, pan=-4, velocity=127, lo='G5', hi='A6', parts={'A': octave(LB_TUNE, 1) + ' | r:6'}),
        Track('teeth', 10, 110, pan=8, velocity=100, lo='A3', hi='B5',
              parts={'A': gen(LB_CH[:7], per_bar(box_teeth)) + ' | r:6'}),
        Track('tick', 115, 64, velocity=76, gate=0.5, lo='G5', hi='C6', parts={'intro': BOX_TICK, 'A': bars(BOX_TICK, 8)}),
    ])

# ============================================================ The trireme crossing
# The Euploia ("fair sailing") carries you from Akti to Emporion. G Dorian (G Greek
# Phrygian), 6/8 at a stroke a bar: the frame drum's dum is the pull, the light taps
# the oars coming back. Real triremes rowed to an aulos player, the trieraules, who set
# the stroke; in C the aulos calls it on every pull while the chorus of rowers
# answers with their cry. The noise channel breathes sea wind under it all.
# A: the syrinx's sea tune, rising and falling with the swell. A2: the aulos joins a
# third under. B: Kleon's shipmate song, his Kleos turn (E-F-E-D-E-B) with its
# Phrygian semitone opened into a whole tone, G-A-G-F-G-D: Kleon at ease on deck,
# with sun glinting off the water. C: open sea, the rowers' chant and a gull's descant.
# F falls to G into the loop.
G_DOR = pcs('G', DORIAN)
TV_CH = {
    'intro': ['Gm', 'Gm'],
    'A': ['Gm', 'C', 'F', 'Dm', 'Gm', 'Bb', 'F', 'Gm'],
    'B': ['Gm', 'Dm', 'C', 'C', 'F', 'Dm', 'C', 'Dm'],
    'C': ['Gm', 'Gm', 'F', 'F', 'C', 'C', 'Dm', 'F'],
}
TV_CH['A2'] = TV_CH['A']
TV_TUNE = ('D5:3 G5:2 A5:1 | Bb5:2 A5:1 G5:2 E5:1 | F5:3 D5:2 C5:1 | D5:6 | '
           'D5:3 G5:2 A5:1 | Bb5:2 C6:1 D6:2 C6:1 | Bb5:2 A5:1 G5:2 F5:1 | G5:6')
TV_KLEON = ('G5:1 A5:1 G5:1 F5:1 G5:2 | D5:4 F5:1 A5:1 | G5:1 A5:1 G5:1 E5:1 G5:2 | C5:4 E5:1 G5:1 | '
            'A5:1 Bb5:1 A5:1 G5:1 A5:2 | F5:3 D5:2 F5:1 | E5:2 F5:1 G5:2 E5:1 | D5:3 A4:3')
TV_GULL = ('D6:6 | Bb5:3 A5:2 G5:1 | A5:6 | F5:3 G5:2 A5:1 | G5:6 | E5:3 F5:2 G5:1 | A5:6 | C6:3 A5:2 F5:1')
TV_CHANT = 'r:5 D4:1 | G4:6^ | r:5 C4:1 | F4:6^ | r:5 C4:1 | E4:6^ | r:5 D4:1 | F4:6^'


def tv_swell(c):
    r, t, f = triad(c, 48)
    return notes([(r, 1), (f, 1), (r + 12, 1), (t + 12, 1), (r + 12, 1), (f, 1)])


def tv_harp(c):
    r, t, f = triad(c, 62)
    return notes([(r, 1), (t, 1), (f, 1), (r + 12, 1), (f, 1), (t, 1)])


def tv_call(c):
    """The trieraules sets the stroke: a short root, a longer fifth, then the glide."""
    r, t, f = triad(c, 62)
    return notes([(r, 1), (f, 2), (None, 3)])


TV_STROKE = 'dum:3 tek:2_ tek:1_'
TV_FILL = 'dum:3 tek:1 tek:1 low:1'
TV_WIND = 'A3:6- | A3:3 r:3 | E3:6- | E3:3 r:3 | A3:6- | A3:3 r:3 | E3:6- | E3:3 r:3'
TRIREME = Song(
    name='mus_ichor_trireme', title='Euploia', meter=(6, 8), grouping=(3, 3), tempo=100,
    voicegroup=VG, volume=98, reverb=50, priority=0,
    sections=[('intro', 2), ('A', 8), ('A2', 8), ('B', 8), ('C', 8)], loop_from='A',
    modes={'*': G_DOR}, target=(55, 65), chords=TV_CH, ref=('MUS_SAILING', -23.4), tracks=[
        Track('syrinx', 73, 100, pan=-8, velocity=100, lo='G4', hi='D6', vibrato=(3, 40, 14), parts={
            'A': TV_TUNE, 'A2': TV_TUNE, 'C': TV_GULL}),
        Track('aulos', 68, 92, pan=14, velocity=100, lo='D4', hi='Bb5', vibrato=(4, 40, 14), parts={
            'intro': 'r:6 | G4:1 D5:2 r:3', 'A2': diatonic(TV_TUNE, G_DOR, -2), 'B': TV_KLEON,
            'C': gen(TV_CH['C'], tv_call)}),
        Track('chorus', 52, 84, pan=-16, velocity=92, lo='C4', hi='D5', parts={'C': TV_CHANT}),
        # The sun on the water in B is a square wave, not the harp: harp tails over the
        # kithara and aulos overran the five DirectSound channels and the steals varied
        # from pass to pass.
        Track('glint', 81, 36, pan=-28, velocity=80, gate=0.6, lo='D4', hi='C6', parts={'B': gen(TV_CH['B'], tv_harp)}),
        Track('kithara', 24, 80, pan=24, velocity=86, gate=0.8, lo='C3', hi='D5',
              parts={s: gen(c, tv_swell) for s, c in TV_CH.items()}),
        # An octave under the kithara's root and fifth, never on them: a sine bass in
        # unison with a DirectSound note beats against it, and the beating differed
        # from pass to pass by up to 4 dB.
        Track('bass', 92, 66, velocity=100, gate=0.9, lo='C2', hi='C4',
              parts={s: gen(c, root_fifth([('r', 3), ('f', 3)], 36)) for s, c in TV_CH.items()}),
        Track('drums', 0, 90, velocity=96, kit=FRAME_KIT, parts={
            'intro': 'dum:3 r:3 | dum:3 tek:1_ tek:1_ tek:1_',
            'A': bars(TV_STROKE, 8, TV_FILL),
            'A2': bars('dum:2 tam:1_ tek:2_ tek:1_', 8, TV_FILL),
            'B': bars('dum:3 low:2_ tek:1_', 8, TV_FILL),
            'C': bars('deep:2^ deep:1 tek:2 tek:1', 8, 'deep:1 tek:1 tek:1 deep:1 tek:1 tek:1')}),
        Track('wind', 122, 64, velocity=70, lo='C3', hi='C5', parts={
            'intro': 'A3:6- | A3:6', 'A': TV_WIND, 'B': TV_WIND,
            'C': 'A3:6- | A3:6 | E3:6- | E3:6 | A3:6- | A3:6 | E3:6- | E3:3 r:3'}),
    ])

# ============================================================ The mainland road
# Act I's long roads: Route 2 under the Skironian cliffs, Route 3 over Kithairon.
# F Mixolydian (F Greek Hypophrygian), 3/4 as the tsamikos, the proud mainland
# dance of the mountain villages: long-short-long (3+1+2). Where Route 1 is an island
# dance for the syrinx, the road belongs to the aulos, as mainland songs belong to the
# reed, with long held notes and phrases that take their time.
# Distance is written in: in A2 a horn far off echoes the aulos's opening call while it
# holds; in C the dance stops for the pass, a horn line and a drone over a heartbeat
# drum, and a distant salpinx plays the Thread's call, C-F-G-A (5-1-2-3), twice, as
# if from the next valley. E-flat to F, the Mixolydian close, ends every phrase.
F_MIX = pcs('F', MIXOLYDIAN)
RD_CH = {
    'intro': ['F', 'F'],
    'A': ['F', 'F', 'Eb', 'F', 'Dm', 'Bb', 'Eb', 'F'],
    'B': ['Bb', 'F', 'Gm', 'Dm', 'Eb', 'Bb', 'Cm', 'F'],
    'C': ['Dm', 'Dm', 'Eb', 'F', 'Bb', 'Bb', 'Cm', 'F'],
}
RD_CH['A2'] = RD_CH['A3'] = RD_CH['A']
RD_TUNE = ('C5:3 F5:1 G5:2 | A5:3 G5:1 F5:2 | Eb5:3 G5:1 Bb5:2 | A5:6 | '
           'D6:3 C6:1 A5:2 | Bb5:3 A5:1 G5:2 | G5:3 Bb5:1 G5:1 Eb5:1 | F5:6')
RD_B = ('D5:3 F5:1 Bb5:2 | A5:3 G5:1 F5:2 | G5:3 A5:1 Bb5:2 | A5:3 F5:1 D5:2 | '
        'Eb5:3 G5:1 Bb5:2 | D6:3 C6:1 Bb5:2 | C6:2 Bb5:1 G5:1 Eb5:2 | F5:3 A5:1 C6:2')
RD_ECHO = 'r:6 | r:6 | r:6 | C4:3 F4:1 G4:2 | r:6 | r:6 | r:6 | C4:3 F4:1 A4:2'
RD_PASS = 'A4:6 | F4:3 G4:1 A4:2 | Bb4:6 | G4:3 F4:1 Eb4:2 | F4:6 | D4:3 Eb4:1 F4:2 | G4:3 Eb4:1 C4:2 | C4:6'
RD_CALL = 'r:6 | r:6 | r:6 | C5:1 F5:1 G5:1 A5:3 | r:6 | r:6 | r:6 | C5:1 F5:1 G5:1 A5:3'
TSAMIKO_KITHARA = offbeats([(0, 3), (1, 1), (1, 2)])
TSAMIKO_BASS = root_fifth([('r', 3), (None, 1), ('f', 2)], 36)
RD_FILL = 'dum:1 tek:1 tek:1 tek:1 low:1 low:1'
RD_SHAKER = bars('C6:1 C6:1_ C6:1_ C6:1 C6:1 C6:1_', 8)
ROAD = Song(
    name='mus_ichor_road', title='The Long Road', meter=(3, 4), grouping=(3, 1, 2), tempo=120,
    voicegroup=VG, volume=127, reverb=50, priority=0,
    sections=[('intro', 2), ('A', 8), ('A2', 8), ('B', 8), ('C', 8), ('A3', 8)], loop_from='A',
    modes={'*': F_MIX}, target=(55, 65), chords=RD_CH, ref=('MUS_ROUTE119', -21.5), tracks=[
        Track('aulos', 68, 112, pan=-6, velocity=104, lo='D4', hi='D6', vibrato=(4, 44, 14), parts={
            'A': RD_TUNE, 'A2': RD_TUNE, 'A3': RD_TUNE,
            'B': 'r:6 | r:6 | r:6 | r:6 | G4:6 | F4:6 | Eb4:6 | F4:3 A4:3'}),
        Track('syrinx', 73, 106, pan=10, velocity=100, lo='G4', hi='D6', vibrato=(3, 44, 12), parts={'B': RD_B}),
        Track('horn', 60, 78, pan=30, velocity=88, gate=0.9, lo='C4', hi='Bb4', parts={'A2': RD_ECHO, 'C': RD_PASS}),
        Track('salpinx', 56, 66, pan=-30, velocity=84, gate=0.9, lo='C5', hi='A5', parts={'C': RD_CALL}),
        Track('strings', 48, 58, pan=-20, velocity=76, lo='C4', hi='C4', parts={'C': bars('C4:6', 8)}),
        Track('kithara', 24, 86, pan=22, velocity=88, gate=0.7, lo='G3', hi='C5',
              parts={s: gen(RD_CH[s], TSAMIKO_KITHARA) for s in ('intro', 'A', 'A2', 'B', 'A3')}),
        Track('bass', 92, 72, velocity=100, gate=0.9, lo='C2', hi='C4', parts={
            **{s: gen(RD_CH[s], TSAMIKO_BASS) for s in ('intro', 'A', 'A2', 'B', 'A3')},
            'C': gen(RD_CH['C'], root_fifth([('r', 6)], 36))}),
        Track('square', 80, 40, pan=28, velocity=80, gate=0.9, lo='C4', hi='D5', parts={'A3': octave(RD_TUNE, -1)}),
        Track('drums', 0, 97, velocity=96, kit=FRAME_KIT, parts={
            'intro': 'dum:3 tek:1 dum:2 | ' + RD_FILL,
            'A': bars('dum:3 tek:1 dum:2', 8, RD_FILL),
            'A2': bars('dum:3 tek:1 low:1 tek:1', 8, RD_FILL),
            'B': bars('dum:3 tek:1_ low:2', 8, RD_FILL),
            'C': bars('dum:3_ r:3', 8, 'dum:3_ tek:1_ tek:1_ tek:1'),
            'A3': bars('dum:2 tam:1 tek:1 low:1 tek:1', 8, RD_FILL)}),
        Track('shaker', 127, 38, velocity=80, gate=0.25, lo='C6', hi='C6', parts={'A3': RD_SHAKER}),
    ])

# The road by night (sNightMusicTable plays it on any road map after dark): the same
# tune with its third darkened, A to A-flat, so F Mixolydian becomes F Dorian. Slower,
# with no dance: the syrinx alone over the lyre, crickets on the noise channel, and in
# A2 the far horn calling the Thread in the night mode, C-F-G-A-flat.
F_DOR = pcs('F', DORIAN)
RN_CH = {
    'intro': ['Fm'],
    'A': ['Fm', 'Fm', 'Eb', 'Fm', 'Bb', 'Bb', 'Eb', 'Fm'],
    'B': ['Bb', 'Fm', 'Eb', 'Bb', 'Eb', 'Bb', 'Cm', 'Fm'],
}
RN_CH['A2'] = RN_CH['A']
RN_TUNE = remap(RD_TUNE, {'A': 'Ab'})
RN_B = remap(RD_B, {'A': 'Ab'})
RN_CALL = 'r:6 | r:6 | r:6 | C4:3 F4:1 G4:2 | r:6 | r:6 | r:6 | C4:1 F4:1 G4:1 Ab4:3'


def rn_harp(c):
    r, t, f = triad(c, 48)
    return notes([(r, 1), (f, 1), (t + 12, 1), (f + 12, 1), (t + 12, 1), (f, 1)])


RN_CRICKETS = bars('G6:0.5 G6:0.5 r:2 G6:0.5 G6:0.5 r:2', 8, 'G6:0.5 G6:0.5 G6:0.5 r:4.5')
ROAD_NIGHT = Song(
    name='mus_ichor_road_night', title='The Long Road by Night', meter=(3, 4), grouping=(3, 1, 2), tempo=90,
    voicegroup=VG, volume=110, reverb=50, priority=0, sections=[('intro', 1), ('A', 8), ('B', 8), ('A2', 8)],
    loop_from='A', modes={'*': F_DOR}, target=(44, 52), chords=RN_CH, ref=('MUS_ROUTE120', -22.0), tracks=[
        Track('syrinx', 73, 127, pan=-8, velocity=96, lo='G4', hi='D6', vibrato=(3, 36, 18),
              parts={'A': RN_TUNE, 'A2': RN_TUNE}),
        Track('aulos', 68, 100, pan=14, velocity=92, lo='D4', hi='D6', vibrato=(4, 36, 18), parts={'B': RN_B}),
        Track('horn', 60, 77, pan=30, velocity=84, gate=0.9, lo='C4', hi='Ab4',
              parts={'A2': RN_CALL}),
        Track('lyre', 46, 106, pan=20, velocity=84, lo='C3', hi='C6',
              parts={s: gen(c, rn_harp) for s, c in RN_CH.items()}),
        Track('bass', 92, 58, velocity=96, lo='C2', hi='C4',
              parts={s: gen(c, root_fifth([('r', 6)], 36)) for s, c in RN_CH.items()}),
        Track('drums', 0, 84, velocity=90, kit=FRAME_KIT, parts={
            'A': bars('dum:3_ r:3', 8), 'B': bars('dum:3_ r:1 low:2_', 8), 'A2': bars('dum:3_ r:3', 8)}),
        Track('crickets', 127, 40, velocity=70, gate=0.25, lo='G6', hi='G6',
              parts={'A': RN_CRICKETS, 'B': RN_CRICKETS, 'A2': RN_CRICKETS}),
    ])

# ============================================================ Emporion City
# Corinth on the Isthmus: two seas, every road and every trader. B-flat Greek Lydian
# (Ionian), 4/4 with the 3+3+2 kick of a busy harbor, and a salpinx fanfare at the
# gate. It is grander than Akti's quay: brass, timpani and strings where Akti has a
# flute and a guitar. A: the aulos's market tune. A2: a syrinx descant and horn stabs.
# B: the eastern quarter, where the Lydian and Phoenician ships tie up. One note
# changes, F to F-sharp, and the same scale becomes D Hijaz (D-E-flat-F-sharp, the
# augmented second) over a maqsum drum. Its D lifts a semitone to E-flat for C, the
# grand harbor: strings sing over horns and timpani, the salpinx calls from the mole,
# and F falls home to B-flat.
BB_ION = pcs('Bb', IONIAN)
D_HIJAZ = pcs('D', (0, 1, 4, 5, 7, 8, 10))
EM_CH = {
    'intro': ['Bb', 'F'],
    'A': ['Bb', 'Eb', 'Bb', 'F', 'Gm', 'Eb', 'F', 'Bb'],
    'B': ['D', 'Cm', 'D', 'Eb', 'D', 'Gm', 'Cm', 'D'],
    'C': ['Eb', 'Bb', 'Cm', 'F', 'Eb', 'Bb', 'Gm', 'F'],
}
EM_CH['A2'] = EM_CH['A']
EM_TUNE = ('F5:3 D5:3 F5:2 | G5:3 Eb5:3 G5:2 | Bb5:2 A5:1 G5:1 F5:2 D5:2 | Eb5:3 D5:1 C5:2 A4:2 | '
           'D5:3 G5:3 Bb5:2 | C6:2 Bb5:1 A5:1 G5:2 Eb5:2 | F5:2 G5:1 A5:1 C6:2 A5:2 | Bb5:6 r:2')
EM_DESCANT = 'D6:8 | Bb5:8 | D6:4 C6:4 | A5:8 | Bb5:8 | G5:8 | A5:4 C6:4 | D6:8'
EM_HIJAZ = ('A4:2 Bb4:1 A4:1 G4:1 F#4:1 G4:2 | Eb5:2 D5:1 C5:1 Bb4:2 G4:2 | F#4:1 G4:1 A4:2 Bb4:1 C5:1 D5:2 | '
            'Eb5:3 D5:1 C5:2 Bb4:2 | D5:2 Eb5:1 F#5:1 G5:2 F#5:1 Eb5:1 | D5:2 Bb4:1 G4:1 D5:2 G5:2 | '
            'G5:2 F#5:1 Eb5:1 D5:2 C5:2 | D5:4 Eb5:1 F#5:1 G5:1 A5:1')
EM_HARBOR = ('Bb4:3 Eb5:3 G5:2 | F5:4 D5:4 | Eb5:3 G5:3 C6:2 | A5:4 F5:4 | '
             'G5:3 Bb5:3 G5:2 | F5:2 D5:2 Bb4:4 | D5:3 G5:3 Bb5:2 | A5:4 C6:4')
EM_CALL = 'r:8 | r:8 | r:8 | F4:1 F4:1 A4:2 C5:4 | r:8 | r:8 | r:8 | F4:1 F4:1 A4:2 C5:4'


def em_stab(c):
    r, t, f = triad(c, 55)
    return notes([(t, 1), (None, 2), (t, 1), (None, 2), (f, 1), (None, 1)])


TRESILLO_KITHARA = offbeats([(0, 1), (1, 2), (0, 1), (1, 2), (1, 2)])
TRESILLO_BASS = root_fifth([('r', 3), ('f', 3), ('o', 2)], 36)
EM_BAR = 'dum:3 tek:1 tam:2 dum:1 tek:1'
EM_FILL = 'dum:2 tek:1 tek:1 dum:1 tek:1 low:1 low:1'
EM_SHAKER = bars('C6:1 C6:1_ C6:1 C6:1_ C6:1 C6:1_ C6:1 C6:1', 8)
EMPORION = Song(
    name='mus_ichor_emporion', title='Emporion', meter=(4, 4), grouping=(3, 3, 2), tempo=120,
    voicegroup=VG, volume=110, reverb=50, priority=0,
    sections=[('intro', 2), ('A', 8), ('A2', 8), ('B', 8), ('C', 8)], loop_from='A',
    modes={'*': BB_ION, 'B': D_HIJAZ}, target=(60, 68), chords=EM_CH, ref=('MUS_SLATEPORT', -22.5), tracks=[
        Track('aulos', 68, 113, pan=-6, velocity=104, lo='F#4', hi='C6', vibrato=(4, 44, 12), parts={
            'A': EM_TUNE, 'A2': EM_TUNE, 'B': EM_HIJAZ}),
        Track('syrinx', 73, 100, pan=12, velocity=96, lo='G5', hi='D6', vibrato=(3, 44, 12), parts={'A2': EM_DESCANT}),
        Track('salpinx', 56, 108, pan=-14, velocity=104, gate=0.9, lo='F4', hi='F5', parts={
            'intro': 'F4:1 F4:1 Bb4:2 D5:2 F5:2 | Eb5:2 D5:1 C5:1 A4:2 C5:2', 'C': EM_CALL}),
        Track('horn', 60, 90, pan=20, velocity=92, gate=0.8, lo='G3', hi='C5', parts={
            'intro': 'D4:4 F4:4 | C4:4 A3:4', 'A2': gen(EM_CH['A2'], em_stab),
            'C': 'G4:8 | F4:8 | G4:8 | A4:8 | G4:8 | F4:8 | G4:8 | A4:8'}),
        Track('strings', 48, 95, pan=24, velocity=96, lo='Bb4', hi='C6', parts={'C': EM_HARBOR}),
        Track('kithara', 24, 90, pan=26, velocity=88, gate=0.6, lo='G3', hi='C5',
              parts={s: gen(EM_CH[s], TRESILLO_KITHARA) for s in ('A', 'B')}),
        Track('bass', 92, 70, velocity=100, gate=0.8, lo='C2', hi='C4', parts={
            **{s: gen(EM_CH[s], TRESILLO_BASS) for s in ('intro', 'A', 'A2', 'C')},
            'B': bars('D2:3 D2:3 A2:2', 8)}),
        Track('timpani', 47, 97, pan=6, velocity=100, gate=0.6, lo='F2', hi='C3', parts={
            'intro': 'Bb2:2 r:2 F2:2 Bb2:2 | ' + roll('F2', 8),
            'C': 'Bb2:2 r:6 | Bb2:2 r:6 | C3:2 r:6 | F2:2 r:4 F2:1 F2:1 | Bb2:2 r:6 | Bb2:2 r:6 | G2:2 r:6 | '
                 'F2:1 F2:1 F2:1 F2:1 C3:2 F2:2'}),
        Track('drums', 0, 102, velocity=96, kit=FRAME_KIT, parts={
            'intro': 'deep+crash:2 r:2 tek:1 tek:1 tek:2 | dum:1 tek:1 tek:1 tek:1 dum:1 tek:1 low:1 low:1',
            'A': bars(EM_BAR, 8, EM_FILL), 'A2': bars('dum:3 tam:1 tek:2 dum:1 tam:1', 8, EM_FILL),
            'B': bars('dum:1 tek:1 tam:1 tek:1 dum:2 tek:1 tam:1', 8, EM_FILL),
            'C': 'deep+crash:2 tek:2 dum:2 tek:1 tek:1 | ' + bars('deep:2 tek:2 dum:2 tek:1 tek:1', 7, EM_FILL)}),
        Track('shaker', 127, 36, velocity=80, gate=0.25, lo='C6', hi='C6', parts={'A2': EM_SHAKER, 'B': EM_SHAKER}),
    ])

# ============================================================ Temple of Hermes
# The Herald's Run (SYSTEMS §12): scrolls to the herms against a step-glass. D
# Hypolydian (church Lydian), 6/8 presto, a bar a second. Hermes invented the lyre on
# the day he was born, from a tortoise shell, then traded it to Apollo and made the
# pipes, so the lyre and the syrinx trade the tune. A: the syrinx over the lyre's
# running ostinato; the G-sharp is the quicksilver. A2: the lyre takes the tune and a
# square wave runs the ostinato. B is the trick: the turnstiles reverse and the mode
# turns under your feet, to D Mixolydian (C and G natural), a sly staccato aulos over
# pizzicato. C is the race, the line split note by note between syrinx and lyre over
# taiko. E to D, the Lydian II-I, brings each lap home.
D_LYD = pcs('D', LYDIAN)
D_MIX = pcs('D', MIXOLYDIAN)
HM_CH = {
    'intro': ['D'],
    'A': ['D', 'A', 'Bm', 'E', 'D', 'E', 'A', 'D'],
    'B': ['D', 'C', 'G', 'D', 'C', 'G', 'Am', 'D'],
    'C': ['E', 'D', 'E', 'D', 'Bm', 'C#m', 'D', 'E'],
}
HM_CH['A2'] = HM_CH['A3'] = HM_CH['A']
HM_TUNE = ('A5:1 F#5:1 D5:1 E5:1 F#5:1 G#5:1 | A5:2 E5:1 C#6:2 A5:1 | B5:1 A5:1 G#5:1 F#5:1 E5:1 D5:1 | '
           'E5:1 G#5:1 B5:2 G#5:1 E5:1 | F#5:1 A5:1 D6:2 C#6:1 A5:1 | B5:1 G#5:1 E5:1 G#5:1 B5:1 C#6:1 | '
           'A5:2 E5:1 C#5:2 E5:1 | D5:2 F#5:1 A5:1 D6:2')
HM_B = ('A4:1 D5:1 F#5:1 E5:1 D5:1 A4:1 | G4:1 C5:1 E5:1 D5:1 C5:1 G4:1 | B4:1 D5:1 G5:1 F#5:1 E5:1 D5:1 | '
        'A4:2 r:1 A4:1 B4:1 C5:1 | E5:2 r:1 E5:1 F#5:1 G5:1 | D5:1 B4:1 G4:1 B4:1 D5:1 E5:1 | '
        'C5:1 E5:1 A5:1 G5:1 E5:1 C5:1 | D5:2 F#5:1 A5:2 r:1')
HM_RACE = ('E5 G#5 B5 E5 G#5 B5 | D5 F#5 A5 D5 F#5 A5 | E5 G#5 B5 C#6 B5 G#5 | F#5 A5 D6 C#6 A5 F#5 | '
           'B4 D5 F#5 B5 F#5 D5 | C#5 E5 G#5 C#6 G#5 E5 | D5 F#5 A5 C#6 A5 F#5 | E5 F#5 G#5 A5 B5 C#6')
HM_PING = 'r:6 | r:6 | r:6 | r:4 B4:0.5 E5:0.5 G#5:1 | r:6 | r:6 | r:6 | r:4 A4:0.5 D5:0.5 F#5:1'


def hm_run(c):
    r, t, f = triad(c, 50)
    return notes([(r, 1), (f, 1), (r + 12, 1), (f, 1), (t + 12, 1), (f, 1)])


HM_PIZZ = root_fifth([('r', 1), (None, 2), ('f', 1), (None, 2)], 40)
HM_BAR = 'dum:1 kro:1 kro:1 low:1 kro:1 kro:1'
HM_FILL = 'dum:1 tek:1 tek:1 dum:1 tek:1 tek:1'
HERMES = Song(
    name='mus_ichor_temple_hermes', title="The Herald's Run", meter=(6, 8), grouping=(3, 3), tempo=180,
    voicegroup=VG, volume=110, reverb=50, priority=0,
    sections=[('intro', 1), ('A', 8), ('A2', 8), ('B', 8), ('C', 8), ('A3', 8)], loop_from='A',
    modes={'*': D_LYD, 'B': D_MIX}, target=(38, 42), chords=HM_CH, ref=('MUS_GYM', -21.9), tracks=[
        Track('syrinx', 73, 124, pan=-10, velocity=100, lo='G4', hi='D6', vibrato=(3, 48, 10), parts={
            'intro': 'A5:1 D6:1 A5:1 F#5:1 G#5:2', 'A': HM_TUNE, 'A3': HM_TUNE, 'C': hocket(HM_RACE, 0)}),
        Track('lyre', 46, 114, pan=14, velocity=96, lo='C3', hi='D6', parts={
            'A': gen(HM_CH['A'], hm_run), 'A2': HM_TUNE, 'C': hocket(HM_RACE, 1),
            'A3': diatonic(HM_TUNE, D_LYD, -2)}),
        Track('aulos', 68, 110, pan=18, velocity=100, gate=0.55, lo='G4', hi='A5', parts={'B': HM_B}),
        Track('pizzicato', 45, 127, pan=-22, velocity=96, gate=0.5, lo='E2', hi='D4',
              parts={s: gen(c, HM_PIZZ) for s, c in HM_CH.items() if s != 'intro'}),
        Track('square', 81, 40, pan=28, velocity=84, gate=0.7, lo='C3', hi='G#5', parts={
            'A': HM_PING, 'A2': gen(HM_CH['A2'], hm_run), 'A3': gen(HM_CH['A3'], hm_run)}),
        Track('drums', 0, 107, velocity=96, kit=FRAME_KIT, parts={
            'intro': 'kro:1 kro:1 kro:1 tek:1 tek:1 tek:1',
            'A': bars(HM_BAR, 8, HM_FILL), 'A2': bars(HM_BAR, 8, HM_FILL), 'B': bars('dum:1 r:2 tek:1_ r:2', 8, HM_FILL),
            'C': bars('taiko:1^ kro:1 tek:1 dum:1 kro:1 tek:1', 8, 'taiko:1 tek:1 tek:1 taiko:1 tek:1 tek:1'),
            'A3': bars(HM_BAR, 8, HM_FILL)}),
        Track('shaker', 127, 34, velocity=80, gate=0.25, lo='C#6', hi='C#6',
              parts={'C': bars('C#6:1 C#6:1_ C#6:1_ C#6:1 C#6:1_ C#6:1_', 8), 'A3': bars('C#6:1 C#6:1_ C#6:1_ C#6:1 C#6:1_ C#6:1_', 8)}),
    ])

# ============================================================ Eleusa Village
# Eleusis, the wheat plain on the Saronic shore. A Greek Lydian (Ionian), 2/4 as an
# easy syrtos, long-short-short, golden and unhurried. A: the syrinx's village tune,
# then the aulos sings Demeter's motif (MUSIC.md) as it sounds above ground, in
# major: A-B-A, then climbing to the light. It is Kore come home, the harvest's
# meaning; under the Telesterion the same motif is her mother's grief. B is a reaping
# song in A Mixolydian (G natural), the aulos calling and the reapers' chorus
# answering over a tsabouna drone, the island bagpipe, and the krotala's snap of the
# sickle. A2: the aulos in thirds under the syrinx, and a descant over Kore's motif.
A_ION = pcs('A', IONIAN)
A_MIX = pcs('A', MIXOLYDIAN)
EL_CH = {
    'intro': ['A', 'A'],
    'A': ['A', 'A', 'D', 'E', 'A', 'D', 'E', 'A', 'A', 'A', 'A', 'D', 'E', 'C#m', 'D', 'E'],
    'B': ['A', 'G', 'A', 'A', 'A', 'D', 'A', 'E', 'G', 'G', 'A', 'G', 'A', 'A', 'E', 'A'],
}
EL_CH['A2'] = EL_CH['A']
EL_TUNE = ('E5:2 A5:1 B5:1 | C#6:2 B5:1 A5:1 | F#5:2 A5:1 F#5:1 | E5:4 | '
           'C#5:2 E5:1 A5:1 | D5:1 F#5:1 B5:1 A5:1 | E5:2 D5:1 B4:1 | A4:4')
EL_KORE = 'A4:2 B4:2 | A4:4 | C#5:2 D5:2 | E5:2 F#5:1 E5:1 | E5:2 F#5:2 | E5:4 | D5:2 C#5:2 | B4:2 A4:2'
EL_REST8 = ' | '.join(['r:4'] * 8)
EL_DESCANT = 'C#6:4 | C#6:2 B5:2 | A5:4 | A5:4 | G#5:4 | G#5:4 | F#5:2 A5:2 | G#5:2 E5:2'
EL_CALL = ('E5:2 G5:1 E5:1 | D5:2 B4:2 | r:4 | r:4 | E5:2 A5:1 G5:1 | F#5:2 D5:2 | r:4 | r:4 | '
           'G5:2 F#5:1 E5:1 | D5:2 B4:2 | r:4 | r:4 | E5:2 G5:1 F#5:1 | E5:2 C#5:2 | r:4 | r:4')
EL_ANSWER = ('r:4 | r:4 | C#5:2 D5:1 C#5:1 | A4:4 | r:4 | r:4 | E5:2 D5:1 C#5:1 | B4:4 | '
             'r:4 | r:4 | C#5:2 B4:1 A4:1 | G4:4 | r:4 | r:4 | D5:2 C#5:1 B4:1 | A4:4')


def el_harp(c):
    r, t, f = triad(c, 62)
    return notes([(r, 1), (t, 1), (f, 1), (r + 12, 1)])


SYRTOS_KITHARA = offbeats([(0, 2), (1, 1), (1, 1)])
EL_FILL = 'dum:1 tek:1 tek:1 tek:1'
ELEUSA = Song(
    name='mus_ichor_eleusa', title='Eleusa', meter=(2, 4), grouping=(2, 1, 1), tempo=100,
    voicegroup=VG, volume=100, reverb=50, priority=0, sections=[('intro', 2), ('A', 16), ('B', 16), ('A2', 16)],
    loop_from='A', modes={'*': A_ION, 'B': A_MIX}, target=(54, 62), chords=EL_CH,
    ref=('MUS_FALLARBOR', -24.6), tracks=[
        Track('syrinx', 73, 100, pan=-8, velocity=100, lo='G4', hi='D6', vibrato=(3, 44, 12), parts={
            'A': EL_TUNE + ' | ' + EL_REST8, 'A2': EL_TUNE + ' | ' + EL_DESCANT}),
        Track('aulos', 68, 92, pan=12, velocity=100, lo='D4', hi='A5', vibrato=(4, 40, 14), parts={
            'A': EL_REST8 + ' | ' + EL_KORE, 'B': EL_CALL,
            'A2': diatonic(EL_TUNE, A_ION, -2) + ' | ' + EL_KORE}),
        Track('chorus', 52, 86, pan=-18, velocity=96, lo='G4', hi='E5', parts={'B': EL_ANSWER}),
        Track('lyre', 46, 74, pan=-26, velocity=84, lo='A3', hi='C#6', parts={
            'intro': 'A3:0.5 C#4:0.5 E4:0.5 A4:0.5 C#5:0.5 E5:0.5 A5:1 | r:4',
            'A': EL_REST8 + ' | ' + gen(EL_CH['A'][8:], el_harp)}),
        Track('kithara', 24, 80, pan=24, velocity=86, gate=0.6, lo='G3', hi='C5',
              parts={s: gen(EL_CH[s], SYRTOS_KITHARA) for s in ('intro', 'A', 'A2')}),
        Track('tsabouna', 21, 60, pan=16, velocity=86, lo='A3', hi='E4', parts={'B': bars('A3+E4:4', 16)}),
        Track('bass', 92, 62, velocity=100, gate=0.9, lo='C2', hi='C4',
              parts={s: gen(c, root_fifth([('r', 2), ('f', 2)], 36)) for s, c in EL_CH.items()}),
        Track('drums', 0, 86, velocity=96, kit=FRAME_KIT, parts={
            'intro': 'dum:2 tek:1 tek:1 | ' + EL_FILL, 'A': bars('dum:2 tek:1 tek:1', 16, EL_FILL),
            'B': bars('dum:2 kro:1 tek:1', 16, EL_FILL), 'A2': bars('dum:2 tek:1 tam:1', 16, EL_FILL)}),
        Track('shaker', 127, 40, velocity=80, gate=0.25, lo='C#6', hi='C#6',
              parts={'A2': bars('C#6:1 C#6:1_ C#6:1 C#6:1_', 16)}),
    ])

# ============================================================ Temple of Demeter: the Mysteries
# The Telesterion, under Eleusa: dark, torchlit and holy. A Greek Dorian (church
# Phrygian), 4/4 at a processional 72. A low A pedal never moves while B-flat grinds
# against it, the Phrygian semitone. A: the mystai's hymn, leaning on F-E, over the
# lyre and a slow heartbeat drum. B: the aulos sings Demeter's motif in its true form,
# her grief for Kore: A-B-flat-A (her daughter's name), a climb that searches and
# finds nothing, and the falling tetrachord D-C-B-flat-A, the lament. It sounds twice,
# the second a fifth higher, while the noise channel crackles like the torches Hecate
# lent her for the search. A2: the hymn with the aulos a third under, and in its
# last bar the chord turns major, C-sharp: Persephone's return, a promise the loop
# doesn't keep yet. "What's reaped grows again."
A_PHR = pcs('A', PHRYGIAN)
TD_CH = {
    'intro': ['Am', 'Am'],
    'A': ['Am', 'Bb', 'Am', 'Gm', 'F', 'Bb', 'Dm', 'Am'],
    'B': ['Am', 'C', 'Am', 'Bb', 'Am', 'F', 'Am', 'Bb'],
    'A2': ['Am', 'Bb', 'Am', 'Gm', 'F', 'Bb', 'Dm', 'A'],
}
TD_HYMN = ('E5:4 F5:2 E5:2 | D5:4 F5:4 | E5:2 D5:2 C5:2 A4:2 | Bb4:4 D5:4 | '
           'C5:4 A4:2 C5:2 | D5:4 F5:2 D5:2 | F5:4 E5:2 D5:2 | E5:8')
TD_GRIEF = ('A4:2 Bb4:2 A4:4 | C5:2 D5:2 E5:2 F5:1 E5:1 | E5:2 F5:2 E5:4 | D5:2 C5:2 Bb4:2 A4:2 | '
            'E5:2 F5:2 E5:4 | F5:2 G5:2 A5:2 G5:1 F5:1 | E5:2 F5:2 E5:4 | D5:2 C5:2 Bb4:2 A4:2')
TD_CRACKLE = ' | '.join(['r:1 C6:1_ r:3 C6:1_ C6:1_ r:1', 'r:3 C6:1_ r:2 C6:1_ r:1'] * 4)


def td_harp(c):
    r, t, f = triad(c, 48)
    return notes([(r, 2), (f, 1), (r + 12, 1), (t + 12, 2), (f, 2)])


TD_HEART = 'dum:1 low:1_ r:6'
TEMPLE_DEMETER = Song(
    name='mus_ichor_temple_demeter', title='The Mysteries', meter=(4, 4), grouping=(2, 2, 2, 2), tempo=72,
    voicegroup=VG, volume=94, reverb=50, priority=0, sections=[('intro', 2), ('A', 8), ('B', 8), ('A2', 8)],
    loop_from='A', modes={'*': A_PHR, 'A2': A_PHR | {1}}, target=(75, 85), chords=TD_CH,
    ref=('MUS_MT_PYRE', -24.5), tracks=[
        Track('chorus', 52, 96, pan=-8, velocity=96, lo='C4', hi='F5', parts={
            'A': TD_HYMN, 'A2': TD_HYMN, 'B': 'E4:8 | E4:8 | E4:8 | D4:8 | E4:8 | C4:8 | E4:8 | D4:8'}),
        Track('aulos', 68, 96, pan=12, velocity=100, lo='F4', hi='A5', vibrato=(5, 30, 20), parts={
            'B': TD_GRIEF,
            'A2': diatonic(' | '.join(TD_HYMN.split(' | ')[:7]), A_PHR, -2) + ' | C#5:8'}),
        Track('lyre', 46, 80, pan=-22, velocity=88, lo='C3', hi='D5', parts={
            'intro': 'r:8 | ' + td_harp('Am'), **{s: gen(TD_CH[s], td_harp) for s in ('A', 'B', 'A2')}}),
        Track('pedal', 92, 62, velocity=96, lo='A2', hi='A2',
              parts={s: bars('A2:8', n) for s, n in (('intro', 2), ('A', 8), ('B', 8), ('A2', 8))}),
        Track('bell', 14, 66, pan=-30, velocity=90, lo='A4', hi='A4', parts={'intro': 'A4:8 | r:8'}),
        Track('frame drum', 0, 84, velocity=96, kit=FRAME_KIT, parts={
            'intro': 'r:8 | ' + TD_HEART, 'A': 'dum+cym:1 low:1_ r:6 | ' + bars(TD_HEART, 7),
            'B': bars('dum:1 low:1_ r:4 tek:1_ r:1', 8), 'A2': 'dum+cym:1 low:1_ r:6 | ' + bars(TD_HEART, 7)}),
        Track('embers', 126, 38, velocity=80, gate=0.25, lo='C6', hi='C6', parts={'B': TD_CRACKLE, 'A2': TD_CRACKLE}),
    ])

# ============================================================ Titan admin battle
# Hyperion at Eleusa; Iapetos and Rhea when they first fight. Above the grunts'
# MUS_ICHOR_TITAN in every way: the grunts are in B Greek Mixolydian (church Locrian)
# and 9/8; the admins are a fourth higher, E Greek Mixolydian, and in 7/8 as 2+2+3,
# a gait the grunts can't march to. The salpinx opens with the Sickle (MUSIC.md), the
# Titans' tritone call, now E-B-flat-A, and the tuba and wave bass grind E-F. A2 adds
# horns in thirds. B shifts the centre to A on the same notes, a horn melody over the
# string ostinato. C is the chant, chorus and horns over pounding drums, and its last
# chord, B-flat to E, is the Sickle's tritone as harmony. Nine tracks: the tenth is
# kept free for each admin's own top layer later (forge hammers for Hyperion, an aulos
# chorus for Iapetos, Rhea's slow Lakonian drum), as STORY's music plan asks.
E_LOC = pcs('E', LOCRIAN)
AD_CH = {
    'intro': ['Edim', 'Edim'],
    'A': ['Edim', 'F', 'Edim', 'Dm', 'Edim', 'F', 'Gm', 'Edim'],
    'B': ['Am', 'Bb', 'Am', 'Gm', 'F', 'Gm', 'Am', 'Bb'],
    'C': ['Dm', 'C', 'Bb', 'Am', 'Dm', 'C', 'Bb', 'Edim'],
}
AD_CH['A2'] = AD_CH['A3'] = AD_CH['A']
AD_THEME = ('E4:2 Bb4:2 A4:3 | F4:1 G4:1 A4:2 C5:3 | E5:2 Bb4:2 A4:3 | F4:2 A4:2 D5:3 | '
            'E5:2 F5:2 E5:1 D5:1 C5:1 | C5:2 D5:2 F5:3 | G5:2 F5:2 D5:1 Bb4:1 G4:1 | A4:2 Bb4:2 E5:3')
AD_HORN_B = ('A4:2 Bb4:2 C5:3 | D5:2 C5:2 Bb4:3 | A4:2 G4:2 A4:3 | Bb4:2 A4:2 G4:3 | '
             'F4:2 G4:2 A4:3 | Bb4:2 C5:2 D5:3 | C5:2 D5:2 E5:3 | D5:2 C5:2 Bb4:3')
AD_CHANT = 'D5:7 | C5:7 | Bb4:7 | A4:7 | D5:7 | E5:7 | F5:7 | E5:7'


def ad_strings(c):
    r = triad(c, 64)[0]
    up, down = step(r, E_LOC, 1), step(r, E_LOC, -1)
    return notes([(r, 1), (up, 1), (r, 1), (up, 1), (r, 1), (down, 1), (r, 1)])


def ad_riff(octave_up=0):
    def fn(c):
        r = triad(c, 36)[0] + 12 * octave_up
        return notes([(r, 2), (step(r, E_LOC, 1), 2), (r, 3)])
    return fn


def ad_timpani(c):
    r = triad(c, 40)[0]
    return notes([(r, 2), (None, 2), (r, 3)])


AD_BAR = 'deep:2 snare:2 taiko:1 snare:1 snare:1'
AD_FILL = 'deep:2 snare:1 snare:1 snare:1 snare:1 snare:1^'
BATTLE_ADMIN = Song(
    name='mus_ichor_battle_admin', title='Titan Admin', meter=(7, 8), grouping=(2, 2, 3), tempo=168,
    voicegroup=VG, volume=69, reverb=50, priority=1,
    sections=[('intro', 2), ('A', 8), ('A2', 8), ('B', 8), ('C', 8), ('A3', 8)], loop_from='A',
    modes={'*': E_LOC}, target=(45, 55), chords=AD_CH, ref=('MUS_VS_AQUA_MAGMA_LEADER', -22.6), tracks=[
        Track('salpinx', 56, 104, pan=-8, velocity=106, gate=0.9, lo='E4', hi='G5',
              parts={'A': AD_THEME, 'A2': AD_THEME, 'A3': AD_THEME}),
        Track('square', 80, 71, pan=-28, velocity=88, gate=0.9, lo='E4', hi='G5', parts={'A': AD_THEME, 'A3': AD_THEME}),
        Track('horn', 60, 88, pan=18, velocity=100, gate=0.9, lo='A3', hi='E5', parts={
            'A2': diatonic(AD_THEME, E_LOC, -2), 'B': AD_HORN_B, 'C': octave(AD_CHANT, -1),
            'A3': diatonic(AD_THEME, E_LOC, -2)}),
        Track('chorus', 52, 90, pan=-16, velocity=100, lo='A4', hi='F5', parts={'C': AD_CHANT}),
        Track('strings', 48, 78, pan=26, velocity=92, gate=0.8, lo='D4', hi='E5', parts={
            'intro': 'E4:1 F4:1 G4:1 A4:1 Bb4:1 C5:1 D5:1 | E5:7',
            **{s: gen(AD_CH[s], ad_strings) for s in ('A', 'A2', 'B', 'A3')}}),
        Track('tuba', 58, 94, pan=-4, velocity=108, gate=0.8, lo='C2', hi='C3',
              parts={s: gen(c, ad_riff()) for s, c in AD_CH.items()}),
        Track('bass', 87, 120, velocity=104, gate=0.7, lo='C3', hi='C4',
              parts={s: gen(c, ad_riff(1)) for s, c in AD_CH.items()}),
        Track('timpani', 47, 90, pan=10, velocity=100, gate=0.6, lo='E2', hi='D3', parts={
            'intro': 'E2:2 r:2 E2:3 | ' + ' '.join(['E2:0.5'] * 14),
            'A': gen(AD_CH['A'], ad_timpani), 'C': gen(AD_CH['C'], ad_timpani)}),
        Track('drums', 0, 96, velocity=100, kit=FRAME_KIT, parts={
            'intro': 'deep:2^ r:2 deep:3 | taiko:1 taiko:1 snare:1 snare:1 snare:1 snare:1 snare:1^',
            'A': 'deep+crash:2 snare:2 taiko:1 snare:1 snare:1 | ' + bars(AD_BAR, 7, AD_FILL),
            'A2': bars('deep:2 snare:2 taiko:1 taiko:1 snare:1', 8, AD_FILL),
            'B': 'taiko+crash:2 tam:2 taiko:1 snare:1 tam:1 | ' + bars('taiko:2 tam:2 taiko:1 snare:1 tam:1', 7, AD_FILL),
            'C': 'deep+crash:2 taiko:2 deep:1 taiko:1 taiko:1 | ' + bars('deep:2 taiko:2 deep:1 taiko:1 taiko:1', 7,
                                                                       'snare:1 snare:1 snare:1 snare:1 snare:1^ '
                                                                       'snare:1^ snare:1^'),
            'A3': 'deep+crash:2 snare:2 taiko:1 snare:1 snare:1 | ' + bars(AD_BAR, 7, AD_FILL)}),
    ])

# ============================================================ Daphne's revelation
# The Telesterion after the theft, one lamp on the steps (STORY §6.2, §7.1). The cue
# opens as the bible asks, with one sustained aulos note: a D that never moves. Over it
# the lyre tries the Thread, A-D-E, and stops where its third should be. It tries
# again and falls back. That is the hero's thread: there is none. B is Daphne's part,
# her theme (the Question) on the syrinx, since Syrinx, like Daphne, was a nymph who
# fled a god and became a plant. She asks it in D Lydian: A-D-E-F-sharp, the Thread
# with the third it was missing, then G-sharp, the raised fourth, hanging. Then the
# lyre joins her in tenths and they climb together ("when people were sure of a
# story, they put it in the sky"), with a triangle for stars, and she ends on her
# G-sharp, which rises to the A that starts the lyre's Thread again at the loop. The
# thread motif meets Daphne's theme: the question is what gives the thread its third.
D_LYD_R = pcs('D', LYDIAN)
RV_CH = {
    'intro': ['Dm', 'Dm'],
    'A': ['Dm', 'Dm', 'Dm', 'Dm', 'C', 'C', 'Am', 'Dm'],
    'B': ['D', 'E', 'D', 'E', 'F#m', 'Bm', 'A', 'E'],
}
RV_THREAD = 'A4:2 D5:2 E5:2 r:2 | r:8 | A4:2 D5:2 E5:2 r:2 | r:4 E5:2 D5:2 | A4:2 D5:2 E5:4 | r:8 | r:8 | r:8'
RV_QUESTION = ('A4:2 D5:1 E5:1 F#5:4 | G#5:6 r:2 | A4:2 D5:1 E5:1 F#5:2 A5:2 | G#5:4 F#5:2 E5:2 | '
               'A5:2 B5:2 C#6:4 | D6:8 | C#6:4 A5:4 | G#5:8')
RV_JOIN = 'r:8 | r:8 | r:8 | r:8 | F#4:2 G#4:2 A4:4 | B4:8 | A4:4 F#4:4 | E4:8'
RV_DRONE = ' | '.join(['D4:8-'] * 7 + ['D4:8'])
REVELATION = Song(
    name='mus_ichor_revelation', title='What You Are', meter=(4, 4), grouping=(2, 2, 2, 2), tempo=72,
    voicegroup=VG, volume=127, reverb=50, priority=0, sections=[('intro', 2), ('A', 8), ('B', 8)], loop_from='A',
    modes={'*': D_DOR, 'B': D_LYD_R}, target=(50, 56), chords=RV_CH, ref=('MUS_SEALED_CHAMBER', -23.7), tracks=[
        Track('aulos', 68, 100, pan=-4, velocity=88, lo='D4', hi='D4', vibrato=(3, 24, 36), parts={
            'intro': 'D4:8- | D4:8', 'A': RV_DRONE, 'B': RV_DRONE}),
        Track('lyre', 46, 127, pan=-14, velocity=96, lo='E4', hi='E5', parts={'A': RV_THREAD, 'B': RV_JOIN}),
        Track('syrinx', 73, 124, pan=12, velocity=96, lo='A4', hi='D6', vibrato=(3, 36, 18), parts={'B': RV_QUESTION}),
        Track('strings', 48, 65, pan=24, velocity=76, lo='E3', hi='A3',
              parts={'A': 'r:8 | r:8 | r:8 | r:8 | E3+G3:8 | E3+G3:8 | E3+A3:8 | F3+A3:8'}),
        Track('bass', 92, 50, velocity=90, lo='D2', hi='B2', parts={'B': 'D2:8 | E2:8 | D2:8 | E2:8 | F#2:8 | B2:8 | A2:8 | E2:8'}),
        Track('stars', 0, 74, velocity=80, kit=FRAME_KIT, parts={
            'B': 'r:8 | r:8 | r:8 | r:8 | tri:2_ r:6 | r:4 tri:2_ r:2 | tri:2_ r:6 | r:8'}),
    ])

# ============================================================ The Hollow (caves and woods)
# Act I's waypoints, Hecate's Hollow first, and any cave or wood after it, as Emerald
# reuses Petalburg Woods. E Hypodorian (Aeolian), 4/4 at a careful walk: pizzicato
# steps, a low aulos, and the syrinx answering it a dotted crotchet later an octave
# up, the hollow's echo. A harp drips now and then. B is Hecate's crossroads: the
# syrinx leads through the chromatic genus E-C-sharp-C-B, the old Greek colour for the
# uncanny. In A2 the syrinx carries the tune and the aulos becomes the echo, below.
E_AEO = pcs('E', AEOLIAN)
HW_CH = {
    'intro': ['Em'],
    'A': ['Em', 'Em', 'C', 'D', 'Em', 'Am', 'Bm', 'Em'],
    'B': ['A Am', 'A', 'Am', 'Em', 'C', 'A Am', 'Am', 'Bm'],
}
HW_CH['A2'] = HW_CH['A']
HW_TUNE = ('E4:3 G4:1 B4:2 A4:2 | G4:3 F#4:1 E4:4 | E4:2 G4:2 C5:3 B4:1 | A4:4 F#4:2 D4:2 | '
           'E4:3 G4:1 B4:2 E5:2 | C5:3 B4:1 A4:2 E4:2 | F#4:3 A4:1 B4:2 D5:2 | B4:4 G4:2 E4:2')
HW_B = ('E5:2 C#5:2 C5:2 B4:2 | A4:4 C#5:2 E5:2 | E5:2 C5:2 B4:2 A4:2 | G4:4 B4:4 | '
        'C5:2 E5:2 G5:2 E5:2 | E5:2 C#5:2 C5:2 B4:2 | A4:2 C5:2 E5:2 A5:2 | F#5:4 D5:2 B4:2')
HW_DRIPS = 'r:5 B6:1_ r:2 | r:8 | r:2 G6:1_ r:5 | r:8 | r:6 E6:1_ r:1 | r:8 | r:1 F#6:1_ r:6 | r:8'


def hw_walk(a, b=None):
    r, t, f = triad(a, 40)
    if b is None:
        return notes([(r, 2), (t, 2), (f, 2), (t, 2)])
    r2, t2, _ = triad(b, 40)
    return notes([(r, 2), (t, 2), (r2, 2), (t2, 2)])


HOLLOW = Song(
    name='mus_ichor_hollow', title='The Hollow', meter=(4, 4), grouping=(2, 2, 2, 2), tempo=96,
    voicegroup=VG, volume=100, reverb=50, priority=0, sections=[('intro', 1), ('A', 8), ('B', 8), ('A2', 8)],
    loop_from='A', modes={'*': E_AEO, 'B': E_AEO | {1}}, target=(56, 64), chords=HW_CH,
    ref=('MUS_PETALBURG_WOODS', -26.4), tracks=[
        Track('aulos', 68, 96, pan=-10, velocity=100, lo='D4', hi='E5', vibrato=(4, 32, 20),
              parts={'A': HW_TUNE, 'A2': delay(HW_TUNE, 3, 96)}),
        Track('syrinx', 73, 84, pan=16, velocity=88, lo='G4', hi='E6', vibrato=(3, 36, 16), parts={
            'A': delay(octave(HW_TUNE, 1), 3, 96), 'B': HW_B, 'A2': octave(HW_TUNE, 1)}),
        Track('lyre', 46, 70, pan=-28, velocity=80, lo='E6', hi='B6', parts={'A': HW_DRIPS, 'B': HW_DRIPS, 'A2': HW_DRIPS}),
        Track('pizzicato', 45, 110, pan=-18, velocity=92, gate=0.5, lo='E2', hi='A3',
              parts={s: gen(c, per_bar(hw_walk)) for s, c in HW_CH.items()}),
        Track('ison', 92, 50, velocity=90, lo='E2', hi='E2',
              parts={s: bars('E2:8', n) for s, n in (('intro', 1), ('A', 8), ('B', 8), ('A2', 8))}),
        Track('frame drum', 0, 70, velocity=90, kit=FRAME_KIT, parts={
            'intro': 'dum:2_ r:2 low:2_ r:2', 'A': bars('dum:2_ r:2 low:2_ r:2', 8),
            'B': bars('dum:2_ tek:1_ r:1 low:2_ r:2', 8), 'A2': bars('dum:2_ r:2 low:2_ r:2', 8)}),
    ])

ACT1_SONGS = [ELPIS_LULLABY, ELPIS_LULLABY_BOX, TRIREME, ROAD, ROAD_NIGHT, EMPORION, HERMES, ELEUSA,
              TEMPLE_DEMETER, BATTLE_ADMIN, REVELATION, HOLLOW]
