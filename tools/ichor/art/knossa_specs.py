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
    if name == "bull_road":
        import knossa_heel as He
        import knossa_road as R
        surf = Co.surf()
        sd = Co.sand_decor()
        rocks = Co.tide_rocks()
        road = {s.key: s for s in R.build()}
        return {
            "symbol": "gTileset_BullRoad", "dir": "bull_road", "label": "BullRoad",
            "doc": "TILES_bull_road.md",
            "title": "the Bull Road, its vineyard terraces and the Bronze Heel",
            "groups": N.groups("minoan", "stone", "foam", "green", "bronze", "terra"),
            "maps": "the Bull Road (`MAP_KNOSSA_BULL_ROAD`), the vineyard terraces "
                    "(`MAP_KNOSSA_BULL_ROAD_VINEYARD`) and the Bronze Heel "
                    "(`MAP_KNOSSA_BRONZE_HEEL`)",
            "images": [("knossa_bull_road.png", "A 240 x 160 screen of the Bull Road: the "
                        "terraces stepping down north, the vineyard, the herd crossing (3x; "
                        "`_1x` is 1x)"),
                       ("knossa_bull_road_wide.png", "A wider stretch: the fork and the great "
                        "herm, the cutting, the labrys door, the beekeeper's hut, Ida's gate"),
                       ("knossa_bronze_heel.png", "The Bronze Heel: Talos's foot, the tide "
                        "pools, the fossil ledge")],
            "sections": [
                ("road", [
                    La.cliff(names_only=["lip_L", "lip", "lip_b", "lip_R", "face_L", "face",
                                         "face_b", "face_R", "side_E", "side_W", "back",
                                         "back_NW", "back_NE", "corner_in_E", "corner_in_W",
                                         "foot_grass", "seep"]),
                    La.terrace(), road["brow"],
                    road["labrys_door"], road["ida_gate"], road["mitato"], road["herm"],
                    road["phrygana"],
                ]),
                ("vineyard", [road["vines"]]),
                ("heel", [
                    He.talos_foot(), He.tide_pools(),
                    K.pick(surf, ["S", "S2", "N", "E", "W", "out_NW", "out_NE", "out_SW",
                                  "out_SE", "in_SE", "in_SW", "in_NE", "in_NW"], w=8, key="surf",
                           notes=surf.notes.replace("Kythera's", "the Bronze Heel's")),
                    K.pick(sd, ["lace", "shells", "wrack", "footprints"], key="sand_decor",
                           notes="On borrowed sand, walkable: `lace` (dried foam), `shells`, "
                                 "`wrack`, `footprints`."),
                    K.pick(rocks, ["tide_rock", "tide_rocks", "rock_sand", "rocks_sand",
                                   "spit_head", "spit_M", "spit_V"], key="rocks", w=7,
                           notes="Kythera's tide rocks: `tide_rock` and `tide_rocks` in the sea "
                                 "(foam round them, animated), `rock_sand` and `rocks_sand` on the "
                                 "beach, and the reef spit, `spit_head` `spit_M` `spit_V`: the "
                                 "Bronze Heel's rocky peninsula out to its tip (walkable; the "
                                 "Metal Coat hides at the tip)."),
                ]),
            ],
            "rows": {"road": 0, "vineyard": 22, "heel": 26},
            "labels": [("labrys_door", [("top_L", "VaultDoor_TL"), ("top", "VaultDoor_T"),
                                        ("top_R", "VaultDoor_TR"), ("foot_L", "VaultDoor_BL"),
                                        ("door", "VaultDoor_B"), ("foot_R", "VaultDoor_BR"),
                                        ("open_top_L", "VaultOpen_TL"), ("open_top", "VaultOpen_T"),
                                        ("open_top_R", "VaultOpen_TR"),
                                        ("open_foot_L", "VaultOpen_BL"),
                                        ("open_door", "VaultOpen_B"),
                                        ("open_foot_R", "VaultOpen_BR")]),
                       ("ida_gate", [("gate_top", "IdaGate_Top"), ("gate", "IdaGate"),
                                     ("open_top", "IdaGate_OpenTop"), ("open", "IdaGate_Open")]),
                       ("tide_pools", [("ledge_skull", "FossilLedge_L"),
                                       ("ledge_dart", "FossilLedge_R"),
                                       ("ledge_gone_L", "FossilLedge_Gone_L"),
                                       ("ledge_gone_R", "FossilLedge_Gone_R")])],
        }
    if name == "palace_minos":
        import knossa_palace as P
        pal = {s.key: s for s in P.build()}
        return {
            "symbol": "gTileset_PalaceMinos", "dir": "palace_minos", "label": "PalaceMinos",
            "doc": "TILES_palace_minos.md", "title": "the Palace of Minos above ground",
            "groups": N.groups("minoan", "fresco", "stone", "green", "terra"),
            "maps": "the Palace of Minos (`MAP_KNOSSA_PALACE`)",
            "images": [("knossa_palace_court.png", "A 240 x 160 screen of the Central Court: "
                        "the bull-leaping lane and its painted line, the Gentle Bull's pen, the "
                        "porticoes, the bull-leapers on the east wall (3x; `_1x` is 1x)"),
                       ("knossa_palace_hill.png", "The palace on its hill from the Bull Road's "
                        "end: the stair up the limestone, the North Entrance and its charging "
                        "bull, the West Court's kouloura, the Theatral Area")],
            "sections": [
                ("court", [pal["paving"], pal["court_works"]]),
                ("walls", [pal["walls"], pal["columns"]]),
                ("fresco", [pal["frescoes"]]),
                ("land", [La.cliff(names_only=["lip_L", "lip", "lip_b", "lip_R", "face_L",
                                               "face", "face_b", "face_R", "side_E", "side_W",
                                               "back", "back_NW", "back_NE", "corner_in_E",
                                               "corner_in_W", "foot_grass"],
                                   notes_extra=" Here it is the palace's hill (Kephala): stack "
                                               "two or three `face` rows along its south and "
                                               "west, the palace's paving on the plateau above, "
                                               "and cut `court_works.stair_*` into it where the "
                                               "Bull Road arrives.")]),
            ],
            "rows": {"court": 0, "walls": 10, "fresco": 18, "land": 21},
            "labels": [("court_works", [("fence_gate", "PenGate")])],
        }
    raise SystemExit(f"knossa_specs: unknown tileset {name}")
