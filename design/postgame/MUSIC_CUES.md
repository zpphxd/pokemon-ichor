# The Aethos post-game: music cue lists

This file turns the post-game docs' music tables into one list of cues. It tells a map agent which `"music"` to set and tells whoever composes what to write, in what order, and at what size.

**Reads with:** `design/MUSIC.md` (motifs, notation, "What the engine taught us"), `tools/ichor/music/README.md` (how a song is written and checked), `include/constants/songs.h`, and the music sections of `design/LABORS.md` §8, `design/UNDERWORLD.md` §2 and §9, `design/ODYSSEY.md` §10, `design/POSTGAME.md` §3, `design/SYSTEMS.md` §10, `design/OIKOUMENE.md` §7 and `design/STORY.md`'s music plan.

**Source tags** in the tables: **L** = LABORS (§8 or the Labor named), **U** = UNDERWORLD §9, **O** = ODYSSEY §10, **P** = POSTGAME, **M** = MUSIC.md, **S** = STORY's music plan, **X** = OIKOUMENE §7, **Sy** = SYSTEMS §10, **Lg** = LEGENDS. **Proposed** means the docs imply the cue but don't name it, and the name, mode or brief is this file's recommendation (see §6).

**Where the docs are silent**, modes come from MUSIC.md's mode table (Mixolydian for roads, Lydian for a question or hope, Phrygian for the sacred, Ionian for a day going by). Nothing here adds story.

---

## 0. What to do first

1. **Songs.h has no post-game constants yet.** The last Ichor song is 638 `MUS_ICHOR_HOLLOW`, and the other branches append at 639 too. Ask the director to claim a song-id block for the post-game in `tools/ichor/claim_ranges.md` (it has no music line). This file names constants and leaves ids to `songs_*.py`.
2. **Recommended: an alias block.** Add every constant in §1 to `songs.h` now as an alias of its stand-in, for example `#define MUS_ICHOR_EUPLOIA MUS_ICHOR_TRIREME`. Map agents then write the final name in `map.json` at once, and composing a cue means swapping one `#define` for a real id. If the director prefers no aliases, agents write the stand-in column and the composer does a find-and-replace from §2's tables, which carry both.
3. **The doc's own gaps** are in §6. The biggest: POSTGAME §3.1 says "5 tracks" for Olympia and names none, and no doc names a cue for Atlantis or the summit.

---

## 1. The master table

**Kinds.** *BGM* loops. *Battle* is a battle theme. *Sting* is a short one-shot that never loops (a fanfare path needs an `sFanfares` entry in `src/sound.c`). *Layer* means the cue is one song whose parts are switched on and off in play (§5, rule 9). **KiB** is the ROM estimate: 3.5 for a full loop, 1.5 for a variant that shares its sequence, 0.5 for a sting. It comes from the docs' own averages (LABORS 45 KiB over 13 tracks, UNDERWORLD 55 over 16, ODYSSEY 60 over 17, POSTGAME §3.1 20 over 5: all about 3.5).

### 1.1 The sea and the ship

The *Euploia* and the sea are one tune family (O §10 says "the same tune" four times). X's *The Wider World* is a fifth member: "the Aethos sea theme widened". Write ours first and X's after.

| # | Constant | Kind | Where it plays | Brief | Source | Stand-in | KiB |
|---|---|---|---|---|---|---|---|
| 1 | `MUS_ICHOR_EUPLOIA` | BGM | The *Euploia*'s deck and below deck | Mixolydian, 7/8 (3+2+2), a rowing pace. The trieraules aulos keeps the stroke, as in 629. Kithara, sine bass an octave under it, frame drum, sea wind (slot 122). It states the sea tune's A phrase. No motif quoted. | O | `MUS_ICHOR_TRIREME` | 3.5 |
| 2 | `MUS_ICHOR_SEA_SAIL` | BGM, layer | Sea maps, downwind: Route 33, Maleia's waters, the wine-dark seas, the Outer Sea, beyond the Pillars | The same tune, fast. Kithara over a swelling drone. The base sequence for #3 and #4. | O | `MUS_ICHOR_TRIREME` | 3.5 |
| 3 | `MUS_ICHOR_SEA_ROW` | BGM | The same maps, upwind or in a calm | The same tune, steady, with the oar-stroke drum | O | `MUS_ICHOR_TRIREME` | 1.5 |
| 4 | `MUS_ICHOR_SEA_NIGHT` | BGM | The same maps at night (the Great Bear's hours) | The tune in Lydian, sparse, with high bells for the stars. **The bells are the temple bell or the triangle, never slot 10** (§5, rule 3). | O | `MUS_ICHOR_TRIREME` | 1.5 |
| 5 | `MUS_ICHOR_STORM` | BGM | Cape Maleia, the Bag's storm, the chase after Tornadus | 9/8 zeibekiko, every instrument, crashing. It must not use the Sickle's 3+2+2+2 grind (§5, rule 7). | O | `MUS_ABNORMAL_WEATHER` | 3.5 |

### 1.2 The Odyssey's islands and the homecoming

| # | Constant | Kind | Where it plays | Brief | Source | Stand-in | KiB |
|---|---|---|---|---|---|---|---|
| 6 | `MUS_ICHOR_LOTUS` | BGM | The Lotus Isle and its hut | Lydian, honeyed. **It never resolves**: a loop with no cadence. The island's clock is stopped, but the tick (slot 115) is the Frozen Hour's alone, so no ticking. | O | `MUS_ICHOR_AKADEMIA` | 3.5 |
| 7 | `MUS_ICHOR_CYCLOPS` | BGM, layer | The Cyclops's cave | A slow two-note breathing in the bass. The melody is a layer that plays only while the eye is shut. | O | `MUS_ICHOR_HOLLOW` | 3.5 |
| 8 | `MUS_ICHOR_AIOLIA` | BGM | Aiolia and Aeolus's hall | Bright Mixolydian. Bronze bells (kymbala, not slot 10) and wind (122). | O | `MUS_ICHOR_ROUTE1` | 3.5 |
| 9 | `MUS_ICHOR_AIAIA` | BGM | Aiaia and Circe's hall | Phrygian, 5/8, a hypnotic aulos, a little too sweet. | O | `MUS_ICHOR_HOLLOW` | 3.5 |
| 10 | `MUS_ICHOR_SIRENS` | BGM, layer | The Sirens' Strait | The game's most beautiful melody: Lydian, a female choir pad and lyre. Way 1 (wax) hears it muffled: the upper tracks ducked. Way 3 (the bard) hears it fighting Phemios's sea song: #2's tune as a layer against it. Two variants of the same song. | O | `MUS_ICHOR_AKADEMIA` | 3.5 + 3.0 |
| 11 | `MUS_ICHOR_STRAIT` | BGM | The Strait, Scylla's cave | 9/8 tension, low strings, a whirlpool swirl in the drone. | O | `MUS_ICHOR_HOLLOW` | 3.5 |
| 12 | `MUS_ICHOR_THRINAKIA` | BGM, layer | Thrinakia | A golden pastoral, Dorian. It **slows as the hunger counter falls** (a tempo change in play, §5, rule 9). | O | `MUS_ICHOR_AKTI` | 3.5 |
| 13 | `MUS_ICHOR_SCHERIA` | BGM | Scheria's shore, the Phaeacians' town and halls | A warm 7/8 dance, the most festive town theme in the game. | O | `MUS_ICHOR_EMPORION` | 3.5 |
| 14 | `MUS_ICHOR_DEMODOKOS` | BGM | Demodokos's song at Alkinoos's table; the music player | A solo lyre setting of the sea tune (#1). It is the voyage looking back at itself. | O | `MUS_ICHOR_ASCLEPEION` | 2.0 |
| 15 | `MUS_ICHOR_ELAIA_MIST` | BGM | The Mist Beach; Elaia in the mist | The Elaia theme slowed and muffled. Mom's countersong is in it, faint (§5, rule 5). | O | `MUS_ICHOR_ELAIA` | 1.5 |
| 16 | `MUS_ICHOR_ELAIA_SUITORS` | BGM | Elaia while the suitors are in it | The Elaia theme as a raucous party tune, slightly out of tune. The countersong is there but buried (§5, rule 5). | O | `MUS_ICHOR_ELAIA` | 1.5 |
| 17 | `MUS_ICHOR_BATTLE_AXES` | Battle | The twelve axes, and the ringleaders' double battle | A bowstring motif over the trainer battle theme (`MUS_ICHOR_BATTLE_TRAINER`, A Phrygian 7/8). | O | `MUS_ICHOR_BATTLE_TRAINER` | 3.5 |
| 18 | `MUS_ICHOR_RECOGNITION` | BGM (scene) | After Mom's question | The Elaia theme restored in full, warm, **with Mom's countersong**, then the main theme (the Thread). | O, M | `MUS_ICHOR_ELAIA` | 2.5 |

### 1.3 The Labors

| # | Constant | Kind | Where it plays | Brief | Source | Stand-in | KiB |
|---|---|---|---|---|---|---|---|
| 19 | `MUS_ICHOR_LABOR` | BGM, layer | Every Labor map with no theme of its own | Dorian, 7/8 kalamatianos, aulos and frame drum. **One song, six steps, one per Pair**: each Pair switches on one more instrument, so by Pair 6 it is a full band. A Pair's step is set from `laborsSet` at map load. Pair 3's farm gains running-water percussion, one layer per flow that reaches the yard (Labor 5). | L §8, Labor 5 | `MUS_ICHOR_ROUTE1` | 4.5 |
| 20 | `MUS_ICHOR_HERAION` | BGM | The Heraion | Lydian, slow, a single kithara and a temple bell. | L §8 | `MUS_ICHOR_ASCLEPEION` | 3.5 |
| 21 | `MUS_ICHOR_LABOR_BOSS` | Battle | Every Labor boss except those below; partner battles with Kleon | 9/8 zeibekiko. A variant of the Ichor trainer theme: its A phrase re-metered into 9/8. Two aulos notes that double on every repeat (the Hydra's figure). | L §8, Labor 2 | `MUS_ICHOR_BATTLE_TRAINER` | 3.5 |
| 22 | `MUS_ICHOR_LION_STING` | Sting | The Nemean Lion's battle, before #21 | One frame-drum hit and a held aulos. | L Labor 1 | none (`SE_BANG`) | 0.5 |
| 23 | `MUS_ICHOR_HIND` | BGM | The Hind's sightings only | A solo kithara in Lydian, fast and light. **It stops dead** when she bolts (a hard stop, no fade). | L §8 | `MUS_ICHOR_TEMPLE_HERMES` | 2.0 |
| 24 | `MUS_ICHOR_BOAR_STING` | Sting | Each paw warning on the Erymanthian Boar | Two thumps. | L Labor 4 | none (`SE_BANG`) | 0.5 |
| 25 | `MUS_ICHOR_REEDS` | BGM | The Stymphalian Reeds | **No melody.** Wind (122), a reed flute, and the krotala's clatter as a rhythm. | L §8 | `MUS_ICHOR_HOLLOW` | 2.5 |
| 26 | `MUS_ICHOR_SKY_BATTLE` | Battle | The Stymphalian Birds | An airy 7/8 battle theme. | L §8 | `MUS_ICHOR_BATTLE_TRAINER` | 3.5 |
| 27 | `MUS_ICHOR_CROSSING` | BGM | The Bull's Crossing (Labor 7) | **The Thread (the main theme) in Mixolydian**, on a galloping frame drum. Not in L §8's table; it is in Labor 7. MUSIC.md needs the Mixolydian form first (§6). | L Labor 7 | `MUS_ICHOR_ROUTE1` | 3.0 |
| 28 | `MUS_ICHOR_THRACE` | BGM | Abdera, the Bistonian Plain, Diomedes's Yard and Stable | Phrygian, 9/8, on a droning bagpipe-like aulos (the tsabouna of `mus_ichor_encounter_hiker`). X reuses it for Thrace's Oikoumene side. | L §8 | `MUS_ICHOR_ROAD` | 3.5 |
| 29 | `MUS_ICHOR_THEMISKYRA` | BGM, layer | Themiskyra, the Thermodon Road, Hippolyta's Hall | A horse-gait 5/8 on frame drums and a low aulos. **Loses a voice per tension step** (the meter runs 0 to 6, so six steps): the melody goes first, one instrument at a time. X reuses it. | L §8, Labor 9 | `MUS_ICHOR_ROAD` | 3.5 |
| 30 | `MUS_ICHOR_OCEAN_STREAM` | BGM | The Ocean Stream | **The Thread in Lydian**, very slow, on a high kithara, no percussion: `A4:2 D5:1 E5:1 F#5:4 \| G#5:2 F#5:1 E5:1 C#5:4` (M §1). | L §8 | `MUS_ICHOR_ASCLEPEION` | 2.5 |
| 31 | `MUS_ICHOR_ERYTHEIA` | BGM | Erytheia, Geryon's Pasture | A sunset theme in Mixolydian, 7/8. X uses it on its own Erytheia maps. | L §8 | `MUS_ICHOR_ROUTE1` | 3.5 |
| 32 | `MUS_ICHOR_GERYON` | Battle (stretch) | Geryon | Three overlapping meters (9/8 over 6/8 over 3/4). If it doesn't fit the budget, use #21. | L Labor 10 | `MUS_ICHOR_BATTLE_TRAINER` | 3.5 |
| 33 | `MUS_ICHOR_GARDEN` | BGM, layer | The Garden of the Hesperides, Atlas's Ridge | Lydian, slow, kithara and a soft choir pad, permanent dusk. Atlas's Ridge adds one low string for as long as you hold the sky (a layer). | L §8, Labor 11 | `MUS_ICHOR_ASCLEPEION` | 3.5 |
| 34 | `MUS_ICHOR_ASCENT_KERBEROS` | BGM, layer | The Ascent of Tainaron during Labor 12 | #54's lament rearranged: the lyre line becomes a plodding, comic frame-drum walk. **Brighter with every shaft you shade** (a layer per shaft). | L §8, Labor 12 | `MUS_ICHOR_HOLLOW` | 2.5 |
| 35 | `MUS_ICHOR_OLYMPIAS` | Battle | The Kotinos finale, Olympias's weekly rematch | The Pantheon theme, Hera's variant: a serpentine aulos line over 7/8. The Pantheon theme is world-act3's (INVENTORY §8 lists it as still needed). | L §8 | `MUS_ICHOR_BATTLE_TRAINER` | 3.5 |
| 36 | `MUS_ICHOR_KOTINOS` | BGM (scene) | The crowning, at noon in the Altis | The Thread (the main theme), full, in Lydian: `A4:2 D5:1 E5:1 F#5:4 \| G#5:2 F#5:1 E5:1 C#5:4`. | L §8 | `MUS_ICHOR_VICTORY_LAUREL` | 3.0 |

### 1.4 The Katabasis

UNDERWORLD's sound rules (U §2) bind every row: **no frame drum anywhere above Tartarus**; the Styx has no music; the Underworld ignores the time of day.

| # | Constant | Kind | Where it plays | Brief | Source | Stand-in | KiB |
|---|---|---|---|---|---|---|---|
| 37 | `MUS_ICHOR_MANI_ROAD` | BGM | The Mani Road (Route 31) | Dorian, a dry 7/8, a bell on the off-beat (the temple bell). The last aboveground drum. | U | `MUS_ICHOR_ROAD` | 3.5 |
| 38 | `MUS_ICHOR_ORPHEUS` | BGM | Cape Tainaron; Orpheus in Elysium (his lyre) | **Orpheus's lament**, the Katabasis's leitmotif: a lyre alone, Hypodorian, slow. The notes aren't in MUSIC.md yet (§6). | U | `MUS_ICHOR_TEMPLE_DEMETER` | 3.0 |
| 39 | `MUS_ICHOR_DESCENT` | BGM | The Descent, upper and lower | A low aulos drone and water drips. | U | `MUS_ICHOR_HOLLOW` | 2.5 |
| 40 | `MUS_ICHOR_GATE` | BGM, layer | The Gate (Kerberos) | Three low notes in a cycle, one per head. **Each head that sleeps drops its note** (a layer per head). | U | `MUS_ICHOR_HOLLOW` | 2.0 |
| 41 | `MUS_ICHOR_ASPHODEL` | BGM | The Meadows of Asphodel; the Riverside of the Oath | Mixolydian, lyre and a soft string pad, no percussion, very slow. | U | `MUS_ICHOR_ASCLEPEION` | 3.5 |
| 42 | `MUS_ICHOR_SHADE_BATTLE` | Battle | Wild and trainer battles below | The trainer theme, drumless, with a breathy aulos lead. | U | `MUS_ICHOR_BATTLE_TRAINER` | 3.5 |
| 43 | `MUS_ICHOR_CROSSROADS` | BGM | The Crossroads of Judgment | Three stately chords, Dorian. | U | `MUS_ICHOR_TEMPLE` | 1.5 |
| 44 | `MUS_ICHOR_LETHE` | BGM | The Plain of Lethe | Almost nothing: a melody that starts, forgets itself after four bars, and starts again. | U | `MUS_ICHOR_HOLLOW` | 2.0 |
| 45 | `MUS_ICHOR_MNEMOSYNE` | BGM | The Lake of Mnemosyne | **The Thread (the main theme), quiet, in Lydian:** the first time it plays below. Lake water is no place for harp arpeggios (§5, rule 2). | U | `MUS_ICHOR_ASCLEPEION` | 2.5 |
| 46 | `MUS_ICHOR_HOUSE_OF_HADES` | BGM | The House of Hades and its Vault | Phrygian, a slow 5/4, a dark kithara and a pomegranate-bright aulos. **Demeter's grief motif on a lyre for Persephone** (M, "Later"), re-metered from 4/4 into 5/4: `A4:2 Bb4:2 A4:4 \| C5:2 D5:2 E5:2 F5:1 E5:1 \| …`. No drum. | U, M | `MUS_ICHOR_TEMPLE_DEMETER` | 3.5 |
| 47 | `MUS_ICHOR_BATTLE_HADES` | Battle | Hades and Persephone | A royal theme in 7/8 with two interlocking lines, his low and hers high. No drum. | U | `MUS_ICHOR_BATTLE_TRAINER` | 3.5 |
| 48 | `MUS_ICHOR_TARTARUS` | BGM | The Bronze Gates, Tartarus, the five cells, Sisyphus's Hill | **The drum returns:** a bronze anvil struck in 9/8 (zeibekiko), a low aulos, grinding strings. It is the Titans' theme, so it carries the Sickle's grind, `B1:3 B1:2 C2:2 B1:2` (M §6; proposed). | U | `MUS_ICHOR_TITAN` | 3.5 |
| 49 | `MUS_ICHOR_BATTLE_TARTARUS` | Battle | The five Titans, and Briareus | The Regi idea re-voiced: an anvil, a drone and a five-note figure (one note per Titan). | U | `MUS_VS_REGI` | 3.5 |
| 50 | `MUS_ICHOR_CHASM` | Battle (stretch) | Giratina in the Chasm | The Tartarus theme played backward (reversed sequence data). If it doesn't fit, use #49. | U | `MUS_ICHOR_BATTLE_TARTARUS` | 3.5 |
| 51 | `MUS_ICHOR_ELYSIUM` | BGM | Elysium and its Shore | Gold: Lydian, kithara and choir, **the warmest music in the game**. | U | `MUS_ICHOR_VICTORY_LAUREL` | 3.5 |
| 52 | `MUS_ICHOR_ASCENT` | BGM, layer | The Ascent of Tainaron during the Katabasis | Orpheus's lament (#38), building. **It drops to one note at landing 3** (the footsteps stop) **and returns.** No drum. | U | `MUS_ICHOR_TEMPLE_DEMETER` | 3.0 |
| 53 | `MUS_ICHOR_ELEUSA_SPRING` | BGM | Eleusa, once spring returns | The Eleusa town theme with a new flute descant. Recommended: the descant is Demeter's **return** form (M): `A4:2 B4:2 \| A4:4 \| C#5:2 D5:2 \| E5:2 F#5:1 E5:1 \| …`. | U | `MUS_ICHOR_ELEUSA` | 3.5 |


### 1.5 Olympia

POSTGAME §3.1 says "music (5 tracks, ~20 KiB)" and names none. These five are **proposed**, one per kind of place, with modes from MUSIC.md's table.

| # | Constant | Kind | Where it plays | Brief | Source | Stand-in | KiB |
|---|---|---|---|---|---|---|---|
| 54 | `MUS_ICHOR_SACRED_WAY` | BGM | The Sacred Way (Route 32) | Mixolydian, a road under the truce. A kalamatianos 7/8 would repeat Route 1; choose 6/8 or 5/4. | P §3.1, proposed | `MUS_ICHOR_ROAD` | 3.5 |
| 55 | `MUS_ICHOR_OLYMPIA` | BGM | The Altis, the Leonidaion's court, the Echo Stoa, Phidias's workshop | Ionian: the world going about its day, and the games held in it. | P §3.1, proposed | `MUS_ICHOR_EMPORION` | 4.0 |
| 56 | `MUS_ICHOR_TEMPLE_ZEUS` | BGM | The Temple of Zeus | Greek Dorian (church Phrygian), the sacred mode, with Phidias's empty throne in mind. A cousin of `MUS_ICHOR_TEMPLE`, not a copy. | P §3.1, proposed | `MUS_ICHOR_TEMPLE` | 3.5 |
| 57 | `MUS_ICHOR_OLYMPIAD` | BGM | The Stadion, the Horse, the Palaestra and the Apple Course: lobbies and battle rooms | One facility theme, brisk, a crowd under it. The Frontier's four rooms share it. | P §3.1, proposed | `MUS_ICHOR_AGORA` | 4.0 |
| 58 | `MUS_ICHOR_BATTLE_BRAIN` | Battle | The five Brains (Achilles, Odysseus, Hippolyta, Atalanta, Ariadne) | A 7/8 or 9/8 duel theme a step above `MUS_ICHOR_BATTLE_TRAINER`. | P §3.1, proposed | `MUS_ICHOR_BATTLE_TRAINER` | 3.5 |
| 59 | `MUS_ICHOR_MOMENT` | Sting | The Moment's pass along the colonnade (Kairazor) | "A fast bright phrase that's over before it starts. Never more than two bars." The tick is not used (§5, rule 3). | S | `MUS_ICHOR_OBTAIN_ITEM` | 0.5 |

### 1.6 Atlantis, the Primordials and the summit (all proposed)

No doc names a cue here. POSTGAME §3.3 keeps the Hoenn set-piece songs (re-themed, not cut: about 336 KiB already in the ROM), so most rows stand on a vanilla song that is already there. Only the two Atlantis themes are new work.

| # | Constant | Kind | Where it plays | Brief | Source | Stand-in | KiB |
|---|---|---|---|---|---|---|---|
| 60 | `MUS_ICHOR_ATLANTIS` | BGM | The Nereids' circle, the rings' surface ruins, the temple, the nursery | Lydian, a question: Daphne's arc. Quotes **Daphne's Question** in G Lydian, `D5:2 G5:1 A5:1 B5:2 G5:2 \| C#6:2 B5:1 A5:1 E5:4`. Lydian kithara and choir. No harp tails on water (§5, rule 2). | P §3.2, M §4, proposed | `MUS_ICHOR_AKADEMIA` | 3.5 |
| 61 | `MUS_ICHOR_ATLANTIS_DEEP` | BGM | The three rings underwater, the abyss, Charybdis's Hoard | Breath, in sound: the same Question, slower, under a held drone. The 60-step breath counter has no sound of its own. | P §3.2, proposed | `MUS_UNDERWATER` | 3.5 |
| 62 | `MUS_ICHOR_OKEANOS` | BGM | The edge of the world (Oceanus, Kyogre) | A slow tidal swell: a river that runs in a circle. **X's cue, shared:** X names *Okeanos* for the Oikoumene's rim. Use one cue on both. | P §3.2, X | `MUS_ICHOR_SEA_NIGHT` | 0 (X's) |
| 63 | `MUS_ICHOR_GAIA` | BGM | The Korykian cave, Gaia's chamber | Earth, under Delphoi. The Hoenn Cave of Origin song is the stand-in; re-theme later. | P §3.3, proposed | `MUS_CAVE_OF_ORIGIN` | 0 |
| 64 | `MUS_ICHOR_OURANOS` | BGM | The cloud meadows, Ouranos's sky, Pegaunos | The sky. The Rayquaza descent scene's song, re-themed. | P §3.3, proposed | `MUS_RAYQUAZA_APPEARS` | 0 |
| 65 | `MUS_ICHOR_PRIME_MOVER` | BGM | The summit path and the summit (Arceus) | The last puzzle is to stop, so the cue should be near-silence: one held note. The composer proposes the rest. | P §3.3, proposed | `MUS_SEALED_CHAMBER` | 1.5 |
| 66 | `MUS_ICHOR_BATTLE_PRIMORDIAL` | Battle | Gaia (Groudon), Oceanus (Kyogre), Ouranos (Rayquaza) | One cue for the three, in 9/8 or 7/8. Their weather (harsh sun, heavy rain) stays as the battle weather. The Hoenn song is kept until re-themed. | P §3.3, proposed | `MUS_VS_KYOGRE_GROUDON` | 0 |
| 67 | `MUS_ICHOR_BATTLE_PRIME_MOVER` | Battle | Arceus, Lv 95 | The top of the curve. The composer proposes it, and it should differ from #66 in feel: the object of love, not a storm. | P §3.3, proposed | `MUS_VS_KYOGRE_GROUDON` | 0 |
| 68 | `MUS_ICHOR_BATTLE_LEGEND` | Battle | Every other post-game legendary: Celebi, Heatran, Type: Null, Magearna, Marshadow, the satyr five, Manaphy, Lugia, Pontanax, Pegaunos, Ichorin, the Moment, Nike | One shared theme, so the legend fights need only one new battle cue. INVENTORY §8 lists no Ichor legend theme as needed. | Lg, proposed | `MUS_VS_MEW` | 3.5 |

### 1.7 Stings, the lullaby and the shared cues

These belong to other branches or to MUSIC.md. The post-game plays them, so they're listed so no agent makes a second copy.

| # | Constant | Kind | Where it plays | Brief | Source | Stand-in | KiB |
|---|---|---|---|---|---|---|---|
| 69 | `MUS_ICHOR_THEOXENIA` | Sting | Every god's reveal: here E6 to E13 and the finale | One shared two-bar sting, drums out of nowhere. The god's own line follows in the scene's music. Never loops. **world-act3 composes it.** | M, Sy | `MUS_ICHOR_OBTAIN_KEY_ITEM` | 0 (act3's) |
| 70 | `MUS_ICHOR_ELAIA_COUNTERSONG` | BGM | Elaia and its interiors in the post-game | The Elaia theme carrying Mom's countersong: the aulos or hum on `F4:3 G4:2 A4:1 \| A4:3 G4:3 \| …` (M §3). **world-act3 builds it** ("for the director to assign when the post-Delphoi maps land"); the name is proposed. | M §3, proposed | `MUS_ICHOR_ELAIA` | 0 (act3's) |
| 71 | `MUS_ICHOR_ELPIS_LULLABY_FINISHED` | BGM | Theano's scene in Elysium; Celebi at Akti; the music player | All eight bars of Elpis's lullaby, **bar 8 sounding: A rises to D.** It is Elpis's resolution, which world-act3 writes. Here the same song is used twice, and X uses it as *The Blessed*. | U scene 14, Lg §7.1, M §2 | `MUS_ICHOR_ELPIS_LULLABY` | 0 (act3's) |
| 72 | `MUS_ICHOR_LOOM` | BGM | The Loom at 100% (POSTGAME §5) | The Fates' three voices (M §7). **world-act3's "The Fates at the Loom".** | M §7, P §5 | `MUS_ICHOR_ELPIS_LULLABY_BOX` | 0 (act3's) |

### 1.8 Reused as they are

| Existing | Post-game use |
|---|---|
| `MUS_ICHOR_AKTI`, `_TEMPLE`, `_ASCLEPEION`, `_AGORA` | Akti and its interiors; the Leonidaion's Asclepeion and Agora |
| `MUS_ICHOR_ROAD`, `_ROAD_NIGHT` | Routes and the night shades. `sNightMusicTable` already maps 630 to 631 |
| `MUS_ICHOR_BATTLE_WILD`, `_BATTLE_TRAINER` | Aethos post-game wild and trainer battles (§4) |
| `MUS_ICHOR_BATTLE_ADMIN` and its admin layers | Iapetos on the Sirens' rocks (the chorus-of-aulos layer, M "Act I's music") |
| `MUS_ICHOR_VICTORY_*`, `_CAUGHT`, `_OBTAIN_*`, `_HEAL` | Every victory, catch, item and symbol |
| `MUS_ICHOR_HOLLOW` | Any cave or wood (the Lion's Den, the Descent's stand-in) |
| `MUS_ICHOR_ELPIS_LULLABY_BOX` (628) | Elpis's shelf at Akti, the box in Celebi's quest |
| Bull-leaping (LABYRINTH §9, a fast 7/8 with crowd claps) | Labor 7's leap and Charybdis's fig tree. The Labyrinth's owner names it. |

**Totals.** 68 new cues in §1.1 to §1.6 (counting `MUS_ICHOR_LABOR`'s six steps and `MUS_ICHOR_SIRENS`' two variants as one cue each), plus 4 shared in §1.7. See §5.2 for sizes.

---

## 2. Map-to-cue lists, by batch

Every table gives **music (final)**, the constant to set once the alias block is in (§0), and **music (now)**, the stand-in that works today. Where the map belongs to another branch, the row is a placement note: don't edit that map.

### Batch 1: set sail

| Map | Music (final) | Music (now) | Notes |
|---|---|---|---|
| `MAP_EUPLOIA_DECK` | `MUS_ICHOR_EUPLOIA` | `MUS_ICHOR_TRIREME` | Nausikles at the oars, Alethea at the chart table |
| `MAP_EUPLOIA_BELOW` | `MUS_ICHOR_EUPLOIA` | `MUS_ICHOR_TRIREME` | The same cue: O §10 gives one for "aboard, below deck" |
| `MAP_ROUTE33_WESTERN_SEA` (and `_SOUTH`) | `MUS_ICHOR_SEA_SAIL` | `MUS_ICHOR_TRIREME` | The sailing layer picks `SEA_ROW` when upwind or calm (§5, rule 8), and `sNightMusicTable` maps `SEA_SAIL` and `SEA_ROW` to `SEA_NIGHT`. Wild and trainer battles: §4. |
| Route 33's stub landings: Cape Tainaron, Ithaka, Kerkyra | the sea's cue, until batch 3 and batch 6 | `MUS_ICHOR_TRIREME` | The rooms are stubs. Cape Tainaron becomes `MUS_ICHOR_ORPHEUS`, and Kerkyra (Scheria) `MUS_ICHOR_SCHERIA`. Ithaka has no cue (§6). |
| `AktiTown` and its interiors (Agora, Asclepeion, the Fisher's house, Diver's, Goatherd's, Temple of Hestia) | unchanged | unchanged | Post-game state behind `FLAG_ICHOR_POSTGAME`: Nausikles and Alethea on the quay, Lampon, Diktys, Glaukias. No new cue. The gangplank's "Board the *Euploia*?" cuts to the deck cue. |
| Lampon's carried flame, Hestia's hearth to the quay | `MUS_ICHOR_TEMPLE` at the hearth, then each map's own | | The flame is a line of dialogue until the engine ask lands |
| `ElaiaVillage`, the Akademia, the Baker's, the Neighbor's, the Player's house 1F and 2F | `MUS_ICHOR_ELAIA_COUNTERSONG` | `MUS_ICHOR_ELAIA` | Act3's variant. Kleon at the well (LABORS scene 0) uses the town theme: no cue. |
| `KallisteRoute1`, `_KronionHill` | unchanged | unchanged | Shades at night: `MUS_ICHOR_ROAD_NIGHT`; battle `MUS_ICHOR_BATTLE_WILD` |
| Crew scenes on other branches' maps (Kydon at Emporion, Phemios at Thyrsa, Lynkeus and Iaso at Astyra, Nolan at Lechaion, the oarsmen at Lakonia) | the map's own | | Placement notes only. The heralds' lines use the town's own theme. |
| The helm's voyages (a short crossing) | the sea's cue | | |

### Batch 2: Olympia

| Map | Music (final) | Music (now) | Notes |
|---|---|---|---|
| The Sacred Way (Route 32) | `MUS_ICHOR_SACRED_WAY` | `MUS_ICHOR_ROAD` | E8 (Sam) and E9 (Hera's ford): the reveal plays `MUS_ICHOR_THEOXENIA`, then the road. Route battles: §4. |
| The Altis | `MUS_ICHOR_OLYMPIA` | `MUS_ICHOR_EMPORION` | The Moment's pass: `MUS_ICHOR_MOMENT`. Nike's pillar: `MUS_ICHOR_OLYMPIA`. The Kotinos at noon: `MUS_ICHOR_KOTINOS`. |
| The Temple of Zeus | `MUS_ICHOR_TEMPLE_ZEUS` | `MUS_ICHOR_TEMPLE` | Olympias's finale battle: `MUS_ICHOR_OLYMPIAS` |
| The Leonidaion (×2) | `MUS_ICHOR_ASCLEPEION` (the Asclepeion), `MUS_ICHOR_AGORA` (the Agora, the Pithos) | same | Existing themes, as in Akti |
| The Echo Stoa (Arena of Champions) | `MUS_ICHOR_OLYMPIA` | `MUS_ICHOR_EMPORION` | Hierophant rematches: §4 |
| Phidias's workshop (prize exchange) | `MUS_ICHOR_AGORA` | same | |
| The Heraion | `MUS_ICHOR_HERAION` | `MUS_ICHOR_ASCLEPEION` | LABORS's cue, on a batch 2 map |
| The Stadion, lobby and battle room | `MUS_ICHOR_OLYMPIAD` | `MUS_ICHOR_AGORA` | Achilles's battle: `MUS_ICHOR_BATTLE_BRAIN`. Kleon's visit: the lobby cue. |
| The Horse, lobby and battle room | `MUS_ICHOR_OLYMPIAD` | `MUS_ICHOR_AGORA` | Odysseus: `MUS_ICHOR_BATTLE_BRAIN` |
| The Palaestra | `MUS_ICHOR_OLYMPIAD` | `MUS_ICHOR_AGORA` | Hippolyta: `MUS_ICHOR_BATTLE_BRAIN` |
| The Apple Course, gate and rooms | `MUS_ICHOR_OLYMPIAD` | `MUS_ICHOR_AGORA` | Atalanta: `MUS_ICHOR_BATTLE_BRAIN` |
| Symbol and streak rewards | `MUS_ICHOR_OBTAIN_BADGE` | same | The five Symbols are the Laurel's fanfare. Victini (Nike): the legend theme, §4. |

### Batch 3: the Katabasis

| Map | Music (final) | Music (now) | Notes |
|---|---|---|---|
| The Mani Road | `MUS_ICHOR_MANI_ROAD` | `MUS_ICHOR_ROAD` | No `sNightMusicTable` entry |
| Cape Tainaron | `MUS_ICHOR_ORPHEUS` | `MUS_ICHOR_TEMPLE_DEMETER` | E11 (Hades) on the river: `MUS_ICHOR_THEOXENIA`, then the cape's cue |
| The Descent, upper and lower | `MUS_ICHOR_DESCENT` | `MUS_ICHOR_HOLLOW` | |
| The Acheron Bank | `MUS_ICHOR_DESCENT` | `MUS_ICHOR_HOLLOW` | No cue is named (§6) |
| The Styx | **no music** | `MUS_DUMMY` | The pole, Charon breathing (U) |
| The Gate | `MUS_ICHOR_GATE` | `MUS_ICHOR_HOLLOW` | One note dropped per sleeping head |
| The Meadows of Asphodel | `MUS_ICHOR_ASPHODEL` | `MUS_ICHOR_ASCLEPEION` | |
| The Riverside of the Oath | `MUS_ICHOR_ASPHODEL` | `MUS_ICHOR_ASCLEPEION` | |
| The Crossroads of Judgment | `MUS_ICHOR_CROSSROADS` | `MUS_ICHOR_TEMPLE` | |
| The Plain of Lethe | `MUS_ICHOR_LETHE` | `MUS_ICHOR_HOLLOW` | |
| The Lake of Mnemosyne | `MUS_ICHOR_MNEMOSYNE` | `MUS_ICHOR_ASCLEPEION` | |
| The House of Hades; the Vault | `MUS_ICHOR_HOUSE_OF_HADES` | `MUS_ICHOR_TEMPLE_DEMETER` | Hades and Persephone: `MUS_ICHOR_BATTLE_HADES` |
| The Bronze Gates; Tartarus; the five cells; Sisyphus's Hill | `MUS_ICHOR_TARTARUS` | `MUS_ICHOR_TITAN` | The Titans and Briareus: `MUS_ICHOR_BATTLE_TARTARUS`. The Fall: no cue is named (§6). |
| The Chasm | `MUS_ICHOR_CHASM` | `MUS_ICHOR_BATTLE_TARTARUS` | Giratina |
| Elysium; Elysium's Shore | `MUS_ICHOR_ELYSIUM` | `MUS_ICHOR_VICTORY_LAUREL` | Orpheus's scene: `MUS_ICHOR_ORPHEUS`. Theano's scene: `MUS_ICHOR_ELPIS_LULLABY_FINISHED` |
| The Ascent of Tainaron | `MUS_ICHOR_ASCENT` (Katabasis) or `MUS_ICHOR_ASCENT_KERBEROS` (Labor 12) | `MUS_ICHOR_TEMPLE_DEMETER` | Shared map. `ON_TRANSITION` picks the cue from `VAR_ICHOR_KATABASIS` and the Labor's state (§3, C5). |
| Eleusa, after the Ascent | `MUS_ICHOR_ELEUSA_SPRING` | `MUS_ICHOR_ELEUSA` | Another branch's map: a placement note. E12 (Persephone) reveal: `MUS_ICHOR_THEOXENIA`. |
| The House of Night (stretch) | none named | `MUS_ICHOR_HOLLOW` | §6 |
| Messages home (Akti, Lakonia) | the map's own | | Scenes 19 and 20 |

### Batches 4 and 5: the Labors

Pair 1 is Labors 1 and 2, Pair 2 is 3 and 4, Pair 3 is 5 and 6, Pair 4 is 7 and 8, Pair 5 is 9 and 10, Pair 6 is 11 and 12. `MUS_ICHOR_LABOR`'s step number is the Pair. Until the layers land (§5, rule 9), the stand-in is `MUS_ICHOR_ROUTE1` on every row it appears.

| Map | Music (final) | Music (now) | Notes |
|---|---|---|---|
| The Heraion (batch 4 with batch 2's building) | `MUS_ICHOR_HERAION` | `MUS_ICHOR_ASCLEPEION` | |
| Nemea Glen | `MUS_ICHOR_LABOR` (step 1) | `MUS_ICHOR_ROUTE1` | |
| The Lion's Den | `MUS_ICHOR_LABOR` (step 1) | `MUS_ICHOR_HOLLOW` | The lions: `MUS_ICHOR_LION_STING`, then `MUS_ICHOR_LABOR_BOSS` (a multi battle with Kleon) |
| The Springs of Lerna | `MUS_ICHOR_LABOR` (step 1) | `MUS_ICHOR_ROUTE1` | The Hydra and the Crab: `MUS_ICHOR_LABOR_BOSS` |
| The Ladon Ford | `MUS_ICHOR_LABOR` (step 2) | `MUS_ICHOR_ROUTE1` | The Hind: `MUS_ICHOR_HIND` at sightings only |
| Erymanthos Slopes; the Snowfield | `MUS_ICHOR_LABOR` (step 2) | `MUS_ICHOR_ROUTE1` | Each paw warning: `MUS_ICHOR_BOAR_STING`. The Boar: `MUS_ICHOR_LABOR_BOSS`. |
| Augeas's Farm | `MUS_ICHOR_LABOR` (step 3) with a water layer per flow | `MUS_ICHOR_ROUTE1` | |
| The Stable Yard | **almost silent** | `MUS_DUMMY` | Hoof shuffles and breathing: sound effects, no cue |
| The Stymphalian Reeds | `MUS_ICHOR_REEDS` | `MUS_ICHOR_HOLLOW` | The Birds: `MUS_ICHOR_SKY_BATTLE` |
| The Bull's Shore | `MUS_ICHOR_LABOR` (step 4) | `MUS_ICHOR_ROUTE1` | The leap: Bull-leaping (reused) |
| The Bull's Crossing | `MUS_ICHOR_CROSSING` | `MUS_ICHOR_ROUTE1` | |
| Abdera; its interiors (×3); the Bistonian Plain; Diomedes's Yard and Stable | `MUS_ICHOR_THRACE` | `MUS_ICHOR_ROAD` | Diomedes: `MUS_ICHOR_LABOR_BOSS` |
| The Thermodon Road; Themiskyra; Hippolyta's Hall | `MUS_ICHOR_THEMISKYRA` (tension layers) | `MUS_ICHOR_ROAD` | The six Amazon battles at tension 6, and Hippolyta: `MUS_ICHOR_LABOR_BOSS` |
| The Western Cape | `MUS_ICHOR_LABOR` (step 5) | `MUS_ICHOR_ROUTE1` | No cue is named for it (§6) |
| The Ocean Stream | `MUS_ICHOR_OCEAN_STREAM` | `MUS_ICHOR_ASCLEPEION` | |
| The Strait of the Pillars | `MUS_ICHOR_LABOR` (step 5) | `MUS_ICHOR_ROUTE1` | Seam with the Oikoumene's waters: see BUILD §5. No cue is named (§6). |
| Erytheia; Geryon's Pasture | `MUS_ICHOR_ERYTHEIA` | `MUS_ICHOR_ROUTE1` | Geryon: `MUS_ICHOR_GERYON`, else `MUS_ICHOR_LABOR_BOSS` |
| The Caucasus Crag | `MUS_ICHOR_LABOR` (step 6) | `MUS_ICHOR_ROUTE1` | |
| The Garden; Atlas's Ridge | `MUS_ICHOR_GARDEN` (Atlas's low string on the Ridge) | `MUS_ICHOR_ASCLEPEION` | Ladon: `MUS_ICHOR_LABOR_BOSS` (Kleon beside you) |
| Kerberos, the Ascent | `MUS_ICHOR_ASCENT_KERBEROS` | `MUS_ICHOR_TEMPLE_DEMETER` | Shared map #27, see batch 3 |
| The Kotinos | `MUS_ICHOR_KOTINOS`, then `MUS_ICHOR_OLYMPIAS` in the Temple | `MUS_ICHOR_VICTORY_LAUREL`, `MUS_ICHOR_BATTLE_TRAINER` | |

### Batch 6: the Odyssey

| Map | Music (final) | Music (now) | Notes |
|---|---|---|---|
| Maleia's waters | `MUS_ICHOR_STORM` during the storm and the chase, else `MUS_ICHOR_SEA_SAIL` | `MUS_ABNORMAL_WEATHER` / `MUS_ICHOR_TRIREME` | |
| The eastern and western wine-dark seas; the Outer Sea | `MUS_ICHOR_SEA_SAIL` (ROW, NIGHT by the engine) | `MUS_ICHOR_TRIREME` | |
| Lotus Isle; its hut | `MUS_ICHOR_LOTUS` | `MUS_ICHOR_AKADEMIA` | No night entry: the clock is stopped |
| Cyclops Isle | none named | `MUS_ICHOR_ROAD` | §6 |
| The Cyclops's cave | `MUS_ICHOR_CYCLOPS` | `MUS_ICHOR_HOLLOW` | The great Polyphant: `MUS_ICHOR_LABOR_BOSS` |
| Aiolia; Aeolus's hall | `MUS_ICHOR_AIOLIA` | `MUS_ICHOR_ROUTE1` | |
| Aiaia; Circe's hall | `MUS_ICHOR_AIAIA` | `MUS_ICHOR_HOLLOW` | |
| The Sirens' Strait | `MUS_ICHOR_SIRENS` (muffled or dueling by way) | `MUS_ICHOR_AKADEMIA` | Iapetos on the skerry: `MUS_ICHOR_BATTLE_ADMIN` with his chorus layer. The two Seirenade: the trainer theme. |
| The Strait; Scylla's cave | `MUS_ICHOR_STRAIT` | `MUS_ICHOR_HOLLOW` | Hexylla: `MUS_ICHOR_BATTLE_TRAINER` |
| Charybdis's Hoard | `MUS_ICHOR_ATLANTIS_DEEP` | `MUS_UNDERWATER` | Underwater, post-Atlantis |
| Thrinakia | `MUS_ICHOR_THRINAKIA` | `MUS_ICHOR_AKTI` | |
| Proteus's islet | none named | `MUS_ICHOR_ROAD` | E13's four battles: `MUS_ICHOR_BATTLE_WILD`. §6. |
| Scheria's shore; the town; Alkinoos's hall; its interiors | `MUS_ICHOR_SCHERIA` | `MUS_ICHOR_EMPORION` | Demodokos's song: `MUS_ICHOR_DEMODOKOS`. The games' three bosses: `MUS_ICHOR_BATTLE_TRAINER`. |
| The Mist Beach | `MUS_ICHOR_ELAIA_MIST` | `MUS_ICHOR_ELAIA` | |
| Elaia, homecoming | `MUS_ICHOR_ELAIA_MIST` (mist and Amaryllis's hut), `MUS_ICHOR_ELAIA_SUITORS` (the suitors in the square), `MUS_ICHOR_BATTLE_AXES` (the gauntlet), `MUS_ICHOR_RECOGNITION` (Mom's question onward) | `MUS_ICHOR_ELAIA` / `MUS_ICHOR_BATTLE_TRAINER` | Argos's scene: the suitor cue, as written. The finale's storm night: §6. |
| Akti, crew objects | unchanged | | |

### Batch 7: Atlantis and the summit

| Map | Music (final) | Music (now) | Notes |
|---|---|---|---|
| Beyond the Pillars (the outer ocean) | `MUS_ICHOR_SEA_SAIL` (ROW, NIGHT by the engine) | `MUS_ICHOR_TRIREME` | The largest sea map |
| The Nereids' circle | `MUS_ICHOR_ATLANTIS` | `MUS_ICHOR_AKADEMIA` | The double battle: the trainer theme |
| The three rings, surface | `MUS_ICHOR_ATLANTIS` | `MUS_ICHOR_AKADEMIA` | |
| The three rings, underwater | `MUS_ICHOR_ATLANTIS_DEEP` | `MUS_UNDERWATER` | |
| The temple; the nursery | `MUS_ICHOR_ATLANTIS` | `MUS_ICHOR_AKADEMIA` | Pontanax, Manaphy: the legend theme |
| The abyss | `MUS_ICHOR_ATLANTIS_DEEP` | `MUS_UNDERWATER` | Lugia: the legend theme |
| The edge of the world | `MUS_ICHOR_OKEANOS` | `MUS_ICHOR_SEA_NIGHT` | Kyogre: `MUS_ICHOR_BATTLE_PRIMORDIAL` |
| The Korykian cave; Gaia's chamber | `MUS_ICHOR_GAIA` | `MUS_CAVE_OF_ORIGIN` | Groudon: `MUS_ICHOR_BATTLE_PRIMORDIAL` |
| The cloud meadows; Ouranos's sky | `MUS_ICHOR_OURANOS` | `MUS_RAYQUAZA_APPEARS` | Pegaunos: the legend theme. Rayquaza: `MUS_ICHOR_BATTLE_PRIMORDIAL`. |
| The summit path; the summit | `MUS_ICHOR_PRIME_MOVER` | `MUS_SEALED_CHAMBER` | Arceus: `MUS_ICHOR_BATTLE_PRIME_MOVER` |
| The colossi's sites (Olympus's storm terrace, Atlantis's temple, the Vault) | the map's cue | | Olympanax, Pontanax, Nekranax: the legend theme |
| Ichorin's pool (Arkadia) | the map's own | | The legend theme |
| The Loom at Delphoi (100%) | `MUS_ICHOR_LOOM` | `MUS_ICHOR_ELPIS_LULLABY_BOX` | The Kleos page: the same scene |

### Batch 8: the rest of the theoxenia and the legends

| Place | Music (final) | Music (now) | Notes |
|---|---|---|---|
| E6 (Thyrsa's vineyards), E7 (Kythera), E10 (Hecate's Hollow, at night) | the map's own, then the reveal's `MUS_ICHOR_THEOXENIA` | | Other branches' maps: placement notes. E10's crossroads: `MUS_ICHOR_HOLLOW` already plays. |
| LEGENDS §7: Celebi (Akti, Time Fractures), Heatran (Kaldera), Type: Null, Magearna, Marshadow, the satyr five | the map's own; battles use the legend theme | | Celebi's box scene: `MUS_ICHOR_ELPIS_LULLABY_BOX`, then `MUS_ICHOR_ELPIS_LULLABY_FINISHED` |
| Aethos homes (POSTGAME §3.4) | the map's own | | |
| Time Fractures (the shimmering tiles) | none named | the route's own | §6 |
| Route 34; Rhodos | none named | `MUS_ICHOR_ROAD`; `MUS_ICHOR_EMPORION` | No doc gives a cue (§6) |

---

## 3. Where the docs disagree

| # | The disagreement | Recommendation |
|---|---|---|
| C1 | **The ship's theme.** O §10 gives the *Euploia* "Mixolydian 7/8". The built Act I cue for the same ship's crossing, `MUS_ICHOR_TRIREME` (629), is G Dorian, 6/8 (M, "Act I's music"). | Keep 629 as Act I's. The post-game's family (#1 to #4) is a new tune in a different key from G, so the two can't be mistaken for each other. |
| C2 | **"The Aethos sea theme."** O §10 builds a four-member family; X's *The Wider World* is "the Aethos sea theme widened". | One tune family. Write #1 to #4 first, then X's as a fifth arrangement. Ask world-oikoumene to take the tune from #1's sequence. |
| C3 | **The Labor boss.** L §8 says "9/8 zeibekiko; a variant of the Ichor trainer theme". But 617 is 7/8, and 9/8 is already `MUS_ICHOR_BATTLE_RIVAL`'s (Kleos) and `MUS_ICHOR_TITAN`'s (the Sickle). The Labors also name *The Lion* and *The Hydra* as battle cues of their own. | One boss track in A Phrygian (617's key, not E or B), re-metered to 9/8, with the Hydra's doubling figure. *The Lion* becomes a one-bar sting (#22) before it. It must never use the 3+2+2+2 grind. |
| C4 | **How many Labor tracks.** L §8 says "about 13", but its table omits the Boar's sting, the Crossing, Geryon's battle and a separate Sky Battle, which the Labors name. The Waterworks, Tension, Atlas and the Stable are layers or silence, not tracks. | 18 cues (#19 to #36, two of them stings): five more than the doc's 13, about 7.5 KiB more. |
| C5 | **The Ascent.** U §9 gives a building lament with no drum. L §8 gives a plodding comic frame-drum walk. It is one shared map (map 27 in U §3). | Two cues (#52, #34), chosen in `ON_TRANSITION` from `VAR_ICHOR_KATABASIS` and Labor 12's state. U's "no frame drum" rule is the dead's, so the comic walk keeps its drum: it is Kerberos's footfall. |
| C6 | **Olympia's tracks.** P §3.1 says "5 tracks". L §8 adds the Heraion's cue, and the Moment's brief is in STORY, not POSTGAME. | Five for Olympia (#54 to #58), the Heraion's cue as L's (#20), and the Moment as a sting (#59). |
| C7 | **The rim of the world.** X names *Okeanos* for the Oikoumene's rim. P §3.2 and §3.3 put Oceanus and the edge of the world on our maps. | One cue, `MUS_ICHOR_OKEANOS`, owned by world-oikoumene. Kyogre's battle stays ours (#62). |
| C8 | **Track counts.** O says "about 17" over 18 rows (16 after the three sea variants share a sequence). U says "about 16" over 17 rows. L says 13 (C4). | Budget from this file's counts (§4). |
| C9 | **Odyssey trainers' theme.** X §7 plays *Battle! Oikoumene Trainer* for "all trainers here", chosen by trainer region. The Odyssey's sea is at the Oikoumene's levels (P §4) but its trainers are Aethos-region and no doc names a cue. | The Odyssey's trainers use `MUS_ICHOR_BATTLE_TRAINER`. The region switch stays for the Oikoumene's lands. |
| C10 | **POSTGAME §7 has no music line.** Each epic's music sits inside its own total, and Atlantis (~280 KiB) and the summit (~140 KiB) have no music estimate at all. | See §4: 7 KiB of new Atlantis music, and the rest of §1.6 stands on kept Hoenn songs. |

---

## 4. Battle music

The engine already has the Ichor wild, trainer, rival and admin themes. Rules: Kleos (the rival theme) belongs to Kleon alone, the Sickle to the Titans, and the lullaby to Elpis.

| Fight | Cue | Stand-in |
|---|---|---|
| **Aethos wild**, post-game (Lv 55 to 70), including at sea and on the Labors' maps | `MUS_ICHOR_BATTLE_WILD` | same |
| **Aethos trainer** (Lv 65 to 75), and the Odyssey's and Atlantis's trainers | `MUS_ICHOR_BATTLE_TRAINER` | same |
| **Shades**, wild and trainer, in the Underworld | `MUS_ICHOR_SHADE_BATTLE` (#42) | `MUS_ICHOR_BATTLE_TRAINER` |
| **Labor bosses**, and Kleon's partner battles (the lions, the Hydra and the Crab, Ladon) | `MUS_ICHOR_LABOR_BOSS` (#21), `MUS_ICHOR_LION_STING` before the Lion | `MUS_ICHOR_BATTLE_TRAINER` |
| **Olympias**, the Kotinos and her weekly rematch | `MUS_ICHOR_OLYMPIAS` (#35) | `MUS_ICHOR_BATTLE_TRAINER` |
| **The five Brains** (Olympia) | `MUS_ICHOR_BATTLE_BRAIN` (#58) | `MUS_ICHOR_BATTLE_TRAINER`, or the vanilla `MUS_VS_FRONTIER_BRAIN` while the Frontier songs aren't cut |
| **Hierophant rematches** at the Echo Stoa; Pantheon and Archon rematches on Olympus | world-act3's Hierophant, Pantheon and Archon themes (not yet scored: INVENTORY §8) | `MUS_ICHOR_BATTLE_TRAINER` |
| **Iapetos** on the Sirens' skerry | `MUS_ICHOR_BATTLE_ADMIN` with his chorus-of-aulos layer | `MUS_ICHOR_BATTLE_ADMIN` |
| **Odyssey bosses** (the Polyphant, Aeolus, Circe, Hexylla, Trybdis, the Phaeacian games) | `MUS_ICHOR_LABOR_BOSS` | `MUS_ICHOR_BATTLE_TRAINER` |
| **The twelve axes**, with Kleon at the end | `MUS_ICHOR_BATTLE_AXES` (#17) | `MUS_ICHOR_BATTLE_TRAINER` |
| **Hades and Persephone** | `MUS_ICHOR_BATTLE_HADES` (#47) | `MUS_ICHOR_BATTLE_TRAINER` |
| **The five Titans and Briareus** | `MUS_ICHOR_BATTLE_TARTARUS` (#49) | `MUS_VS_REGI` |
| **Giratina** | `MUS_ICHOR_CHASM` (#50, stretch) | `MUS_ICHOR_BATTLE_TARTARUS` |
| **Gaia, Oceanus, Ouranos** (Groudon, Kyogre, Rayquaza) | `MUS_ICHOR_BATTLE_PRIMORDIAL` (proposed, one cue for the three) | `MUS_VS_KYOGRE_GROUDON` (the same song as `MUS_VS_RAYQUAZA`, per songs.h) |
| **The Prime Mover** (Arceus, Lv 95) | `MUS_ICHOR_BATTLE_PRIME_MOVER` (proposed) | `MUS_VS_KYOGRE_GROUDON` |
| **Every other legendary** in the post-game: Celebi, Heatran, Type: Null, Magearna, Marshadow, the satyr five, Manaphy, Lugia, Pontanax, Pegaunos, Ichorin, the Moment, Nike | `MUS_ICHOR_BATTLE_LEGEND` (proposed, one shared cue; 3.5 KiB) | `MUS_VS_MEW` or `MUS_ICHOR_BATTLE_WILD` |
| **The Lord of Time's rematch** | M §8: "the battle, unchanged". world-act3's cue. | act3's |
| **Kleon's post-game battles** | No doc names one. Recommended: the boss cue as above, no Kleos, since he fights beside you. | `MUS_ICHOR_BATTLE_TRAINER` |

Victories: trainers `MUS_ICHOR_VICTORY_TRAINER`, wild `_VICTORY_WILD`, Hierophants and Brains `_VICTORY_LAUREL`, catches `_CAUGHT`.

The Primordial, Prime Mover and legend rows (the last three of the battle rows) are **proposed**: no doc names them (§6).

---

## 5. Composition order, ROM and the rules

### 5.1 Order: most heard first

Heard time follows how long the player stays in a place. The ship is home for the whole post-game, and the Labors fill ten maps. Tiers 1 and 2 also match the batch order, so the maps never wait long on a stand-in.

| Order | Cues | Why first | KiB | Running total |
|---|---|---|---|---|
| **Tier 1** | #1 `EUPLOIA`, #2 `SEA_SAIL`, #3 `SEA_ROW`, #4 `SEA_NIGHT`; #19 `LABOR`, #21 `LABOR_BOSS`; #55 `OLYMPIA`, #57 `OLYMPIAD`, #58 `BATTLE_BRAIN`, #54 `SACRED_WAY`; #20 `HERAION` | The ship, the Labors' route theme, the Olympiad: the post-game's three places you return to most. | 36.5 | 36.5 |
| **Tier 2** | #41 `ASPHODEL`, #37 `MANI_ROAD`, #38 `ORPHEUS`, #39 `DESCENT`, #46 `HOUSE_OF_HADES`, #42 `SHADE_BATTLE`, #51 `ELYSIUM`, #48 `TARTARUS`, #52 `ASCENT`; #28 `THRACE`, #29 `THEMISKYRA`, #31 `ERYTHEIA`, #33 `GARDEN`, #30 `OCEAN_STREAM`, #27 `CROSSING`, #25 `REEDS`, #26 `SKY_BATTLE`, #23 `HIND`; #56 `TEMPLE_ZEUS`, #35 `OLYMPIAS` | The Katabasis's hub and its road, and each Labor's own land. | 64.0 | 100.5 |
| **Tier 3** | #6 `LOTUS`, #9 `AIAIA`, #10 `SIRENS`, #13 `SCHERIA`, #5 `STORM`, #7 `CYCLOPS`, #8 `AIOLIA`, #11 `STRAIT`, #12 `THRINAKIA`; #15 `ELAIA_MIST`, #16 `ELAIA_SUITORS`, #17 `BATTLE_AXES`, #18 `RECOGNITION`, #14 `DEMODOKOS` | The Odyssey is heard once, so its set pieces come after the places the player returns to. | 45.5 | 146.0 |
| **Tier 4** | #36 `KOTINOS`, #47 `BATTLE_HADES`, #49 `BATTLE_TARTARUS`, #43 `CROSSROADS`, #44 `LETHE`, #45 `MNEMOSYNE`, #40 `GATE`, #53 `ELEUSA_SPRING`, #34 `ASCENT_KERBEROS`; stings #22, #24, #59 | Single scenes and one-time boss fights | 25.5 | 171.5 |
| **Tier 5** | #60 `ATLANTIS`, #61 `ATLANTIS_DEEP`, #65 `PRIME_MOVER`, #68 `BATTLE_LEGEND`; the stretch cues #32 `GERYON`, #50 `CHASM` | Atlantis's two themes and the shared legend battle are the only new work in the summit chain. The two stretch cues come last. | 19.0 | 190.5 |

### 5.2 ROM against POSTGAME §7

| Epic | This file's cues | Estimate | The doc's figure |
|---|---|---|---|
| The Odyssey | #1 to #18 | 55.5 KiB | ~60 KiB (ODYSSEY §13) |
| The Labors | #19 to #36 | 52.5 KiB | ~45 KiB (LABORS §10) |
| The Katabasis | #37 to #53 | 51.5 KiB | ~55 KiB (UNDERWORLD §12) |
| Olympia | #54 to #59 | 19.0 KiB | ~20 KiB (POSTGAME §3.1) |
| **Subtotal: what the docs priced** | 59 cues | **178.5 KiB** | **~180 KiB** |
| Atlantis, Primordials, summit | #60 to #68 | 12.0 KiB (the rest stands on kept Hoenn songs) | none (P §3.2, §3.3) |
| Shared cues from other branches | #69 to #72 | 0 here | counted in their own branches |
| **Total new music** | 68 cues | **190.5 KiB** | |

POSTGAME §7's table has **no separate music line**: music sits inside each epic's figure, and §7's total is ~2.0 MiB. This list is about 9% of that total (190.5 of 2,048 KiB) and under 3% of the dex's ~7 MB room for all of Ichor. If the ROM runs short, the stretch cues (#32, #50: 7 KiB) come off first, then #60 and #61 can stay on their stand-ins (7 KiB). Check `make`'s memory line after each tier (CLAUDE.md).

The estimate is the docs' own 3.5 KiB a loop. The Act I `.mid` files run 3 to 8 KiB each before `mid2agb`, which agrees.

### 5.3 The rules, from "What the engine taught us" and MUSIC.md

1. **A sine bass never doubles a DirectSound note in unison.** Keep it an octave under the lowest kithara, aulos or horn note in the cue. This bites hardest in the sea family (#1 to #4): 629's bass and kithara roots differed by up to 4 dB between loop passes. "A swelling drone" under sail (#2) is a bass part, so the same rule holds. Also #7's breathing bass, #39's drone, #48's strings, and #37's.
2. **Harp tails count.** The harp (slot 46) rings a second after each note, and six notes a bar can hold four or five channels. For water sparkle or stars, in the sea cues, Atlantis (#60, #61), the Lake of Mnemosyne (#45) and the Garden's dusk (#33), use a square wave, the triangle or the temple bell.
3. **The music box is reserved** (M rule 2). Slot 10, the glockenspiel, and slot 115, the tick, are Elpis's box and the Frozen Hour's. They may not appear in the night sea's bells (#4), Aiolia's bronze bells (#8), the Heraion's bell (#20), the Mani Road's bell (#37), the Lotus Isle's frozen clock (#6) or the Moment's sting (#59). The box plays only as `MUS_ICHOR_ELPIS_LULLABY_BOX`.
4. **The lullaby resolves only after Elpis** (M rule 1). The post-game is after the resolution, so #71 may sound bar 8. Nothing else may quote the lullaby: not the Lord of Time's rematch, not the House of Hades.
5. **Mom's countersong rides every Elaia variant** (M rule 3, "after Delphoi Elaia's theme always carries it"): #70, and #15, #16 and #18 here. In the mist it is faint. In the suitors' party it is buried under the party tune. At the recognition it comes forward.
6. **All three Fates' voices sound together only at the Loom** (M rule 4): #72. The Labor theme's aulos and frame drum are instruments, not the Fates' parts.
7. **Each motif keeps its owner.** The Sickle (3+2+2+2 grind, tritone) is the Titans', in #48 and #49 only. Kleos is Kleon's. The Labor boss (#21) uses 9/8 as 2+2+2+3 in A Phrygian, which sits between them and is neither.
8. **Sea music follows the wind and the clock.** `sNightMusicTable` (`src/overworld.c`) maps `SEA_SAIL` and `SEA_ROW` to `SEA_NIGHT`. It switches on a map change, as with any night music, so the sailing layer must call a BGM change when the wind goes upwind or calm (an ask to sail-engine). Until then, the sea maps use `SEA_SAIL` only. **No night entries** for the Underworld (U: time of day is ignored) or the Lotus Isle (its clock is stopped).
9. **Layers.** The cues marked *layer* (#2, #7, #10, #12, #19, #29, #33, #34, #40, #52) need track-level control in play. `m4aMPlayVolumeControl(mplayInfo, trackBits, volume)` takes a track bitmask, so a layer is a track at volume 0 or full, and a tempo change is `m4aMPlayTempoControl`. That is a small ask for the ichor-engine session: `special(Ichor_SetMusicLayers)` with a bitmask in `VAR_0x8004`. **Fallback:** a fixed full mix, or separate songs per state swapped on a map change. Every layered cue must pass `compose.py --check` with all its layers ON, since the full band is the worst case for channel steals.
10. **Silence is a cue.** The Styx, the Stable Yard, Lethe and the summit are near or full silence. Use `MUS_DUMMY` or a fade, and don't pad them with a drone.
11. **Loops fill whole frames.** `--check` warns when loop ticks × 150 ÷ tempo isn't a whole number. Pick a nearby even tempo, especially for 7/8, 9/8 and 5/4, whose bar lengths are awkward.
12. **A sting that plays as a fanfare** (#22, #24, #59, and `MUS_ICHOR_THEOXENIA`) needs an `sFanfares` entry in `src/sound.c` with a `FANFARE_*` constant, and it must last at least as long as the song and at most 30 frames more.
13. **A cue that quotes a motif takes the notes from MUSIC.md.** Where MUSIC.md lacks the form, add it there first (§6).

---

## 6. What the docs imply but don't name

Every item below needs a decision or a line in a doc before it can be composed.

| # | What | Where it shows up | What this file did |
|---|---|---|---|
| I1 | **Olympia's five tracks.** POSTGAME §3.1 gives a count and no names or modes. | Batch 2 | Named five (#54 to #58) from MUSIC.md's mode table |
| I2 | **Atlantis.** No cue for the Nereids, the rings, the temple, the nursery or the abyss. | P §3.2 | Proposed `ATLANTIS` and `ATLANTIS_DEEP` (#60, #61), quoting Daphne's Question |
| I3 | **Gaia's cave, Ouranos's sky, the summit.** P §3.3 says the Hoenn songs are re-themed and names no cue. | P §3.3 | Proposed #63 to #65, standing on the kept Hoenn songs |
| I4 | **Primordial, Prime Mover and legend battle themes.** INVENTORY §8 lists "legend beast" among the kept Hoenn themes and no Ichor one. | Batches 7 and 8 | Proposed `BATTLE_PRIMORDIAL`, `BATTLE_PRIME_MOVER`, `BATTLE_LEGEND` |
| I5 | **The finished lullaby.** U scene 14 and Lg §7.1 both play "the version Elpis finished", and X names *The Blessed*. M has no row for the song after the resolution. | Batches 3 and 8 | One cue, #71 (act3's), plus the box variant for Celebi |
| I6 | **Orpheus's lament.** U calls it "the Katabasis's leitmotif", but MUSIC.md has no entry for it: no notes. | Batch 3 | #38. MUSIC.md needs the lament's notation first. |
| I7 | **The main theme in Mixolydian** (Labor 7's Crossing). M §1 has no Mixolydian form. | Batch 5 | #27. MUSIC.md needs it first. |
| I8 | **Elaia with Mom's countersong.** M §3 says it's "for the director to assign" and names nothing. | Batch 1 | Proposed `ELAIA_COUNTERSONG` (#70), act3's |
| I9 | **The Moment's sting.** STORY gives a brief ("never more than two bars") with no constant. | Batch 2 | Proposed `MUS_ICHOR_MOMENT` (#59) |
| I10 | **Eleusa while its fields are gray** (U scene 1). Only the spring return is scored. | Batch 3 | Recommended `MUS_ICHOR_TEMPLE_DEMETER`'s grief form until Eleusa's owner picks |
| I11 | **No cue named** for the Acheron Bank, the Fall (nine days of falling), the five cells, the House of Night, the Western Cape, the Strait of the Pillars, Cyclops Isle, Proteus's islet, Ithaka, Route 34, Rhodos, the Time Fractures and Sky Fractures. | Batches 3 to 8 | Reuse rows in §2, each marked "none named" |
| I12 | **The finale at home** (Zeus and Hermes, the storm night; Sy). A scene with no music line. | Batch 6 | The theoxenia sting, then the Elaia cue in force |
| I13 | **Celebi's skipping music box** (Lg §7.1). A box that "misses a beat" is a new cue, or a script trick. | Batch 8 | Stand-in `MUS_ICHOR_ELPIS_LULLABY_BOX`; the miss is a script pause |
| I14 | **Kleon's post-game battles** and the Kallisto full-moon rematch. | Batches 4 and 5 | The boss cue, no Kleos |
| I15 | **Hierophant, Pantheon, Archon and Kronos battle themes.** world-act3's. | Batches 2 and 5 | Stand-in `MUS_ICHOR_BATTLE_TRAINER`; swap when act3 merges |
| I16 | **Phemios's music player** lists "any song you've heard". That needs a heard-song record per cue. | Batch 6 | Not a cue: an ask for the sail-engine and ichor-engine sessions |
| I17 | **The Pantheon theme's Hera variant** (L §8) needs act3's Pantheon theme to exist. | Batch 5 | #35 stands on the trainer theme |

**Asks that follow.** (1) The director claims a song-id block (§0). (2) sail-engine switches sea music with the wind (§5, rule 8). (3) ichor-engine adds `Ichor_SetMusicLayers` and tempo control (rule 9). (4) The MUSIC.md owner adds Orpheus's lament, the Mixolydian main theme and the post-resolution lullaby (I5 to I7). (5) world-oikoumene takes `MUS_ICHOR_OKEANOS` and the sea tune (C2, C7).
