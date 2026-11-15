"""What each Knossa secondary holds: its sections, rows, groups, fronts and the
labels scripts swap. knossa_build.py builds from these."""
from __future__ import annotations

import knossa_lib as N
import kythera_lib as K

SEAMS = """\
| Seam | Tilesets | Rule |
|---|---|---|
| Amnisos's south gap ↔ the Bull Road's north end | amnisos / bull_road | the 6 rows nearest the seam, on both maps, use only `aethos` |
| the Bull Road's south end ↔ the Palace of Minos's north edge | bull_road / palace_minos | 6 rows, both maps |
| the Bull Road's fork ↔ the Bronze Heel | bull_road / bull_road | exempt (one tileset) |
| the Bull Road ↔ the vineyard terraces | bull_road / bull_road | exempt, if it is a connection; a warp through the terrace gap needs nothing |
| the Bull Road's Ida gate ↔ the Ida path | bull_road / ida | a warp through the gate needs nothing; as a connection, 6 rows (or 8 columns), both maps |
| the Ida path ↔ the cradle shrine | ida / ida | exempt |
| Amnisos ↔ the Cave of Eileithyia, the palace ↔ its rooms, the cradle shrine ↔ the Idaean Cave | — | warps, no seam |
"""


def _kythera():
    import kythera_coast as Co
    import kythera_harbor as H
    return Co, H


def spec(name):
    import knossa_land as La
    import knossa_town as T
    Co, H = _kythera()
    if name == "amnisos":
        quay = H.quay()
        surf = Co.surf()
        sd = Co.sand_decor()
        gear = H.gear()
        kaiki = H.kaiki()
        return {
            "symbol": "gTileset_Amnisos", "dir": "amnisos", "label": "Amnisos",
            "doc": "TILES_amnisos.md", "title": "Amnisos, the harbor of Knossa",
            "groups": N.groups("minoan", "fresco", "stone", "foam", "green", "bronze", "terra"),
            "images": [("knossa_amnisos_quay.png", "A 240 x 160 screen of Amnisos's quay at dawn: "
                        "the Titan ships at the mole, the Asclepeion and the Agora, hives on every "
                        "roof (3x; `_1x` is 1x)"),
                       ("knossa_amnisos_town.png", "Amnisos: the quay and the mole, the five "
                        "houses, the cliff and the Cave of Eileithyia's mouth, the south gap")],
            "maps": "Amnisos (`MAP_KNOSSA_AMNISOS`)",
            "sections": [
                ("harbor", [
                    K.pick(quay, ["S", "S_b", "N", "E", "W", "out_SE", "out_SW", "out_NE",
                                  "out_NW", "in_SE", "in_SW", "in_NE", "in_NW", "steps_E",
                                  "steps_S", "ring_S", "N_plank", "S_plank"], w=8, key="quay",
                           notes="Amnisos's quay and the mole that curves out east from it "
                                 "(Kythera's quay kit). Its top is aethos's limestone path "
                                 "(`0x1D9`); these edges finish it where the wall drops into the "
                                 "sea (each borrows aethos's sea). Named by where the sea is: `S` "
                                 "(`S_b` adds a drain, `ring_S` a mooring ring), `N`, `E`, `W`; "
                                 "`out_*` are rounded outer corners, `in_*` the inside of a bend, "
                                 "so the mole can curve. A mole two cells wide is an `N` row over "
                                 "an `S` row. `steps_E` / `steps_S` go down to the water "
                                 "(walkable); `N_plank` takes a gangplank from a ship moored north "
                                 "of the quay, `S_plank` one going down to a boat (walkable). "
                                 "Other edge cells are impassable."),
                    T.titan_trireme(),
                    K.pick(kaiki, ["afloat", "beached"], key="kaiki", w=2,
                           notes=kaiki.notes),
                    K.pick(gear, ["oars", "nets", "rope", "amphorae", "crate", "bollard"],
                           key="gear", notes="Harbor gear on borrowed path (Kythera's): `oars`, "
                           "`nets` (walkable), `rope`, `amphorae`, `crate`, `bollard`. Impassable "
                           "but `nets`."),
                    T.shrine(),
                    H.flags(),
                ]),
                ("town", [T.house_kit()]),
                ("coast", [
                    K.pick(surf, ["S", "S2", "N", "E", "W", "out_NW", "out_NE", "out_SW",
                                  "out_SE", "in_SE", "in_SW", "in_NE", "in_NW"], w=8, key="surf",
                           notes=surf.notes.replace("Kythera's", "Amnisos's")),
                    K.pick(sd, ["lace", "shells", "wrack", "footprints", "sherd_dig"],
                           key="sand_decor",
                           notes="On borrowed sand, walkable: `lace` (dried foam), `shells`, "
                                 "`wrack`, `footprints`, `sherd_dig` (turned earth: Amnisos's "
                                 "beach sherd of amphora #12, and its daily dig spot)."),
                ]),
                ("land", [
                    La.cliff(names_only=["lip_L", "lip", "lip_b", "lip_R", "face_L", "face",
                                         "face_b", "face_R", "side_E", "side_W", "back",
                                         "back_NW", "back_NE", "corner_in_E", "corner_in_W",
                                         "foot_grass", "foot_sand", "foot_sand_rocks",
                                         "foot_sea_L", "foot_sea", "foot_sea_R"]),
                    La.terrace(key="wall", title="The town wall and its terraces",
                               notes="Amnisos's town wall and the terraces the houses climb, in "
                                     "dry-stone Cretan limestone (Kythera's terrace kit). A "
                                     "`top_*` row (walkable, on borrowed grass) over a wall row "
                                     "`L` `M` (`M2`) `R`. **The south gap** to the Bull Road: end "
                                     "the wall `R`, leave the gap (two or three cells of aethos "
                                     "path), start again `L`, a sign beside it. `steps` cuts a "
                                     "stair through a terrace wall (walkable); `niche` holds a "
                                     "votive; `spout` is the town's fountain into a trough."),
                    La.cave_mouth(),
                ]),
            ],
            "rows": {"harbor": 0, "town": 10, "coast": 14, "land": 18},
            "fronts": T.FRONTS,
            "labels": [],
        }
    raise SystemExit(f"knossa_specs: unknown tileset {name}")
