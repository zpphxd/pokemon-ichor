# Route 8, the Kopais road, and the Kopais katavothres

Built by `tools/ichor/maps/kopais.py`. Renders: `img/route8_before.png`, `_pass1`, `_pass2`, `_after` (with `_after_views`, `_after_walk`); `img/katavothres_pass1.png`, `_pass2`, `_after`.

## Brief

- **Sentence:** a Mycenaean dike carries the road across Lake Kopais's reeds from Thyrsa to the mountain's foot, where the lake drains into the katavothres; through them, the Herkyna's valley climbs to Lebadeia.
- **Land:** the marsh lake (black water, reed islets) fills the east two-thirds; Mt. Ptoon's spur, pine-wooded and stepped by three dark rock faces, closes the west; the Herkyna's pool and stream run down the valley behind it.
- **Settlement logic:** the dike crosses the marsh where the old kings drained it; eel-fishers work its landings; the road can't climb the spur, so it follows the water into the sinkholes.
- **Reveal:** from the dike, Gla's broken tower on its island; from inside the mountain, daylight at the west mouth and the valley below.
- **Signature:** the dike over the reeds, and the road that goes underground with the lake.

Tilesets: aethos and Stymphalia's marsh, reeds, causeway, boardwalks, river, trees and Taygetos rock (Route 8, 72x26, 12.5 screens); cave_dark (the katavothres, 40x22, dark).

## The walk

| Stretch | Terrain | Trainers | Grass |
|---|---|---|---|
| Thyrsa's olives (aethos strip) | olives, cypresses, the east sign | | band 1 (3) |
| The dike | causeway deck over the marsh, two reed bars to wade | Enchelys (new), Panos | bands 2-3 (reeds, 3 + 3) |
| The landing and the shore road | grass, long grass | Schoinis (new) | |
| The katavothres | dark cave: drain passage, sink hall, brazier hall | Dipsas (new), Agamedes (new) | |
| The Herkyna's valley | pine wood, the stream and its ford, a wayside shrine | Meda, Thyone | bands 4-5 (3 + 2) |

Side areas: the south bank (sand, long reeds, a ledge, the eel-fisher's gift of three Net Balls, Ampelis and Kephalos), the boardwalk into the reeds behind a reed thicket (the Sickle), the valley meadow (Melas, an Ether).

## Hooks for later

| Gate | Where | Relic | Behind it |
|---|---|---|---|
| Gla's island | Route 8, (42-49, 3-7) | Poseidon's Conch | A Big Pearl by the tower. Proposal: the tower's closed door (47, 5) opens later onto the Minyan treasury of Orchomenos |
| The channel's rock | Katavothres, (18-19, 3-4) | Poseidon's Conch | A Deep Sea Scale |
| The handholds | Katavothres, (8, 10): chalk marks on the wet rock, "a draught comes down from above" | **Climbing relic** | Proposal: a shaft up through the spur to a ledge over the lake, or a back way into Trophonios's oracle under Lebadeia |
| The gallery | Katavothres, rubble at (20, 13) | Bronze Hammer (held now) | A Nugget and a hidden Rare Bone by the old bones |
| The boardwalk | Route 8, thicket at (47, 17) | Demeter's Sickle (held now) | An Ultra Ball at the boardwalk's end |
| The brazier | Katavothres, (21-22, 7-8) | Hecate's Torch (held now) | Lights the whole cave for good (`FLAG_ICHOR_BRAZIERS_START + 0x5A`) |
