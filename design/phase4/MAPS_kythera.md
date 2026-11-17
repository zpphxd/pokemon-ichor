# Kythera's maps: briefs and design passes

> **Landed on 2026-11-17 on Samuel's Kythera (from main):** Skandeia, Paphia, the Foam Road, Neraida Falls and the Spring of Kallirhoe, whose layouts were byte-identical to this pass's starting point. Melos and Routes 22–23 aren't in that build; their passes wait on branch `kythera-design-passes-wip`.

Act III's first chapter (STORY III-1), ported from `claude/world-act3-4e546d`
to main in 2026-11. The outdoor maps are built by the generators in
`tools/ichor/maps/` (`kythera_outdoor.py` drives Skandeia, Melos, the three sea
routes and the southern deck; `kythera_foam_road.py`, `kythera_paphia.py`,
`kythera_spring.py`, `kythera_neraida.py` and `kythera_echo_caves.py` build the
rest on `kythera_maps.py`). Edit a generator and rerun it; never hand-edit a
`map.bin` the generators own. `woods.py` plants every wood.

```bash
/usr/bin/python3 tools/ichor/maps/kythera_outdoor.py [skandeia|melos|kythera_seas|euploia_south]
/usr/bin/python3 tools/ichor/maps/kythera_foam_road.py   # and the other four
```

Renders of every pass are in `img/kythera_passes/<map>_p0.png` (as ported)
through `_p3.png` (after the third pass).

## The five-line briefs (STYLE.md §4.6)

**Skandeia, Kythera's harbor**
- Sentence: a shipyard with no ships, its empty slips facing the bay under an olive-dark hill.
- Land: a wooded limestone slope falls east to a sheltered bay; a terrace wall splits the town into the high street and a lower lane; a pocket beach at the south.
- Settlement logic: the quay, Asclepeion and Agora on the only flat ground by the water; houses up the one street that climbs west to the gate and the Foam Road; slips on the north shore where the water is deep; Aphrodite of the Harbor at the quay's end.
- Reveal: stepping off the gangplank, the row of empty slips chalked with sickles, and the Euploia the only hull afloat.
- Signature: the empty, chalk-marked slipways.

**The Foam Road**
- Sentence: a shore road along the bay where Aphrodite came ashore, her foam rock standing in the surf.
- Land: pink limestone cliffs and a quarried scarp step down to a sandy bay; woods on the ridge; a stream falls off the western headland; a sand islet in the bay.
- Settlement logic: the road keeps above the tide line along the cliff foot, forks north at the great herm to the spring, squeezes through the cutting under the sea cliff; the quarry is cut where the stone is; fishers keep to the jetty and the shingle cove.
- Reveal: the road leaves the cutting and the foam rock appears whole in the shallows.
- Signature: Aphrodite's foam rock.

**The Spring of Kallirhoe**
- Sentence: a hidden spring in a myrtle glade where Narcissus kneels at the pool forever.
- Land: a hollow under a pink scarp, the sea cliff on the west, the rock over Echo's caves to the north-east.
- Settlement logic: the spring is holy, so it is ringed with stones and narcissus and left wild; one path climbs from the Foam Road; the cave stair is cut into the rock.
- Reveal: the path comes through the grass and the round pool opens in the glade's heart.
- Signature: Narcissus' round pool in its ring of narcissus.

**Paphia, the temple town**
- Sentence: the Temple of Aphrodite on its terrace above rose gardens and the beach where pilgrims land.
- Land: wooded hills fall south in two terraces to a sandy bay with a spit; a road runs north to the falls.
- Settlement logic: the sanctuary holds the high terrace, reached by one processional stair; houses and sculptors' yards on the terraces; the Agora and Asclepeion on the flat east road; the jetty where the honey boat lands.
- Reveal: from the jetty the pink stair frames the temple whole.
- Signature: rose gardens either side of the processional stair.

**The Neraida falls**
- Sentence: a stepped river valley of mills under a waterfall whose spring has gone quiet.
- Land: the river leaves a high pool, falls over a pink cliff and runs south through kerbed pools to Paphia, terraces on both banks.
- Settlement logic: the mills sit on the race; fields and hives on the terraces; Krenaia's shrine at the falls; a one-way ledge path down the east bank.
- Reveal: climbing the race, the falls appear in the cliff.
- Signature: the watermills on the race.

**Melos (Klima)**
- Sentence: a fishing hamlet of painted boathouses under terraced fields and an obsidian slope.
- Land: a round bay, terraces stepping up, a black-glass scree slope under the wooded crest, pumice cliffs at the west point.
- Settlement logic: boathouses at the water, farms on the terraces, the armless goddess in a niche in the field wall.
- Reveal: the goddess in her niche, watching from the terrace.
- Signature: the boathouses' coloured doors (syrmata) and the obsidian slope.

**Route 22, the Myrtoan Sea**
- Sentence: open water under Cape Malea, surf lanes between reefs.
- Land: the cape's gray cliffs swell out to a point; Melos's wooded shore to the east; Myrtilos's grave islet.
- Settlement logic: reefs break the sea into lanes where swimmers wait; the trireme lane is staked.
- Reveal: the cape's full height from the open water.
- Signature: Cape Malea.

**Route 22, the Cretan Sea**
- Sentence: Melos's eastern arm and the islets toward Kaldera.
- Land: the cape's pine woods and cove, Polyaigos, Anydros in its reef ring, a sandbar.
- Settlement logic: goats on Polyaigos, a fig on Anydros; the reef ring opens only south.
- Reveal: the ring of reef round Anydros.
- Signature: Anydros's reef ring and dead fig.

**Route 23, the Cretan Sea**
- Sentence: the open run south past Antikythera toward Knossa.
- Land: sandbars and Antikythera's green hump with its reef and wreck.
- Settlement logic: a reef line closes the islet's lane; the wreck lies where the reef caught it.
- Reveal: the wreck's ribs in the shallows.
- Signature: the Antikythera wreck.

## The passes

**Pass 1 (structure).** The branch's woods were olives in rows two cells
apart, trunks showing in every other row: a grid. `woods.py` now plants one
canopy wall per wood (crowns stacked, trunks only along the foot), bites a
ragged foot and crown where it meets open ground and stands a cypress or pine
in some bites. Flowers strewn one by one (the Foam Road's anemones, Paphia's
petals, Melos's field) were gathered into beds by signs, doors, shrines and the
goddess's niche. Lone rocks were gathered into skerries and reefs. Skandeia's
quay face steps back into a mooring bay and its north beach pushes out a sandy
point. Cape Malea swells to a point instead of a 60-cell wall with a ruler
line of rocks under it; the reef lines meander a row at most per rock, so they
never leak; Melos's west shore on Route 22 comes and goes. The Neraida falls'
west ledge no longer drops into a three-cell pit (the audit's only FAIL).

**Pass 2 (edges).** `map_style_audit.py` found the long straight edges: Paphia's
beach (24 cells) now has an inlet and a spit; Skandeia's promenade hedge (16)
opens a thrift gap; the Foam Road's cutting and quarry foot (13, 11) have a
fallen block and drum; Melos's 21-cell edge was already gone after pass 1's
woods, leaving wall B's 11-cell coping (a terrace, kept). Woods never bite at a map's side edge, so no
opened cell faces a neighbour's solid seam.

**Pass 3 (polish).** The Spring's glade lost its sprinkled petals and the rocks
strewn round the wood's rim: the narcissus ring is its bed, with two clumps
where the path comes in. The Foam Road's clipped hedges are notched by round
bushes. Route 23's last lone rocks are skerries. Each wood pairs its columns
from its own west edge, so the Neraida falls' east wood is one canopy with a
cypress at its edge, not a column of single cypresses.

Style audit, before (branch) and after pass 3, straight-edge cells: Paphia
24 to 10, Melos 21 to 11, Skandeia 16 to 9, Foam Road 13 to 10, the rest
unchanged at 10 or less. The sea routes' "barren" screens are open sea, as in
Emerald's ocean routes. "No height" is the heuristic missing the tilesets'
own stairs: Skandeia's terrace stair, Paphia's two terraces and processional
stair, the spring's scarp and Melos's terraces all read as height in the
renders.

## Still to do

- Aethos has no grass variant for open ground besides shade and the ledge
  shadow, so open grass stays one metatile; two tuft variants should be drawn.
- Paphia's north road runs straight between its woods; give it a bend and a
  roadside shrine when the falls' south seam is next touched.
- The Neraida race is kerbed straight for twenty rows; a jog at the lower mill
  would read better.
- Route 23's reef shallows are a hard-edged square; the reef needs shallow-water
  edge pieces.
