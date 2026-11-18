# Daphni

Apollo's laurels at the top of the Sacred Way, rebuilt (2026-11-18) from the
bare outdoor stop astyra.py's `daphni()` wrote (a healer, a merchant, a sign).
`tools/ichor/maps/sacredway.py` owns the town and its three rooms; astyra.py
no longer calls `daphni()`.

| Map | Size | Tilesets | What it is |
|---|---|---|---|
| Daphni | 40x34 | Aethos + Skiron (was Kalliste) | The village on the pass: the sanctuary in its laurel grove, the lookout, the rest, the laurel-cutter's |
| Daphni_Sanctuary | 14x10 | Aethos + Oikia | Apollo Daphnaios's house: the priestess, an acolyte |
| Daphni_PilgrimsRest | 12x9 | Aethos + Oikia | Iambe's rest for initiates walking to Eleusis |
| Daphni_LaurelHouse | 10x8 | Aethos + Oikia | Dryas the laurel-cutter's cottage |

The rooms use only cells gTileset_Oikia already has (the generator checks), and no two share a layout.
Renders: `design/maps/img/daphni_before.png`, `daphni_pass1.png`, `daphni_pass2.png`, `daphni_after.png`,
`daphni_after_walk.png`, `daphni_after_views.png`.

## Seams, herm, healer

- The Sacred Way runs straight through on rows 16-19, offset 0 both sides; 8 aethos-only columns each side.
- **Travel herm** at (4,15), plaque (5,15), landing (4,16) on the west road (town_herms.py's row and
  ichor_town_herms.h's landing updated; herm_audit passes).
- **Healer** (LOCALID_DAPHNI_HEALER) on the rest's porch at (16,21) behind its counter; HEAL_LOCATION_DAPHNI
  respawns at (16,23). The merchant stands beside her.
- **(9,10)** is a walkable cell: the laurel walk into the grove (an existing save stands there). The
  walk test saves and CONTINUEs on it.

## The town

- **The sanctuary of Apollo Daphnaios** on its paving in the laurel grove (bay laurels, cypresses, stone
  pines), with the god's altar in the court. Inside, the priestess.
- **The prayer laurel** (16,9): a cord tied with a prayer has cut into the bark. Demeter's Sickle cuts it
  free (FLAG_ICHOR_DAPHNI_CORD_CUT); the priestess then gives a laurel crown (King's Rock).
- **The Aigaleo lookout** (A2) up a Pan's Crook face behind the grove: the stone seat Xerxes watched
  Salamis from, the traveler from the east (the Oikoumene's first rumor: the Troad), a Star Piece jar,
  hidden Nugget.
- **The pilgrims' rest:** Iambe (a gift of kykeon: 2 Moomoo Milk) and an initiate who trades two Lum
  Berries for a Honey.
- **The laurel-cutter's cottage:** Dryas, whose gift (a Miracle Seed) waits until after the capital's
  ostracism (FLAG_ICHOR_ASTYRA_OSTRACISM_DONE); his daughter Daphne, Daphne's namesake, outside.
- **The pilgrims' fountain** in the square, the guide, the town sign. Hidden: a Heart Scale at the end
  of the laurel walk, a Big Root behind the rest.

## Hooks for later

| Where | What | Later |
|---|---|---|
| The lookout | the traveler from the east | the Oikoumene's Troad lead (OIKOUMENE_GUIDE); A2's Daphnyad Lv 37 static is not placed (Daphnyad is a starter line, held out of the wild by DISTRIBUTION.md): ask the director before adding it |
| The sanctuary | the priestess's Daphne story | the Vale of Tempe (Daphne's laurel by the river) at the League: a laurel to carry there |
| Dryas | crowns for the Archon's guests | a post-Act-III return when the city crowns its victors |
| The rest | the initiates walking to Eleusis | the Mysteries' night (PITCH Act II) could start or end here |
