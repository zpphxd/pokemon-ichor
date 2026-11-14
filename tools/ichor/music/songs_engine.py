"""The music the engine triggers rather than a map: fanfares and jingles, evolution,
caught, the victories, trainer encounter (eye-contact) themes, the title, the intro and
the new-game speech. All original, all on the `ichor` voicegroup. Notation is as in
songs.py, which imports this module at its end (so import songs, not this).

Most of these replace a vanilla song at its own ID: song_id names the songs.h constant
whose gSongTable slot now plays the Ichor song, so no caller changes, and the FRLG
MUS_RG_* slots stay as they were. ref is the vanilla song's level, measured before
its slot was repointed. Fanfare lengths must fit their sFanfares entry in src/sound.c;
compose.py --check enforces it.
"""
from compose import Song, Track
from songs import (AEOLIAN, DORIAN, FRAME_KIT, IONIAN, LOCRIAN, LYDIAN, MIXOLYDIAN, PHRYGIAN, VG,
                   B_GMIX, ak_harp, bars, diatonic, gen, notes, octave, pcs, step, ti_riff,
                   ti_strings, triad)


def one_shot(name, title, meter, tempo, sections, modes, chords, tracks, target, song_id, ref,
             fanfare=True, volume=100, priority=5):
    return Song(name=name, title=title, meter=meter, grouping=(meter[0],), tempo=tempo,
                voicegroup=VG, volume=volume, reverb=50, priority=priority, sections=sections,
                loop_from=None, modes=modes, tracks=tracks, target=target, chords=chords,
                song_id=song_id, fanfare=fanfare, ref=ref)


def arp(lo):
    """Harp arpeggio up and back over a 4/4 bar."""
    def fn(c):
        r, t, f = triad(c, lo)
        return notes([(r, 1), (t, 1), (f, 1), (r + 12, 1), (t + 12, 1), (r + 12, 1), (f, 1), (t, 1)])
    return fn


def offbeats(pattern, lo=55):
    """Kithara dyads on the beats a pattern marks with 'x' (each item: (hit?, eighths))."""
    def fn(c):
        r, t, f = triad(c, lo)
        dy = sorted([t, f if f < r + 12 else f - 12])
        return notes([(dy if hit else None, d) for hit, d in pattern])
    return fn


def root_fifth(pattern, lo):
    """Bass on root (r), fifth (f), octave (o) or rest (None) per (kind, eighths)."""
    def fn(c):
        r = triad(c, lo)[0]
        return notes([({'r': r, 'f': r + 7, 'o': r + 12}.get(k), d) for k, d in pattern])
    return fn


def roll(note, eighths):
    return ' '.join([f'{note}:0.5'] * (2 * eighths))


# ============================================================ fanfares
# Each opens with or leans on the slice's call, 5-1-2-3 (Elaia's lyre opens A-D-E-F),
# and each is cut to fit the vanilla fanfare's slot so script pacing doesn't change.

# Level up: the lyre runs up D Hypolydian (the raised fourth, G#, glints) under a salpinx call.
LEVEL_UP = one_shot(
    'mus_ichor_level_up', 'Level Up', (3, 4), 150, [('A', 1)], {'*': pcs('D', LYDIAN)}, {'A': ['D']},
    target=(1.0, 1.4), song_id='MUS_LEVEL_UP', ref=('MUS_LEVEL_UP', -27.1), tracks=[
        Track('salpinx', 56, 92, pan=-8, velocity=104, gate=0.9, lo='A4', hi='A5', parts={'A': 'A4:1 D5:1 F#5:1 A5:3'}),
        Track('lyre', 46, 100, pan=16, velocity=100, lo='D5', hi='D6',
              parts={'A': 'D5:0.5 E5:0.5 F#5:0.5 G#5:0.5 A5:0.5 B5:0.5 C#6:0.5 D6:2.5'}),
        Track('square', 81, 40, pan=-24, velocity=88, gate=0.9, lo='A3', hi='A4', parts={'A': 'A3:1 D4:1 F#4:1 A4:3'}),
        Track('bass', 92, 60, velocity=100, lo='D2', hi='D3', parts={'A': 'D2:1 r:2 D3:3'}),
        Track('kymbala', 0, 70, velocity=90, kit=FRAME_KIT, parts={'A': 'tri:6'}),
    ])

# Obtain item: the syrinx finds it (G Greek Lydian), the lyre rolls a cadence IV-V-I.
OBTAIN_ITEM = one_shot(
    'mus_ichor_obtain_item', 'Obtain Item', (3, 4), 150, [('A', 2)], {'*': pcs('G', IONIAN)}, {'A': ['G', 'C']},
    target=(2.0, 2.8), song_id='MUS_OBTAIN_ITEM', ref=('MUS_OBTAIN_ITEM', -24.7), volume=90, tracks=[
        Track('syrinx', 73, 100, pan=-8, velocity=104, lo='D5', hi='D6',
              parts={'A': 'D5:1 G5:1 A5:1 B5:2 D6:1 | C6:1 A5:0.5 B5:0.5 G5:4'}),
        Track('lyre', 46, 92, pan=18, velocity=96, lo='G3', hi='G5',
              parts={'A': 'G3:1 D4:1 G4:1 B4:1 D5:1 G5:1 | C4:1 E4:0.5 G4:0.5 D4:1 B4:3'}),
        Track('bass', 92, 60, velocity=100, lo='G2', hi='D3', parts={'A': 'G2:6 | C3:2 D3:1 G2:3'}),
        Track('kymbala', 0, 66, velocity=90, kit=FRAME_KIT, parts={'A': 'tri:6 | r:3 tri:3'}),
    ])

# Obtain key item (new slot): weightier, C Greek Lydian, horns and timpani under the call.
OBTAIN_KEY_ITEM = one_shot(
    'mus_ichor_obtain_key_item', 'Obtain Key Item', (4, 4), 128, [('A', 2)], {'*': pcs('C', IONIAN)},
    {'A': ['C', 'F']}, target=(3.4, 4.0), song_id='MUS_ICHOR_OBTAIN_KEY_ITEM',
    ref=('MUS_RG_OBTAIN_KEY_ITEM', -26.9), tracks=[
        Track('salpinx', 56, 96, pan=-8, velocity=104, gate=0.9, lo='G4', hi='G5',
              parts={'A': 'G4:2 C5:1 D5:1 E5:3 G5:1 | F5:2 D5:1 B4:1 C5:4'}),
        Track('horn', 60, 84, pan=16, velocity=96, gate=0.9, lo='C4', hi='A4',
              parts={'A': 'C4:2 E4:2 G4:4 | A4:2 G4:2 E4:4'}),
        Track('lyre', 46, 84, pan=-22, velocity=92, lo='C4', hi='G5',
              parts={'A': 'C4:1 G4:1 C5:1 E5:1 G5:1 E5:1 C5:1 G4:1 | F4:1 A4:1 C5:1 G4:1 E4:0.5 G4:0.5 C5:3'}),
        Track('timpani', 47, 86, pan=8, velocity=100, gate=0.6, lo='G2', hi='C3',
              parts={'A': 'C3:2 r:2 C3:1 C3:1 G2:2 | C3:2 G2:2 C3:4'}),
        Track('bass', 92, 60, velocity=100, lo='C2', hi='G2', parts={'A': 'C2:8 | F2:2 G2:2 C2:4'}),
        Track('kymbala', 0, 66, velocity=90, kit=FRAME_KIT, parts={'A': 'cym:8 | r:4 tri:4'}),
    ])

# Obtain TM: a technique learned, A Greek Phrygian (Dorian F#), aulos over a kithara roll.
OBTAIN_TMHM = one_shot(
    'mus_ichor_obtain_tmhm', 'Obtain TM', (4, 4), 150, [('A', 2)], {'*': pcs('A', DORIAN)},
    {'A': ['Am', 'D']}, target=(3.0, 3.4), song_id='MUS_OBTAIN_TMHM', ref=('MUS_OBTAIN_TMHM', -20.4), volume=127, tracks=[
        Track('aulos', 68, 120, pan=-8, velocity=104, lo='A4', hi='A5', vibrato=(4, 50, 12),
              parts={'A': 'A4:1 C5:1 E5:1 F#5:1 G5:2 E5:2 | G5:1 F#5:1 D5:1 E5:1 A5:4'}),
        Track('square', 82, 44, pan=8, velocity=92, gate=0.9, lo='A3', hi='A4',
              parts={'A': 'A3:1 C4:1 E4:1 F#4:1 G4:2 E4:2 | G4:1 F#4:1 D4:1 E4:1 A4:4'}),
        Track('kithara', 24, 100, pan=22, velocity=92, lo='A3', hi='C5',
              parts={'A': 'A3:1 E4:1 A4:1 C5:1 A3:1 E4:1 A4:1 C5:1 | D4:1 F#4:1 A4:1 B4:1 E4:1 A4:1 C5:2'}),
        Track('bass', 87, 60, velocity=100, gate=0.8, lo='A2', hi='D3', parts={'A': 'A2:8 | D3:4 A2:4'}),
        Track('frame drum', 0, 100, velocity=96, kit=FRAME_KIT,
              parts={'A': 'dum:2 tek:1 tek:1 dum:2 tek:2 | dum:2 tek:1 tek:1 low:1 low:1 dum+cym:2'}),
    ])

# Heal: the Asclepeion's own mode, F Hypolydian; the lyre's B natural lifts and settles.
HEAL = one_shot(
    'mus_ichor_heal', 'Heal', (4, 4), 100, [('A', 1)], {'*': pcs('F', LYDIAN)}, {'A': ['F']},
    target=(2.2, 2.6), song_id='MUS_HEAL', ref=('MUS_HEAL', -28.1), volume=72, tracks=[
        Track('lyre', 46, 100, pan=-10, velocity=100, lo='C5', hi='C6',
              parts={'A': 'C5:0.5 F5:0.5 A5:0.5 C6:0.5 B5:1 G5:1 A5:4'}),
        Track('syrinx', 73, 84, pan=12, velocity=92, lo='E5', hi='G5', vibrato=(3, 40, 16),
              parts={'A': 'r:2 G5:1 E5:1 F5:4'}),
        Track('strings', 48, 50, pan=-24, velocity=76, lo='A3', hi='A3', parts={'A': 'A3:8'}),
        Track('bass', 92, 56, velocity=96, lo='F2', hi='G2', parts={'A': 'F2:2 G2:2 F2:4'}),
        Track('kymbala', 0, 60, velocity=80, kit=FRAME_KIT, parts={'A': 'tri:8'}),
    ])

# Badge (the Laurel): D Greek Lydian, the call lifting through C major (bVII) to a held D
# crowned by the chorus, a harp sweep and a timpani roll.
OBTAIN_BADGE = one_shot(
    'mus_ichor_obtain_badge', 'Obtain Laurel', (4, 4), 132, [('A', 3)], {'*': pcs('D', IONIAN) | {0}},
    {'A': ['D', 'G C', 'D']}, target=(5.0, 5.7), song_id='MUS_OBTAIN_BADGE', ref=('MUS_OBTAIN_BADGE', -20.2),
    volume=127, tracks=[
        Track('salpinx', 56, 116, pan=-8, velocity=108, gate=0.9, lo='A4', hi='A5',
              parts={'A': 'D5:1 D5:1 D5:1 A4:1 D5:2 F#5:2 | G5:2 A5:1 G5:1 E5:2 C5:2 | F#5:2 A5:6'}),
        Track('horn', 60, 86, pan=18, velocity=96, gate=0.9, lo='D4', hi='G4',
              parts={'A': 'D4:4 F#4:4 | G4:4 E4:4 | r:8'}),
        Track('chorus', 52, 86, pan=-16, velocity=96, lo='D5', hi='D5', parts={'A': 'r:8 | r:8 | D5:8'}),
        Track('lyre', 46, 84, pan=-26, velocity=92, lo='D4', hi='D6',
              parts={'A': 'r:8 | r:8 | D4:0.5 F#4:0.5 A4:0.5 D5:0.5 F#5:0.5 A5:0.5 D6:1 r:4'}),
        Track('timpani', 47, 88, pan=8, velocity=100, gate=0.6, lo='G2', hi='D3',
              parts={'A': 'D3:1 D3:1 D3:1 A2:1 D3:2 A2:2 | G2:2 r:2 C3:2 r:2 | ' + roll('D3', 8)}),
        Track('bass', 92, 60, velocity=100, lo='D2', hi='C3', parts={'A': 'D2:8 | G2:4 C3:4 | D2:8'}),
        Track('drums', 0, 88, velocity=100, kit=FRAME_KIT, parts={
            'A': 'deep+crash:2 r:2 snare:1 snare:1 snare:2 | deep:2 snare:2 deep:2 snare:1 snare:1 | crash:8'}),
    ])

# Evolved (also the "Gotcha!" jingle when a ball holds, as in Emerald): A Greek Lydian,
# the flute climbing to C#6 and resolving IV-V-I.
EVOLVED = one_shot(
    'mus_ichor_evolved', 'Evolved', (4, 4), 132, [('A', 2)], {'*': pcs('A', IONIAN)}, {'A': ['A', 'D E']},
    target=(3.2, 3.8), song_id='MUS_EVOLVED', ref=('MUS_EVOLVED', -22.8), volume=110, tracks=[
        Track('syrinx', 73, 100, pan=-8, velocity=104, lo='E5', hi='D6', vibrato=(3, 44, 12),
              parts={'A': 'E5:1 A5:1 B5:1 C#6:3 B5:1 C#6:1 | D6:2 B5:1 G#5:1 A5:4'}),
        Track('salpinx', 56, 92, pan=14, velocity=100, gate=0.9, lo='A4', hi='F#5',
              parts={'A': 'A4:2 C#5:2 E5:4 | F#5:2 E5:2 C#5:4'}),
        Track('lyre', 46, 86, pan=-22, velocity=92, lo='A3', hi='A5',
              parts={'A': 'A3:1 E4:1 A4:1 C#5:1 E5:1 A5:1 E5:1 C#5:1 | D4:1 F#4:1 E4:1 G#4:1 A4:4'}),
        Track('bass', 92, 60, velocity=100, lo='A2', hi='E3', parts={'A': 'A2:8 | D3:2 E3:2 A2:4'}),
        Track('kymbala', 0, 66, velocity=90, kit=FRAME_KIT, parts={'A': 'tri:8 | r:4 tri:4'}),
    ])

# Evolution intro (a one-second SE before the evolution music): the harp stacks
# Pythagorean fifths, C-G-D-A-E, over a chorus breath.
EVOLUTION_INTRO = one_shot(
    'mus_ichor_evolution_intro', 'Evolution Intro', (5, 8), 150, [('A', 1)], {'*': pcs('C', IONIAN)}, {'A': ['C']},
    target=(0.9, 1.1), song_id='MUS_EVOLUTION_INTRO', ref=('MUS_EVOLUTION_INTRO', -25.8), fanfare=False,
    priority=0, volume=110, tracks=[
        Track('lyre', 46, 100, velocity=100, lo='C4', hi='E6', parts={'A': 'C4:0.5 G4:0.5 D5:0.5 A5:0.5 E6:0.5 r:2.5'}),
        Track('chorus', 52, 80, pan=-12, velocity=90, lo='E5', hi='E5', parts={'A': 'E5:5'}),
        Track('kymbala', 0, 60, velocity=80, kit=FRAME_KIT, parts={'A': 'tri:5'}),
    ])

# Obtain a Pokemon (new slot; the starter): F Greek Lydian, the call (C-F-G-A) on the
# syrinx with the aulos a third under it, landing warmly on F.
OBTAIN_MON = one_shot(
    'mus_ichor_obtain_mon', 'Obtain Pokemon', (4, 4), 132, [('A', 2)], {'*': pcs('F', IONIAN)},
    {'A': ['F', 'Bb C']}, target=(3.2, 3.8), song_id='MUS_ICHOR_OBTAIN_MON', ref=('MUS_OBTAIN_ITEM', -24.7),
    tracks=[
        Track('syrinx', 73, 100, pan=-8, velocity=104, lo='C5', hi='C6', vibrato=(3, 44, 12),
              parts={'A': 'C5:2 F5:1 G5:1 A5:3 C6:1 | Bb5:2 G5:1 E5:1 F5:4'}),
        Track('aulos', 68, 86, pan=14, velocity=96, lo='A4', hi='A5', vibrato=(4, 44, 12),
              parts={'A': 'A4:2 C5:1 E5:1 F5:3 A5:1 | G5:2 E5:1 C5:1 A4:4'}),
        Track('lyre', 46, 86, pan=-22, velocity=92, lo='F3', hi='F5',
              parts={'A': 'F3:1 C4:1 F4:1 A4:1 C5:1 F5:1 C5:1 A4:1 | Bb3:1 D4:1 F4:1 C4:1 F3:4'}),
        Track('bass', 92, 60, velocity=100, lo='F2', hi='C3', parts={'A': 'F2:8 | Bb2:2 C3:2 F2:4'}),
        Track('frame drum', 0, 80, velocity=96, kit=FRAME_KIT,
              parts={'A': 'dum:2 tek:1 tek:1 dum:2 tek:2 | dum:2 tek:2 tri:4'}),
    ])

# ============================================================ evolution and caught
# Evolution: D Hypodorian (Aeolian) with Eb (the Phrygian bII) at the turn. A harp
# ostinato and a heartbeat timpani under a chorus that climbs a step every bar, D to
# A, and sinks to E, which leans back into the loop's D.
EV_CH = {'intro': ['Dm', 'Dm'], 'A': ['Dm', 'Dm', 'Bb', 'Bb', 'Gm', 'C', 'Eb', 'Dm']}


def ev_harp(c):
    r, t, f = triad(c, 50)
    return notes([(r, 1), (f, 1), (r + 12, 1), (t + 12, 1), (f + 12, 1), (t + 12, 1), (r + 12, 1), (f, 1)])


EVOLUTION = Song(
    name='mus_ichor_evolution', title='Evolution', meter=(4, 4), grouping=(2, 2, 2, 2), tempo=120,
    voicegroup=VG, volume=120, reverb=50, priority=0, sections=[('intro', 2), ('A', 8)], loop_from='A',
    modes={'*': pcs('D', AEOLIAN) | {3}}, target=(14, 18), chords=EV_CH, song_id='MUS_EVOLUTION',
    ref=('MUS_EVOLUTION', -22.3), tracks=[
        Track('lyre', 46, 96, pan=-14, velocity=96, lo='C3', hi='A5', parts={s: gen(c, ev_harp) for s, c in EV_CH.items()}),
        Track('chorus', 52, 92, pan=10, velocity=96, lo='D5', hi='A5',
              parts={'A': 'D5:8 | E5:8 | F5:8 | G5:8 | A5:8 | G5:8 | G5:4 F5:4 | E5:8'}),
        Track('strings', 48, 60, pan=24, velocity=84, gate=0.5, lo='D4', hi='C5',
              parts={'A': gen(EV_CH['A'], lambda c: notes([(triad(c, 62)[0], 1)] * 8))}),
        Track('timpani', 47, 84, velocity=100, gate=0.5, lo='D3', hi='D3',
              parts={s: bars('D3:1 D3:1 r:6', n) for s, n in (('intro', 2), ('A', 8))}),
        Track('bass', 92, 56, velocity=96, lo='D2', hi='D2', parts={s: bars('D2:8', n) for s, n in (('intro', 2), ('A', 8))}),
    ])

# Caught: C Greek Lydian in a bouncing 6/8, syrinx and lyre in parallel thirds over the
# kithara and krotala. Its last bar (G) falls to the C that opens the loop.
CA_CH = {'intro': ['C'], 'A': ['C', 'F', 'G', 'C', 'Am', 'Dm', 'G', 'C', 'F', 'C', 'Dm', 'G']}
C_LYD = pcs('C', IONIAN)
CA_TUNE = ('E5:2 G5:1 C6:2 G5:1 | A5:2 C6:1 A5:2 F5:1 | G5:2 B5:1 D6:2 B5:1 | C6:3 G5:3 | '
           'A5:2 G5:1 E5:2 C5:1 | D5:2 F5:1 A5:2 F5:1 | G5:1 A5:1 B5:1 D6:2 B5:1 | C6:3 E5:3 | '
           'F5:2 A5:1 C6:2 A5:1 | G5:2 E5:1 C5:2 E5:1 | F5:2 E5:1 D5:2 F5:1 | B5:2 A5:1 G5:2 F5:1')
CAUGHT = Song(
    name='mus_ichor_caught', title='Caught', meter=(6, 8), grouping=(3, 3), tempo=144,
    voicegroup=VG, volume=106, reverb=50, priority=0, sections=[('intro', 1), ('A', 12)], loop_from='A',
    modes={'*': C_LYD}, target=(13, 17), chords=CA_CH, song_id='MUS_CAUGHT', ref=('MUS_CAUGHT', -22.5), tracks=[
        Track('syrinx', 73, 98, pan=-10, velocity=100, lo='C5', hi='D6', vibrato=(3, 44, 12),
              parts={'intro': 'C5:1 E5:1 G5:1 C6:3', 'A': CA_TUNE}),
        Track('lyre', 46, 90, pan=16, velocity=96, lo='G4', hi='B5', parts={'A': diatonic(CA_TUNE, C_LYD, -2)}),
        Track('kithara', 24, 80, pan=24, velocity=88, gate=0.5, lo='G3', hi='C5',
              parts={s: gen(c, offbeats([(0, 1), (1, 1), (1, 1), (0, 1), (1, 1), (1, 1)])) for s, c in CA_CH.items()}),
        Track('bass', 92, 64, velocity=100, gate=0.9, lo='C2', hi='C4',
              parts={s: gen(c, root_fifth([('r', 3), ('f', 3)], 36)) for s, c in CA_CH.items()}),
        Track('frame drum', 0, 86, velocity=96, kit=FRAME_KIT, parts={
            'intro': 'dum:3 tek:1 tek:1 tek:1',
            'A': bars('dum:2 kro:1 tek:2 kro:1', 12, 'dum:1 tek:1 tek:1 dum:1 tek:1 tek:1')}),
    ])

# ============================================================ victories
HASAPIKO_BASS = root_fifth([('r', 2), (None, 2), ('f', 2), (None, 2)], 36)
HASAPIKO_KITHARA = offbeats([(0, 2), (1, 2), (0, 2), (1, 2)])
VICTORY_FILL = 'dum:2 tek:1 tek:1 dum:1 tek:1 low:1 low:1'

# Wild victory: G Greek Lydian, a short syrinx flourish then an 8-bar dance over lyre
# arpeggios. The last bar climbs G-A into the loop's B.
VW_CH = {'intro': ['G'], 'A': ['G', 'C', 'G', 'D', 'Em', 'C', 'D', 'G']}
VICTORY_WILD = Song(
    name='mus_ichor_victory_wild', title='Wild Victory', meter=(4, 4), grouping=(2, 2, 2, 2), tempo=144,
    voicegroup=VG, volume=106, reverb=50, priority=0, sections=[('intro', 1), ('A', 8)], loop_from='A',
    modes={'*': pcs('G', IONIAN)}, target=(12, 15), chords=VW_CH, song_id='MUS_VICTORY_WILD',
    ref=('MUS_VICTORY_WILD', -22.4), tracks=[
        Track('syrinx', 73, 100, pan=-8, velocity=100, lo='C5', hi='D6', vibrato=(3, 44, 12), parts={
            'intro': 'D5:0.5 G5:0.5 B5:1 A5:1 B5:1 D6:4',
            'A': 'B5:2 A5:1 G5:1 D5:2 G5:2 | E5:2 G5:1 E5:1 C5:2 E5:2 | D5:2 G5:1 B5:1 D6:2 B5:2 | '
                 'A5:2 F#5:1 E5:1 D5:4 | E5:1 F#5:1 G5:2 B5:2 G5:2 | C6:2 B5:1 A5:1 G5:2 E5:2 | '
                 'D5:1 E5:1 F#5:1 G5:1 A5:2 F#5:2 | G5:5 F#5:1 G5:1 A5:1'}),
        Track('lyre', 46, 84, pan=-24, velocity=90, lo='G3', hi='B5', parts={
            'intro': 'G3:1 B3:1 D4:1 G4:1 B4:1 D5:1 G5:2', 'A': gen(VW_CH['A'], ak_harp)}),
        Track('kithara', 24, 78, pan=24, velocity=88, gate=0.6, lo='G3', hi='C5',
              parts={'A': gen(VW_CH['A'], HASAPIKO_KITHARA)}),
        Track('bass', 92, 62, velocity=100, gate=0.9, lo='C2', hi='C4',
              parts={s: gen(c, HASAPIKO_BASS) for s, c in VW_CH.items()}),
        Track('frame drum', 0, 88, velocity=96, kit=FRAME_KIT, parts={
            'intro': 'dum+cym:2 r:2 tek:1 tek:1 tek:2', 'A': bars('dum:2 tek:2 dum:2 tam:2', 8, VICTORY_FILL)}),
    ])

# The Laurel won (a Hierophant): F Greek Lydian, a fanfare lifting through Eb (bVII) to
# C, then a processional: salpinx in A, syrinx and chorus in B, chorus and salpinx
# together in A2. B's last bar is C, which falls to the loop's F.
VL_CH = {'intro': ['F', 'Eb', 'C'], 'A': ['F', 'Bb', 'F', 'C', 'Dm', 'Bb', 'C', 'F'],
         'B': ['Bb', 'F', 'Gm', 'Dm', 'Bb', 'F', 'Gm', 'C']}
VL_CH['A2'] = VL_CH['A']
VL_TUNE = ('C5:2 F5:2 A5:3 G5:1 | F5:2 D5:2 Bb4:4 | A4:2 C5:2 F5:3 E5:1 | G5:4 E5:2 C5:2 | '
           'D5:2 F5:2 A5:3 G5:1 | F5:2 G5:1 F5:1 D5:4 | C5:2 D5:1 E5:1 G5:2 E5:2 | F5:6 C5:2')
VL_BAR = 'deep:2 tek:2 dum:2 tek:1 tek:1'
VICTORY_LAUREL = Song(
    name='mus_ichor_victory_laurel', title='Laurel Victory', meter=(4, 4), grouping=(2, 2, 2, 2), tempo=144,
    voicegroup=VG, volume=113, reverb=50, priority=0,
    sections=[('intro', 3), ('A', 8), ('B', 8), ('A2', 8)], loop_from='A',
    modes={'*': pcs('F', IONIAN), 'intro': pcs('F', IONIAN) | {3}}, target=(38, 42), chords=VL_CH,
    song_id='MUS_VICTORY_GYM_LEADER', ref=('MUS_VICTORY_GYM_LEADER', -22.2), tracks=[
        Track('salpinx', 56, 100, pan=-8, velocity=106, gate=0.9, lo='A4', hi='A5', parts={
            'intro': 'C5:1 C5:1 C5:1 F5:1 A5:4 | G5:2 F5:1 Eb5:1 Bb4:4 | C5:2 E5:2 G5:4',
            'A': VL_TUNE, 'A2': VL_TUNE}),
        Track('horn', 60, 84, pan=18, velocity=96, gate=0.9, lo='E4', hi='A4',
              parts={'intro': 'F4:4 A4:4 | G4:4 F4:4 | E4:8'}),
        Track('syrinx', 73, 96, pan=12, velocity=100, lo='C5', hi='D6', vibrato=(3, 44, 12), parts={
            'B': 'D6:3 C6:1 Bb5:2 F5:2 | A5:3 G5:1 F5:2 C5:2 | D5:2 G5:2 Bb5:3 A5:1 | A5:4 F5:4 | '
                 'Bb5:2 D6:2 C6:3 Bb5:1 | A5:2 C6:2 F5:4 | G5:2 Bb5:2 D6:2 Bb5:2 | C6:2 Bb5:1 A5:1 G5:2 E5:2'}),
        Track('chorus', 52, 84, pan=-18, velocity=96, lo='G4', hi='A5', parts={
            'intro': 'r:8 | r:8 | G4:8', 'B': 'F5:8 | C5:8 | D5:8 | D5:8 | F5:8 | C5:8 | D5:8 | E5:8',
            'A2': VL_TUNE}),
        Track('lyre', 46, 82, pan=-26, velocity=90, lo='G3', hi='C6', parts={
            'intro': 'r:8 | r:8 | C4:0.5 E4:0.5 G4:0.5 C5:0.5 E5:0.5 G5:0.5 C6:1 r:4',
            'A': gen(VL_CH['A'], ak_harp)}),
        Track('kithara', 24, 78, pan=24, velocity=88, gate=0.6, lo='G3', hi='C5',
              parts={s: gen(VL_CH[s], HASAPIKO_KITHARA) for s in ('A', 'B', 'A2')}),
        Track('bass', 92, 62, velocity=100, gate=0.9, lo='C2', hi='C4',
              parts={s: gen(VL_CH[s], HASAPIKO_BASS) for s in ('A', 'B', 'A2')}),
        Track('timpani', 47, 86, pan=8, velocity=100, gate=0.6, lo='F2', hi='C3',
              parts={'intro': 'F2:1 F2:1 F2:1 C3:1 F2:4 | r:8 | ' + roll('C3', 8)}),
        Track('drums', 0, 88, velocity=100, kit=FRAME_KIT, parts={
            'intro': 'deep+crash:2 r:2 snare:1 snare:1 snare:2 | deep:2 snare:2 deep:2 snare:1 snare:1 | '
                     'deep:1 snare:1 snare:1 snare:1 snare:1 snare:1 snare:1 snare:1',
            'A': bars(VL_BAR, 8, VICTORY_FILL), 'B': bars(VL_BAR, 8, VICTORY_FILL),
            'A2': 'deep+crash:2 tek:2 dum:2 tek:1 tek:1 | ' + bars(VL_BAR, 7, VICTORY_FILL)}),
        Track('square', 80, 40, pan=30, velocity=88, gate=0.9, lo='A3', hi='A4', parts={'A2': octave(VL_TUNE, -1)}),
    ])

# Titanborn beaten: the Titan call (B-F, the tritone) sounds once more, then its B turns
# into the bright dominant of E, and the loop dances in E Greek Lydian.
VT_CH = {'intro': ['Bdim', 'B'], 'A': ['E', 'A', 'E', 'B', 'C#m', 'A', 'B', 'E']}
SYRTOS_KITHARA = offbeats([(0, 3), (1, 1), (1, 2), (1, 2)])
VICTORY_TITAN = Song(
    name='mus_ichor_victory_titan', title='Titan Victory', meter=(4, 4), grouping=(3, 1, 2, 2), tempo=144,
    voicegroup=VG, volume=88, reverb=50, priority=0, sections=[('intro', 2), ('A', 8)], loop_from='A',
    modes={'*': pcs('E', IONIAN), 'intro': B_GMIX | {3, 6}}, target=(12, 15), chords=VT_CH,
    song_id='MUS_VICTORY_AQUA_MAGMA', ref=('MUS_VICTORY_AQUA_MAGMA', -23.7), tracks=[
        Track('salpinx', 56, 100, pan=-8, velocity=106, gate=0.9, lo='B4', hi='F#5',
              parts={'intro': 'B4:2 F5:4 E5:2 | B4:2 D#5:2 F#5:4'}),
        Track('tuba', 58, 92, velocity=104, gate=0.8, lo='B1', hi='C2', parts={'intro': 'B1:2 B1:1 C2:1 B1:2 C2:2 | B1:8'}),
        Track('syrinx', 73, 98, pan=-10, velocity=100, lo='B4', hi='C#6', vibrato=(3, 44, 12), parts={
            'A': 'G#5:2 B5:2 E5:2 G#5:2 | A5:2 C#6:2 E5:2 A5:2 | G#5:1 A5:1 B5:2 C#6:2 B5:2 | F#5:2 D#5:2 B4:4 | '
                 'C#5:2 E5:2 G#5:2 C#6:2 | A5:3 G#5:1 F#5:2 E5:2 | D#5:2 F#5:2 B5:4 | E5:4 G#5:2 F#5:2'}),
        Track('horn', 60, 76, pan=18, velocity=92, gate=0.9, lo='F#4', hi='C#5',
              parts={'A': 'B4:8 | C#5:8 | B4:8 | B4:8 | G#4:8 | A4:8 | F#4:8 | G#4:8'}),
        Track('kithara', 24, 78, pan=24, velocity=88, gate=0.6, lo='G3', hi='C5', parts={'A': gen(VT_CH['A'], SYRTOS_KITHARA)}),
        Track('bass', 92, 62, velocity=100, gate=0.9, lo='C2', hi='C4',
              parts={'A': gen(VT_CH['A'], root_fifth([('r', 3), (None, 1), ('f', 2), ('r', 2)], 36))}),
        Track('timpani', 47, 86, pan=8, velocity=100, gate=0.6, lo='B2', hi='B2', parts={'intro': 'B2:2 r:4 B2:2 | ' + roll('B2', 8)}),
        Track('drums', 0, 88, velocity=100, kit=FRAME_KIT, parts={
            'intro': 'deep:2 snare:2 deep:2 snare:2 | deep+crash:8',
            'A': bars('dum:3 tek:1 dum:2 tek:2', 8, 'dum:3 tek:1 tek:1 tek:1 low:1 low:1')}),
    ])

# ============================================================ trainer encounter themes
# These play from the moment a trainer spots you until the battle starts, so each opens
# at once (a one-bar intro at most) and loops in 12 to 16 seconds.

# Lads (Shepherds, Acolytes): C Greek Hypophrygian (Mixolydian, Bb), a cocky aulos in a
# fast hasapiko. Its last bar walks down to the G that opens the loop.
EM_CH = {'intro': ['C'], 'A': ['C', 'C', 'Bb', 'C', 'F', 'Bb', 'Gm', 'C']}
EM_TUNE = ('G4:1 C5:1 E5:1 G5:1 F5:1 E5:1 D5:1 E5:1 | C5:2 G4:2 C5:1 D5:1 E5:2 | F5:1 D5:1 Bb4:1 D5:1 F5:2 D5:2 | '
           'E5:1 G5:1 E5:1 C5:1 G4:4 | A4:1 C5:1 F5:1 A5:1 G5:1 F5:1 E5:1 F5:1 | D5:2 Bb4:2 C5:1 D5:1 F5:2 | '
           'G5:1 F5:1 D5:1 Bb4:1 G4:2 Bb4:2 | C5:2 E5:2 D5:1 C5:1 Bb4:1 A4:1')
HASAPISERVIKO_KITHARA = offbeats([(0, 1), (1, 1)] * 4)
ENCOUNTER_MALE = Song(
    name='mus_ichor_encounter_male', title='Encounter: Lad', meter=(4, 4), grouping=(2, 2, 2, 2), tempo=144,
    voicegroup=VG, volume=127, reverb=50, priority=0, sections=[('intro', 1), ('A', 8)], loop_from='A',
    modes={'*': pcs('C', MIXOLYDIAN)}, target=(12, 15), chords=EM_CH, song_id='MUS_ENCOUNTER_MALE',
    ref=('MUS_ENCOUNTER_MALE', -21.6), tracks=[
        Track('aulos', 68, 104, pan=-6, velocity=104, lo='G4', hi='A5', vibrato=(4, 50, 12), parts={'A': EM_TUNE}),
        Track('square', 80, 42, pan=10, velocity=88, gate=0.8, lo='G3', hi='A4', parts={'A': octave(EM_TUNE, -1)}),
        Track('kithara', 24, 80, pan=24, velocity=90, gate=0.5, lo='G3', hi='C5',
              parts={s: gen(c, HASAPISERVIKO_KITHARA) for s, c in EM_CH.items()}),
        Track('bass', 87, 80, velocity=104, gate=0.7, lo='C2', hi='C4',
              parts={s: gen(c, root_fifth([('r', 1), (None, 1), ('f', 1), (None, 1)] * 2, 36)) for s, c in EM_CH.items()}),
        Track('frame drum', 0, 90, velocity=96, kit=FRAME_KIT, parts={
            'intro': 'dum:1 tek:1 tek:1 tek:1 dum:1 tek:1 low:1 low:1',
            'A': bars('dum:1 tek:1 low:1 tek:1 dum:1 tek:1 low:1 tam:1', 8,
                      'dum:1 tek:1 tek:1 tek:1 dum:1 dum:1 tek:1 tek:1')}),
    ])

# Maidens (Harvesters, Acolytes, Hierophants): Bb Hypolydian (Lydian, E natural), a
# graceful 3/4 for the syrinx over harp. It ends on C, the Lydian II, which falls
# back to Bb.
EF_CH = {'intro': ['Bb'], 'A': ['Bb', 'C', 'Bb', 'F', 'Gm', 'C', 'Dm', 'C']}


def ef_harp(c):
    r, t, f = triad(c, 55)
    return notes([(r, 1), (t, 1), (f, 1), (r + 12, 1), (f, 1), (t, 1)])


ENCOUNTER_FEMALE = Song(
    name='mus_ichor_encounter_female', title='Encounter: Maiden', meter=(3, 4), grouping=(2, 2, 2), tempo=120,
    voicegroup=VG, volume=113, reverb=50, priority=0, sections=[('intro', 1), ('A', 8)], loop_from='A',
    modes={'*': pcs('Bb', LYDIAN)}, target=(10, 14), chords=EF_CH, song_id='MUS_ENCOUNTER_FEMALE',
    ref=('MUS_ENCOUNTER_FEMALE', -23.1), tracks=[
        Track('syrinx', 73, 100, pan=-8, velocity=100, lo='D5', hi='D6', vibrato=(3, 40, 14), parts={
            'A': 'F5:2 Bb5:2 A5:1 G5:1 | E5:3 F5:1 G5:2 | D5:2 F5:2 Bb5:2 | A5:4 F5:2 | '
                 'G5:2 Bb5:2 D6:2 | C6:3 Bb5:1 A5:1 G5:1 | F5:2 D5:2 A5:2 | G5:4 E5:2'}),
        Track('lyre', 46, 88, pan=18, velocity=92, lo='G3', hi='F5', parts={s: gen(c, ef_harp) for s, c in EF_CH.items()}),
        Track('strings', 48, 50, pan=-24, velocity=76, lo='A3', hi='A4',
              parts={'A': gen(EF_CH['A'], lambda c: notes([(triad(c, 55)[1], 6)]))}),
        Track('bass', 92, 60, velocity=96, lo='C2', hi='C4',
              parts={s: gen(c, root_fifth([('r', 4), ('f', 2)], 41)) for s, c in EF_CH.items()}),
        Track('kymbala', 0, 62, velocity=80, kit=FRAME_KIT, parts={'intro': 'tri:6_', 'A': bars('tri:6_ | r:6', 4)}),
    ])

# Hoplites: the pyrrhic war dance in a quick 2/4, A Greek Dorian (A Phrygian, Bb), the
# salpinx over war drums and a sawing string ostinato.
EI_CH = {'intro': ['Am'], 'A': ['Am', 'Dm', 'Am', 'Am', 'C', 'F', 'C', 'Am', 'Dm', 'Am', 'Gm', 'Am', 'Dm', 'Bb', 'Gm', 'Am']}
A_GDOR = pcs('A', PHRYGIAN)


def ei_strings(c):
    r = triad(c, 57)[0]
    return notes([(r, 1), (r, 1), (step(r, A_GDOR, 1), 1), (r, 1)])


EI_TUNE = ('A4:1 A4:1 E5:2 | D5:1 E5:1 F5:2 | E5:1 D5:1 C5:1 Bb4:1 | A4:4 | C5:1 C5:1 G5:2 | F5:1 G5:1 A5:2 | '
           'G5:1 F5:1 E5:1 D5:1 | E5:4 | F5:1 E5:1 D5:2 | E5:1 D5:1 C5:2 | D5:1 C5:1 Bb4:2 | A4:2 E5:2 | '
           'F5:1 F5:1 E5:1 D5:1 | E5:2 Bb4:2 | C5:1 Bb4:1 A4:1 Bb4:1 | A4:4')
ENCOUNTER_INTENSE = Song(
    name='mus_ichor_encounter_intense', title='Encounter: Hoplite', meter=(2, 4), grouping=(2, 2), tempo=160,
    voicegroup=VG, volume=100, reverb=50, priority=0, sections=[('intro', 1), ('A', 16)], loop_from='A',
    modes={'*': A_GDOR}, target=(10, 14), chords=EI_CH, song_id='MUS_ENCOUNTER_INTENSE',
    ref=('MUS_ENCOUNTER_INTENSE', -21.9), tracks=[
        Track('salpinx', 56, 100, pan=-8, velocity=106, gate=0.85, lo='A4', hi='A5', parts={'A': EI_TUNE}),
        Track('square', 80, 42, pan=10, velocity=88, gate=0.85, lo='A3', hi='A4', parts={'A': octave(EI_TUNE, -1)}),
        Track('strings', 48, 78, pan=24, velocity=92, gate=0.8, lo='G3', hi='A4', parts={'A': gen(EI_CH['A'], ei_strings)}),
        Track('bass', 87, 80, velocity=104, gate=0.7, lo='E2', hi='E4',
              parts={s: gen(c, root_fifth([('r', 1), ('r', 1), ('o', 1), ('r', 1)], 40)) for s, c in EI_CH.items()}),
        Track('drums', 0, 92, velocity=100, kit=FRAME_KIT, parts={
            'intro': 'taiko:1 taiko:1 snare:1 snare:1',
            'A': 'taiko+crash:1 snare:1 deep:1 snare:1 | ' + bars('taiko:1 snare:1 deep:1 snare:1', 6)
                 + ' | snare:1 snare:1 snare:1 snare:1 | ' + bars('taiko:1 snare:1 deep:1 snare:1', 7)
                 + ' | snare:1 snare:1 snare:1 snare:1'}),
    ])

# Augurs: the chromatic genus on both of D's tetrachords (D-Eb-E-G, A-Bb-B-D), creeping
# pizzicato and an aulos that slides between the semitones, over a low D drone (ison).
D_CHROM = pcs('D', (0, 1, 2, 5, 7, 8, 9))
ES_PIZZ = ('D3:1 r:1 A3:1 r:1 B3:1 r:1 Bb3:1 r:1 | A3:1 r:1 E3:1 r:1 Eb3:1 r:1 D3:1 r:1 | '
           'D3:1 r:1 A3:1 r:1 B3:1 r:1 Bb3:1 r:1 | A3:1 r:1 G3:1 r:1 E3:1 r:1 Eb3:1 r:1 | '
           'G3:1 r:1 D4:1 r:1 Eb4:1 r:1 D4:1 r:1 | B3:1 r:1 Bb3:1 r:1 A3:1 r:1 G3:1 r:1 | '
           'E3:1 r:1 G3:1 r:1 A3:1 r:1 Bb3:1 r:1 | B3:1 r:1 Bb3:1 r:1 A3:1 r:1 Eb3:1 r:1')
ES_BAR = 'r:1 tek:1_ r:1 tek:1_ r:1 tek:1_ r:1 tam:1_'
ENCOUNTER_SUSPICIOUS = Song(
    name='mus_ichor_encounter_suspicious', title='Encounter: Augur', meter=(4, 4), grouping=(2, 2, 2, 2), tempo=120,
    voicegroup=VG, volume=127, reverb=50, priority=0, sections=[('intro', 1), ('A', 8)], loop_from='A',
    modes={'*': D_CHROM}, target=(14, 18), chords={'intro': ['Dm'], 'A': ['Dm'] * 8},
    song_id='MUS_ENCOUNTER_SUSPICIOUS', ref=('MUS_ENCOUNTER_SUSPICIOUS', -22.8), tracks=[
        Track('pizzicato', 45, 127, pan=-14, velocity=100, gate=0.5, lo='D3', hi='Eb4',
              parts={'intro': 'D3:1 r:1 A3:1 r:1 D3:1 r:1 A3:1 r:1', 'A': ES_PIZZ}),
        Track('aulos', 68, 127, pan=14, velocity=100, lo='D4', hi='A5', vibrato=(6, 30, 20), parts={
            'A': 'r:4 D5:1 Eb5:1 E5:2 | G5:3 E5:1 Eb5:2 D5:2 | r:4 A4:1 Bb4:1 B4:2 | D5:3 B4:1 Bb4:2 A4:2 | '
                 'r:2 G4:1 A4:1 Bb4:1 B4:1 D5:2 | Eb5:2 D5:1 B4:1 Bb4:2 A4:2 | r:2 E5:1 Eb5:1 D5:1 B4:1 A4:2 | '
                 'Bb4:1 A4:1 G4:1 E4:1 Eb4:2 D4:2'}),
        Track('ison', 92, 70, velocity=96, lo='D2', hi='D2', parts={'intro': 'D2:8', 'A': bars('D2:8', 8)}),
        Track('frame drum', 0, 104, velocity=96, kit=FRAME_KIT, parts={
            'intro': ES_BAR,
            'A': 'tri:1_ tek:1_ r:1 tek:1_ r:1 tek:1_ r:1 tam:1_ | ' + bars(ES_BAR, 3) + ' | '
                 'tri:1_ tek:1_ r:1 tek:1_ r:1 tek:1_ r:1 tam:1_ | ' + bars(ES_BAR, 3)}),
    ])

# Goatherds: A Greek Hypophrygian (Mixolydian, G natural), a shepherd's syrinx in 6/8
# over a tsabouna drone (the island bagpipe, here the accordion), with goat bells.
EH_CH = {'intro': ['A'], 'A': ['A', 'A', 'G', 'A', 'A', 'D', 'G', 'A', 'D', 'G', 'G', 'A']}
ENCOUNTER_HIKER = Song(
    name='mus_ichor_encounter_hiker', title='Encounter: Goatherd', meter=(6, 8), grouping=(3, 3), tempo=144,
    voicegroup=VG, volume=100, reverb=50, priority=0, sections=[('intro', 1), ('A', 12)], loop_from='A',
    modes={'*': pcs('A', MIXOLYDIAN)}, target=(13, 17), chords=EH_CH, song_id='MUS_ENCOUNTER_HIKER',
    ref=('MUS_ENCOUNTER_HIKER', -23.7), tracks=[
        Track('syrinx', 73, 100, pan=-8, velocity=100, lo='A4', hi='D6', vibrato=(3, 48, 10), parts={
            'A': 'E5:2 A5:1 G5:2 E5:1 | F#5:2 E5:1 D5:2 C#5:1 | D5:2 G5:1 F#5:2 D5:1 | E5:3 A4:3 | '
                 'C#5:1 E5:1 A5:1 B5:2 A5:1 | F#5:1 A5:1 D6:1 C#6:2 A5:1 | B5:2 G5:1 D5:2 B4:1 | C#5:3 E5:3 | '
                 'F#5:2 E5:1 D5:2 F#5:1 | G5:2 F#5:1 E5:2 D5:1 | D5:1 E5:1 F#5:1 G5:2 B5:1 | A5:4 G5:1 F#5:1'}),
        Track('tsabouna', 21, 66, pan=14, velocity=90, lo='A3', hi='E4',
              parts={'intro': 'A3+E4:6', 'A': bars('A3+E4:6', 12)}),
        Track('bass', 92, 58, velocity=96, gate=0.9, lo='C2', hi='C4',
              parts={s: gen(c, root_fifth([('r', 3), ('f', 3)], 40)) for s, c in EH_CH.items()}),
        Track('frame drum', 0, 84, velocity=96, kit=FRAME_KIT, parts={
            'intro': 'dum:3 tek:2 tek:1', 'A': bars('dum:2 bell:1_ tek:2 tek:1', 12, 'dum:1 tek:1 tek:1 dum:1 tek:1 tek:1')}),
    ])

# Kleon, the Lakonian (new style, "Music: Rival"; also plays for MUS_ENCOUNTER_BRENDAN
# and MAY): Spartans marched to the aulos, and Plato called Dorian the Spartan mode.
# E Greek Dorian (E Phrygian), 9/8 like his battle theme, which it quotes (E-F-E-D-E-B).
ER_CH = {'intro': ['Em'], 'A': ['Em', 'Dm', 'C', 'Em', 'Am', 'Dm', 'F', 'Em']}
ER_TUNE = ('E5:1 F5:1 E5:1 D5:1 E5:2 B4:3 | D5:1 E5:1 F5:1 E5:1 D5:2 A4:3 | C5:1 D5:1 E5:1 G5:1 F5:2 E5:3 | '
           'E5:2 B4:2 E5:2 G5:3 | A5:1 G5:1 F5:1 E5:1 A5:2 E5:3 | F5:1 E5:1 D5:1 C5:1 D5:2 A4:3 | '
           'C5:1 D5:1 F5:1 G5:1 A5:2 F5:3 | G5:2 F5:2 E5:2 F5:3')
ENCOUNTER_RIVAL = Song(
    name='mus_ichor_encounter_rival', title='Encounter: Kleon', meter=(9, 8), grouping=(2, 2, 2, 3), tempo=160,
    voicegroup=VG, volume=100, reverb=50, priority=0, sections=[('intro', 1), ('A', 8)], loop_from='A',
    modes={'*': pcs('E', PHRYGIAN)}, target=(12, 15), chords=ER_CH, song_id='MUS_ICHOR_ENCOUNTER_RIVAL',
    ref=('MUS_ENCOUNTER_BRENDAN', -23.2), tracks=[
        Track('aulos', 68, 104, pan=-6, velocity=104, lo='A4', hi='A5', vibrato=(5, 52, 16), parts={'A': ER_TUNE}),
        Track('square', 82, 46, pan=8, velocity=92, gate=0.9, lo='A3', hi='A4', parts={'A': octave(ER_TUNE, -1)}),
        Track('kithara', 24, 80, pan=24, velocity=90, gate=0.5, lo='G3', hi='C5',
              parts={s: gen(c, offbeats([(0, 2), (1, 2), (0, 2), (1, 3)])) for s, c in ER_CH.items()}),
        Track('bass', 87, 82, velocity=104, gate=0.7, lo='E2', hi='E4',
              parts={s: gen(c, root_fifth([('r', 2), ('f', 2), ('r', 2), ('o', 3)], 40)) for s, c in ER_CH.items()}),
        Track('drums', 0, 92, velocity=100, kit=FRAME_KIT, parts={
            'intro': 'deep:2 snare:2 deep:2 snare:1 snare:1 snare:1',
            'A': 'dum+crash:2 tek:2 dum:2 snare:1 tek:1 tek:1 | '
                 + bars('dum:2 tek:2 dum:2 snare:1 tek:1 tek:1', 7, 'deep:2 snare:2 deep:2 snare:1 snare:1 snare:1')}),
    ])

# Titanborn (new style, "Music: Titan"; also plays for MUS_ENCOUNTER_MAGMA): the Titan
# battle theme's riff and tritone call (B-F) in B Greek Mixolydian, the call answered
# by silence and war drums.
ET_CH = {'intro': ['Bdim'], 'A': ['Bdim', 'Bdim', 'C', 'Bdim', 'Bdim', 'Bdim', 'F', 'Bdim']}
ENCOUNTER_TITAN = Song(
    name='mus_ichor_encounter_titan', title='Encounter: Titanborn', meter=(9, 8), grouping=(3, 2, 2, 2), tempo=144,
    voicegroup=VG, volume=86, reverb=50, priority=0, sections=[('intro', 1), ('A', 8)], loop_from='A',
    modes={'*': B_GMIX}, target=(13, 17), chords=ET_CH, song_id='MUS_ICHOR_ENCOUNTER_TITAN',
    ref=('MUS_ENCOUNTER_MAGMA', -24.6), tracks=[
        Track('salpinx', 56, 100, pan=-8, velocity=106, gate=0.9, lo='B4', hi='A5', parts={
            'A': 'r:9 | B4:3 F5:4 E5:2 | r:9 | D5:3 C5:2 B4:4 | r:9 | B4:3 F5:4 G5:2 | '
                 'A5:3 G5:2 F5:2 E5:2 | F5:3 E5:2 D5:2 C5:2'}),
        Track('strings', 48, 72, pan=26, velocity=90, gate=0.8, lo='A4', hi='G5', parts={'A': gen(ET_CH['A'], ti_strings)}),
        Track('tuba', 58, 92, pan=-4, velocity=106, gate=0.8, lo='B1', hi='G2',
              parts={s: gen(c, ti_riff) for s, c in ET_CH.items()}),
        Track('bass', 87, 74, velocity=104, gate=0.7, lo='C2', hi='G3',
              parts={s: gen(c, lambda x: ti_riff(x, 1)) for s, c in ET_CH.items()}),
        Track('drums', 0, 94, velocity=100, kit=FRAME_KIT, parts={
            'intro': 'deep:3^ r:2 deep:2 r:2',
            'A': 'deep+crash:3 snare:2 taiko:2 snare:2 | '
                 + bars('deep:3 snare:2 taiko:2 snare:2', 7, 'deep:3 snare:2 snare:1 snare:1 snare:1 snare:1')}),
    ])

# ============================================================ title, intro, new game
# The title: the main theme of Ichor, D Greek Phrygian (D Dorian, as Elaia; home). The
# lyre spins the Fates' thread from Elaia's motif (A-D-E-F), the chorus sings the theme
# with the aulos, the salpinx raises it in B, the aulos sings alone in C, and a coda
# settles. Like Emerald's, it plays once; when it ends the title returns to the intro.
D_GPHR = pcs('D', DORIAN)
TT_CH = {'intro': ['Dm', 'Dm', 'C', 'C'], 'A': ['Dm', 'C', 'F', 'C', 'Dm', 'F', 'G', 'Dm'],
         'B': ['F', 'C', 'Dm', 'Am', 'F', 'C', 'G', 'Am'], 'C': ['Am', 'Em', 'F', 'C', 'Dm', 'Am', 'G', 'G'],
         'coda': ['Dm', 'G', 'Dm', 'Dm']}
THEME = ('A4:2 D5:1 E5:1 F5:4 | G5:2 F5:1 E5:1 C5:4 | D5:2 F5:1 G5:1 A5:3 G5:1 | G5:2 E5:2 C5:4 | '
         'A4:2 D5:1 E5:1 F5:2 A5:2 | A5:3 G5:1 F5:2 C5:2 | B4:2 D5:1 E5:1 G5:2 F5:1 E5:1 | D5:8')
THREAD = ('D4:1 A4:1 D5:1 E5:1 F5:4 | D4:1 A4:1 D5:1 E5:1 G5:4 | C4:1 G4:1 C5:1 D5:1 E5:4 | '
          'C4:1 G4:1 C5:1 E5:1 G5:4')
TITLE = Song(
    name='mus_ichor_title', title='Pokemon Ichor', meter=(4, 4), grouping=(2, 2, 2, 2), tempo=112,
    voicegroup=VG, volume=127, reverb=50, priority=0,
    sections=[('intro', 4), ('A', 8), ('B', 8), ('C', 8), ('coda', 4)], loop_from=None,
    modes={'*': D_GPHR}, target=(60, 80), chords=TT_CH, song_id='MUS_TITLE', ref=('MUS_TITLE', -21.4), tracks=[
        Track('chorus', 52, 96, pan=-8, velocity=100, lo='A4', hi='A5', parts={
            'intro': 'D5:8 | D5:8 | E5:8 | E5:8', 'A': THEME, 'coda': 'A4:8 | B4:8 | A4:8 | A4:8'}),
        Track('aulos', 68, 88, pan=10, velocity=100, lo='G4', hi='A5', vibrato=(4, 40, 16), parts={
            'A': THEME,
            'C': 'E5:3 D5:1 C5:2 A4:2 | B4:4 G4:4 | A4:2 C5:2 F5:3 E5:1 | E5:4 G5:4 | '
                 'F5:3 E5:1 D5:2 A4:2 | C5:3 B4:1 A4:2 E5:2 | D5:2 B4:2 G4:2 B4:2 | D5:8'}),
        Track('salpinx', 56, 100, pan=-14, velocity=106, gate=0.9, lo='B4', hi='A5', parts={
            'B': 'C5:2 F5:1 G5:1 A5:4 | G5:2 E5:1 F5:1 G5:4 | F5:2 D5:1 E5:1 F5:2 A5:2 | E5:4 C5:4 | '
                 'D5:2 F5:1 G5:1 A5:4 | C5:2 F5:2 A5:3 G5:1 | G5:2 B4:1 D5:1 G5:2 F5:1 E5:1 | E5:8'}),
        Track('horn', 60, 80, pan=18, velocity=96, gate=0.9, lo='D4', hi='A4',
              parts={'B': 'A4:8 | G4:8 | F4:8 | E4:8 | F4:8 | E4:8 | D4:8 | E4:8'}),
        Track('lyre', 46, 90, pan=-24, velocity=94, lo='G3', hi='A5', parts={
            'intro': THREAD, 'A': gen(TT_CH['A'], ak_harp), 'C': gen(TT_CH['C'], ak_harp),
            'coda': ' | '.join(ak_harp(c) for c in TT_CH['coda'][:3]) + ' | D4:1 A4:1 D5:1 F5:1 A5:4'}),
        Track('kithara', 24, 78, pan=24, velocity=88, gate=0.6, lo='G3', hi='C5',
              parts={'B': gen(TT_CH['B'], HASAPIKO_KITHARA)}),
        Track('strings', 48, 58, pan=26, velocity=80, lo='A3', hi='A4',
              parts={s: gen(TT_CH[s], lambda c: notes([(triad(c, 55)[1], 8)])) for s in ('C', 'coda')}),
        Track('timpani', 47, 84, pan=6, velocity=100, gate=0.6, lo='A2', hi='D3', parts={
            'intro': 'r:8 | r:8 | r:8 | ' + roll('A2', 8), 'coda': 'D3:2 r:6 | r:8 | r:8 | ' + roll('D3', 8)}),
        Track('bass', 92, 60, velocity=100, lo='C2', hi='C4',
              parts={s: gen(TT_CH[s], root_fifth([('r', 4), ('f', 4)], 38)) for s in ('A', 'B', 'C', 'coda')}),
        Track('drums', 0, 86, velocity=96, kit=FRAME_KIT, parts={
            'intro': 'r:8 | r:8 | r:8 | taiko:1 taiko:1 taiko:1 taiko:1 snare:1 snare:1 snare:1 snare:1',
            'A': 'dum+cym:2 tek:2 dum:2 tek:2 | ' + bars('dum:2 tek:2 dum:2 tek:2', 7),
            'B': 'deep+crash:2 snare:2 deep:2 snare:1 snare:1 | ' + bars('deep:2 snare:2 deep:2 snare:1 snare:1', 6)
                 + ' | deep:1 snare:1 snare:1 snare:1 snare:1 snare:1 snare:1 snare:1',
            'C': bars('dum:4 tek:2_ tek:2_', 8), 'coda': 'r:8 | r:8 | r:8 | deep+crash:8'}),
    ])

# The intro movie (one-shot): cut to its scene timers in src/intro.c. At 140 BPM ten 4/4
# bars last 1028.6 frames, so A ends with scene 1 (frame 1026), B with scene 2 (frame
# 2057 against 2068), and C (3 bars) carries the legendaries' scene to the title. A: the
# lyre's thread over a chorus rising a step every two bars. B: the title theme on the
# aulos, at a gallop. C: salpinx and horns.
IN_CH = {'A': ['Dm', 'Dm', 'C', 'C', 'Dm', 'F', 'G', 'G', 'Am', 'Am'],
         'B': ['Dm', 'C', 'F', 'C', 'Dm', 'F', 'G', 'Dm', 'Am', 'Am'], 'C': ['Dm', 'C', 'Dm']}
INTRO = Song(
    name='mus_ichor_intro', title='Intro', meter=(4, 4), grouping=(2, 2, 2, 2), tempo=140,
    voicegroup=VG, volume=100, reverb=50, priority=0, sections=[('A', 10), ('B', 10), ('C', 3)], loop_from=None,
    modes={'*': D_GPHR}, target=(38, 42), chords=IN_CH, song_id='MUS_INTRO', ref=('MUS_INTRO', -24.1), tracks=[
        Track('lyre', 46, 92, pan=-16, velocity=96, lo='C4', hi='D6', parts={
            'A': THREAD + ' | D4:1 A4:1 D5:1 E5:1 F5:2 A5:2 | F4:1 C5:1 F5:1 G5:1 A5:4 | G4:1 D5:1 G5:1 A5:1 B5:4 | '
                 'G4:1 D5:1 G5:1 B5:1 D6:4 | A4:1 E5:1 A5:1 B5:1 C6:4 | A4:1 E5:1 A5:1 C6:1 A5:4'}),
        Track('chorus', 52, 90, pan=8, velocity=96, lo='D5', hi='A5', parts={
            'A': 'D5:8 | D5:8 | E5:8 | E5:8 | F5:8 | F5:8 | G5:8 | G5:8 | A5:8 | A5:8', 'C': 'F5:8 | E5:8 | D5:8'}),
        Track('aulos', 68, 96, pan=10, velocity=100, lo='A4', hi='A5', vibrato=(4, 40, 16),
              parts={'B': THEME + ' | E5:2 F5:2 G5:2 A5:2 | A5:8'}),
        Track('kithara', 24, 78, pan=24, velocity=88, gate=0.5, lo='G3', hi='C5',
              parts={'B': gen(IN_CH['B'], offbeats([(1, 1)] * 8))}),
        Track('bass', 87, 78, velocity=104, gate=0.7, lo='C2', hi='C4', parts={
            'B': gen(IN_CH['B'], root_fifth([('r', 1), ('r', 1), ('o', 1), ('r', 1)] * 2, 36)),
            'C': gen(IN_CH['C'], root_fifth([('r', 8)], 36))}),
        Track('salpinx', 56, 100, pan=-10, velocity=106, gate=0.9, lo='D5', hi='A5',
              parts={'C': 'D5:2 D5:1 D5:1 A5:4 | G5:2 F5:1 E5:1 G5:4 | D5:8'}),
        Track('horn', 60, 82, pan=18, velocity=96, gate=0.9, lo='D4', hi='F4', parts={'C': 'F4:8 | E4:8 | D4:8'}),
        Track('timpani', 47, 86, pan=6, velocity=100, gate=0.6, lo='A2', hi='D3', parts={
            'A': ' | '.join(['r:8'] * 8 + [roll('A2', 8)] * 2), 'C': 'D3:2 r:6 | C3:2 r:6 | ' + roll('D3', 8)}),
        Track('drums', 0, 88, velocity=96, kit=FRAME_KIT, parts={
            'B': bars('dum:1 tek:1 tek:1 dum:1 dum:1 tek:1 tek:1 tek:1', 10,
                      'snare:1 snare:1 snare:1 snare:1 snare:1 snare:1 snare:1 snare:1'),
            'C': 'deep+crash:2 r:2 snare:1 snare:1 snare:2 | deep:2 snare:2 deep:2 snare:1 snare:1 | deep+crash:8'}),
    ])

# Daphne's new-game speech (new slot; main_menu.c played Route 122): Bb Greek Lydian, a
# warm welcome. The syrinx over lyre arpeggios in A, the lyre's own tune over a rolling
# kithara in B. B ends on F, which falls home to the loop's Bb.
NG_CH = {'intro': ['Bb'], 'A': ['Bb', 'F', 'Gm', 'Eb', 'Bb', 'F', 'Eb', 'F'],
         'B': ['Gm', 'Dm', 'Eb', 'Bb', 'Cm', 'F', 'Eb', 'F']}


def ng_kithara(c):
    r, t, f = triad(c, 46)
    return notes([(r, 1), (f, 1), (t + 12, 1), (f, 1), (r + 12, 1), (f, 1), (t + 12, 1), (f, 1)])


NEW_GAME = Song(
    name='mus_ichor_new_game', title='A New Thread', meter=(4, 4), grouping=(2, 2, 2, 2), tempo=96,
    voicegroup=VG, volume=127, reverb=50, priority=0, sections=[('intro', 1), ('A', 8), ('B', 8)], loop_from='A',
    modes={'*': pcs('Bb', IONIAN)}, target=(36, 44), chords=NG_CH, song_id='MUS_ICHOR_NEW_GAME',
    ref=('MUS_ROUTE122', -21.5), tracks=[
        Track('syrinx', 73, 98, pan=-8, velocity=100, lo='Bb4', hi='C6', vibrato=(3, 40, 16), parts={
            'A': 'F5:3 D5:1 F5:2 Bb5:2 | A5:3 G5:1 F5:2 C5:2 | D5:3 Eb5:1 D5:2 Bb4:2 | G5:4 Eb5:4 | '
                 'F5:3 D5:1 F5:2 Bb5:2 | C6:3 Bb5:1 A5:2 F5:2 | G5:3 F5:1 Eb5:2 G5:2 | F5:8'}),
        Track('lyre', 46, 94, pan=14, velocity=96, lo='G3', hi='C6', parts={
            'intro': ak_harp('Bb'), 'A': gen(NG_CH['A'], ak_harp),
            'B': 'D5:2 G5:2 Bb5:3 A5:1 | A5:2 F5:2 D5:4 | Eb5:2 G5:2 Bb5:3 G5:1 | F5:4 D5:4 | '
                 'C5:2 Eb5:2 G5:3 F5:1 | F5:2 A5:2 C6:4 | Bb5:2 G5:2 Eb5:2 G5:2 | A5:2 G5:2 F5:2 Eb5:2'}),
        Track('kithara', 24, 76, pan=24, velocity=86, lo='Bb2', hi='Bb4', parts={'B': gen(NG_CH['B'], ng_kithara)}),
        Track('strings', 48, 54, pan=-24, velocity=78, lo='A3', hi='A4',
              parts={s: gen(NG_CH[s], lambda c: notes([(triad(c, 55)[1], 8)])) for s in ('A', 'B')}),
        Track('bass', 92, 58, velocity=96, lo='C2', hi='C4',
              parts={s: gen(c, root_fifth([('r', 4), ('f', 4)], 36)) for s, c in NG_CH.items()}),
        Track('kymbala', 0, 60, velocity=80, kit=FRAME_KIT, parts={
            'intro': 'tri:8_', 'A': bars('tri:8_ | r:8', 4), 'B': bars('tri:8_ | r:8', 4)}),
    ])

ENGINE_SONGS = [LEVEL_UP, OBTAIN_ITEM, OBTAIN_KEY_ITEM, OBTAIN_TMHM, HEAL, OBTAIN_BADGE, EVOLVED,
                EVOLUTION_INTRO, OBTAIN_MON, EVOLUTION, CAUGHT, VICTORY_WILD, VICTORY_LAUREL,
                VICTORY_TITAN, ENCOUNTER_MALE, ENCOUNTER_FEMALE, ENCOUNTER_INTENSE,
                ENCOUNTER_SUSPICIOUS, ENCOUNTER_HIKER, ENCOUNTER_RIVAL, ENCOUNTER_TITAN, TITLE,
                INTRO, NEW_GAME]
