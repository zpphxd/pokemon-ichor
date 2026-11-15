"""gTileset_Kirrha (the harbor towns) and gTileset_GulfFerry (Panopeus's deck),
every structure by section.

Sections start on fixed rows of the 8-wide metatile sheet (0x200 + row * 8), so
adding to one section never renumbers another. Append new pieces at the end of
their section. kirrha_build.py draws, compiles and catalogs both sets.
"""
from __future__ import annotations

import kirrha_deck
import kirrha_harbor
import kirrha_land
import kirrha_lib as KL
import kirrha_town

# (start row, key, title, blurb) for each tileset
SECTIONS = {
    "kirrha": [
        (0, "harbor", "The waterfront",
         "The grey quay and its steps, bollard and drain; moored boats on aethos's animated "
         "sea (a kaiki, a rowing boat, Panopeus's ferry with its patched sail); nets, crates, "
         "amphorae, an octopus line and the pilgrims' bundles; an upturned boat; the fish "
         "market under the old fig; the Agora stall in its fishing shed; the Kronist's crate."),
        (24, "land", "Parnassos, the groves and the sacred places",
         "The grey cliff band and crags of Parnassos; Delphoi's roofs in the Phaidriades' "
         "cleft and the sacred road's steps; laurels and old planes; the pilgrims' gate; the "
         "fence of Apollo's plain; the altar of Zeus the Assembler; street steps; the rock "
         "in Kirrha's bay; Helike's drowned roofs."),
        (46, "town", "Houses",
         "A kit of house parts (roof rows, storeys, doors, windows, a balcony) and the "
         "households' signs, in Kirrha's limewash and Aigion's ochre; the muleteer's stable."),
    ],
    "aigion": [
        (0, "harbor", "The terrace quay",
         "The same grey quay, steps and bollard, the moored boats and Panopeus's ferry, the "
         "nets and crates (drawn by the same painters as Kirrha's)."),
        (20, "land", "The grove of Zeus and the hillside",
         "Old plane trees (one hollow, with wild bees), the altar of Zeus the Assembler, "
         "the street's stone steps, the grey cliff band the goatherd built against, laurels, "
         "Helike's drowned roofs under the water off the quay."),
        (40, "town", "Houses",
         "The house kit and the households' signs in Aigion's ochre stucco and blue paint."),
    ],
    "gulf_ferry": [
        (0, "deck", "Panopeus's ferry",
         "The hull amidships, the bow and the stern with its steering oar, the deckhouse, "
         "the mast and the patched sail, the goats' pen, the cargo at the bow."),
    ],
}

GROUPS = KL.GROUPS

# Which pieces each town's set carries (both are drawn by the same functions).
PIECES = {
    "kirrha": {
        "harbor": ["quay", "quay_steps", "kaiki", "rowboat", "ferry", "quay_goods", "upturned",
                   "fish_market", "stall", "kronist_crate"],
        "land": ["cliff", "rocks", "delphoi", "cleft", "laurel", "gate", "fence", "bay_rock"],
        "town": ["house", "house_signs", "stable"],
    },
    "aigion": {
        "harbor": ["quay", "quay_steps", "rowboat", "kaiki", "ferry", "quay_goods"],
        "land": ["cliff", "rocks", "laurel", "plane", "plane_hollow", "zeus_altar", "steps",
                 "drowned"],
        "town": ["house_aigion", "house_signs_aigion"],
    },
}


def build(name="kirrha"):
    if name in PIECES:
        made = {"harbor": kirrha_harbor.build(), "land": kirrha_land.build(),
                "town": kirrha_town.build()}
        parts = {}
        for sec, keys in PIECES[name].items():
            by_key = {s.key: s for s in made[sec]}
            parts[sec] = [by_key[k] for k in keys]
    else:
        parts = {"deck": kirrha_deck.build()}
    for key, ss in parts.items():
        for s in ss:
            s.section = key
            KL.finish(s)
    return [(row, parts[key]) for row, key, _, _ in SECTIONS[name]]
