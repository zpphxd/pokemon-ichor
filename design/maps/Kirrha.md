# Kirrha (`Kirrha`)

Built by `tools/ichor/maps/gulf.py`; the hostel's room by `gulf_rooms.py` on `gTileset_Domos`. 28x32, aethos + skiron. North: Route 9 (x 14-17, offset 0). The trireme lands at (16, 26) on the quay.

## Brief

- **Sentence:** Delphoi's port: a crescent of beach below the olive sea, the pilgrims' hostel at the foot of the washed-out Sacred Way, and Apollo Delphinios's rock shrine where he came ashore as a dolphin.
- **Land:** Parnassos's cliff in the north-west with the Kastalian falls coming down it into a pool; the olive sea north-east; a beach and a stone quay into the Gulf; a sea-cliff headland east.
- **Settlement logic:** pilgrims camp where the Sacred Way's stair used to start; the hostel stands on the road from the mountain; the shrine faces the harbor.
- **Reveal:** coming out of the olives, the falls and the sea in one screen.
- **Signature:** the waterfall that ate the Sacred Way's stair.

## People and places

- **Outdoor healer** (12, 11): `HEAL_LOCATION_KIRRHA` and the respawn are (12, 12). The merchant, the guide, the captain at the quay's end (15, 27).
- **The pilgrims' outcamp:** a tent, fire, bedrolls, myrtle staves; a pilgrim who has waited a year.
- **The pilgrims' hostel** (door 21, 8 → `Kirrha_PilgrimsHostel`): Xenarete the keeper (gift: Mystic Water, Kastalian water carried down by a priest); Hesychia, an old melissa of Delphoi (the bee errand: she sends you to Pan's niche in the Korykian Cave for her gold bee; reward Soothe Bell); Lykinos, a pilgrim waiting for the falls.
- **Apollo Delphinios's shrine:** the rock niches with doves and lamps, the bronze tripod altar before it.
- **The fisher and the upturned boat** on the beach.
- Items: an Elixir under the falls, a Big Pearl on the islet; hidden Stardust in the shrine's niches and a Heart Scale under the headland. Water: surf and fishing (`water_tables.py`'s Gulf tables).

## Hooks for later

| Gate | Relic | Where | Behind it |
|---|---|---|---|
| The Kastalian falls | Poseidon's Conch, then the Horn of Achelous | the pool (2-7, 4-5) and the falls (4-5, 1-3) | Route 28 up to Delphoi (Act III, Laurel 8). The stair sign at (9, 1) says the falls took it |
| The islet | Poseidon's Conch | (3-4, 23-24) | a Big Pearl |
| The pilgrims | story | the outcamp | they wait for the way up; when Route 28 opens they can move up the mountain (a scene) |
| Hesychia | story | the hostel | she was a melissa with a girl who "ran away to the islands, with your eyes": Mom (Melitta). She can speak again at the Delphoi reveal |

## Render passes

`img/kirrha_before.png` (four NPCs on open grass), `_pass1.png`, `_pass2.png`, `_after.png` with `_after_walk.png` and `_after_views.png`; the room is `img/kirrha_hostel.png`.
- Pass 1: tall grass in town (no land table), rows of stray boulders where olives didn't make whole blocks, an empty west half.
- Pass 2: no grass in town, whole olive blocks, olives west of the plaza, the camp filled out, an upturned boat.
- Pass 3: the shrine's sign made readable, the bedrolls moved so the camp has no closed pocket.
