"""Song data for Pokemon Ichor. All three are original compositions.

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

QUALITY = {'': (0, 4, 7), 'm': (0, 3, 7)}


def triad(name, lo):
    """Chord tones of e.g. 'Dm' with the root in [lo, lo + 11]."""
    m = re.match(r'^([A-G][#b]?)(m?)$', name)
    root = pitch(m.group(1) + '4') % 12
    base = lo + (root - lo) % 12
    return [base + i for i in QUALITY[m.group(2)]]


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


DORIAN = (0, 2, 3, 5, 7, 9, 10)
MIXOLYDIAN = (0, 2, 4, 5, 7, 9, 10)
PHRYGIAN = (0, 1, 3, 5, 7, 8, 10)

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
    voicegroup='rg_credits', volume=100, reverb=50, priority=0,
    sections=[('intro', 2), ('A', 8), ('A2', 8), ('B', 8), ('C', 4), ('A3', 8)], loop_from='A',
    modes={'*': pcs('D', DORIAN)}, target=(60, 90), chords=E_CH,
    tracks=[
        Track('lyre', 46, 110, pan=-12, velocity=100, lo='G3', hi='C6', parts={
            'A': E_LYRE_A, 'A2': E_LYRE_A2_HEAD + ' | D5:5 r:1',
            'C': 'D5:1 E5:1 F5:1 A5:2 F5:1 | r:6 | D5:1 B4:1 G4:1 B4:1 D5:1 G5:1 | r:6',
            'A3': E_LYRE_A2_HEAD + ' | D5:3 C5:2 B4:1'}),
        Track('aulos', 68, 92, pan=14, velocity=96, lo='D4', hi='A5', vibrato=(4, 40, 14), parts={
            'A2': E_AULOS_A2_HEAD + ' | F4:6',
            'B': 'A4:3 C5:3 | E5:4 D5:1 C5:1 | B4:3 G4:3 | A4:2 F4:1 D4:3 | '
                 'F4:2 A4:1 C5:3 | E5:3 G5:2 E5:1 | D5:2 C5:1 B4:2 G4:1 | A4:6',
            'C': 'r:6 | G5:1 F5:1 E5:1 C5:2 E5:1 | r:6 | E5:2 D5:1 C5:1 B4:1 G4:1',
            'A3': E_AULOS_A2_HEAD + ' | F4:3 G4:3'}),
        Track('kithara', 46, 80, pan=22, velocity=84, lo='C3', hi='C5',
              parts={s: gen(c, e_kithara) for s, c in E_CH.items()}),
        Track('bass', 92, 76, velocity=100, lo='C2', hi='C4',
              parts={s: gen(c, e_bass) for s, c in E_CH.items() if s != 'intro'}),
        Track('pad', 48, 52, pan=-24, velocity=72, lo='G3', hi='C5',
              parts={s: gen(E_CH[s], e_pad) for s in ('B', 'C', 'A3')}),
        Track('frame drum', 0, 84, velocity=92, kit=E_DRUM, parts=E_D),
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
    voicegroup='rg_sevii_route', volume=98, reverb=50, priority=0,
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

SONGS = [ELAIA, ROUTE1, BATTLE_RIVAL]
