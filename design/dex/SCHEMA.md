# Aethos dex: entry schema (Gate 2)

How to write a full species entry. `tools/dex/validate.py` enforces everything marked **must**. The finished example is `design/dex/species/laurel.yaml`; match its depth and voice.

## Sources of truth

- `design/dex/plan.yaml` fixes each line's members, order, concept, types, evolution method and level, myth and habitat. Entries **must** match it. If a line needs a structural change, raise it instead of editing the plan.
- `design/PITCH.md` has the places, cast and story. `design/research/LAZARUS.md` has the avoid-list.
- `design/phase1/PLAN.md` has the master palette: Aegean blue, marble, olive, cypress, terracotta, sun-gold, limestone and black-figure ink.

## Files

There is one file per line: `design/dex/species/<line id>.yaml`, holding `line: <id>` and a `species:` list in dex order. Run `python3 tools/dex/validate.py --lines <id>,<id>` on your files until it reports no errors.

## Fields

| Field | Rule |
|---|---|
| `dex` | **Must** equal the plan's number. |
| `concept` | **Must** equal the plan's label. |
| `name` | **Must** be letters only, capitalized, 12 characters at most; aim for 10. **Must** be Greek-rooted, unique in the dex, and not the same as an existing Pokémon. See Names. |
| `etymology` | The roots and their meanings, for example "nebros (Greek, fawn) + laurel". |
| `category` | "The ___ Pokémon". **Must** be 12 characters at most, letters, spaces and hyphens only. |
| `types` | **Must** equal the plan's. |
| `abilities` | 1 or 2 regular abilities, using the expansion's display names. |
| `hidden_ability` | 1 hidden ability, or `null`. **Must** be an existing ability, not a repeat of a regular one. |
| `base_stats` | `hp, atk, def, spa, spd, spe`, each 1–255. The BST is computed. See Stats. |
| `ev_yield` | Stat keys as above. Total **must** be 1–3 and **must** not fall along a line. |
| `exp_yield` | Base experience. First stages about 50–70, middle about 140, final stages 170–270, legendaries 300–340. |
| `catch_rate` | 3–255. Commons 190–255, middle stages 90–120, finals 45–60, starters and pseudos 45, legendaries 3–45. |
| `gender` | `female_pct` set to one of 0, 12.5, 25, 50, 75, 87.5 or 100, or `genderless: true`. |
| `egg_groups` | 1–2 from: Monster, Water 1, Water 2, Water 3, Bug, Flying, Field, Fairy, Grass, Human-Like, Mineral, Amorphous, Dragon, Ditto, Undiscovered. Babies, legendaries and mythicals use Undiscovered. |
| `egg_cycles` | 5–120. Normally 15–25, starters 20, pseudos 40, legendaries 80–120. |
| `growth_rate` | Erratic, Fast, Medium Fast, Medium Slow, Slow or Fluctuating. Keep it the same across a line. |
| `base_friendship` | Optional, default 50. Use 0–35 for legendaries and 70–140 for very friendly species. |
| `height_m`, `weight_kg` | Positive, to one decimal place. |
| `myth` | The specific myth with a source citation, in 1–3 sentences. Stages can share the line's myth. |
| `expression` | How *this stage's* design shows the myth, in 1–2 sentences. |
| `art` | A brief an artist can draw a 64×64 Gen 3 front sprite from. See Art. |
| `shiny` | The shiny palette swap, in one sentence. |
| `dex_entry` | A list of 3–4 lines. See Pokédex text. |
| `habitat` | Where in Aethos, using the bible's place names, with time of day, rarity and how it's found. |
| `learnset` | See Moves. |
| `signature` | 1–2 sentences on the moves or quirk that define it. |
| `new_move` | Normally `null`. A truly new move is a cost, written as `{name, type, effect, why}`. |

## Names

- Each name blends at least one Greek root, real and recognizable, with a second root (Greek or English), the way official names blend. For example: *nebros* "fawn" + laurel = Nebrel; *klados* "branch" + doe = Kladoe.
- Prefer names a 10-year-old can say. Avoid three consonants in a row and silent letters.
- Lines often share a root or a sound, but they don't have to.
- **Never** use a bare myth or cast name: Daphne, Kerberos, Kronos, Talos, Galatea, Kallisto, Ione, Elpis, Kleon, Phaedon, Hyperion, Iapetos, Rhea, Daedalus and so on. Pokémon names are coined (Dialga, not Chronos).
- **Never** use Lazarus's places, characters or prefixes, Muse names, or Aegis-, Gryphon-, Medusa- or Titan- forms.
- The validator rejects exact matches with the 1,025 existing species and warns when a name is within two letters of one. Change any name it warns about unless the resemblance is clearly harmless.

## Stats

Use these BST bands. The validator checks each species against its role's band.

| Role | BST |
|---|---|
| Starters | 309–318 / 405 / 525–535 |
| Route bird (3 stages) | 245–260 / 340–360 / 480–500 |
| Fast early bug | 195–210 / 205–225 / 395–420 |
| Common mammal | 240–265 / 400–430 |
| Ordinary 3-stage lines | 280–330 / 380–430 / 480–535 |
| Ordinary 2-stage lines | 250–340 / 420–510 |
| Babies | 180–250 |
| Mascot middle / final | 300–330 / 480–495 |
| Magikarp role | 190–210 / 520–545 |
| Fossils | 340–380 / 480–525 |
| Single-stage oddities | 380–510 |
| Pseudo-legendary | 300 / 420 / 600 exactly |
| Legendary trio | 570–590 |
| Box legendaries | 670–690 |
| Pegasus | 570–590 |
| Mythicals | 600 exactly |

- Spread the stats to fit the myth and the role. A Hierophant's ace should be good at something. Not every final stage needs high Speed.
- BST **must** rise along each line.
- EV yield follows the role: 1 for first stages, 2 for middle stages and two-stage finals, 2–3 for three-stage finals, 3 for legendaries. Give EVs in the stat the species is best at.

## Moves

`learnset` has three lists. Write moves by their exact display names in the expansion, such as `Fire Fang`, `U-turn` or `Will-O-Wisp`. The validator **must** find each one.

- **`level_up`**: a list of `[level, move]` pairs, in order. Levels are 0–100, and 0 means "learned on evolving".
  - First stages: 10–16 moves, starting with 2–3 at level 1.
  - Evolved stages: 14–22 moves. Repeat the pre-evolution's moves at the same or later levels, add an evolution move at level 0, and continue to about level 55–65.
  - Early learnsets get a new move every 3–5 levels.
  - Every species **should** learn at least one damaging move of each of its types by level-up. Give STAB a sensible power curve, for example 40 → 60 → 80 → 100+ power.
- **`teachable`**: moves taught by TM or tutor. Ichor's TM list isn't fixed yet, so list what the species could plausibly learn from any generation's TMs and tutors, the way modern games do.
  - 30–70 moves for full species, fewer for very limited ones. Include the usual coverage (Protect, Rest, Sleep Talk, Substitute, Facade, Endure) plus type-fitting moves.
  - Evolved stages keep everything their pre-evolution has and can add more.
- **`egg`**: egg moves, 4–10, on the first stage only (and on the baby where there is one). Later stages leave it empty.
- Use existing moves only. Note a truly new move in `new_move`.

## Pokédex text

- 3–4 lines, each **at most 42 characters**, written as Gen 3 entries are: in-world and a little uncanny.
- Weave the myth in; don't lecture. "It is said…" and "Old shepherds claim…" are the right register. Encyclopedia sentences and modern-world references are not.
- Characters **must** be ASCII letters, digits, spaces and `. , ' ! ? - : ; ( )`, plus `é` and `…`. No straight double quotes and no em dashes, because the Gen 3 charmap lacks them.

## Art

The `art` field is the brief for a 64×64, 16-color front sprite, with color 0 transparent. In 3–5 sentences it covers:

- **Size:** how much of the 64×64 box it fills. Small Pokémon sit at about 32–40 px and the largest fill the box.
- **Silhouette and pose:** three-quarter view facing left, as Gen 3 fronts are.
- **Key features:** the details that carry the myth, which must read at 64 px.
- **Palette:** which master-palette families to use, plus at most one or two type-accent colors, outlined in black-figure ink.
- **Back and follower:** one clause on the back sprite or the follower if anything is special.

Keep each line visually related, so the final stage clearly grows from the first.
