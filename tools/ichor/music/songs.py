"""Song data for Pokemon Ichor. All of them are original compositions.

Notation (one string per track per section; bars split by '|'):
  D5          pitch, scientific octaves (C4 = middle C = MIDI 60); F#4, Bb3 for accidentals
  :n          duration in eighth notes, sticky until changed (:3 dotted quarter, :0.5 sixteenth)
  r           rest
  D4+F4       notes struck together
  ^ _ . -     suffixes: accent, soft, staccato, tie into the next (same) note
  dum tek     drum names, mapped per track through `kit`
Every bar must add up to the meter. Accompaniment is generated from each section's
chord list by the small helpers below, so revising harmony means editing one list.
"""
import re
from compose import Song, Track, pitch, pname

QUALITY = {'': (0, 4, 7), 'm': (0, 3, 7), 'dim': (0, 3, 6)}


def triad(name, lo):
    """Chord tones of e.g. 'Dm' with the root in [lo, lo + 11]."""
    m = re.match(r'^([A-G][#b]?)(m|dim|)$', name)
    root = pitch(m.group(1) + '4') % 12
    base = lo + (root - lo) % 12
    return [base + i for i in QUALITY[m.group(2)]]


def step(n, scale, k):
    """The pitch k scale degrees from n (n itself need not be in the scale)."""
    for _ in range(abs(k)):
        n += 1 if k > 0 else -1
        while n % 12 not in scale:
            n += 1 if k > 0 else -1
    return n


def bar_chords(spec):
    return spec.split()


def notes(seq):
    """[(midi or None, eighths)] -> notation string for one bar."""
    return ' '.join(('r' if k is None else '+'.join(pname(x) for x in (k if isinstance(k, list) else [k])))
                    + f':{d:g}' for k, d in seq)


def gen(chords, fn):
    return ' | '.join(fn(c) for c in chords)


def diatonic(part, scale, steps):
    """Shift every pitch in a part by `steps` scale degrees (e.g. -2 = a third below)."""
    pcs = sorted(scale)

    def move(tok):
        def one(p):
            n = pitch(p)
            for _ in range(abs(steps)):
                n += -1 if steps < 0 else 1
                while n % 12 not in pcs:
                    n += -1 if steps < 0 else 1
            return pname(n)
        m = re.match(r'^([A-G][#b]?\d(?:\+[A-G][#b]?\d)*)(.*)$', tok)
        if not m:
            return tok
        return '+'.join(one(p) for p in m.group(1).split('+')) + m.group(2)
    return ' '.join(move(t) for t in part.split())


def octave(part, n):
    return re.sub(r'([A-G][#b]?)(\d)', lambda m: m.group(1) + str(int(m.group(2)) + n), part)


def pcs(tonic, intervals):
    t = pitch(tonic + '4') % 12
    return {(t + i) % 12 for i in intervals}


# These constants use the church-mode names. The Greek octave species, as Cleonides
# lays them out on the white notes, carry different names for the same scales:
#   Mixolydian   B-B = church Locrian       Hypolydian   F-F = church Lydian
#   Lydian       C-C = Ionian              Hypophrygian G-G = church Mixolydian
#   Phrygian     D-D = church Dorian        Hypodorian   A-A = Aeolian
#   Dorian       E-E = church Phrygian
# Each song's header names both. Genus colour: the diatonic tetrachord falls
# tone-tone-semitone (A-G-F-E); the chromatic one falls a minor third and two
# semitones (A-F#-F-E). Some sections borrow the chromatic notes on purpose.
DORIAN = (0, 2, 3, 5, 7, 9, 10)
MIXOLYDIAN = (0, 2, 4, 5, 7, 9, 10)
PHRYGIAN = (0, 1, 3, 5, 7, 8, 10)
IONIAN = (0, 2, 4, 5, 7, 9, 11)
LYDIAN = (0, 2, 4, 6, 7, 9, 11)
AEOLIAN = (0, 2, 3, 5, 7, 8, 10)
LOCRIAN = (0, 1, 3, 5, 6, 8, 10)

# ============================================================ Elaia Village
# D Dorian, 6/8. The lyre (harp) sings the tune, the kithara (low harp) rolls
# arpeggios, the aulos (oboe) answers. B natural and the G major chord are the
# Dorian colour; the loop's last bar turns Dm -> G (plagal) back to the top.
E_CH = {
    'intro': ['Dm', 'C'],
    'A': ['Dm', 'Dm C', 'G', 'Dm', 'F', 'C', 'G', 'Am'],
    'A2': ['Dm', 'C', 'G', 'Dm', 'F', 'C', 'C', 'Dm'],
    'B': ['F', 'C', 'G', 'Dm', 'F', 'Am', 'G', 'Am'],
    'C': ['Dm', 'C', 'G', 'Am'],
    'A3': ['Dm', 'C', 'G', 'Dm', 'F', 'C', 'C', 'Dm G'],
}


def e_kithara(spec):
    cs = bar_chords(spec)
    if len(cs) == 1:
        r, t, f = triad(cs[0], 48)
        return notes([(r, 1), (f, 1), (r + 12, 1), (t + 12, 1), (r + 12, 1), (f, 1)])
    out = []
    for c in cs:
        r, t, f = triad(c, 48)
        out += [(r, 1), (f, 1), (r + 12, 1)]
    return notes(out)


def e_bass(spec):
    cs = bar_chords(spec)
    if len(cs) == 1:
        r, t, f = triad(cs[0], 38)
        return notes([(r, 3), (f, 3)])
    return notes([(triad(c, 38)[0], 3) for c in cs])


def e_pad(spec):
    return notes([(triad(c, 55)[1], 6 // len(bar_chords(spec))) for c in bar_chords(spec)])


E_LYRE_A = ('A4:2 D5:1 E5:2 F5:1 | E5:2 D5:1 C5:2 A4:1 | B4:2 D5:1 G5:2 F5:1 | E5:3 D5:3 | '
            'F5:2 A5:1 G5:2 F5:1 | E5:2 G5:1 E5:2 C5:1 | D5:2 C5:1 B4:2 G4:1 | A4:3 E5:1 D5:1 C5:1')
E_LYRE_A2_HEAD = ('A4:2 D5:1 E5:2 F5:1 | G5:2 F5:1 E5:2 D5:1 | B4:2 D5:1 G5:2 A5:1 | F5:3 E5:2 D5:1 | '
                  'C5:2 F5:1 A5:2 F5:1 | G5:2 E5:1 C5:2 E5:1 | D5:2 E5:1 F5:2 E5:1')
E_AULOS_A2_HEAD = 'F4:6 | E4:3 G4:3 | G4:3 B4:3 | A4:6 | A4:3 C5:3 | C5:3 G4:3 | G4:3 E4:3'

E_DRUM = {'dum': 61, 'tek': 62, 'tam': 54, 'low': 64}
E_D = {
    'A': ' | '.join(['dum:3 tek:3_'] * 8),
    'A2': ' | '.join(['dum:3 tek:2_ tam:1_'] * 8),
    'B': ' | '.join(['dum:3 tek:2_ tam:1_'] * 8),
    'C': ' | '.join(['dum:1^ tek:1 tek:1 low:1 tek:1 tam:1'] * 3 + ['dum:1^ tek:1 tek:1 dum:1 dum:1 tek:1']),
    'A3': ' | '.join(['dum:2 tam:1_ tek:2 tam:1_'] * 8),
}

ELAIA = Song(
    name='mus_ichor_elaia', title='Elaia Village', meter=(6, 8), grouping=(3, 3), tempo=100,
    voicegroup='rg_credits', volume=127, reverb=50, priority=0,
    sections=[('intro', 2), ('A', 8), ('A2', 8), ('B', 8), ('C', 4), ('A3', 8)], loop_from='A',
    modes={'*': pcs('D', DORIAN)}, target=(60, 90), chords=E_CH,
    tracks=[
        Track('lyre', 46, 127, pan=-12, velocity=108, lo='G3', hi='C6', parts={
            'A': E_LYRE_A, 'A2': E_LYRE_A2_HEAD + ' | D5:5 r:1',
            'C': 'D5:1 E5:1 F5:1 A5:2 F5:1 | r:6 | D5:1 B4:1 G4:1 B4:1 D5:1 G5:1 | r:6',
            'A3': E_LYRE_A2_HEAD + ' | D5:3 C5:2 B4:1'}),
        Track('aulos', 68, 106, pan=14, velocity=104, lo='D4', hi='A5', vibrato=(4, 40, 14), parts={
            'A2': E_AULOS_A2_HEAD + ' | F4:6',
            'B': 'A4:3 C5:3 | E5:4 D5:1 C5:1 | B4:3 G4:3 | A4:2 F4:1 D4:3 | '
                 'F4:2 A4:1 C5:3 | E5:3 G5:2 E5:1 | D5:2 C5:1 B4:2 G4:1 | A4:6',
            'C': 'r:6 | G5:1 F5:1 E5:1 C5:2 E5:1 | r:6 | E5:2 D5:1 C5:1 B4:1 G4:1',
            'A3': E_AULOS_A2_HEAD + ' | F4:3 G4:3'}),
        Track('kithara', 46, 92, pan=22, velocity=90, lo='C3', hi='C5',
              parts={s: gen(c, e_kithara) for s, c in E_CH.items()}),
        # The GB wave channel has four output levels (gCgb3Vol). Volume 62 at -V127 keeps
        # this sine bass on the 25% step; one more and it jumps 6 dB and swamps the lyre.
        Track('bass', 92, 62, velocity=100, lo='C2', hi='C4',
              parts={s: gen(c, e_bass) for s, c in E_CH.items() if s != 'intro'}),
        Track('pad', 48, 60, pan=-24, velocity=76, lo='G3', hi='C5',
              parts={s: gen(E_CH[s], e_pad) for s in ('B', 'C', 'A3')}),
        Track('frame drum', 0, 97, velocity=100, kit=E_DRUM, parts=E_D),
    ])

# ============================================================ Route 1
# G Mixolydian, 7/8 kalamatianos (3+2+2). The syrinx (flute) leads, the kithara
# (nylon guitar) plays the laouto "boom-chick-chick" (bass on 1, dyads on 4 and 6),
# the reedy accordion stands in for a second aulos, the trumpet is the salpinx.
# F natural and the F major chord (bVII) carry the Mixolydian colour.
R_CH = {
    'intro': ['G', 'G'],
    'A': ['G', 'F', 'C', 'Dm', 'G', 'F', 'F', 'G'],
    'B': ['C', 'C', 'Am', 'Am', 'F', 'F', 'Dm', 'G'],
    'C': ['F', 'G', 'F', 'G', 'C', 'Dm', 'F', 'G'],
}
R_CH['A2'] = R_CH['A3'] = R_CH['A']
G_MIX = pcs('G', MIXOLYDIAN)


def r_guitar(c):
    r, t, f = triad(c, 55)
    dy = sorted([t, f if f < r + 12 else f - 12])
    return notes([(None, 3), (dy, 2), (dy, 2)])


def r_bass(c):
    r, t, f = triad(c, 43)
    return notes([(r, 3), (f - 12 if f - 12 >= 36 else f, 2), (r, 2)])


def r_harp(c):
    r, t, f = triad(c, 67)
    return notes([(r, 1), (t, 1), (f, 1), (r + 12, 2), (f, 2)])


R_FLUTE_A = ('D5:2 G5:1 G5:1 A5:1 B5:1 G5:1 | A5:2 F5:1 F5:1 G5:1 A5:1 F5:1 | '
             'G5:2 E5:1 E5:1 F5:1 G5:1 E5:1 | D5:3 C5:2 A4:2 | D5:2 G5:1 G5:1 A5:1 B5:1 D6:1 | '
             'C6:2 A5:1 F5:1 A5:1 G5:1 F5:1 | F5:2 G5:1 A5:1 G5:1 F5:1 E5:1 | D5:3 B4:2 G4:2')
R_KIT = {'dum': 64, 'tek': 62, 'tam': 54, 'taiko': 87, 'kick': 36}
R_DRUM_BAR = 'dum:3 tek:2 tek:2'
R_D = {
    'intro': 'dum:3 tek:2 tek:2 | dum:3 tek:1 tek:1 tek:1 tek:1',
    'A': ' | '.join([R_DRUM_BAR] * 8),
    'A2': ' | '.join(['dum:2 tam:1 tek:2 tek:2'] * 8),
    'B': ' | '.join(['dum:3 tek:2 tam:2'] * 8),
    'C': ' | '.join(['taiko:3^ tek:2 dum:2'] * 7 + ['taiko:3^ tek:1 tek:1 dum:1 dum:1']),
    'A3': ' | '.join(['dum:2 tam:1 tek:2 tek:1 tam:1'] * 8),
}
R_SHAKER = ' | '.join(['C6:1_ C6:1_ C6:1 C6:1_ C6:1 C6:1_ C6:1'] * 8)

ROUTE1 = Song(
    name='mus_ichor_route1', title='Route 1', meter=(7, 8), grouping=(3, 2, 2), tempo=150,
    voicegroup='rg_sevii_route', volume=107, reverb=50, priority=0,
    sections=[('intro', 2), ('A', 8), ('A2', 8), ('B', 8), ('C', 8), ('A3', 8)], loop_from='A',
    modes={'*': G_MIX}, target=(45, 75), chords=R_CH,
    tracks=[
        Track('syrinx', 73, 104, pan=-8, velocity=100, lo='G4', hi='D6', vibrato=(3, 44, 12), parts={
            'A': R_FLUTE_A, 'A2': R_FLUTE_A, 'A3': R_FLUTE_A,
            'C': 'r:7 | B5:1 A5:1 G5:1 D5:2 G5:2 | r:7 | D6:1 B5:1 G5:1 A5:2 B5:2 | '
                 'G5:3 E5:2 G5:2 | A5:3 F5:2 A5:2 | A5:2 B5:1 C6:2 A5:2 | B5:3 r:4'}),
        Track('aulos', 21, 84, pan=16, velocity=92, lo='E4', hi='B5', parts={
            'A2': diatonic(R_FLUTE_A, G_MIX, -2), 'A3': diatonic(R_FLUTE_A, G_MIX, -2),
            'B': 'E5:3 G5:4 | F5:1 E5:1 D5:1 E5:2 C5:2 | A4:3 C5:2 E5:2 | D5:3 C5:2 B4:2 | '
                 'C5:3 F5:4 | G5:1 F5:1 E5:1 F5:2 A5:2 | G5:3 F5:2 E5:2 | D5:3 B4:2 D5:2'}),
        Track('salpinx', 56, 96, pan=-20, velocity=104, gate=0.9, lo='C4', hi='D5', parts={
            'C': 'C4:1 C4:1 F4:1 A4:2 F4:2 | r:7 | C4:1 C4:1 F4:1 A4:2 C5:2 | r:7 | '
                 'E4:3 G4:2 C5:2 | F4:3 A4:2 D5:2 | F4:2 G4:1 A4:2 C5:2 | B4:3 D5:4'}),
        Track('kithara', 24, 88, pan=24, velocity=88, gate=0.8, lo='G3', hi='C5',
              parts={s: gen(c, r_guitar) for s, c in R_CH.items()}),
        Track('lyre', 46, 70, pan=-30, velocity=80, lo='G4', hi='C7',
              parts={'B': gen(R_CH['B'], r_harp)}),
        Track('bass', 92, 80, velocity=104, gate=0.85, lo='C2', hi='C4',
              parts={s: gen(c, r_bass) for s, c in R_CH.items()}),
        Track('square', 81, 44, pan=30, velocity=80, gate=0.9, lo='G3', hi='D5',
              parts={'A3': octave(R_FLUTE_A, -1)}),
        Track('frame drum', 0, 90, velocity=96, kit=R_KIT, parts=R_D),
        Track('shaker', 127, 40, velocity=80, gate=0.25, lo='C6', hi='C6',
              parts={s: R_SHAKER for s in ('A2', 'C', 'A3')}),
    ])

# ============================================================ Rival battle
# E Phrygian, 9/8 aksak (2+2+2+3). An aulos (oboe, doubled by a square for bite)
# over a string ostinato that leans on the F-E semitone. B turns to A minor with
# an E major chord (Phrygian dominant, G#), and C is a held, wailing build whose
# last bar (F -> Em, bII-i) drops straight back into the loop.
B_CH = {
    'intro': ['Em', 'Em'],
    'A': ['Em', 'Am', 'Dm', 'F', 'Em', 'Am', 'F', 'Em'],
    'A2': ['Em', 'Am', 'Dm', 'F', 'Em', 'Am', 'F', 'E'],
    'B': ['Am', 'Am', 'G', 'G', 'F', 'F', 'E', 'E'],
    'C': ['Em', 'Em', 'Dm', 'Dm', 'C', 'C', 'F', 'F'],
}
E_PHRY = pcs('E', PHRYGIAN) | {8}  # G# allowed: the Phrygian-dominant E major chord


def b_bass(c):
    r, t, f = triad(c, 36)
    return notes([(r, 1), (r, 1), (r + 12, 1), (r, 1), (f, 1), (r, 1), (r + 12, 1), (f, 1), (r, 1)])


def b_strings(c):
    r, t, f = triad(c, 64)
    up = r + (1 if (r + 1) % 12 in E_PHRY and c.startswith('E') else 2)
    return notes([(r, 1), (up, 1), (r, 1), (f - 12, 1), (r, 1), (up, 1), (t, 1), (up, 1), (r, 1)])


def b_arp(c):
    r, t, f = triad(c, 64)
    return notes([(r, 1), (t, 1), (f, 1), (r + 12, 1), (f, 1), (t, 1), (r, 1), (t, 1), (f, 1)])


def b_stab(c):
    r, t, f = triad(c, 55)
    return notes([([r, t], 1), (None, 3), ([t, f], 1), (None, 1), ([r, t], 1), (None, 2)])


B_OBOE_A = ('E5:1 F5:1 E5:1 D5:1 E5:2 B4:3 | C5:1 D5:1 C5:1 B4:1 C5:2 A4:3 | '
            'D5:1 E5:1 F5:1 E5:1 D5:2 A5:3 | G5:2 F5:2 E5:2 F5:3 | '
            'B4:1 E5:1 G5:1 F5:1 E5:2 B5:3 | C6:1 B5:1 A5:1 G5:1 A5:2 E5:3')
B_OBOE = {
    'A': B_OBOE_A + ' | F5:1 G5:1 A5:1 G5:1 F5:1 E5:1 D5:1 E5:1 F5:1 | E5:2 B4:2 E5:2 r:3',
    'A2': B_OBOE_A + ' | F5:1 E5:1 F5:1 G5:1 A5:2 C6:3 | B5:2 A5:2 G#5:2 B5:3',
    'C': 'E5:9 | F5:6 E5:3 | D5:9 | E5:6 F5:3 | G5:9 | F5:6 E5:3 | F5:4 G5:2 A5:3 | G5:2 F5:2 E5:2 F5:3',
}
B_KIT = {'kick': 36, 'snare': 38, 'taiko': 87, 'tek': 62, 'dum': 64, 'crash': 49, 'tam': 54}
B_BAR = 'kick:2 tek:2 dum:2 snare:1 tek:1 tek:1'
B_D = {
    'intro': 'crash:2^ r:4 taiko:3 | taiko:1 taiko:1 taiko:1 taiko:1 snare:1 snare:1 snare:1 snare:1 snare:1^',
    'A': ' | '.join(['crash:2 tek:2 dum:2 snare:1 tek:1 tek:1'] + [B_BAR] * 7),
    'A2': ' | '.join(['crash:2 tek:2 dum:2 snare:1 tek:1 tek:1'] + [B_BAR] * 6
                     + ['kick:2 snare:2 kick:2 snare:1 snare:1 snare:1^']),
    'B': ' | '.join(['taiko:2 tam:2 dum:2 snare:1 tam:1 tek:1'] * 8),
    'C': ' | '.join(['taiko:3 r:3 taiko:3'] * 4 + ['taiko:2 tek:2 taiko:2 tek:3'] * 2
                    + ['kick:2 snare:2 kick:2 snare:1 snare:1 snare:1', 'snare:1 snare:1 snare:1 snare:1 '
                       'snare:1 snare:1 snare:1^ snare:1^ snare:1^']),
}

BATTLE_RIVAL = Song(
    name='mus_ichor_battle_rival', title='Rival Battle', meter=(9, 8), grouping=(2, 2, 2, 3), tempo=180,
    voicegroup='rg_credits', volume=127, reverb=50, priority=1,
    sections=[('intro', 2), ('A', 8), ('A2', 8), ('B', 8), ('C', 8)], loop_from='A',
    modes={'*': E_PHRY}, target=(40, 70), chords=B_CH,
    tracks=[
        Track('aulos', 68, 110, pan=-6, velocity=104, lo='A4', hi='C6', vibrato=(5, 52, 18), parts=B_OBOE),
        Track('square', 82, 56, pan=8, velocity=96, gate=0.9, lo='A3', hi='C5',
              parts={s: octave(p, -1) for s, p in B_OBOE.items()}),
        Track('strings', 48, 84, pan=20, velocity=96, gate=0.85, lo='B3', hi='B5', parts={
            'intro': 'B5:1 A5:1 G5:1 F5:1 E5:1 D5:1 C5:1 B4:1 A4:1 | F4:2 E4:2 F4:2 E4:3',
            **{s: gen(B_CH[s], b_strings) for s in ('A', 'A2', 'C')}}),
        Track('salpinx', 56, 100, pan=-22, velocity=104, gate=0.9, lo='E4', hi='F5', parts={
            'B': 'A4:4 C5:2 B4:3 | A4:2 E4:2 A4:2 C5:3 | B4:4 D5:2 C5:3 | B4:2 G4:2 B4:2 D5:3 | '
                 'C5:4 E5:2 D5:3 | C5:2 A4:2 C5:2 F5:3 | E5:2 F5:2 E5:2 D5:1 C5:1 B4:1 | A4:2 G#4:2 F4:2 E4:3'}),
        Track('horn', 60, 76, pan=26, velocity=96, gate=0.8, lo='E3', hi='C5',
              parts={s: gen(B_CH[s], b_stab) for s in ('A2',)}),
        Track('bass', 87, 88, velocity=108, gate=0.8, lo='C2', hi='C4',
              parts={s: gen(c, b_bass) for s, c in B_CH.items() if s != 'intro'}),
        Track('arp', 81, 40, pan=-30, velocity=80, gate=0.7, lo='E4', hi='E6',
              parts={'B': gen(B_CH['B'], b_arp)}),
        Track('drums', 0, 96, velocity=100, kit=B_KIT, parts=B_D),
    ])

# ================================================================ the rest of the slice
# These all use the `ichor` voicegroup (sound/voicegroups/ichor.inc): one palette for
# the slice, GM-numbered, over Emerald drumset 1 for frame drums, krotala and kymbala.
VG = 'ichor'
FRAME_KIT = {'dum': 61, 'tek': 62, 'low': 63, 'tam': 54, 'kro': 75, 'pok': 76, 'tri': 80,
             'cym': 86, 'taiko': 87, 'deep': 36, 'snare': 38, 'crash': 49, 'tom': 45}


def bars(pattern, n, last=None):
    """n bars of one drum or noise pattern, the last one optionally replaced (a fill)."""
    return ' | '.join([pattern] * (n - 1) + [last or pattern])


# ============================================================ Akti harbor town
# C Greek Lydian (C-C, the Ionian scale), 4/4 with the island syrtos lilt (long,
# short, short, short: 3+1+2+2 eighths). The syrinx (flute) sings a hook that walks
# down in sequence, the aulos (oboe) joins it in parallel thirds the way island
# bands double a tune, and the kithara (nylon guitar) strums on the short beats.
# B swaps B for B-flat: the synemmenon, the "joined" tetrachord of the Lesser
# Perfect System, which turns the harbor toward F for eight bars. C is the quay
# festival with krotala (hyoushigi). Its last bar is G, which falls back to the C
# that opens the loop.
AK_CH = {
    'intro': ['C', 'C'],
    'A': ['C', 'Dm', 'C', 'G', 'C', 'F', 'G', 'C'],
    'B': ['F', 'Bb', 'F', 'C', 'Dm', 'Gm', 'Bb', 'C'],
    'C': ['Am', 'Am', 'F', 'G', 'C', 'C', 'F', 'G'],
}
AK_CH['A2'] = AK_CH['A']
C_LYD = pcs('C', IONIAN)
F_SYN = pcs('F', IONIAN)  # the synemmenon: B-flat in place of B

AK_TUNE = ('G5:3 A5:1 G5:2 E5:2 | F5:3 G5:1 F5:2 D5:2 | E5:3 F5:1 E5:2 C5:2 | D5:3 E5:1 D5:1 C5:1 B4:2 | '
           'C5:3 D5:1 E5:2 G5:2 | A5:3 B5:1 C6:2 A5:2 | G5:2 F5:1 E5:1 D5:2 B4:2 | C5:3 G4:1 C5:2 r:2')
AK_FLUTE_C = ('E5:0.5 F5:0.5 E5:1 D5:1 E5:1 A5:2 C6:2 | B5:1 A5:1 G5:1 A5:1 E5:4 | r:8 | r:8 | '
              'G5:1 E5:1 G5:1 C6:1 B5:1 A5:1 G5:1 E5:1 | F5:1 E5:1 D5:1 E5:1 C5:4 | '
              'A5:2 G5:1 F5:1 E5:2 D5:2 | B4:2 C5:1 D5:1 E5:2 F5:2')
AK_OBOE_C = ('r:8 | r:8 | C5:0.5 D5:0.5 C5:1 B4:1 C5:1 F5:2 A5:2 | G5:1 F5:1 E5:1 F5:1 D5:4 | r:8 | r:8 | '
             'F5:2 E5:1 D5:1 C5:2 B4:2 | G4:2 A4:1 B4:1 C5:2 D5:2')
# The square doubles whichever pipe has the tune in C, an octave down.
AK_SQUARE_C = ('E4:0.5 F4:0.5 E4:1 D4:1 E4:1 A4:2 C5:2 | B4:1 A4:1 G4:1 A4:1 E4:4 | '
               'C4:0.5 D4:0.5 C4:1 B3:1 C4:1 F4:2 A4:2 | G4:1 F4:1 E4:1 F4:1 D4:4 | '
               'G4:1 E4:1 G4:1 C5:1 B4:1 A4:1 G4:1 E4:1 | F4:1 E4:1 D4:1 E4:1 C4:4 | '
               'A4:2 G4:1 F4:1 E4:2 D4:2 | B3:2 C4:1 D4:1 E4:2 F4:2')


def ak_guitar(c):
    r, t, f = triad(c, 55)
    dy = sorted([t, f if f < r + 12 else f - 12])
    return notes([(None, 3), (dy, 1), (dy, 2), (dy, 2)])


def ak_bass(c):
    r, t, f = triad(c, 36)
    return notes([(r, 3), (None, 1), (f, 2), (r, 2)])


def ak_harp(c):
    r, t, f = triad(c, 55)
    return notes([(r, 1), (t, 1), (f, 1), (r + 12, 1), (t + 12, 1), (r + 12, 1), (f, 1), (t, 1)])


AK_FILL = 'dum:3 tek:1 tek:1 tek:1 low:1 low:1'
AK_D = {
    'intro': 'dum:3 tek:1 dum:2 tek:2 | ' + AK_FILL,
    'A': bars('dum:3 tek:1 dum:2 tek:2', 8, AK_FILL),
    'A2': bars('dum:3 tek:1 dum:2 tek:1 tam:1', 8, AK_FILL),
    'B': bars('dum:3 tek:1_ low:2 tek:2_', 8, 'dum:3 tek:1_ low:2 tek:1 tek:1'),
    'C': bars('dum:3 kro:1 dum:1 kro:1 tek:1 kro:1', 8, 'dum:1^ tek:1 tek:1 dum:1^ tek:1 tek:1 low:1 low:1'),
}
AK_SHAKER = bars('C6:1 C6:1_ C6:1_ C6:1 C6:1 C6:1_ C6:1 C6:1_', 8)

AKTI = Song(
    name='mus_ichor_akti', title='Akti', meter=(4, 4), grouping=(3, 1, 2, 2), tempo=128,
    voicegroup=VG, volume=100, reverb=50, priority=0,
    sections=[('intro', 2), ('A', 8), ('A2', 8), ('B', 8), ('C', 8)], loop_from='A',
    modes={'*': C_LYD, 'B': F_SYN}, target=(45, 75), chords=AK_CH,
    tracks=[
        Track('syrinx', 73, 100, pan=-10, velocity=100, lo='G4', hi='D6', vibrato=(3, 44, 12), parts={
            'A': AK_TUNE, 'A2': AK_TUNE, 'C': AK_FLUTE_C,
            'B': 'r:8 | r:4 F5:1 G5:1 A5:2 | r:8 | r:4 C6:1 Bb5:1 G5:2 | r:8 | r:4 Bb5:1 C6:1 D6:2 | '
                 'r:8 | r:4 E5:1 F5:1 G5:2'}),
        Track('aulos', 68, 92, pan=14, velocity=100, lo='D4', hi='A5', vibrato=(4, 40, 14), parts={
            'A2': diatonic(AK_TUNE, C_LYD, -2), 'C': AK_OBOE_C,
            'B': 'A4:3 Bb4:1 C5:2 F5:2 | D5:3 C5:1 Bb4:2 D5:2 | C5:3 A4:1 F4:2 A4:2 | G4:3 A4:1 Bb4:2 G4:2 | '
                 'F4:3 G4:1 A4:2 D5:2 | D5:3 C5:1 Bb4:2 G4:2 | F4:2 G4:1 A4:1 Bb4:2 D5:2 | C5:6 r:2'}),
        Track('lyre', 46, 80, pan=-26, velocity=88, lo='G3', hi='C6', parts={
            'intro': 'r:8 | C4:1 E4:1 G4:1 C5:1 E5:1 G5:1 C6:2',
            'B': gen(AK_CH['B'], ak_harp)}),
        Track('kithara', 24, 80, pan=24, velocity=88, gate=0.7, lo='G3', hi='C5',
              parts={s: gen(AK_CH[s], ak_guitar) for s in ('intro', 'A', 'A2', 'C')}),
        Track('bass', 92, 70, velocity=100, gate=0.9, lo='C2', hi='C4',
              parts={s: gen(c, ak_bass) for s, c in AK_CH.items()}),
        Track('square', 80, 40, pan=30, velocity=80, gate=0.9, lo='G3', hi='C5', parts={'C': AK_SQUARE_C}),
        Track('frame drum', 0, 88, velocity=96, kit=FRAME_KIT, parts=AK_D),
        Track('shaker', 127, 36, velocity=80, gate=0.25, lo='C6', hi='C6',
              parts={'A2': AK_SHAKER, 'C': AK_SHAKER}),
    ])

# ============================================================ Temple of Hestia
# D Greek Dorian (E-E's species on D: D Eb F G A Bb C, the church Phrygian), 5/4
# as 3+2, the cretic and paeonic feet of the Delphic hymns. The chorus (choir) opens
# with Elaia's lyre motif in this mode (A D Eb F), since Hestia's hearth is the
# heart of the home. Under it the frame drum keeps a steady hearth pulse, struck
# on 1 and 4, and the lyre turns slow broken chords. In B the aulos takes over
# and falls through the chromatic genus, G-E-Eb-D, while the chorus holds a slow
# descant and the noise channel starts to crackle like embers (it stays for A2).
# Phrases close Eb -> Dm, the falling semitone of the Dorian tetrachord, so the
# loop settles home each time.
TP_CH = {
    'intro': ['Dm', 'Dm'],
    'A': ['Dm', 'Cm', 'Bb', 'F', 'Dm', 'Gm', 'Eb', 'Dm'],
    'B': ['Bb', 'F', 'Gm', 'Dm', 'Bb', 'Cm', 'Eb', 'Dm'],
}
TP_CH['A2'] = TP_CH['A']
D_GDOR = pcs('D', PHRYGIAN)

TP_HYMN = ('A4:4 D5:2 Eb5:2 F5:2 | Eb5:4 D5:2 C5:4 | D5:6 Bb4:4 | C5:4 A4:2 C5:4 | '
           'A4:4 D5:2 F5:2 A5:2 | G5:4 F5:2 Eb5:2 D5:2 | Eb5:4 D5:2 C5:2 Bb4:2 | D5:10')
TP_HYMN_LOW = ('F4:4 A4:2 C5:2 D5:2 | C5:4 Bb4:2 G4:4 | Bb4:6 F4:4 | A4:4 F4:2 A4:4 | '
               'F4:4 A4:2 D5:2 F5:2 | Bb4:4 D5:2 C5:2 Bb4:2 | G4:4 Bb4:2 A4:2 G4:2 | A4:10')


def tp_harp(c):
    r, t, f = triad(c, 48)
    return notes([(r, 2), (f, 1), (r + 12, 1), (t + 12, 2), (f, 2), (r + 12, 2)])


def tp_pad(c):
    return notes([(triad(c, 48)[1], 10)])


def tp_bass(c):
    r = triad(c, 38)[0]
    return notes([(r, 6), (r + 7, 4)])


TP_PULSE = 'dum:2 tek:2_ tek:2_ low:2 tek:2_'
TP_D = {
    'intro': 'dum+cym:2 tek:2_ tek:2_ low:2 tek:2_ | ' + TP_PULSE,
    'A': 'dum+cym:2 tek:2_ tek:2_ low:2 tek:2_ | ' + bars(TP_PULSE, 7),
    'B': 'dum+cym:2 tek:2_ pok:2_ low:2 tek:2_ | ' + bars('dum:2 tek:2_ pok:2_ low:2 tek:2_', 7),
    'A2': 'dum+cym:2 tek:2_ tek:2_ low:2 tek:2_ | ' + bars(TP_PULSE, 7),
}
TP_CRACKLE = ' | '.join(['r:1 C6:1_ r:3 C6:1_ C6:1_ r:3', 'r:3 C6:1_ r:2 C6:1_ r:1 C6:1_ r:1'] * 4)

TEMPLE = Song(
    name='mus_ichor_temple', title='Temple of Hestia', meter=(5, 4), grouping=(3, 2), tempo=80,
    voicegroup=VG, volume=100, reverb=50, priority=0,
    sections=[('intro', 2), ('A', 8), ('B', 8), ('A2', 8)], loop_from='A',
    modes={'*': D_GDOR, 'B': D_GDOR | {4}}, target=(60, 95), chords=TP_CH,
    tracks=[
        Track('chorus', 52, 100, pan=-6, velocity=100, lo='F4', hi='A5', parts={
            'A': TP_HYMN, 'A2': TP_HYMN_LOW,
            'B': 'D5:10 | C5:10 | Bb4:10 | A4:10 | Bb4:10 | C5:10 | Bb4:10 | A4:10'}),
        Track('aulos', 68, 96, pan=14, velocity=100, lo='D4', hi='A5', vibrato=(4, 36, 18), parts={
            'B': 'F5:4 D5:2 Bb4:2 D5:2 | C5:4 A4:2 C5:2 F5:2 | G5:4 E5:1 Eb5:1 D5:4 | F5:2 D5:2 A4:6 | '
                 'Bb4:2 D5:2 F5:4 G5:2 | G5:4 Eb5:2 C5:4 | Bb4:2 C5:2 D5:2 Eb5:4 | G5:2 E5:1 Eb5:1 D5:6',
            'A2': TP_HYMN}),
        Track('lyre', 46, 84, pan=-22, velocity=90, lo='C3', hi='D5',
              parts={s: gen(TP_CH[s], tp_harp) for s in ('A', 'B', 'A2')} | {'intro': 'r:10 | ' + tp_harp('Dm')}),
        Track('strings', 48, 56, pan=24, velocity=80, lo='C3', hi='D4',
              parts={s: gen(TP_CH[s], tp_pad) for s in ('A', 'B', 'A2')}),
        Track('bass', 92, 66, velocity=100, lo='C2', hi='C4',
              parts={s: gen(c, tp_bass) for s, c in TP_CH.items()}),
        Track('bell', 14, 70, pan=-30, velocity=90, lo='D5', hi='D5', parts={'intro': 'D5:10 | r:10'}),
        Track('frame drum', 0, 80, velocity=96, kit=FRAME_KIT, parts=TP_D),
        Track('embers', 126, 28, velocity=80, gate=0.25, lo='C6', hi='C6',
              parts={'B': TP_CRACKLE, 'A2': TP_CRACKLE}),
    ])

# ============================================================ Asclepeion (the Pokemon Center)
# F Hypolydian (F-F, the church Lydian), 3/4. The healing god is Apollo's son, and
# Apollo's lyre was the healing instrument, so the lyre (harp) carries A over a
# rolling kithara (nylon guitar). B natural, the raised fourth, colours the G major
# chord the tune keeps leaning on. In B the syrinx (flute) answers over soft strings
# and harp arpeggios. A finger cymbal (triangle) marks every other bar. B ends on C,
# with the flute's E rising to the F that opens the loop.
AS_CH = {
    'intro': ['F'],
    'A': ['F', 'G', 'F', 'C', 'Dm', 'G', 'C', 'F'],
    'B': ['Dm', 'Am', 'G', 'C', 'Dm', 'Am', 'G', 'C'],
}
F_HLYD = pcs('F', LYDIAN)


def as_guitar(c):
    r, t, f = triad(c, 48)
    return notes([(r, 1), (f, 1), (t + 12, 1), (f, 1), (r + 12, 1), (f, 1)])


def as_harp(c):
    r, t, f = triad(c, 55)
    return notes([(r, 1), (t, 1), (f, 1), (r + 12, 1), (f, 1), (t, 1)])


def as_bass(c):
    r = triad(c, 41)[0]
    return notes([(r, 4), (r + 7, 2)])


ASCLEPEION = Song(
    name='mus_ichor_asclepeion', title='Asclepeion', meter=(3, 4), grouping=(2, 2, 2), tempo=90,
    voicegroup=VG, volume=127, reverb=50, priority=0,
    sections=[('intro', 1), ('A', 8), ('B', 8)], loop_from='A',
    modes={'*': F_HLYD}, target=(25, 50), chords=AS_CH,
    tracks=[
        Track('lyre', 46, 108, pan=-10, velocity=104, lo='G3', hi='C6', parts={
            'intro': 'F4:1 A4:1 C5:1 F5:1 E5:2',
            'A': 'F5:3 E5:1 F5:1 G5:1 | A5:2 B5:2 G5:2 | A5:3 G5:1 F5:2 | E5:4 C5:2 | '
                 'D5:3 E5:1 F5:1 A5:1 | B5:4 A5:1 G5:1 | G5:2 E5:2 D5:1 E5:1 | F5:6',
            'B': gen(AS_CH['B'], as_harp)}),
        Track('syrinx', 73, 96, pan=12, velocity=96, lo='G4', hi='D6', vibrato=(3, 40, 16), parts={
            'B': 'A5:3 G5:1 F5:2 | E5:3 D5:1 C5:2 | D5:2 G5:2 B5:2 | G5:4 E5:2 | '
                 'F5:3 E5:1 D5:2 | C5:2 E5:2 A5:2 | B5:3 A5:1 G5:2 | G5:4 E5:2'}),
        Track('kithara', 24, 76, pan=22, velocity=84, lo='C3', hi='C5',
              parts={s: gen(AS_CH[s], as_guitar) for s in ('intro', 'A')}),
        Track('strings', 48, 54, pan=-24, velocity=76, lo='A3', hi='F4',
              parts={'B': gen(AS_CH['B'], lambda c: notes([(triad(c, 55)[1], 6)]))}),
        Track('bass', 92, 62, velocity=96, lo='C2', hi='C4',
              parts={s: gen(c, as_bass) for s, c in AS_CH.items()}),
        Track('kymbala', 0, 64, velocity=80, kit=FRAME_KIT, parts={
            'intro': 'tri:6_', 'A': bars('tri:6_ | r:6', 4), 'B': bars('tri:6_ | r:6', 4)}),
    ])

# ============================================================ Team Titan battle
# B Greek Mixolydian (B-B on the white notes, the church Locrian). Its fifth is the
# tritone B-F, and the salpinx (trumpet) theme opens by leaping it. 9/8 as
# 3+2+2+2, a heavy zeibekiko-weighted aksak. Tuba and wave bass grind the B-C
# semitone under war drums (taiko, no kit kick) and timpani, strings saw the same
# semitone above. A2 adds horns an octave down. B moves the centre to E on the same
# notes (a metabole of tonos) for horn and trumpet calls. C is the Titans' chant:
# chorus and horns in long tones over pounding drums. It ends on B, which the loop
# restarts on.
TI_CH = {
    'intro': ['Bdim', 'Bdim'],
    'A': ['Bdim', 'Bdim', 'C', 'Bdim', 'Dm', 'C', 'F', 'Bdim'],
    'B': ['Em', 'F', 'Em', 'Dm', 'C', 'F', 'Em', 'Bdim'],
    'C': ['Bdim', 'C', 'Dm', 'C', 'Em', 'Dm', 'C', 'Bdim'],
}
TI_CH['A2'] = TI_CH['A']
B_GMIX = pcs('B', LOCRIAN)

TI_HEAD = ('B4:3 F5:4 E5:2 | D5:3 C5:2 D5:2 E5:2 | F5:3 G5:2 F5:2 E5:2 | D5:3 C5:2 B4:4 | '
           'D5:3 A5:4 G5:2 | F5:3 E5:2 F5:2 G5:2 | A5:3 G5:2 F5:2 E5:2')
TI_THEME = TI_HEAD + ' | F5:3 E5:2 D5:2 C5:2'
TI_THEME2 = TI_HEAD + ' | F5:3 E5:2 D5:2 C5:1 D5:1'
TI_TRUMPET_B = 'r:9 | r:9 | r:9 | r:9 | E5:3 G5:2 E5:2 C5:2 | F5:3 A5:2 F5:2 C5:2 | G5:3 F5:2 E5:2 D5:2 | F5:3 D5:2 B4:4'
TI_CHANT = 'B4:9 | C5:9 | D5:9 | C5:6 B4:3 | E5:9 | D5:9 | C5:9 | B4:9'


def ti_strings(c):
    r = triad(c, 67)[0]
    up, down = step(r, B_GMIX, 1), step(r, B_GMIX, -1)
    return notes([(r, 1), (r, 1), (up, 1), (r, 1), (up, 1), (r, 1), (down, 1), (r, 1), (up, 1)])


def ti_riff(c, octave_up=0):
    r = triad(c, 35)[0] + 12 * octave_up
    return notes([(r, 3), (r, 2), (step(r, B_GMIX, 1), 2), (r, 2)])


def ti_timpani(c):
    r = triad(c, 40)[0]
    return notes([(r, 3), (None, 4), (r, 2)])


def ti_arp(c):
    r, t, f = triad(c, 64)
    return notes([(r, 1), (t, 1), (f, 1), (r + 12, 1), (f, 1), (t, 1), (r, 1), (t, 1), (f, 1)])


TI_BAR = 'deep:3 snare:2 taiko:2 snare:2'
TI_FILL = 'deep:3 snare:2 snare:1 snare:1 snare:1 snare:1'
TI_D = {
    'intro': 'deep:3^ r:2 deep:2 r:2 | taiko:1 taiko:1 taiko:1 snare:1 snare:1 snare:1 snare:1 snare:1^ snare:1^',
    'A': 'deep+crash:3 snare:2 taiko:2 snare:2 | ' + bars(TI_BAR, 7, TI_FILL),
    'A2': 'deep+crash:3 snare:2 taiko:2 snare:1 snare:1 | ' + bars('deep:3 snare:2 taiko:2 snare:1 snare:1', 7, TI_FILL),
    'B': 'taiko+crash:3 tam:2 taiko:2 snare:2 | ' + bars('taiko:3 tam:2 taiko:2 snare:2', 7, TI_FILL),
    'C': 'deep+crash:3 taiko:2 deep:2 taiko:2 | ' + bars('deep:3 taiko:2 deep:2 taiko:2', 7,
                                                        'snare:1 snare:1 snare:1 snare:1 snare:1 snare:1 '
                                                        'snare:1^ snare:1^ snare:1^'),
}

TITAN = Song(
    name='mus_ichor_titan', title='Team Titan', meter=(9, 8), grouping=(3, 2, 2, 2), tempo=162,
    voicegroup=VG, volume=110, reverb=50, priority=1,
    sections=[('intro', 2), ('A', 8), ('A2', 8), ('B', 8), ('C', 8)], loop_from='A',
    modes={'*': B_GMIX}, target=(40, 70), chords=TI_CH,
    tracks=[
        Track('salpinx', 56, 104, pan=-8, velocity=106, gate=0.9, lo='E4', hi='A5',
              parts={'A': TI_THEME, 'A2': TI_THEME2, 'B': TI_TRUMPET_B}),
        Track('horn', 60, 90, pan=18, velocity=100, gate=0.9, lo='B3', hi='D5', parts={
            'A2': octave(TI_THEME2, -1), 'C': octave(TI_CHANT, -1),
            'B': 'E4:3 G4:2 B4:2 A4:2 | A4:3 G4:2 F4:2 E4:2 | G4:3 A4:2 B4:2 C5:2 | D5:3 C5:2 A4:4 | '
                 'E4:9 | F4:9 | E4:9 | D4:9'}),
        Track('chorus', 52, 92, pan=-16, velocity=100, lo='B4', hi='E5', parts={'C': TI_CHANT}),
        Track('strings', 48, 80, pan=26, velocity=92, gate=0.8, lo='A4', hi='G5',
              parts={s: gen(TI_CH[s], ti_strings) for s in ('A', 'A2', 'B')}),
        Track('tuba', 58, 96, pan=-4, velocity=108, gate=0.8, lo='B1', hi='G2',
              parts={s: gen(c, ti_riff) for s, c in TI_CH.items()}),
        Track('bass', 87, 76, velocity=104, gate=0.7, lo='C2', hi='G3',
              parts={s: gen(c, lambda x: ti_riff(x, 1)) for s, c in TI_CH.items()}),
        Track('timpani', 47, 92, pan=10, velocity=100, gate=0.6, lo='E2', hi='D3', parts={
            'intro': 'B2:3 r:4 B2:2 | ' + ' '.join(['B2:0.5'] * 18),
            'A': gen(TI_CH['A'], ti_timpani), 'C': gen(TI_CH['C'], ti_timpani)}),
        Track('square', 80, 44, pan=-28, velocity=88, gate=0.9, lo='B4', hi='A5',
              parts={'A': TI_THEME, 'A2': TI_THEME2, 'B': TI_TRUMPET_B}),
        Track('arp', 81, 36, pan=30, velocity=80, gate=0.7, lo='E4', hi='F6',
              parts={'C': gen(TI_CH['C'], ti_arp)}),
        Track('drums', 0, 96, velocity=100, kit=FRAME_KIT, parts=TI_D),
    ])

# ============================================================ Trainer battle
# A Greek Phrygian (D-D's species on A: the church A Dorian, with F#), 7/8 as the
# kalamatianos 3+2+2, the bible's battle meter. The aulos (oboe) leads; in A2 and
# A3 a square an octave down adds bite. B stops over an E drone, the Byzantine ison, and
# the salpinx (trumpet) climbs and falls through the chromatic genus E-F-F#-A.
# C is a running duet for syrinx and aulos in thirds. A3 doubles the aulos the
# way the real instrument did, with a second pipe (accordion) a third below.
# The loop ends on Am after G, the bVII-i close of the Phrygian species.
TR_CH = {
    'intro': ['Am', 'Am'],
    'A': ['Am', 'G', 'Am', 'Em', 'Am', 'D', 'G', 'Am'],
    'B': ['Em', 'Em', 'Em', 'Em', 'Dm', 'Dm', 'F', 'Em'],
    'C': ['C', 'G', 'Am', 'Em', 'F', 'C', 'D', 'Em'],
}
TR_CH['A2'] = TR_CH['A3'] = TR_CH['A']
A_GPHR = pcs('A', DORIAN)
A_CHROM = A_GPHR | {5}  # F natural: the chromatic genus E-F-F#-A
E_WHITE = pcs('E', PHRYGIAN)

TR_TUNE = ('A4:1 C5:1 E5:1 A5:2 G5:2 | G5:1 A5:1 G5:1 F#5:2 D5:2 | E5:1 F#5:1 E5:1 D5:2 C5:2 | B4:3 E5:2 G5:2 | '
           'A5:1 G5:1 A5:1 C6:2 B5:2 | A5:1 F#5:1 A5:1 D6:2 C6:2 | B5:1 A5:1 G5:1 F#5:2 D5:2 | E5:3 A4:2 r:2')
TR_FLUTE_C = ('G5:1 E5:1 G5:1 C6:2 G5:2 | B5:1 A5:1 G5:1 D5:2 G5:2 | A5:1 G5:1 A5:1 E5:2 C5:2 | B4:3 E5:2 G5:2 | '
              'A5:1 G5:1 F5:1 C6:2 A5:2 | G5:1 F5:1 E5:1 C5:2 E5:2 | F#5:1 E5:1 F#5:1 A5:2 D6:2 | B5:3 G5:2 E5:2')
TR_OBOE_C = ('E5:1 C5:1 E5:1 G5:2 E5:2 | G5:1 F#5:1 E5:1 B4:2 D5:2 | F#5:1 E5:1 F#5:1 C5:2 A4:2 | G4:3 B4:2 E5:2 | '
             'F5:1 E5:1 D5:1 A5:2 F5:2 | E5:1 D5:1 C5:1 A4:2 C5:2 | D5:1 C5:1 D5:1 F#5:2 B5:2 | G5:3 E5:2 B4:2')


def tr_guitar(c):
    r, t, f = triad(c, 55)
    dy = sorted([t, f if f < r + 12 else f - 12])
    return notes([(None, 3), (dy, 2), (dy, 2)])


def tr_bass(c):
    r = triad(c, 40)[0]
    return notes([(r, 1), (r, 1), (r + 12, 1), (r + 7, 1), (r, 1), (r + 12, 1), (r + 7, 1)])


def tr_strings(scale):
    def fn(c):
        r = triad(c, 64)[0]
        up, down = step(r, scale, 1), step(r, scale, -1)
        return notes([(r, 1), (up, 1), (r, 1), (down, 1), (r, 1), (up, 1), (r, 1)])
    return fn


def tr_arp(c):
    r, t, f = triad(c, 64)
    return notes([(r, 1), (t, 1), (f, 1), (r + 12, 1), (f, 1), (t, 1), (r, 1)])


TR_FILL = 'deep:3 snare:1 snare:1 snare:1 snare:1'
TR_A2_BAR = 'deep:2 tam:1 snare:2 tek:1 tek:1'
TR_D = {
    'intro': 'deep:3^ r:2 snare:1 snare:1 | taiko:1 taiko:1 taiko:1 snare:1 snare:1 snare:1 snare:1^',
    'A': 'deep+crash:3 tek:2 snare:2 | ' + bars('deep:3 tek:2 snare:2', 7, TR_FILL),
    'A2': 'deep+crash:2 tam:1 snare:2 tek:1 tek:1 | ' + bars(TR_A2_BAR, 7, TR_FILL),
    'B': 'taiko+crash:3 dum:2 snare:2 | ' + bars('taiko:3 dum:2 snare:2', 7, TR_FILL),
    'C': 'deep+crash:3 snare:2 deep:1 snare:1 | ' + bars('deep:3 snare:2 deep:1 snare:1', 7,
                                                         'snare:1 snare:1 snare:1 snare:1 snare:1 snare:1^ snare:1^'),
    'A3': 'deep+crash:2 tam:1 snare:2 tek:1 tek:1 | ' + bars(TR_A2_BAR, 7, TR_FILL),
}
TR_SHAKER = bars('C6:1 C6:1_ C6:1_ C6:1 C6:1_ C6:1 C6:1_', 8)

BATTLE_TRAINER = Song(
    name='mus_ichor_battle_trainer', title='Trainer Battle', meter=(7, 8), grouping=(3, 2, 2), tempo=180,
    voicegroup=VG, volume=127, reverb=50, priority=1,
    sections=[('intro', 2), ('A', 8), ('A2', 8), ('B', 8), ('C', 8), ('A3', 8)], loop_from='A',
    modes={'*': A_GPHR, 'B': A_CHROM, 'C': A_CHROM}, target=(40, 70), chords=TR_CH,
    tracks=[
        Track('aulos', 68, 108, pan=-6, velocity=104, lo='G4', hi='D6', vibrato=(4, 50, 16), parts={
            'A': TR_TUNE, 'A2': TR_TUNE, 'C': TR_OBOE_C, 'A3': TR_TUNE}),
        Track('aulos 2', 21, 76, pan=18, velocity=96, lo='E4', hi='B5',
              parts={'A3': diatonic(TR_TUNE, A_GPHR, -2)}),
        Track('syrinx', 73, 92, pan=-20, velocity=100, lo='G4', hi='D6', vibrato=(3, 44, 12),
              parts={'C': TR_FLUTE_C}),
        Track('salpinx', 56, 100, pan=-14, velocity=104, gate=0.9, lo='B4', hi='A5', parts={
            'B': 'E5:3 F5:2 F#5:2 | A5:3 F#5:2 F5:2 | E5:3 B4:2 E5:2 | F5:3 E5:2 D5:2 | '
                 'D5:3 F5:2 A5:2 | G5:3 F5:2 E5:2 | F5:3 G5:2 A5:2 | A5:2 F#5:1 F5:1 E5:3'}),
        Track('kithara', 24, 80, pan=24, velocity=90, gate=0.5, lo='G3', hi='C5',
              parts={s: gen(TR_CH[s], tr_guitar) for s in ('intro', 'A', 'A2', 'B', 'A3')}),
        Track('strings', 48, 74, pan=28, velocity=90, gate=0.8, lo='D4', hi='A5', parts={
            'intro': 'A4:1 B4:1 C5:1 D5:1 E5:1 F#5:1 G5:1 | A5:3 E5:2 A4:2',
            'A2': gen(TR_CH['A2'], tr_strings(A_GPHR)), 'B': gen(TR_CH['B'], tr_strings(E_WHITE))}),
        Track('bass', 87, 84, velocity=106, gate=0.7, lo='E2', hi='E4',
              parts={s: gen(c, tr_bass) for s, c in TR_CH.items()}),
        Track('square', 82, 50, pan=8, velocity=92, gate=0.9, lo='A3', hi='D6', parts={
            'A2': octave(TR_TUNE, -1), 'A3': octave(TR_TUNE, -1), 'C': gen(TR_CH['C'], tr_arp)}),
        Track('drums', 0, 96, velocity=100, kit=FRAME_KIT, parts=TR_D),
        Track('shaker', 127, 38, velocity=80, gate=0.25, lo='C6', hi='C6',
              parts={'A2': TR_SHAKER, 'B': TR_SHAKER, 'A3': TR_SHAKER}),
    ])

# ============================================================ Wild battle
# C Hypodorian (A-A's species on C: the Aeolian, C D Eb F G Ab Bb) with the
# chromatic genus C-A-Ab-G as its colour: the tune keeps falling through it.
# 5/8 as 2+3, lopsided and quick. Wild Pokemon are Pan's, so his syrinx (flute)
# leads, in a sequence that steps down C, Bb, Ab to G. The aulos (oboe) joins in
# thirds in A2 and leads B; C is a hocket between the two pipes over krotala and
# string stabs. Every section ends on G, which the loop's C answers.
WI_CH = {
    'intro': ['Cm', 'Cm'],
    'A': ['Cm', 'Cm', 'Bb', 'Bb', 'Ab', 'Ab', 'Gm', 'Gm'],
    'B': ['Fm', 'Fm', 'Cm', 'Cm', 'Ab', 'Bb', 'Gm', 'Gm'],
    'C': ['Ab', 'Bb', 'Cm', 'Cm', 'Ab', 'Bb', 'Gm', 'Gm'],
}
WI_CH['A2'] = WI_CH['A3'] = WI_CH['A']
WI_CH['B2'] = WI_CH['B']
C_HDOR = pcs('C', AEOLIAN)
C_CHROM = C_HDOR | {9}  # A natural: the chromatic genus C-A-Ab-G

WI_TUNE = ('G4:1 C5:1 Eb5:1 D5:1 C5:1 | G5:2 F5:1 Eb5:1 D5:1 | Bb4:1 D5:1 F5:1 Eb5:1 D5:1 | F5:2 Eb5:1 D5:1 C5:1 | '
           'Eb5:1 F5:1 G5:1 Ab5:1 G5:1 | F5:2 Eb5:1 D5:1 C5:1 | C6:2 A5:1 Ab5:1 G5:1 | G5:2 F5:1 D5:1 Bb4:1')
WI_OBOE_B = ('C5:2 F5:1 Ab5:1 G5:1 | F5:2 Eb5:1 D5:1 C5:1 | Eb5:2 G5:1 F5:1 Eb5:1 | D5:2 C5:3 | '
             'C5:2 Eb5:1 Ab5:1 G5:1 | F5:2 D5:1 Bb4:1 D5:1 | G5:2 F5:1 Eb5:1 D5:1 | C5:1 A4:1 Ab4:1 G4:2')


def wi_guitar(c):
    r, t, f = triad(c, 55)
    dy = sorted([t, f if f < r + 12 else f - 12])
    return notes([(None, 1), (dy, 1), (None, 1), (dy, 1), (dy, 1)])


def wi_bass(c):
    r = triad(c, 36)[0]
    return notes([(r, 1), (r, 1), (r + 7, 1), (r, 1), (r + 12, 1)])


def wi_stab(c):
    r, t, f = triad(c, 55)
    return notes([([r, f], 1), (None, 1), ([r, f], 1), (None, 2)])


WI_D = {
    'intro': 'deep:2^ r:3 | taiko:1 taiko:1 snare:1 snare:1 snare:1^',
    'A': 'dum+crash:2 tek:1 low:1 tek:1 | ' + bars('dum:2 tek:1 low:1 tek:1', 7),
    'A2': bars('dum:1 tam:1 tek:1 low:1 tek:1', 8),
    'B': 'deep+crash:2 tek:1 snare:1 tek:1 | ' + bars('deep:2 tek:1 snare:1 tek:1', 7),
    'B2': bars('deep:2 tek:1 snare:1 snare:1', 8),
    'C': bars('deep:1 kro:1 snare:1 kro:1 kro:1', 8, 'snare:1 snare:1 snare:1 snare:1^ snare:1^'),
    'A3': 'dum+crash:1 tam:1 snare:1 low:1 tek:1 | ' + bars('dum:1 tam:1 snare:1 low:1 tek:1', 7,
                                                            'deep:1 snare:1 snare:1 snare:1 snare:1'),
}
WI_SHAKER = bars('C6:1 C6:1_ C6:1 C6:1_ C6:1_', 8)

BATTLE_WILD = Song(
    name='mus_ichor_battle_wild', title='Wild Battle', meter=(5, 8), grouping=(2, 3), tempo=180,
    voicegroup=VG, volume=110, reverb=50, priority=1,
    sections=[('intro', 2), ('A', 8), ('A2', 8), ('B', 8), ('B2', 8), ('C', 8), ('A3', 8)], loop_from='A',
    modes={'*': C_CHROM}, target=(35, 60), chords=WI_CH,
    tracks=[
        Track('syrinx', 73, 104, pan=-8, velocity=104, lo='G4', hi='D6', vibrato=(3, 48, 10), parts={
            'intro': 'r:5 | G5:0.5 Ab5:0.5 G5:0.5 Ab5:0.5 G5:0.5 Ab5:0.5 G5:2',
            'A': WI_TUNE, 'A2': WI_TUNE, 'A3': WI_TUNE,
            'B2': 'Ab5:5 | C6:2 Ab5:3 | G5:5 | Eb5:2 G5:3 | Ab5:5 | F5:2 Bb5:3 | D6:2 C6:1 Bb5:1 A5:1 | Ab5:2 G5:3',
            'C': 'Eb5:1 Ab5:1 C6:1 r:2 | F5:1 Bb5:1 D6:1 r:2 | C6:2 Bb5:1 G5:1 Eb5:1 | r:5 | '
                 'Ab5:1 G5:1 F5:1 Eb5:1 C5:1 | r:5 | D6:2 C6:1 A5:1 Ab5:1 | G5:5'}),
        Track('aulos', 68, 98, pan=16, velocity=100, lo='D4', hi='A5', vibrato=(4, 50, 14), parts={
            'A2': diatonic(WI_TUNE, C_HDOR, -2), 'B': WI_OBOE_B, 'B2': WI_OBOE_B,
            'C': 'r:3 C5:1 Eb5:1 | r:3 D5:1 F5:1 | r:5 | G4:1 C5:1 Eb5:1 D5:1 C5:1 | '
                 'r:5 | Bb4:1 C5:1 D5:1 F5:1 D5:1 | G5:2 F5:1 C5:2 | Bb4:5'}),
        Track('kithara', 24, 80, pan=24, velocity=90, gate=0.5, lo='G3', hi='C5',
              parts={s: gen(WI_CH[s], wi_guitar) for s in ('intro', 'A', 'A2', 'B', 'B2', 'A3')}),
        Track('strings', 48, 76, pan=-26, velocity=96, gate=0.6, lo='G3', hi='G4',
              parts={'C': gen(WI_CH['C'], wi_stab)}),
        Track('bass', 87, 84, velocity=106, gate=0.7, lo='C2', hi='C4',
              parts={s: gen(c, wi_bass) for s, c in WI_CH.items()}),
        Track('square', 80, 42, pan=30, velocity=88, gate=0.9, lo='G3', hi='C5',
              parts={'A3': octave(WI_TUNE, -1)}),
        Track('drums', 0, 94, velocity=100, kit=FRAME_KIT, parts=WI_D),
        Track('shaker', 127, 38, velocity=80, gate=0.25, lo='C6', hi='C6',
              parts={'A2': WI_SHAKER, 'B2': WI_SHAKER, 'A3': WI_SHAKER}),
    ])

# ============================================================ Trainer victory
# D Greek Lydian (C-C's species on D: the Ionian), the mode Plato called fit for the
# symposium, so it suits a win. The salpinx (trumpet) fanfare lifts through C major
# (bVII, the Hypophrygian colour) to a held D with a harp sweep and a timpani roll.
# The loop is a hasapiko-like dance for the syrinx (flute), and in B the trumpet
# answers over lyre arpeggios. B ends on A, which falls home to the D that opens
# the loop.
VI_CH = {
    'intro': ['D', 'C', 'D'],
    'A': ['D', 'G', 'D', 'A', 'Bm', 'G', 'A', 'D'],
    'B': ['G', 'D', 'C', 'D', 'G', 'D', 'Em', 'A'],
}
D_GLYD = pcs('D', IONIAN)

VI_TUNE = ('A4:1 D5:1 F#5:2 A5:2 F#5:2 | G5:1 A5:1 B5:2 G5:2 D5:2 | F#5:1 G5:1 A5:2 F#5:2 D5:2 | '
           'E5:1 F#5:1 E5:1 D5:1 C#5:2 A4:2 | B4:1 D5:1 F#5:2 B5:2 A5:2 | G5:1 F#5:1 E5:2 G5:2 B5:2 | '
           'A5:2 G5:1 F#5:1 E5:2 C#5:2 | D5:4 r:4')


def vi_guitar(c):
    r, t, f = triad(c, 55)
    dy = sorted([t, f if f < r + 12 else f - 12])
    return notes([(None, 2), (dy, 2), (None, 2), (dy, 2)])


def vi_bass(c):
    r = triad(c, 38)[0]
    return notes([(r, 2), (None, 2), (r + 7, 2), (None, 2)])


VI_FILL = 'dum:2 tek:1 tek:1 dum:1 tek:1 low:1 low:1'
VI_D = {
    'intro': 'deep+crash:2 r:2 snare:1 snare:1 snare:2 | deep:2 snare:2 deep:2 snare:1 snare:1 | deep+crash:4 r:4',
    'A': bars('dum:2 tek:2 dum:2 tam:2', 8, VI_FILL),
    'B': bars('dum:2 kro:1 kro:1 dum:2 tam:2', 8, VI_FILL),
}

VICTORY_TRAINER = Song(
    name='mus_ichor_victory_trainer', title='Trainer Victory', meter=(4, 4), grouping=(2, 2, 2, 2), tempo=144,
    voicegroup=VG, volume=127, reverb=50, priority=0,
    sections=[('intro', 3), ('A', 8), ('B', 8)], loop_from='A',
    modes={'*': D_GLYD, 'intro': D_GLYD | {0}, 'B': D_GLYD | {0}}, target=(18, 40), chords=VI_CH,
    tracks=[
        Track('salpinx', 56, 104, pan=-8, velocity=108, gate=0.9, lo='D4', hi='A5', parts={
            'intro': 'D4:1 D4:1 D4:1 F#4:1 A4:2 D5:2 | C5:2 B4:1 C5:1 E5:4 | D5:8',
            'B': 'D5:2 B4:1 D5:1 G5:4 | F#5:2 E5:1 D5:1 A4:4 | G4:1 C5:1 E5:2 G5:2 E5:2 | F#5:4 D5:4 | '
                 'r:8 | r:8 | r:8 | r:8'}),
        Track('horn', 60, 80, pan=18, velocity=96, gate=0.9, lo='A3', hi='A4',
              parts={'intro': 'r:4 A3:2 F#4:2 | G4:4 E4:4 | F#4:8'}),
        Track('syrinx', 73, 100, pan=10, velocity=100, lo='G4', hi='D6', vibrato=(3, 44, 12), parts={
            'A': VI_TUNE,
            'B': 'r:8 | r:8 | r:8 | r:8 | B5:2 A5:1 G5:1 D5:2 G5:2 | A5:2 G5:1 F#5:1 D5:2 F#5:2 | '
                 'G5:2 F#5:1 E5:1 B4:2 E5:2 | E5:3 D5:1 C#5:2 B4:2'}),
        Track('square', 80, 44, pan=-28, velocity=88, gate=0.9, lo='D3', hi='E4',
              parts={'intro': 'D3:1 D3:1 D3:1 F#3:1 A3:2 D4:2 | C4:2 B3:1 C4:1 E4:4 | D4:8'}),
        Track('lyre', 46, 84, pan=-22, velocity=92, lo='G3', hi='D6', parts={
            'intro': 'r:8 | r:8 | D4:0.5 F#4:0.5 A4:0.5 D5:0.5 F#5:0.5 A5:0.5 D6:1 r:4',
            'B': gen(VI_CH['B'], ak_harp)}),
        Track('kithara', 24, 80, pan=24, velocity=88, gate=0.6, lo='G3', hi='C5',
              parts={s: gen(VI_CH[s], vi_guitar) for s in ('A', 'B')}),
        Track('bass', 92, 60, velocity=100, gate=0.9, lo='D2', hi='D4',
              parts={s: gen(VI_CH[s], vi_bass) for s in ('A', 'B')}),
        Track('timpani', 47, 90, pan=6, velocity=100, gate=0.6, lo='G2', hi='D3', parts={
            'intro': 'D3:1 D3:1 D3:1 r:1 A2:2 D3:2 | C3:2 r:2 C3:2 G2:2 | ' + ' '.join(['D3:0.5'] * 16)}),
        Track('drums', 0, 90, velocity=100, kit=FRAME_KIT, parts=VI_D),
    ])

SONGS = [ELAIA, ROUTE1, BATTLE_RIVAL, AKTI, TEMPLE, ASCLEPEION, TITAN, BATTLE_TRAINER, BATTLE_WILD,
         VICTORY_TRAINER]
