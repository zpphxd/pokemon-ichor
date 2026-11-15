"""The Oikoumene's music, batch 1 (design/oikoumene/BUILD.md §5; OIKOUMENE.md §7;
PERIODOS.md §6). All original, all on the `ichor` voicegroup. Notation is as in
songs.py, which imports this module at its end (so import songs, not this). The
motifs these songs quote are mapped in design/MUSIC.md; the cue sheet, with each
song's maps and its revision passes, is design/oikoumene/MUSIC_cues.md.

Each land track has its own mode and meter, so a player can tell the lands apart
by ear:
  The Wider World   D Mixolydian   6/8          the chart and the sea lanes
  The Plain of Troy E Dorian       4/4 march    the Troad
  The Black Land    A "Hijazkar"   2/4 malfuf   Egypt by day
  The Necropolis    A "Hijazkar"   4/4, slow    Egypt by night
  The Black Sea     G Phrygian     9/8 3+3+3    the Black Sea

The Periodos (the ten halls) changes meter between its sections, which compose.Song
can't, so those songs are MeterSongs: the same Song with a meter per section.
"""
from collections import namedtuple

from compose import EIGHTH, TPQ, Song, Track, parse_part, pname
from songs import (AEOLIAN, DORIAN, FRAME_KIT, MIXOLYDIAN, PHRYGIAN, VG, bars, diatonic, gen,
                   notes, octave, pcs, triad)
from songs_act1 import render
from songs_engine import offbeats, root_fifth

# The double harmonic ("Hijazkar" to an Arab musician): a Hijaz tetrachord on the
# tonic and another on the fifth, A-Bb-C#-D and E-F-G#-A. Every Greek genus puts its
# widest step at the top of the tetrachord; this one puts it in the middle, so to a
# Greek ear it is the foreign mode, the sound of the Black Land.
HIJAZKAR = (0, 1, 4, 5, 7, 8, 11)


# ---------------------------------------------------------------- helpers

class MeterSong(Song):
    """A Song whose sections may each have their own meter: meters={'B': (9, 8)}.
    `meter` is the default (and the one the .mid's time signature names; mid2agb uses
    time signatures only for its bar comments, so timing is exact either way)."""
    def __init__(self, meters=None, **kw):
        super().__init__(**kw)
        self.meters = meters or {}

    def sec_bar_ticks(self, sec):
        num, den = self.meters.get(sec, self.meter)
        return num * (TPQ * 4 // den)

    def section_starts(self):
        starts, t = {}, 0
        for name, n in self.sections:
            starts[name] = t
            t += n * self.sec_bar_ticks(name)
        return starts, t

    def build(self):
        starts, _ = self.section_starts()
        out = {}
        for tr in self.tracks:
            evs = []
            for sec, n in self.sections:
                if sec not in tr.parts:
                    continue
                bt = self.sec_bar_ticks(sec)
                got, nb = parse_part(tr.parts[sec], bt, tr.kit, f'{self.name}/{tr.name}/{sec}')
                if nb != n:
                    raise ValueError(f'{self.name}/{tr.name}/{sec}: {nb} bars, expected {n}')
                for start, dur, keys, dv, gs in got:
                    sound = max(1, int(round(dur * tr.gate * gs)))
                    vel = max(1, min(127, tr.velocity + dv))
                    for k in keys:
                        evs.append((starts[sec] + start, sound, k, vel, sec))
            out[tr] = evs
        return out


def phrase(part, first, last=None):
    """Bars first..last (1-based, inclusive) of a part."""
    b = part.split(' | ')
    return ' | '.join(b[first - 1:last or first])


def augment(part, bar_eighths, factor=2):
    """A part played `factor` times slower, rebarred into bars `factor` times as long:
    the day's tune at the pace of a funeral."""
    evs, n = parse_part(part, bar_eighths * EIGHTH, {}, 'augment')
    return render([(s * factor, d * factor, pname(k[0])) for s, d, k, *_ in evs],
                  bar_eighths * EIGHTH * factor, n)


def low_fifth(lo=36, hi=47):
    """The root's fifth, above if it stays at or under `hi`, else an octave down."""
    def fn(c):
        r = triad(c, lo)[0]
        return r + 7 if r + 7 <= hi else r - 5
    return fn


def timp_fifth(lo=40):
    """The timpani on the chord's fifth, in lo..lo+11: off the bass's roots, so the
    DirectSound drum never sits in unison with a PSG bass."""
    def fn(c):
        f = triad(c, lo)[2]
        return f - 12 if f > lo + 11 else f
    return fn


def arp(pattern, lo):
    """A broken chord from (degree, eighths): r t f, R T F an octave up, None a rest."""
    def fn(c):
        r, t, f = triad(c, lo)
        tone = {'r': r, 't': t, 'f': f, 'R': r + 12, 'T': t + 12, 'F': f + 12}
        return notes([(tone.get(k), d) for k, d in pattern])
    return fn


# ============================================================ The Wider World
# The Oikoumene chart, and the sea lanes between its lands. It is the Aethos sea
# theme, the trireme's syrinx tune (mus_ichor_trireme A), widened: moved to D and from
# Dorian to Mixolydian, so its third rises (F to F#) and its head becomes the Thread in
# major, A-D-E-F# (5-1-2-3, MUSIC.md motif 1). Where the trireme's second phrase
# climbs by step to its fifth, this one leaps an octave to D6: the sea opening out.
# D Mixolydian (Greek Hypophrygian), 6/8, a little broader than the trireme (96, not
# 100), and the kithara rolls across two octaves the whole way.
# A: the syrinx. A2: the horn takes the tune an octave down, with a syrinx descant.
# B: the open sea, an aulos strain on C and G, the flat seventh (C) carrying the
# Mixolydian colour, with a square glint on the water. C: the chart unrolls: the
# strings play the Thread in augmentation, a bar a note (A, D, E, F#), with the horn
# under it and the syrinx soaring over. C falls C to D, the Mixolydian close, into A.
D_MIX = pcs('D', MIXOLYDIAN)
WW_CH = {
    'intro': ['D', 'C'],
    'A': ['D', 'Bm', 'C', 'Am', 'D', 'D', 'C', 'D'],
    'B': ['C', 'G', 'D', 'Am', 'C', 'G', 'C', 'D'],
    'C': ['D', 'G', 'C', 'D', 'G', 'Am', 'C', 'D'],
}
WW_CH['A2'] = WW_CH['A']
WW_TUNE = ('A4:3 D5:2 E5:1 | F#5:2 E5:1 D5:2 B4:1 | C5:3 A4:2 G4:1 | A4:6 | '
           'A4:3 D5:2 E5:1 | F#5:2 A5:1 D6:3 | C6:2 A5:1 G5:2 E5:1 | D5:6')
WW_DESCANT = ('F#5:3 E5:2 F#5:1 | D5:3 B4:2 D5:1 | E5:3 G5:2 E5:1 | C5:3 E5:3 | '
              'F#5:3 A5:2 F#5:1 | A5:3 F#5:2 A5:1 | G5:3 E5:2 C5:1 | D5:3 F#5:2 A5:1')
WW_SEA = ('E5:3 G5:2 E5:1 | D5:3 B4:2 G4:1 | A4:3 D5:2 F#5:1 | E5:6 | '
          'E5:3 G5:2 C6:1 | B5:3 G5:2 D5:1 | C5:2 E5:1 G5:2 E5:1 | D5:3 E5:2 F#5:1')
WW_THREAD = 'A4:6 | D5:6 | E5:6 | F#5:6 | G5:6 | E5:6 | C5:6 | D5:6'
WW_UNDER = 'F#4:6 | B4:6 | C5:6 | A4:6 | D5:6 | C5:6 | G4:6 | A4:6'
WW_SOAR = 'r:6 | D6:3 B5:2 G5:1 | C6:3 G5:2 E5:1 | D6:3 A5:2 F#5:1 | B5:3 D6:2 B5:1 | C6:3 A5:2 E5:1 | G5:3 E5:2 C5:1 | A5:6'
WW_ROLL = arp([('r', 1), ('f', 1), ('R', 1), ('T', 1), ('R', 1), ('f', 1)], 48)
WW_STRUM = arp([('r', 1), ('f', 1), ('R', 1), ('T', 1), ('F', 1), ('T', 1)], 48)
WW_WIND = 'A3:6- | A3:3 r:3 | E3:6- | E3:3 r:3 | A3:6- | A3:3 r:3 | E3:6- | E3:3 r:3'
WW_FILL = 'dum:3 tek:1 tek:1 low:1'
WIDER_WORLD = Song(
    name='mus_ichor_wider_world', title='The Wider World', meter=(6, 8), grouping=(3, 3), tempo=96,
    voicegroup=VG, volume=100, reverb=50, priority=0,
    sections=[('intro', 2), ('A', 8), ('A2', 8), ('B', 8), ('C', 8)], loop_from='A',
    modes={'*': D_MIX}, target=(55, 65), chords=WW_CH, ref=('MUS_SAILING', -23.4), tracks=[
        Track('syrinx', 73, 100, pan=-8, velocity=100, lo='G4', hi='D6', vibrato=(3, 40, 14), parts={
            'A': WW_TUNE, 'A2': WW_DESCANT, 'C': WW_SOAR}),
        Track('aulos', 68, 108, pan=14, velocity=100, lo='D4', hi='C6', vibrato=(4, 40, 14), parts={
            'intro': 'r:6 | A4:3 D5:2 E5:1', 'B': WW_SEA}),
        Track('horn', 60, 84, pan=20, velocity=92, gate=0.9, lo='G3', hi='D5', parts={
            'A2': octave(WW_TUNE, -1), 'C': WW_UNDER}),
        Track('strings', 48, 84, pan=-20, velocity=88, lo='B3', hi='G5', parts={
            'B': gen(WW_CH['B'], lambda c: notes([(triad(c, 57)[1], 6)])), 'C': WW_THREAD}),
        # Above the aulos and kithara (from D6), so the square never doubles a
        # DirectSound note in unison.
        Track('glint', 81, 36, pan=-28, velocity=80, gate=0.6, lo='D6', hi='G7',
              parts={'B': gen(WW_CH['B'], arp([('r', 1), ('t', 1), ('f', 1), ('t', 1), ('r', 1), ('t', 1)], 86))}),
        Track('kithara', 24, 84, pan=24, velocity=86, gate=0.8, lo='C3', hi='E5', parts={
            'intro': gen(WW_CH['intro'], WW_ROLL), 'A': gen(WW_CH['A'], WW_ROLL), 'A2': gen(WW_CH['A2'], WW_ROLL),
            'B': gen(WW_CH['B'], WW_STRUM), 'C': gen(WW_CH['C'], WW_STRUM)}),
        # An octave under the kithara's roots and fifths, never on them (MUSIC.md's
        # engine lessons: a sine in unison with a DirectSound note beats differently
        # from pass to pass).
        Track('bass', 92, 66, velocity=100, gate=0.9, lo='C2', hi='B3',
              parts={s: gen(c, root_fifth([('r', 3), ('f', 3)], 36)) for s, c in WW_CH.items()}),
        Track('drums', 0, 86, velocity=96, kit=FRAME_KIT, parts={
            'intro': 'dum:3 r:3 | dum:3 tek:1_ tek:1_ tek:1_',
            'A': bars('dum:3 tek:2_ tek:1_', 8, WW_FILL),
            'A2': bars('dum:2 tam:1_ tek:2_ tek:1_', 8, WW_FILL),
            'B': 'dum+cym:2 tam:1_ low:2 tek:1_ | ' + bars('dum:2 tam:1_ low:2 tek:1_', 7, WW_FILL),
            'C': 'deep+cym:3 tek:2_ tek:1_ | ' + bars('deep:3 tek:2_ tek:1_', 7, 'deep:1 tek:1 tek:1 deep:1 tek:1 tek:1')}),
        Track('wind', 122, 56, velocity=70, lo='C3', hi='C5', parts={
            'intro': 'A3:6- | A3:6', 'A': WW_WIND, 'B': WW_WIND, 'C': WW_WIND}),
    ])

# ============================================================ The Plain of Troy
# The Troad: Sestos, Ilion and the roads across the Skamander plain. E Dorian (E Greek
# Phrygian), 4/4, a slow march at 80 for aulos and frame drum, the march that has
# gone on for ten years and never reaches the city. The drum walks a dotted step
# (long-short, long, long), and the aulos walks it too.
# "Never quite arrives": E is home, and the plain says so, a pedal E in the bass and
# strings under the whole of A. But no phrase ends there. The first stops a step
# above it, on F#; the second climbs to C#, the Dorian sixth, and sinks to D, the
# step below. The march's last bar is always D major, and the loop marches on.
# Homer's Troy is "windy Ilion", so the sea wind blows through A.
# A: aulos, frame drum, the pedal. A2: the double aulos's second pipe (accordion)
# holds the drone E4 above the pedal, and the kithara steps in on the off beats.
# B: the walls. The pedal lifts, the harmony moves (G, D, A), horns and strings hold
# under the aulos, timpani on each downbeat; it reaches C#6 and still ends on D.
E_DOR = pcs('E', DORIAN)
PT_CH = {
    'intro': ['Em', 'Em'],
    'A': ['Em', 'A', 'Em', 'Bm', 'Em', 'A', 'G', 'D'],
    'B': ['G', 'D', 'A', 'Bm', 'G', 'F#m', 'A', 'D'],
}
PT_CH['A2'] = PT_CH['A']
PT_TUNE = ('B4:3 B4:1 E5:2 F#5:2 | G5:3 F#5:1 E5:2 C#5:2 | E5:3 F#5:1 G5:2 A5:2 | F#5:6 r:2 | '
           'B4:3 B4:1 E5:2 F#5:2 | G5:3 A5:1 B5:2 C#6:2 | B5:3 A5:1 G5:2 F#5:1 E5:1 | D5:6 r:2')
PT_WALLS = ('D5:3 G5:1 B5:4 | A5:3 F#5:1 D5:4 | C#5:3 E5:1 A5:2 G5:1 F#5:1 | F#5:6 r:2 | '
            'D5:3 G5:1 B5:2 D6:2 | C#6:3 B5:1 A5:2 F#5:2 | E5:3 F#5:1 G5:2 A5:2 | B5:3 A5:1 F#5:4')
PT_HORN = 'B3:8 | A3:8 | C#4:8 | D4:8 | B3:8 | C#4:8 | E4:8 | D4:8'
PT_STEP = 'dum:3 tek:1_ dum:2 tek:2_'
PT_FILL = 'dum:2 tek:1 tek:1 dum:1 tek:1 tek:1 tek:1'
PT_KITHARA = offbeats([(0, 2), (1, 2), (0, 2), (1, 2)], 55)
PT_WIND = bars('A3:8- | A3:4 r:4', 4)
PLAIN_OF_TROY = Song(
    name='mus_ichor_plain_of_troy', title='The Plain of Troy', meter=(4, 4), grouping=(3, 1, 2, 2), tempo=80,
    voicegroup=VG, volume=127, reverb=50, priority=0,
    sections=[('intro', 2), ('A', 8), ('A2', 8), ('B', 8)], loop_from='A',
    modes={'*': E_DOR}, target=(65, 75), chords=PT_CH, ref=('MUS_ROUTE120', -22.0), tracks=[
        Track('aulos', 68, 108, pan=-6, velocity=104, lo='B4', hi='D6', vibrato=(4, 36, 16), parts={
            'A': PT_TUNE, 'A2': PT_TUNE, 'B': PT_WALLS}),
        Track('aulos 2', 21, 64, pan=16, velocity=90, lo='E4', hi='E4', parts={'A2': bars('E4:8', 8)}),
        Track('horn', 60, 74, pan=24, velocity=88, gate=0.95, lo='A3', hi='E4', parts={'B': PT_HORN}),
        Track('strings', 48, 56, pan=-22, velocity=80, lo='E3', hi='B3', parts={
            'intro': 'r:8 | E3+B3:8', 'A': bars('E3+B3:8', 8)}),
        Track('kithara', 24, 80, pan=26, velocity=86, gate=0.5, lo='G3', hi='C#5',
              parts={'A2': gen(PT_CH['A2'], PT_KITHARA), 'B': gen(PT_CH['B'], PT_KITHARA)}),
        Track('bass', 92, 49, velocity=100, gate=0.95, lo='C2', hi='C3', parts={
            'intro': 'E2:8 | E2:8', 'A': bars('E2:3 E2:1 E2:4', 8), 'A2': bars('E2:3 E2:1 E2:4', 8),
            'B': gen(PT_CH['B'], root_fifth([('r', 6), ('r', 2)], 36))}),
        Track('timpani', 47, 84, pan=8, velocity=96, gate=0.6, lo='E2', hi='D#3',
              parts={'B': gen(PT_CH['B'], lambda c: notes([(timp_fifth()(c), 2), (None, 6)]))}),
        Track('frame drum', 0, 96, velocity=100, kit=FRAME_KIT, parts={
            'intro': 'dum:2 r:2 dum:2 r:2 | ' + PT_FILL,
            'A': bars(PT_STEP, 8, PT_FILL),
            'A2': bars('dum:3 tek:1_ dum:2 low:1 tek:1_', 8, PT_FILL),
            'B': 'deep+cym:3 tek:1 dum:2 tek:1 tek:1 | ' + bars('deep:3 tek:1 dum:2 tek:1 tek:1', 7, PT_FILL)}),
        Track('wind', 122, 39, velocity=70, lo='A3', hi='A3', parts={
            'intro': 'A3:8- | A3:8', 'A': PT_WIND, 'A2': PT_WIND}),
    ])

# ============================================================ The Black Land
# Egypt by day: Naukratis, Memphis, the Delta. Herodotus calls the country "the gift
# of the river", and Kemet, its own name for itself, means the Black Land: the river's
# mud. A double harmonic on A (Hijazkar), the foreign mode: A-Bb-C#-D-E-F-G#. 2/4 on
# the malfuf, Egypt's own rhythm, three-three-two in sixteenths, at 96.
# The harp sings (Egypt's harp, held upright like a bow), the sistrum rattles on the
# noise channel (Hathor's and Isis's rattle of bronze discs), and the kithara keeps a
# single-note drone figure under it, the way an oud would.
# The hook is the first bar, E-F-E falling to C#: the sigh on the fifth, then the
# augmented second turning, C#-Bb-C#. Every phrase comes home to A.
# A: the harp. B: the aulos sings a long answer around D. A2: the harp and the aulos
# together in heterophony, one tune at two speeds as an Egyptian band plays it, with
# the riq (tambourine) on the downbeats.
A_HJK = pcs('A', HIJAZKAR)
BL_CH = {
    'intro': ['A', 'A'],
    'A': ['A', 'Bb', 'A', 'A', 'Dm', 'Dm', 'Bb', 'A', 'A', 'Bb', 'A', 'A', 'Bb', 'A', 'Bb', 'A'],
    'B': ['Dm', 'Dm', 'Dm', 'A', 'Bb', 'Dm', 'A', 'A', 'Dm', 'Dm', 'Bb', 'A', 'Dm', 'Dm', 'A', 'A'],
}
BL_CH['A2'] = BL_CH['A']
BL_TUNE = ('E5:1.5 F5:0.5 E5:1 C#5:1 | D5:1 C#5:1 Bb4:1 C#5:1 | A4:1 C#5:1 E5:1 G#5:1 | A5:3 r:1 | '
           'F5:1.5 G#5:0.5 F5:1 E5:1 | D5:1 E5:1 F5:1 D5:1 | C#5:1 D5:1 Bb4:1 C#5:1 | A4:4 | '
           'E5:1.5 F5:0.5 E5:1 C#5:1 | D5:1 C#5:1 Bb4:1 C#5:1 | A4:1 C#5:1 E5:1 G#5:1 | A5:2 C#6:2 | '
           'Bb5:1 A5:1 G#5:1 F5:1 | E5:2 F5:1 E5:1 | D5:1 C#5:1 Bb4:1 G#4:1 | A4:4')
BL_HEAD = phrase(BL_TUNE, 1, 8)  # the first phrase: the hall of Egypt quotes it
# A2's last bar walks up to the loop's E instead of resting on A.
BL_TUNE_A2 = phrase(BL_TUNE, 1, 15) + ' | A4:2 C#5:1 D5:1'
BL_ANSWER = ('D5:2 F5:1 E5:1 | D5:1 C#5:1 D5:2 | F5:2 A5:1 G#5:1 | A5:4 | '
             'Bb5:2 A5:1 G#5:1 | A5:1 F5:1 D5:2 | E5:1 F5:1 E5:1 D5:1 | C#5:4 | '
             'D5:2 F5:1 A5:1 | G#5:1 F5:1 E5:2 | F5:1 D5:1 Bb4:2 | C#5:4 | '
             'D5:1 E5:1 F5:1 G#5:1 | A5:2 F5:2 | E5:1 D5:1 C#5:1 Bb4:1 | A4:4')
# The aulos's half of the heterophony: the same tune with its ornaments smoothed.
BL_PLAIN = ('E5:2 C#5:2 | D5:2 C#5:2 | A4:2 E5:2 | A5:4 | F5:2 E5:2 | D5:2 F5:2 | C#5:2 Bb4:2 | A4:4 | '
            'E5:2 C#5:2 | D5:2 C#5:2 | A4:2 G#5:2 | A5:4 | Bb5:2 G#5:2 | E5:4 | D5:2 Bb4:2 | A4:4')
BL_OUD = arp([('r', 1.5), ('f', 1.5), ('r', 1)], 50)
BL_DROPS = arp([('R', 2), ('F', 2)], 50)
BL_MALFUF = 'dum:1.5 tek:1.5_ tek:1'
BL_FILL = 'dum:1 tek:0.5 tek:0.5 tek:0.5 tek:0.5 low:1'
BL_SISTRUM = 'D6:1 D6:0.5_ D6:0.5_ D6:1 D6:0.5_ D6:0.5_'  # noise: any in-mode key
BLACK_LAND = Song(
    name='mus_ichor_black_land', title='The Black Land', meter=(2, 4), grouping=(3, 3, 2), tempo=96,
    voicegroup=VG, volume=127, reverb=50, priority=0,
    sections=[('intro', 2), ('A', 16), ('B', 16), ('A2', 16)], loop_from='A',
    modes={'*': A_HJK}, target=(55, 65), chords=BL_CH, ref=('MUS_ROUTE111', -22.0), tracks=[
        Track('harp', 46, 116, pan=-10, velocity=104, lo='D4', hi='C#6', parts={
            'intro': 'A4:0.5 C#5:0.5 E5:0.5 G#5:0.5 A5:2 | r:4', 'A': BL_TUNE, 'B': gen(BL_CH['B'], BL_DROPS),
            'A2': BL_TUNE_A2}),
        Track('aulos', 68, 100, pan=14, velocity=100, lo='A4', hi='Bb5', vibrato=(4, 44, 14), parts={
            'B': BL_ANSWER, 'A2': BL_PLAIN}),
        Track('kithara', 24, 86, pan=24, velocity=88, gate=0.7, lo='D3', hi='F4', parts={
            'intro': gen(BL_CH['intro'], BL_OUD), **{s: gen(BL_CH[s], BL_OUD) for s in ('A', 'B', 'A2')}}),
        Track('strings', 48, 54, pan=-24, velocity=76, lo='D4', hi='Bb4',
              parts={'B': gen(BL_CH['B'], lambda c: notes([(triad(c, 62)[0], 4)]))}),
        Track('bass', 92, 49, velocity=100, gate=0.9, lo='C2', hi='C3',
              parts={s: gen(c, root_fifth([('r', 2), (None, 2)], 38)) for s, c in BL_CH.items()}),
        Track('drums', 0, 90, velocity=96, kit=FRAME_KIT, parts={
            'intro': BL_MALFUF + ' | ' + BL_FILL,
            'A': bars(BL_MALFUF + ' | ' + BL_MALFUF, 8, BL_MALFUF + ' | ' + BL_FILL),
            'B': bars('dum:1 tek:1_ dum:1 tek:1_ | dum:1 tek:1_ dum:1 tek:1_', 8, 'dum:1 tek:1_ dum:1 tek:1_ | ' + BL_FILL),
            'A2': bars('dum+tam:1.5 tek:1.5_ tek:1 | ' + BL_MALFUF, 8, 'dum+tam:1.5 tek:1.5_ tek:1 | ' + BL_FILL)}),
        Track('sistrum', 127, 31, velocity=80, gate=0.25, lo='D6', hi='D6', parts={
            'A': bars(BL_SISTRUM, 16), 'B': bars('D6:1 r:1 D6:1 r:1', 16), 'A2': bars(BL_SISTRUM, 16)}),
    ])

# ============================================================ The Necropolis
# Egypt by night (each outdoor Egyptian map names it as its night_music, so houses
# keep the day tune): the tombs at Saqqara, the embalmers' lamps, the City of the
# Dead across the river.
# The same mode, slowed to a funeral pace, 4/4 at 64, and handed to the low reeds: an
# arghul, Egypt's double clarinet, whose melody pipe (the aulos at the bottom of its
# range) plays the Black Land's first phrase at half speed an octave down, while its
# drone pipe (the accordion, a free reed) holds A under it all night.
# A: the reed alone over the drone, the heartbeat drum and a harp's single drops.
# B: Isis's lament for Osiris, a woman's voice (the hum) high above the reed's
# held line. One soft sistrum shake every other bar: the rattle that woke the dead.
NC_CH = {
    'intro': ['A'],
    'A': ['A', 'Bb', 'A', 'A', 'Dm', 'Dm', 'Bb', 'A'],
    'B': ['Dm', 'Dm', 'Bb', 'A', 'Dm', 'Bb', 'A', 'A'],
}
NC_REED = octave(augment(BL_HEAD, 4), -1)
NC_LAMENT = ('r:2 A5:4 G#5:1 F5:1 | E5:4 F5:2 E5:2 | D5:4 C#5:2 D5:2 | E5:8 | '
             'r:2 F5:2 A5:2 G#5:1 A5:1 | Bb5:4 A5:2 F5:2 | E5:3 F5:1 E5:2 C#5:2 | A4:8')
NC_HELD = 'D4:8 | C#4:8 | D4:8 | C#4:4 E4:4 | D4:8 | D4:8 | C#4:8 | A3:8'
NC_DROPS = 'r:4 A3:2_ r:2 | r:8 | r:2 E4:2_ r:4 | r:8 | r:4 D4:2_ r:2 | r:8 | r:2 C#4:2_ r:4 | r:8'
NC_HEART = 'dum:3_ low:1_ r:4'
NECROPOLIS = Song(
    name='mus_ichor_necropolis', title='The Necropolis', meter=(4, 4), grouping=(4, 4), tempo=64,
    voicegroup=VG, volume=127, reverb=50, priority=0, sections=[('intro', 1), ('A', 8), ('B', 8)],
    loop_from='A', modes={'*': A_HJK}, target=(55, 65), chords=NC_CH, ref=('MUS_MT_PYRE', -24.5), tracks=[
        Track('reed', 68, 120, pan=-6, velocity=112, lo='A3', hi='A4', vibrato=(4, 30, 22), parts={
            'A': NC_REED, 'B': NC_HELD}),
        Track('drone', 21, 70, pan=10, velocity=90, lo='A2', hi='A2',
              parts={'intro': 'A2:8', 'A': bars('A2:8', 8), 'B': bars('A2:8', 8)}),
        Track('lament', 53, 100, pan=-16, velocity=96, lo='A4', hi='Bb5', vibrato=(3, 30, 24), parts={'B': NC_LAMENT}),
        Track('harp', 46, 76, pan=22, velocity=84, lo='A3', hi='E4', parts={'A': NC_DROPS, 'B': NC_DROPS}),
        Track('frame drum', 0, 78, velocity=90, kit=FRAME_KIT, parts={
            'intro': NC_HEART, 'A': bars(NC_HEART, 8), 'B': bars(NC_HEART, 8)}),
        Track('sistrum', 127, 24, velocity=70, gate=0.25, lo='D6', hi='D6', parts={
            'A': bars('D6:1_ r:7 | r:8', 4), 'B': bars('D6:1_ r:7 | r:8', 4)}),
    ])

# ============================================================ The Black Sea
# The Pontos, "the sea without hospitality": the Bosporus, Salmydessos, the Pontic
# coast and Aia. G Phrygian (G Greek Dorian), 9/8 as three slow beats, 3+3+3, a stroke
# a bar: the drum pulls on the first beat and the oars come back over the other two,
# as the Argo's fifty rowed. At 108 a stroke is 2.5 seconds, a cruising rate.
# The low strings carry it. Their tune opens D-G-Ab-G: the Thread's 5-1-2 bent by the
# Phrygian semitone (the Thread is home's; out here its second step is a half-step,
# Ab, that won't sit still), and its phrases close Ab to G, the Phrygian cadence.
# A: low strings over a wave-channel bass that rows root, low fifth, root. A2: a horn
# above, and Orpheus's lyre setting the stroke, as he did for the Argonauts. B: the
# Clashing Rocks: the strings an octave up and faster, the rowers' hummed chant, and
# timpani rolling at every fourth stroke. The sea wind blows through it all.
G_PHR = pcs('G', PHRYGIAN)
BS_CH = {
    'intro': ['Gm', 'Gm'],
    'A': ['Gm', 'Fm', 'Eb', 'Gm', 'Gm', 'Cm', 'Ab', 'Gm'],
    'B': ['Cm', 'Bb', 'Ab', 'Gm', 'Cm', 'Bb', 'Ab', 'Gm'],
}
BS_CH['A2'] = BS_CH['A']
BS_TUNE = ('D3:3 G3:3 Ab3:2 G3:1 | F3:3 Eb3:3 C3:3 | Eb3:3 G3:3 Bb3:2 Ab3:1 | G3:6 D3:3 | '
           'D3:3 G3:3 Bb3:2 Ab3:1 | C4:3 Bb3:3 G3:3 | Ab3:3 G3:3 F3:2 Eb3:1 | G3:9')
BS_ROCKS = ('G4:3 C5:3 D5:2 Eb5:1 | D5:3 Bb4:3 F4:3 | Eb5:3 C5:3 Ab4:2 C5:1 | Bb4:3 G4:3 D4:3 | '
            'G4:3 C5:3 D5:2 Eb5:1 | F5:3 D5:3 Bb4:3 | C5:3 Bb4:3 Ab4:3 | G4:6 D4:3')
BS_HORN = 'Bb3:9 | C4:9 | Bb3:9 | D4:9 | Bb3:9 | Eb4:9 | C4:9 | D4:6 Bb3:3'
BS_CHANT = 'C4:9 | D4:9 | Eb4:9 | D4:9 | C4:9 | D4:9 | Eb4:6 C4:3 | D4:9'
BS_ORPHEUS = arp([('R', 3), (None, 3), ('F', 3)], 43)


def bs_row(c):
    """The bass rows: root, the low fifth, root."""
    r = triad(c, 36)[0]
    return notes([(r, 3), (low_fifth()(c), 3), (r, 3)])


BS_STROKE = 'deep:3^ tek:3_ low:3_'  # the pull, then the oars come back over two beats
BS_FILL = 'deep:3 tek:1 tek:1 tek:1 low:1 low:1 low:1'
BS_WIND = bars('G3:9- | G3:6 r:3', 4)
BLACK_SEA = Song(
    name='mus_ichor_black_sea', title='The Black Sea', meter=(9, 8), grouping=(3, 3, 3), tempo=108,
    voicegroup=VG, volume=100, reverb=50, priority=0,
    sections=[('intro', 2), ('A', 8), ('A2', 8), ('B', 8)], loop_from='A',
    modes={'*': G_PHR}, target=(55, 65), chords=BS_CH, ref=('MUS_SURF', -22.0), tracks=[
        Track('strings', 48, 112, pan=-8, velocity=104, lo='C3', hi='F5', parts={
            'intro': 'r:9 | D3:6 r:3', 'A': BS_TUNE, 'A2': BS_TUNE, 'B': BS_ROCKS}),
        Track('horn', 60, 80, pan=20, velocity=90, gate=0.95, lo='Bb3', hi='Eb4', parts={'A2': BS_HORN}),
        Track('chorus', 52, 82, pan=-18, velocity=92, lo='C4', hi='Eb4', parts={'B': BS_CHANT}),
        Track('lyre', 46, 84, pan=26, velocity=88, lo='G3', hi='Eb5', parts={'A2': gen(BS_CH['A2'], BS_ORPHEUS)}),
        Track('bass', 87, 72, velocity=104, gate=0.85, lo='C2', hi='B2',
              parts={s: gen(c, bs_row) for s, c in BS_CH.items()}),
        Track('timpani', 47, 86, pan=10, velocity=96, gate=0.6, lo='D3', hi='D3', parts={
            'B': bars('D3:3 r:6 | r:9 | r:9 | ' + ' '.join(['D3:0.5'] * 18), 2)}),
        Track('drums', 0, 92, velocity=100, kit=FRAME_KIT, parts={
            'intro': 'deep:3 r:6 | ' + BS_FILL,
            'A': bars(BS_STROKE, 8, BS_FILL), 'A2': bars(BS_STROKE, 8, BS_FILL),
            'B': 'deep+cym:3^ tek:1 tek:1 tek:1 dum:3 | ' + bars('deep:3^ tek:1 tek:1 tek:1 dum:3', 7, BS_FILL)}),
        Track('wind', 122, 56, velocity=70, lo='G3', hi='G3', parts={
            'intro': 'G3:9- | G3:9', 'A': BS_WIND, 'A2': BS_WIND, 'B': BS_WIND}),
    ])

# ============================================================ Battle! Oikoumene Trainer
# Every trainer in the Oikoumene (the chart agent's region branch in src/pokemon.c).
# The Aethos battle is A Dorian, 7/8 kalamatianos at 180; this one is the same dance
# at 200 and in B Aeolian (B Greek Hypodorian), so it is plainly a step up.
# A: the aulos's tune turns on its upper neighbour (F#-G-F#) in the long beat, then
# falls through the two short ones. A2: a square an octave down, the strings' ostinato.
# B: the salpinx plays The Wider World's head in 7/8, A-D-E-F#, the Thread in major,
# and the mode turns to D Mixolydian (C natural) under it: the world you sailed to.
# C: the syrinx runs over the horn a sixth below. A3: the double aulos, a second pipe
# (accordion) a third under. F#m closes every section, the minor dominant, into Bm.
B_AEO = pcs('B', AEOLIAN)
OK_CH = {
    'intro': ['Bm', 'Bm'],
    'A': ['Bm', 'A', 'G', 'F#m', 'Bm', 'A', 'Em', 'F#m'],
    'B': ['D', 'Bm', 'C', 'Am', 'D', 'D', 'C', 'D'],
    'C': ['G', 'D', 'Em', 'Bm', 'G', 'D', 'Em', 'F#m'],
}
OK_CH['A2'] = OK_CH['A3'] = OK_CH['A']
OK_TUNE = ('F#5:1 G5:1 F#5:1 D5:2 B4:2 | E5:1 F#5:1 E5:1 C#5:2 A4:2 | D5:1 E5:1 D5:1 B4:2 G5:2 | F#5:3 C#5:2 A4:2 | '
           'B5:1 C#6:1 B5:1 F#5:2 D5:2 | E5:1 F#5:1 G5:1 A5:2 E5:2 | G5:1 F#5:1 E5:1 D5:2 C#5:2 | F#5:3 r:4')
OK_WORLD = ('A4:3 D5:2 E5:2 | F#5:3 D5:2 B4:2 | C5:3 A4:2 G4:2 | A4:7 | '
            'A4:3 D5:2 E5:2 | F#5:2 G5:1 A5:4 | G5:3 E5:2 C5:2 | D5:3 F#5:2 A5:2')
OK_RUN = ('B5:1 A5:1 G5:1 D5:2 B4:2 | A5:1 G5:1 F#5:1 D5:2 A4:2 | G5:1 F#5:1 E5:1 B4:2 E5:2 | F#5:3 D5:2 B4:2 | '
          'D6:1 C#6:1 B5:1 G5:2 D5:2 | F#5:1 G5:1 A5:1 F#5:2 D5:2 | E5:1 F#5:1 G5:1 B5:2 G5:2 | A5:3 F#5:2 C#5:2')
OK_BASS = root_fifth([('r', 1), ('r', 1), ('o', 1), ('f', 2), ('o', 2)], 38)


def ok_strings(scale):
    """The strings' ostinato: a turn on the root, 3+2+2."""
    def fn(c):
        r = triad(c, 62)[0]
        up = r + next(i for i in (1, 2) if (r + i) % 12 in scale)
        down = r - next(i for i in (1, 2) if (r - i) % 12 in scale)
        return notes([(r, 1), (up, 1), (r, 1), (down, 1), (r, 1), (up, 1), (r, 1)])
    return fn


OK_BAR = 'deep:2 tek:1 snare:2 dum:1 tek:1'
OK_FILL = 'deep:2 snare:1 snare:1 snare:1 snare:1 snare:1^'
OK_SHAKER = bars('D6:1 D6:1_ D6:1_ D6:1 D6:1_ D6:1 D6:1_', 8)  # D: in both modes
BATTLE_OIKOUMENE = Song(
    name='mus_ichor_battle_oikoumene', title='Battle! Oikoumene Trainer', meter=(7, 8), grouping=(3, 2, 2),
    tempo=200, voicegroup=VG, volume=120, reverb=50, priority=1,
    sections=[('intro', 2), ('A', 8), ('A2', 8), ('B', 8), ('C', 8), ('A3', 8)], loop_from='A',
    modes={'*': B_AEO, 'B': D_MIX}, target=(38, 46), chords=OK_CH, ref=('MUS_VS_TRAINER', -21.0), tracks=[
        Track('aulos', 68, 108, pan=-6, velocity=104, lo='A4', hi='C#6', vibrato=(4, 50, 16), parts={
            'A': OK_TUNE, 'A2': OK_TUNE, 'A3': OK_TUNE}),
        Track('aulos 2', 21, 76, pan=18, velocity=96, lo='F#4', hi='A5', parts={'A3': diatonic(OK_TUNE, B_AEO, -2)}),
        Track('salpinx', 56, 102, pan=-14, velocity=104, gate=0.9, lo='G4', hi='A5', parts={'B': OK_WORLD}),
        Track('syrinx', 73, 96, pan=-20, velocity=100, lo='A4', hi='D6', vibrato=(3, 44, 12), parts={'C': OK_RUN}),
        Track('horn', 60, 82, pan=22, velocity=96, gate=0.85, lo='C4', hi='F#5', parts={
            'C': diatonic(OK_RUN, B_AEO, -5),
            'B': gen(OK_CH['B'], lambda c: notes([(triad(c, 55)[1], 3), (None, 4)]))}),
        Track('strings', 48, 72, pan=28, velocity=90, gate=0.8, lo='C4', hi='F#5', parts={
            'intro': 'B4:1 C#5:1 D5:1 E5:1 F#5:1 D5:1 C#5:1 | B4:3 F#4:2 B4:2',
            'A2': gen(OK_CH['A2'], ok_strings(B_AEO)), 'B': gen(OK_CH['B'], ok_strings(D_MIX)),
            'A3': gen(OK_CH['A3'], ok_strings(B_AEO))}),
        Track('kithara', 24, 80, pan=24, velocity=90, gate=0.5, lo='G3', hi='C#5',
              parts={s: gen(OK_CH[s], offbeats([(0, 3), (1, 2), (1, 2)])) for s in ('intro', 'A', 'B', 'C')}),
        Track('bass', 87, 84, velocity=106, gate=0.7, lo='D2', hi='D4',
              parts={s: gen(c, OK_BASS) for s, c in OK_CH.items()}),
        Track('drums', 0, 96, velocity=100, kit=FRAME_KIT, parts={
            'intro': 'deep:3^ r:2 snare:1 snare:1 | taiko:1 taiko:1 taiko:1 snare:1 snare:1 snare:1 snare:1^',
            'A': 'deep+crash:2 tek:1 snare:2 dum:1 tek:1 | ' + bars(OK_BAR, 7, OK_FILL),
            'A2': 'deep+crash:2 tam:1 snare:2 dum:1 tam:1 | ' + bars('deep:2 tam:1 snare:2 dum:1 tam:1', 7, OK_FILL),
            'B': 'taiko+crash:3 dum:2 snare:1 tek:1 | ' + bars('taiko:3 dum:2 snare:1 tek:1', 7, OK_FILL),
            'C': 'deep+crash:3 snare:2 deep:1 snare:1 | ' + bars('deep:3 snare:2 deep:1 snare:1', 7,
                                                                       'snare:1 snare:1 snare:1 snare:1 snare:1 snare:1^ snare:1^'),
            'A3': 'deep+crash:2 tam:1 snare:2 dum:1 tam:1 | ' + bars('deep:2 tam:1 snare:2 dum:1 tam:1', 7, OK_FILL)}),
        Track('shaker', 127, 38, velocity=80, gate=0.25, lo='D6', hi='D6',
              parts={'A2': OK_SHAKER, 'B': OK_SHAKER, 'A3': OK_SHAKER}),
    ])

# ============================================================ The Periodos (the ten halls)
# PERIODOS.md §6: one hall theme in ten short arrangements. A is home, the same in
# every hall: the Thread (MUSIC.md motif 1, A-D-E-F, 5-1-2-3) in D Dorian as a
# processional for aulos, kithara and frame drum, at a stately two-in-a-bar (120).
# B is the land: the land's own mode and meter, quoting the first phrase of its land
# track on its land track's instrument, over its drum and its colour. The form is
# intro 1, then a loop of A 8 and B 8, about 30 seconds.
# B's last bar leads home: Troy's march stops on D, and here D is home; the Black Land
# stops on A, the Thread's first note; the Black Sea on G, a step under it.
#
# Every hall is one call to periodos(). The seven still to come (Lydia, Scythia and
# Hyperborea, Aithiopia, Libya, the Far West, the Western Sea, Okeanos) need only
# their land track's opening phrase and the land's voices, for example:
#   PERIODOS_LYDIA = periodos('lydia', 'The Periodos: Sardis', mode=pcs('F', LYDIAN),
#       meter=(4, 4), grouping=(2, 2, 2, 2), chords=[...8...], quote=GOLD_OF_SARDIS_HEAD, turn='r:7 G4:1',
#       lead=Voice('harp', 46, 112, 104, 'C4', 'C6'), colour=Voice('kymbala', 127, 36, 80, 'C6', 'C6', part=...),
#       drum=..., kithara=..., bass=..., song_id='MUS_ICHOR_PERIODOS_LYDIA')
# and a songs.h constant, a song_table.inc line and a midi.cfg line.
D_DOR = pcs('D', DORIAN)
PD_TEMPO = 120
PD_CH = ['Dm', 'C', 'Dm', 'G', 'F', 'C', 'G', 'Dm']
PD_THREAD = ('A4:2 D5:1 E5:1 F5:4 | E5:3 D5:1 C5:2 A4:2 | A4:2 D5:1 E5:1 F5:2 A5:2 | G5:4 B4:4 | '
             'C5:2 F5:1 G5:1 A5:4 | G5:3 F5:1 E5:2 C5:2 | D5:2 B4:1 C5:1 D5:2 E5:2 | D5:6 r:2')
PD_KITHARA = offbeats([(1, 2), (1, 2), (1, 2), (1, 2)], 55)
PD_BASS = root_fifth([('r', 4), ('f', 4)], 36)
PD_STEP = 'dum:2 tek:2_ dum:2 tek:1_ tek:1_'
PD_FILL = 'dum:2 tek:1 tek:1 dum:1 tek:1 tek:1 tek:1'

# One voice of a hall's B: its program, levels and range, and its part (8 bars).
Voice = namedtuple('Voice', 'name program volume velocity lo hi pan gate vibrato part',
                   defaults=(0, 1.0, None, None))


def periodos(land, title, *, mode, meter, grouping, chords, quote, turn, lead, drum, kithara=None, bass=None,
             second=None, colour=None, song_id=None, volume=127):
    """The Periodos in one land's hall. `quote` is the first phrase of the land track,
    8 bars in `meter`, played by `lead` (a Voice without a part); `turn` is the home
    aulos's way back, B's last bar in the land's meter and mode, rising to the Thread's
    first note, A. `second` and `colour` are optional Voices with their own 8-bar parts
    (colour on the noise channel). `drum` is B's 8 bars on FRAME_KIT, and `kithara` and
    `bass` map a chord to a bar. The PSG tracks' volumes are set for -V127 (README)."""
    rest = f'r:{meter[0] * 8 // meter[1]}'
    tracks = [
        Track('aulos', 68, 108, pan=-6, velocity=104, lo='F4', hi='A5', vibrato=(4, 40, 14),
              parts={'intro': 'r:6 A4:1 C5:1', 'A': PD_THREAD, 'B': ' | '.join([rest] * 7 + [turn])}),
        Track(lead.name, lead.program, lead.volume, pan=lead.pan, velocity=lead.velocity, gate=lead.gate,
              lo=lead.lo, hi=lead.hi, vibrato=lead.vibrato, parts={'B': quote}),
    ]
    for v in (second, colour):
        if v:
            tracks.append(Track(v.name, v.program, v.volume, pan=v.pan, velocity=v.velocity, gate=v.gate,
                                lo=v.lo, hi=v.hi, vibrato=v.vibrato, parts={'B': v.part}))
    kparts = {'intro': PD_KITHARA('Dm'), 'A': gen(PD_CH, PD_KITHARA)}
    if kithara:
        kparts['B'] = gen(chords, kithara)
    tracks += [
        Track('kithara', 24, 84, pan=24, velocity=88, gate=0.6, lo='D3', hi='C5', parts=kparts),
        Track('bass', 92, 49, velocity=100, gate=0.9, lo='C2', hi='B3', parts={
            'intro': 'D2:8', 'A': gen(PD_CH, PD_BASS), **({'B': gen(chords, bass)} if bass else {})}),
        Track('drums', 0, 92, velocity=96, kit=FRAME_KIT, parts={
            'intro': 'dum:2 r:2 tek:1 tek:1 tek:1 tek:1', 'A': 'dum+cym:2 tek:2_ dum:2 tek:1_ tek:1_ | '
            + bars(PD_STEP, 7, PD_FILL), 'B': drum}),
    ]
    return MeterSong(
        name=f'mus_ichor_periodos_{land}', title=title, meter=(4, 4), grouping=(2, 2, 2, 2), tempo=PD_TEMPO,
        voicegroup=VG, volume=volume, reverb=50, priority=0, sections=[('intro', 1), ('A', 8), ('B', 8)],
        loop_from='A', modes={'*': D_DOR, 'B': mode}, target=(20, 40),
        chords={'intro': ['Dm'], 'A': PD_CH, 'B': chords}, ref=('MUS_GYM', -21.9),
        meters={'B': meter}, song_id=song_id, tracks=tracks)


# The Troad's hall (the Skaian Gate): Troy's march on the double aulos, the second pipe
# droning E; the wind of windy Ilion. Its last bar, D major, turns minor into home.
PERIODOS_TROAD = periodos(
    'troad', 'The Periodos: Troad', mode=E_DOR, meter=(4, 4), grouping=(3, 1, 2, 2), chords=PT_CH['A'],
    quote=PT_TUNE, turn='r:6 F#4:1 G4:1', lead=Voice('troy aulos', 68, 104, 104, 'B4', 'C#6', pan=10, vibrato=(4, 36, 16)),
    second=Voice('drone pipe', 21, 64, 90, 'E4', 'E4', pan=16, part=bars('E4:8', 8)),
    colour=Voice('wind', 122, 39, 70, 'A3', 'A3', part=PT_WIND),
    drum=bars(PT_STEP, 8, PT_FILL), kithara=PT_KITHARA, bass=lambda c: 'E2:3 E2:1 E2:4')

# Egypt's hall (Proteus's precinct): the Black Land's first phrase on the harp, the
# sistrum, the malfuf. It ends on A, and the Thread starts on A; the turn is G#, the
# foreign mode's leading tone, resolving into home.
PERIODOS_EGYPT = periodos(
    'egypt', 'The Periodos: Egypt', mode=A_HJK, meter=(2, 4), grouping=(3, 3, 2), chords=BL_CH['A'][:8],
    quote=BL_HEAD, turn='r:3 G#4:1', lead=Voice('harp', 46, 116, 104, 'A4', 'A5', pan=-10),
    colour=Voice('sistrum', 127, 31, 80, 'D6', 'D6', gate=0.25, part=bars(BL_SISTRUM, 8)),
    drum=bars(BL_MALFUF, 8, BL_FILL), kithara=BL_OUD, bass=root_fifth([('r', 2), (None, 2)], 38))

# The Black Sea's hall (Aietes's palace): the Black Sea's low strings in 9/8, rowing.
# The turn climbs F-G out of the Phrygian, and home's A arrives as a step it lacked.
PERIODOS_PONTOS = periodos(
    'pontos', 'The Periodos: Black Sea', mode=G_PHR, meter=(9, 8), grouping=(3, 3, 3), chords=BS_CH['A'],
    quote=BS_TUNE, turn='r:7 F4:1 G4:1', lead=Voice('strings', 48, 112, 104, 'C3', 'C4', pan=-8),
    colour=Voice('wind', 122, 44, 70, 'G3', 'G3', part=BS_WIND),
    drum=bars(BS_STROKE, 8, BS_FILL), bass=bs_row)

# ============================================================ Battle! Champion of the Periodos
# The ten champions, and Helen. 9/8 zeibekiko, 2+2+2+3: the solo dance a man does for
# himself, heavy on its long last beat. D Dorian, home's own mode, because the halls
# play home first and this is the battle for your thread: B is the Periodos's
# processional itself, the Thread, stretched from four beats to the zeibekiko's nine
# and sung by the chorus over the aulos. The Aethos rival battle (Kleon's) is 9/8 too,
# E Phrygian at 180; this one is slower and heavier, 150, with the strings running
# sixteenths under it so the weight never stands still.
# A: the salpinx alone over the strings, the champion's call. A2: horns join in thirds. B: the
# Thread. C: the climb, strings and horns over timpani, to the A that opens the loop.
CP_CH = {
    'intro': ['Dm', 'Dm'],
    'A': ['Dm', 'C', 'Dm', 'Am', 'Dm', 'C', 'G', 'Am'],
    'B': PD_CH,
    'C': ['F', 'G', 'Am', 'Am', 'F', 'G', 'Em', 'Am'],
}
CP_CH['A2'] = CP_CH['A']
CP_THEME = ('A4:2 D5:2 F5:2 E5:3 | G5:2 F5:2 E5:2 C5:3 | A4:2 D5:2 F5:2 A5:3 | G5:2 E5:2 C5:2 A4:3 | '
            'D5:2 F5:2 A5:2 G5:1 F5:1 E5:1 | F5:2 E5:2 C5:2 G5:3 | B4:2 D5:2 G5:2 F5:1 E5:1 D5:1 | E5:6 r:3')


def stretch(part, extra=1):
    """Each bar's last note held `extra` eighths longer: a 4/4 bar into 9/8."""
    out = []
    for b in part.split(' | '):
        toks = b.split()
        head, _, dur = toks[-1].partition(':')
        toks[-1] = f'{head}:{float(dur) + extra:g}'
        out.append(' '.join(toks))
    return ' | '.join(out)


CP_THREAD = stretch(PD_THREAD)
CP_CLIMB = ('F4:2 A4:2 C5:2 F5:3 | G4:2 B4:2 D5:2 G5:3 | A4:2 C5:2 E5:2 A5:3 | G5:2 E5:2 C5:2 A4:3 | '
            'F4:2 A4:2 C5:2 F5:3 | G4:2 B4:2 D5:2 G5:3 | E5:2 G5:2 B5:2 G5:3 | A5:6 E5:3')
# Sixteenths in the zeibekiko's groups: four in each short beat, six in the long one.
CP_RUN = arp([('r', 0.5), ('t', 0.5), ('f', 0.5), ('t', 0.5)] * 3 + [('r', 0.5), ('t', 0.5), ('f', 0.5),
                                                                       ('R', 0.5), ('f', 0.5), ('t', 0.5)], 62)
CP_BAR = 'deep:2^ tek:2 snare:2 deep:1 tek:1 r:1'
CP_FILL = 'deep:2 snare:1 snare:1 deep:1 snare:1 snare:1 snare:1 snare:1^'
BATTLE_PERIODOS = Song(
    name='mus_ichor_battle_periodos', title='Battle! Champion of the Periodos', meter=(9, 8), grouping=(2, 2, 2, 3),
    tempo=150, voicegroup=VG, volume=120, reverb=50, priority=1,
    sections=[('intro', 2), ('A', 8), ('A2', 8), ('B', 8), ('C', 8)], loop_from='A',
    modes={'*': D_DOR}, target=(50, 62), chords=CP_CH, ref=('MUS_VS_ELITE_FOUR', -21.0), tracks=[
        Track('salpinx', 56, 106, pan=-8, velocity=106, gate=0.92, lo='A4', hi='A5', parts={
            'intro': 'A4:2 D5:2 F5:2 A5:3 | r:9', 'A': CP_THEME, 'A2': CP_THEME}),
        Track('horn', 60, 86, pan=18, velocity=98, gate=0.9, lo='C4', hi='G5', parts={
            'A2': diatonic(CP_THEME, D_DOR, -2), 'C': diatonic(CP_CLIMB, D_DOR, -2)}),
        Track('aulos', 68, 100, pan=10, velocity=100, lo='A4', hi='A5', vibrato=(4, 40, 14), parts={'B': CP_THREAD}),
        Track('chorus', 52, 84, pan=-16, velocity=96, lo='F4', hi='F5', parts={'B': diatonic(CP_THREAD, D_DOR, -2)}),
        Track('strings', 48, 72, pan=26, velocity=88, gate=0.8, lo='D4', hi='D6', parts={
            'intro': 'D5:0.5 E5:0.5 F5:0.5 G5:0.5 A5:0.5 G5:0.5 F5:0.5 E5:0.5 D5:0.5 E5:0.5 F5:0.5 '
                     'G5:0.5 A5:0.5 B5:0.5 C6:0.5 D6:0.5 A5:1 | r:9',
            **{s: gen(CP_CH[s], CP_RUN) for s in ('A', 'A2', 'B')}, 'C': CP_CLIMB}),
        Track('bass', 87, 84, velocity=106, gate=0.75, lo='C2', hi='C4',
              parts={**{s: gen(CP_CH[s], root_fifth([('r', 2), ('o', 2), ('f', 2), ('r', 2), (None, 1)], 38))
                        for s in ('A', 'A2', 'B')},
                     'C': gen(CP_CH['C'], root_fifth([('r', 2), ('r', 2), ('r', 2), ('r', 2), (None, 1)], 38))}),
        Track('timpani', 47, 90, pan=6, velocity=100, gate=0.6, lo='E2', hi='D3', parts={
            'intro': 'D3:2 r:4 A2:3 | ' + ' '.join(['D3:0.5'] * 18),
            'C': gen(CP_CH['C'], lambda c: notes([(timp_fifth()(c), 2), (None, 4), (timp_fifth()(c), 3)]))}),
        Track('drums', 0, 98, velocity=100, kit=FRAME_KIT, parts={
            'intro': 'deep+crash:2 r:4 taiko:3 | taiko:1 taiko:1 taiko:1 taiko:1 snare:1 snare:1 snare:1 snare:1 snare:1^',
            'A': 'deep+crash:2^ tek:2 snare:2 deep:1 tek:1 r:1 | ' + bars(CP_BAR, 7, CP_FILL),
            'A2': 'deep+crash:2^ tam:2 snare:2 deep:1 tam:1 r:1 | ' + bars('deep:2^ tam:2 snare:2 deep:1 tam:1 r:1', 7, CP_FILL),
            'B': 'taiko+crash:2^ dum:2 taiko:2 dum:1 tek:1 r:1 | ' + bars('taiko:2^ dum:2 taiko:2 dum:1 tek:1 r:1', 7, CP_FILL),
            'C': 'deep+crash:2^ taiko:2 deep:2 taiko:1 taiko:1 r:1 | ' + bars('deep:2^ taiko:2 deep:2 taiko:1 taiko:1 r:1', 7,
                                                                               'snare:1 snare:1 snare:1 snare:1 snare:1 snare:1 snare:1^ snare:1^ snare:1^')}),
    ])

OIKOUMENE_SONGS = [WIDER_WORLD, PLAIN_OF_TROY, BLACK_LAND, NECROPOLIS, BLACK_SEA, BATTLE_OIKOUMENE,
                   BATTLE_PERIODOS, PERIODOS_TROAD, PERIODOS_EGYPT, PERIODOS_PONTOS]
