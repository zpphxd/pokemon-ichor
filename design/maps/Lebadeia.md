# Lebadeia

Built by `tools/ichor/maps/kopais.py` (with Route 7, Route 8 and the Kopais katavothres). Renders: `img/lebadeia_before.png`, `_pass1`, `_pass2`, `_after` (with `_after_views`, `_after_walk`), `img/lebadeia_trophoneion_after.png`, `img/lebadeia_honey_house_after.png`.

## Brief

- **Sentence:** a pilgrims' stop in the gorge where the Herkyna leaves the rock: Trophonios's temple, a rest-house for travelers, on its terrace above the springs of Lethe and Mnemosyne, with the oracle's sealed mouth in the cliff behind.
- **Land:** a dark gorge wall across the north; the springs and a grove of planes at its foot; the Herkyna running south past the town into a pool; olives on the slope down to Route 9.
- **Settlement logic:** the temple sits where the pilgrims gather, between the springs they drink from and the road they arrive by. The honey-baker lives by the road, because every pilgrim needs her cakes. The footbridge carries the Kopais road over the stream.
- **Reveal:** coming in from the katavothres, the road crosses the Herkyna and the temple front opens up with the black mouth in the cliff above it.
- **Signature:** the two springs flanking the path to the oracle's mouth.

## What's here

| Thing | Where | What it does |
|---|---|---|
| The Trophoneion (`Lebadeia_Trophoneion`) | door at (15, 14) | The Asclepeion: the healer (`HEAL_LOCATION_LEBADEIA`; respawn at (10, 5) inside), the Pithos, a stall (`ArkadiaApproach_EventScript_Merchant`, which Kirrha, Aigion and Arkadia also use), couches for sleeping pilgrims, the keeper (two Barley Cakes once, and the story of the closed descent) |
| Euanthe's house (`Lebadeia_HoneyHouse`) | door at (5, 15) | Bring her Honey (hidden on Routes 7 and 8): three Sitrus Berries. `FLAG_ICHOR_LEBADEIA_HONEY_TRADE` |
| The springs of Lethe and Mnemosyne | (13-14, 6), (20-21, 6) | Signs today |
| The oracle's mouth | (17, 4) | Sealed: solid, no warp, a sign |
| A pilgrim from Euboia, a traveler, a child | the grove, the meadow, the green | Lore |
| Sitrus Berry (ball), Pearl and Stardust (hidden) | (24, 9); (12, 7), (20, 15) | |

## Hooks for later

Every closed thing here is meant to open. None of them needs work today; the flags and events are in place.

| Hook | Where | Opens with | What's behind it (proposal) |
|---|---|---|---|
| **The Descent of Trophonios** | The stair behind Trophonios's statue in the Trophoneion (roped off, (0-1, 2), the keeper standing in front at (1, 3)) and the sealed mouth in the gorge wall (17, 4) | A story flag: the keeper reopens it, perhaps in the post-game. `FLAG_ICHOR_LEBADEIA_KEEPER_TALK` records that she has told the player | A side quest that follows the myth: drink from Lethe, then Mnemosyne (the two spring signs become scripts), take a honey cake in each hand from Euanthe (`FLAG_ICHOR_LEBADEIA_HONEY_TRADE` marks her as met), go down feet first into a dark cave (Hecate's Torch; the deepest part needs the Three-Flamed Torch). The keeper's line "something answers before the god does" sets up the twist: a Titan voice, or the Lord of Time's echo, has taken the oracle's place. The visitor "returns, but does not laugh" (Route 8's shrine says so): the reward could be an oracle that names a hidden legendary's place, and a Lebadeia NPC who has lost his laugh until you bring it back |
| **Lethe and Mnemosyne as services** | The two springs | Today (any time) | Lethe forgets a move (the move deleter), Mnemosyne remembers one (the move relearner). A natural fit, and it makes Lebadeia worth flying back to |
| **The pilgrim from Euboia** | The grove, (16, 7) | The descent reopening | She is the first to go down; she comes back changed. A seed for Euboia (across the Euripus from Thyrsa) |
| **Euanthe's cakes** | Euanthe's house | The descent reopening | She gives the two honey cakes the descent needs; without them the snakes below won't let you pass |

## Missing pieces (STYLE.md)

- **A Doric temple front.** Lebadeia uses aethos's palaestra (General's gym, retextured). It reads as a civic building, not a temple: no columns, no raised stylobate. A 6x5 temple front with a colonnade and steps would serve every small sanctuary (Lebadeia, Nemea, roadside shrines).
- **A dark-rock cave mouth.** The oracle's mouth and the katavothres' mouths use aethos's warm limestone arch (`0x09F`/`0x0A7`) set into Taygetos's dark face. A mouth drawn in the dark rock would sit better.
- **Inner corners for Taygetos.** The stymphalia kit has lip, face, foot, flanks and rims, but no inner corner where a south face meets a flank; the builder keeps its rock to straight bands for that reason.
