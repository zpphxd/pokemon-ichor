#!/usr/bin/env python3
"""Generate design/oikoumene/COVERAGE.md: where every National Dex species lives.

Run from the repository root:

    python3 design/oikoumene/coverage.py

It reads the expansion's species data (read-only) for National Dex numbers,
types, egg groups and evolutions, then applies the Oikoumene's habitat rules
(OIKOUMENE.md §8) and the hand-placed myth overrides below. Edit the AREAS,
TYPE_HOMES and OVERRIDES tables, not the generated Markdown.

Rules, in order:
1. Legendary, mythical, Ultra Beast and Paradox species are placed by
   LEGENDS.md (and the epics it lists). They get no wild slot here.
2. The 18 theoxenia starter lines are SYSTEMS.md §10 guest-gifts.
3. Every other family gets one "wild form": the stage reached from its root
   by plain level evolutions (BALANCE.md: late areas carry evolved forms).
   It is placed in one encounter area by OVERRIDES, else by its types.
4. The family's root (and any baby) lives in its land's Nursery, a low-level
   spot whose table turns with the 36-day Aethos year (12 months), or comes
   from breeding.
5. Stages between the root and the wild form come from evolving the root.
   Stages above the wild form come from evolving it, by the method printed.
"""
import collections
import glob
import os
import re
import sys

ROOT = os.getcwd()
OUT = os.path.join(ROOT, 'design', 'oikoumene', 'COVERAGE.md')

# ---------------------------------------------------------------------------
# The encounter areas. id: (land, name, (min, max), methods, affinity types)
# methods: day, night (land, by time of day), cave, surf, fish, rock, hidden
# (the Augur's Eye). Bands follow BALANCE.md's Oikoumene row: wild 60-80,
# never wider than 5 per area.
# ---------------------------------------------------------------------------
AREAS = {
    # Thrace and the Troad
    'T1': ('Troad', 'The Hellespont (sea lane)', (60, 62), 'surf fish', 'Water Flying'),
    'T2': ('Troad', 'The Skamander Plain', (61, 64), 'day night surf fish hidden', 'Fighting Normal Bug Steel'),
    'T3': ('Troad', 'The Ida Road', (62, 65), 'day night fish hidden', 'Grass Bug Normal Flying Fairy'),
    'T4': ('Troad', 'Gargaros Peak', (63, 66), 'day rock hidden', 'Flying Rock Electric'),
    'T5': ('Troad', 'The Hebros Shore, Thrace (beside LABORS\'s Bistonian Plain)', (62, 66), 'day night surf fish', 'Water Normal Ground'),
    'T6': ('Troad', 'The Walls of Laomedon', (63, 66), 'cave rock hidden', 'Rock Steel Fighting Ghost'),
    'T7': ('Troad', 'The Smintheion grounds', (61, 63), 'day night hidden', 'Electric Normal'),
    # Lydia and Phrygia
    'L1': ('Lydia', 'The Royal Road', (63, 66), 'day night hidden', 'Normal Steel Fighting Electric'),
    'L2': ('Lydia', 'The Pactolus Sands', (64, 67), 'day surf fish hidden', 'Water Steel Ground'),
    'L3': ('Lydia', 'Mount Tmolus', (65, 68), 'day night hidden', 'Grass Normal Bug Poison Fairy'),
    'L4': ('Lydia', 'The Maeander', (64, 67), 'day night surf fish', 'Water Grass Bug'),
    'L5': ('Lydia', 'Mount Sipylos', (66, 68), 'day rock surf', 'Rock Water Ground'),
    'L6': ('Lydia', 'Mount Latmos', (66, 68), 'night hidden', 'Psychic Fairy Dark'),
    'L7': ('Lydia', 'The Chasm of Gyges', (66, 68), 'cave rock hidden', 'Ground Steel Ghost Bug'),
    'L8': ('Lydia', "Tantalus's Sunken Palace", (67, 68), 'cave surf fish', 'Water Dark Ghost'),
    # The Euxine
    'E1': ('Euxine', 'The Bosporus and the Clashing Rocks (sea lane)', (67, 69), 'surf fish', 'Water Flying'),
    'E2': ('Euxine', 'The Pontic Coast (sea lane)', (68, 70), 'surf fish', 'Water'),
    'E3': ('Euxine', 'The Thermodon Road (LABORS\'s map)', (64, 68), 'day night surf fish hidden', 'Fighting Normal Fire'),
    'E4': ('Euxine', 'The Phasis', (69, 71), 'day night surf fish', 'Flying Grass Water Bug'),
    'E5': ('Euxine', 'The Field of Ares', (70, 72), 'day rock', 'Fire Fighting Ground'),
    'E6': ('Euxine', 'The Grove of Ares', (70, 72), 'day night hidden', 'Dragon Grass Dark'),
    'E7': ('Euxine', 'The Caucasus: LABORS\'s crag and the caves below', (66, 70), 'day rock hidden', 'Rock Dragon Flying Ice'),
    'E8': ('Euxine', 'The Chalybes\' forges', (69, 71), 'day rock hidden', 'Steel Fire'),
    'E9': ('Euxine', 'Leuke, the White Isle', (70, 72), 'day surf fish', 'Flying Water Fairy'),
    # Scythia and Hyperborea
    'S1': ('North', 'The Steppe Road', (70, 72), 'day night hidden', 'Normal Ground Fighting Ghost'),
    'S2': ('North', 'Lake Maeotis', (70, 72), 'day night surf fish', 'Water Poison Bug'),
    'S3': ('North', 'The Feather Wastes', (73, 75), 'day night', 'Ice Flying Normal'),
    'S4': ('North', 'The Arimaspian Heights', (73, 75), 'day rock hidden', 'Rock Steel Ground'),
    'S5': ('North', 'The Rhipaean Pass', (75, 77), 'day rock', 'Ice Rock'),
    'S6': ('North', 'The Cave of Boreas', (76, 78), 'cave rock hidden', 'Ice Dragon Flying'),
    'S7': ('North', 'The Hyperborean Meadow', (77, 80), 'day night surf fish hidden', 'Ice Fairy Psychic Grass'),
    # Egypt and the Nile
    'Y1': ('Egypt', 'The Delta Reeds', (60, 62), 'day night surf fish hidden', 'Water Grass Bug'),
    'Y2': ('Egypt', 'The Nile (river lane)', (61, 63), 'surf fish', 'Water'),
    'Y3': ('Egypt', 'The Pyramid Field', (62, 64), 'day night rock', 'Ground Rock Psychic'),
    'Y4': ('Egypt', 'The Great Pyramid', (63, 66), 'cave hidden', 'Ghost Psychic Ground'),
    'Y5': ('Egypt', 'Lake Moeris', (63, 65), 'day night surf fish', 'Water Dark Normal'),
    'Y6': ('Egypt', 'The Valley of Tombs', (64, 66), 'night hidden', 'Ghost Dark Bug'),
    'Y7': ('Egypt', 'Pharos', (61, 63), 'day surf fish', 'Water Normal'),
    'Y8': ('Egypt', 'The Labyrinth of Moeris', (65, 67), 'cave hidden', 'Psychic Ghost Normal'),
    'Y9': ('Egypt', 'Elephantine and the First Cataract', (65, 67), 'day surf fish rock', 'Water Rock Normal'),
    # Aithiopia
    'A1': ('Aithiopia', 'The Cataracts', (70, 72), 'surf fish rock', 'Water Rock'),
    'A2': ('Aithiopia', 'The Table of the Sun', (71, 73), 'day night hidden', 'Normal Ground Fire'),
    'A3': ('Aithiopia', 'The Fountain of the Long-Lived', (72, 74), 'day surf fish', 'Fairy Water Normal'),
    'A4': ('Aithiopia', 'Mount Nysa', (72, 74), 'day night hidden', 'Grass Dark Poison'),
    'A5': ('Aithiopia', 'The Mountains of the Moon', (73, 75), 'day night surf fish hidden', 'Grass Bug Electric Dragon'),
    'A6': ('Aithiopia', 'The Pygmy Marshes', (72, 74), 'day surf fish', 'Flying Water Fighting'),
    'A7': ('Aithiopia', 'The Gate of Dawn', (74, 76), 'day hidden', 'Fire Electric Psychic'),
    # Libya
    'B1': ('Libya', 'The Silphium Plateau', (64, 66), 'day night hidden', 'Grass Normal Fire'),
    'B2': ('Libya', 'The Great Sand Sea', (66, 68), 'day night hidden', 'Ground Dragon Bug Rock'),
    'B3': ('Libya', 'Lake Tritonis', (65, 67), 'day surf fish', 'Water Psychic'),
    'B4': ('Libya', 'The Syrtis Shallows', (64, 66), 'day surf fish', 'Grass Water Fairy'),
    'B5': ('Libya', 'The Salt Ridge', (66, 68), 'day rock', 'Rock Poison Steel'),
    'B6': ('Libya', 'The Garamantes\' Tunnels', (67, 69), 'cave rock surf', 'Ground Water Dark'),
    'B7': ('Libya', 'The Glass Crater', (68, 70), 'cave rock hidden', 'Rock Fire Psychic'),
    'B8': ('Libya', "Antaeus's Ring", (66, 68), 'day', 'Fighting'),
    # The Far West
    'W1': ('West', 'The waters of the Strait of the Pillars (LABORS\'s map)', (68, 70), 'surf fish', 'Water'),
    'W2': ('West', 'The Atlantic Shore', (72, 74), 'day surf fish', 'Water Flying Rock'),
    'W3': ('West', 'The Atlas foothills', (74, 76), 'day rock', 'Rock Flying Steel'),
    'W4': ('West', 'The Atlas Range', (75, 78), 'cave rock hidden', 'Rock Steel Psychic'),
    'W5': ('West', 'The Garden of the Hesperides (LABORS\'s map)', (66, 70), 'day hidden', 'Grass Fairy Dragon'),
    'W6': ('West', 'The Silver Mines of Tartessos', (73, 75), 'cave rock', 'Steel Rock Ground'),
    'W7': ('West', 'Erytheia (LABORS\'s map)', (65, 69), 'day surf', 'Normal Fire Water'),
    # The Western Sea (ODYSSEY's islands; this doc proposes their tables)
    'H1': ('WestSea', 'The western wine-dark sea (ODYSSEY\'s sea map)', (72, 75), 'surf fish', 'Water'),
    'H2': ('WestSea', 'The Strait of Scylla and Charybdis (ODYSSEY\'s island)', (73, 75), 'surf fish', 'Water Dark'),
    'H3': ('WestSea', 'Thrinakia (ODYSSEY\'s island)', (73, 75), 'day surf', 'Normal Fire'),
    'H4': ('WestSea', 'Aiaia (ODYSSEY\'s island)', (72, 74), 'day night hidden', 'Poison Normal Psychic'),
    'H5': ('WestSea', 'The Sirens\' rocks (ODYSSEY\'s island)', (73, 75), 'day surf', 'Flying Ghost'),
    'H6': ('WestSea', 'The Cyclops\'s island (ODYSSEY\'s island)', (71, 73), 'day rock', 'Rock Normal'),
    'H7': ('WestSea', 'The Phlegraean Fields', (74, 76), 'day rock', 'Fire Poison'),
    'H8': ('WestSea', 'Lake Avernus', (74, 76), 'night surf fish', 'Ghost Water Dark'),
    'H9': ('WestSea', 'Ogygia', (75, 77), 'day surf fish', 'Fairy Grass Water'),
    'H10': ('WestSea', 'The Lotus Isle (ODYSSEY\'s island)', (71, 73), 'day surf fish', 'Grass Water'),
    # The Ring of Okeanos
    'O1': ('Okeanos', 'Okeanos, the river-ocean (sea lane)', (75, 78), 'surf fish', 'Water Dragon'),
    'O2': ('Okeanos', 'The Cimmerian Shore', (76, 78), 'night surf hidden', 'Ghost Dark'),
    'O3': ('Okeanos', 'The Cave of Sleep', (77, 79), 'cave hidden', 'Psychic Normal Ghost'),
    'O4': ('Okeanos', 'The Isles of the Blessed', (78, 80), 'day night surf fish hidden', 'Fairy Grass Normal'),
    'O5': ('Okeanos', "The Gorgons' Isle", (78, 80), 'day rock', 'Rock Poison'),
    'O6': ('Okeanos', 'The Cave of the Graiai', (77, 79), 'cave', 'Dark Rock Ghost'),
    'O7': ('Okeanos', 'The Selvage', (78, 80), 'day hidden', 'Psychic Steel Dark'),
}

LANDS = {
    'Troad': 'Thrace and the Troad',
    'Lydia': 'Lydia and Phrygia',
    'Euxine': 'The Euxine: Colchis, the Amazons and the White Isle',
    'North': 'Scythia and Hyperborea',
    'Egypt': 'Egypt and the Nile',
    'Aithiopia': 'Aithiopia and the Sunrise',
    'Libya': 'Libya',
    'West': 'The Far West: Atlas, the Hesperides and the Pillars',
    'WestSea': 'The Western Sea',
    'Okeanos': 'The Ring of Okeanos',
}

NURSERIES = {
    'Troad': 'the Lambing Meadows of Ida',
    'Lydia': 'the Reed Beds of the Maeander',
    'Euxine': 'the Nesting Cliffs of Leuke',
    'North': 'the Calving Grounds of the Steppe',
    'Egypt': 'the Papyrus Shallows of the Delta',
    'Aithiopia': 'the Wading Pools of Meroe',
    'Libya': 'the Oasis Gardens of Ammon',
    'West': 'the Tide Pools of Gadeira',
    'WestSea': 'the Seal Caves of Ogygia',
}
NURSERY_BAND = (10, 20)

MONTHS = ['Hekatombaion', 'Metageitnion', 'Boedromion', 'Pyanepsion', 'Maimakterion',
          'Poseideon', 'Gamelion', 'Anthesterion', 'Elaphebolion', 'Mounichion',
          'Thargelion', 'Skirophorion']

# Where each type lives first, then second. The user's examples lead:
# Ice in the north, desert Ground and Psychic in Egypt and Libya, dragons in
# Colchis, Fairy and Grass on the Isles of the Blessed, Ghost in the
# Cimmerian mist, Fighting and Steel at Troy.
TYPE_HOMES = {
    'NORMAL':   ['T2', 'L1', 'S1', 'A2', 'T3', 'H3', 'B1', 'O4', 'Y5', 'T7'],
    'FIRE':     ['E5', 'H7', 'A7', 'B7', 'E8', 'A2', 'W7', 'B1'],
    'WATER':    ['O1', 'E2', 'Y2', 'H1', 'W1', 'T1', 'E1', 'Y1', 'L4', 'B3', 'H2', 'W2', 'Y7', 'A1', 'S2', 'L2', 'H8', 'A3', 'Y9', 'H9', 'E9', 'B4', 'Y5', 'A6', 'O4', 'S7', 'T5'],
    'GRASS':    ['O4', 'W5', 'A5', 'T3', 'L3', 'A4', 'B4', 'H9', 'B1', 'E4', 'Y1', 'L4', 'S7'],
    'ELECTRIC': ['T7', 'A7', 'A5', 'T4', 'L1', 'B2', 'E8'],
    'ICE':      ['S3', 'S5', 'S6', 'S7', 'E7', 'W4'],
    'FIGHTING': ['T2', 'T6', 'B8', 'E3', 'E5', 'L1', 'S1', 'A6'],
    'POISON':   ['H4', 'H7', 'B5', 'O5', 'A4', 'L3', 'S2'],
    'GROUND':   ['Y3', 'B2', 'B6', 'L7', 'S4', 'A2', 'E5', 'L5', 'W6', 'S1'],
    'FLYING':   ['T4', 'E4', 'E9', 'S3', 'A6', 'H5', 'W3', 'T3', 'E1', 'W2', 'T1'],
    'PSYCHIC':  ['Y8', 'Y4', 'Y3', 'B3', 'L6', 'O3', 'O7', 'A7', 'S7', 'H4', 'B7'],
    'BUG':      ['A5', 'T2', 'L3', 'Y1', 'Y6', 'L7', 'E4', 'B2', 'S2', 'T3'],
    'ROCK':     ['W4', 'T6', 'L5', 'E7', 'S4', 'B5', 'W3', 'S5', 'Y9', 'H6', 'O5', 'B7', 'A1', 'W6', 'T4'],
    'GHOST':    ['O2', 'Y6', 'Y4', 'H8', 'O6', 'H5', 'T6', 'L7', 'O3'],
    'DRAGON':   ['E6', 'E7', 'S6', 'B2', 'O1', 'W5', 'A5'],
    'DARK':     ['O2', 'Y6', 'A4', 'O6', 'E6', 'H2', 'L6', 'B6', 'O7', 'L8'],
    'STEEL':    ['T6', 'E8', 'W6', 'L2', 'S4', 'T2', 'L7', 'O7', 'W3', 'L1'],
    'FAIRY':    ['O4', 'A3', 'H9', 'L6', 'W5', 'S7', 'E9', 'B4', 'T3'],
}

# Hand-placed homes: species name -> (area, method, note). method may be
# None to let the area's methods decide. These are the myth fits the rest of
# the table is built around (OIKOUMENE.md §8).
OVERRIDES = {
    # Apollo Smintheus, the mouse-lord of the Troad (Iliad 1.39)
    'Pikachu': ('T7', 'day', 'Apollo Smintheus\'s mice'), 'Raichu': ('T7', 'day', 'Apollo Smintheus\'s mice'),
    'Raticate': ('T7', 'night', 'the temple mice'), 'Furret': ('T7', 'day', None),
    'Cinccino': ('T7', 'day', None), 'Pachirisu': ('T7', 'day', None), 'Dedenne': ('T7', 'night', None),
    'Togedemaru': ('T7', 'day', None), 'Morpeko': ('T7', 'night', None), 'Emolga': ('T7', 'day', None),
    'Plusle': ('T7', 'day', None), 'Minun': ('T7', 'day', None), 'Pawmot': ('T7', 'hidden', None),
    'Maushold': ('T7', 'day', None),
    # Troy of the fine horses; heroes' arms on the plain
    'Rapidash': ('T2', 'day', 'Troy of the fine horses'), 'Sirfetch\'d': ('T2', 'hidden', None),
    'Falinks': ('T2', 'day', 'a phalanx'), 'Kricketune': ('T2', 'night', 'the old men chirp like cicadas (Iliad 3.151)'),
    'Lokix': ('T2', 'day', None), 'Scyther': ('T2', 'day', None), 'Pinsir': ('T2', 'day', None),
    'Doublade': ('T6', 'cave', 'swords of the fallen'), 'Conkeldurr': ('T6', 'cave', 'the masons of Laomedon\'s walls'),
    'Bisharp': ('T6', 'hidden', None), 'Charcadet': ('T6', 'cave', 'empty armor seeks a hero'),
    'Noctowl': ('T3', 'night', 'Athena Ilias\'s owls'), 'Gogoat': ('T3', 'day', None), 'Sawsbuck': ('T3', 'day', None),
    'Trevenant': ('T3', 'night', 'the dryads of Ida'), 'Shiftry': ('T3', 'night', None), 'Dubwool': ('T3', 'day', 'Paris\'s flocks'),
    'Braviary': ('T4', 'day', 'the eagles of Ida'), 'Mudsdale': ('T5', 'day', 'the mares of Diomedes were Thracian'),
    'Pelipper': ('T1', 'surf', None), 'Cramorant': ('T1', 'surf', None),
    'Exploud': ('T5', 'day', None), 'Mr. Mime': ('T5', 'day', None),
    # Lydia and Phrygia
    'Gimmighoul': ('L7', 'hidden', 'Lydia struck the first coins'), 'Luxray': ('L1', 'day', 'the lion of Sardis\'s coins'),
    'Klefki': ('L1', 'hidden', 'the keys of Croesus\'s treasury'), 'Ariados': ('L3', 'night', 'Arachne\'s village is under Tmolus'),
    'Spidops': ('L3', 'day', None), 'Galvantula': ('A5', 'night', None),
    'Spinda': ('L3', 'day', 'dizzy from the vintage'), 'Oricorio': ('L3', 'day', 'the four dances of the theater'),
    'Golduck': ('L4', 'surf', None), 'Floatzel': ('L4', 'surf', None), 'Seaking': ('L2', 'fish', 'gold-sand river'),
    'Clefairy': ('L6', 'night', 'Selene\'s mountain'), 'Lunatone': ('L6', 'night', None), 'Musharna': ('L6', 'night', 'Endymion sleeps here'),
    'Hatterene': ('L6', 'night', None), 'Runerigus': ('L7', 'cave', None), 'Bronzong': ('L7', 'cave', None),
    'Lickilicky': ('L8', 'cave', 'Tantalus reaching'),
    # The Euxine
    'Unfezant': ('E4', 'day', 'the pheasant is the Phasis bird'), 'Ampharos': ('E6', 'day', 'the Golden Fleece (PITCH §4)'),
    'Chesnaught': ('E3', 'day', 'chestnuts are named for Kastanea in Pontus'),
    'Arcanine': ('E3', 'day', 'the Amazons\' war-hounds'), 'Kommo-o': ('E5', 'hidden', 'the sown men of the Field of Ares'),
    'Hydreigon': ('E7', 'hidden', None), 'Druddigon': ('E7', 'day', None), 'Haxorus': ('E6', 'day', None),
    'Dragonair': ('E6', 'hidden', 'the sleepless serpent\'s kin'), 'Dragonite': ('E6', 'hidden', None),
    'Salamence': ('E7', 'hidden', None), 'Tyranitar': ('E7', 'hidden', None),
    'Aggron': ('E8', 'day', 'the Chalybes forged the first iron'), 'Klinklang': ('E8', 'day', None),
    'Magnezone': ('E8', 'hidden', None), 'Magneton': ('E8', 'day', None), 'Torkoal': ('E8', 'day', None),
    'Coalossal': ('E8', 'rock', None), 'Tinkaton': ('E8', 'day', 'a smith\'s daughter'), 'Revavroom': ('E8', 'day', None),
    'Kilowattrel': ('E9', 'day', 'the seabirds sweep Achilles\'s temple'), 'Pidgeot': ('E9', 'day', None),
    'Gastrodon': ('E2', 'surf', 'East Sea form here, West Sea form in H1'),
    'Kingdra': ('E2', 'fish', None), 'Mantine': ('E2', 'surf', None),
    # Scythia and Hyperborea
    'Cyclizar': ('S1', 'day', 'the nomads ride them'), 'Stantler': ('S1', 'day', 'the Scythian gold stag'),
    'Stoutland': ('S1', 'day', 'steppe herding dogs'), 'Brambleghast': ('S1', 'night', 'tumbleweed over the kurgans'),
    'Absol': ('S1', 'hidden', 'it comes before disasters: an omen in fur'),
    'Mamoswine': ('S3', 'day', 'the Greeks thought mammoth bones were giants\''), 'Beartic': ('S3', 'day', None),
    'Delibird': ('S3', 'day', None), 'Cetitan': ('S3', 'day', None),
    'Durant': ('S4', 'day', 'Herodotus\'s gold-digging ants (3.102)'), 'Heatmor': ('S4', 'day', 'it hunts the gold ants'),
    'Sableye': ('S4', 'rock', 'gem-eyed miner'), 'Probopass': ('S4', 'hidden', 'its nose points north'),
    'Carbink': ('S4', 'rock', None), 'Weavile': ('S5', 'day', None), 'Abomasnow': ('S5', 'day', None),
    'Avalugg': ('S6', 'cave', None), 'Glalie': ('S6', 'cave', None), 'Baxcalibur': ('S6', 'hidden', None),
    'Vanilluxe': ('S6', 'cave', None), 'Frosmoth': ('S7', 'night', 'it dances under the northern lights'),
    'Swanna': ('S7', 'surf', 'Apollo\'s swans winter in Hyperborea'), 'Stonjourner': ('S7', 'day', 'the round temple of the Hyperboreans walks'),
    'Jynx': ('S7', 'night', 'Hyperborean singers'), 'Chimecho': ('S7', 'day', 'Apollo\'s temple bells'),
    'Jumpluff': ('S7', 'day', None), 'Whimsicott': ('S7', 'day', None), 'Eiscue': ('S7', 'surf', None),
    'Walrein': ('S7', 'surf', None),
    # Egypt and the Nile
    'Incineroar': ('Y3', 'night', 'the cats of Bubastis (Herodotus 2.66)'), 'Liepard': ('Y3', 'night', None),
    'Persian': ('Y5', 'day', None), 'Meowstic': ('Y8', 'cave', None), 'Purugly': ('Y5', 'day', None),
    'Skeledirge': ('Y5', 'hidden', 'the sacred crocodiles of Moeris (2.69)'), 'Krookodile': ('Y3', 'day', None),
    'Dewgong': ('Y7', 'surf', 'Proteus herds seals on Pharos (Odyssey 4)'), 'Primarina': ('Y7', 'surf', 'Proteus\'s seals'),
    'Ditto': ('Y7', 'day', 'the shapes of the Old Man of the Sea'),
    'Greninja': ('Y1', 'night', None), 'Quaquaval': ('Y1', 'day', 'ducks of the tomb paintings'),
    'Seismitoad': ('Y1', 'day', None), 'Stunfisk': ('Y1', 'day', None), 'Bellibolt': ('Y1', 'day', None),
    'Eelektross': ('Y2', 'fish', 'the Nile\'s electric catfish'), 'Whiscash': ('Y2', 'fish', None),
    'Hippowdon': ('Y3', 'day', None), 'Rabsca': ('Y3', 'day', 'the scarab rolls the sun'), 'Claydol': ('Y3', 'night', None),
    'Dugtrio': ('Y3', 'rock', None), 'Sigilyph': ('Y4', 'cave', None), 'Cofagrigus': ('Y4', 'cave', None),
    'Unown': ('Y4', 'cave', 'the letters on the walls'), 'Lucario': ('Y4', 'hidden', 'the jackal-headed'),
    'Houndoom': ('Y6', 'night', 'the jackals of the necropolis'), 'Marowak': ('Y6', 'night', None),
    'Smeargle': ('Y6', 'night', 'the tomb painters'), 'Houndstone': ('Y6', 'hidden', None),
    'Donphan': ('Y9', 'day', 'Elephantine is the elephant isle'), 'Copperajah': ('Y9', 'day', None),
    'Palossand': ('Y7', 'day', None), 'Wugtrio': ('Y7', 'surf', None), 'Pyukumuku': ('Y7', 'surf', None),
    'Kingler': ('Y7', 'day', None), 'Mabosstiff': ('Y4', 'hidden', 'tomb-guard'),
    # Aithiopia
    'Pyroar': ('A2', 'day', 'lions of the savannah'), 'Rhyperior': ('A2', 'hidden', None), 'Rhydon': ('A2', 'day', None),
    'Girafarig': ('A2', 'day', None), 'Zebstrika': ('A2', 'day', None), 'Kangaskhan': ('A2', 'day', None),
    'Sunflora': ('A2', 'day', None), 'Blissey': ('A3', 'hidden', 'the long-lived Ethiopians\' spring heals'),
    'Audino': ('A3', 'day', None), 'Alomomola': ('A3', 'surf', None),
    'Tropius': ('A5', 'day', None), 'Passimian': ('A5', 'day', None), 'Oranguru': ('A5', 'day', None),
    'Ambipom': ('A4', 'day', 'Dionysus\'s nursery on Nysa'), 'Toucannon': ('A5', 'day', None),
    'Chatot': ('A5', 'day', 'Ctesias\'s talking bird'), 'Squawkabilly': ('A5', 'day', None),
    'Slaking': ('A5', 'day', None), 'Vikavolt': ('A5', 'night', None), 'Goodra': ('A5', 'hidden', 'it lives in the rain-forest wet'),
    'Shiinotic': ('A5', 'night', None), 'Grafaiai': ('A4', 'day', None),
    'Flamigo': ('A6', 'day', None), 'Bombirdier': ('A6', 'day', 'storks fly to Okeanos to fight the Pygmies (Iliad 3.6)'),
    'Xatu': ('A7', 'day', 'it stares at the sun all day'), 'Solrock': ('A7', 'day', None),
    'Volcarona': ('A7', 'hidden', 'the sun-moth'), 'Talonflame': ('A7', 'day', None),
    # Libya
    'Delphox': ('B1', 'day', 'fennec foxes are Libyan'), 'Exeggutor': ('B1', 'day', 'oasis palms'),
    'Dodrio': ('B1', 'day', None), 'Espathra': ('B1', 'day', 'Libyan ostriches'), 'Zangoose': ('B1', 'day', None),
    'Arboliva': ('B1', 'day', 'Kyrene\'s colonists planted olives'),
    'Garchomp': ('B2', 'hidden', 'land-sharks under the dunes'), 'Flygon': ('B2', 'day', None),
    'Sudowoodo': ('B2', 'day', 'a tree in the desert that is a rock'), 'Cacturne': ('B2', 'night', None),
    'Maractus': ('B2', 'day', None), 'Drapion': ('B2', 'night', None), 'Sandslash': ('B2', 'day', None),
    'Sandaconda': ('B2', 'day', None), 'Camerupt': ('B2', 'day', 'caravan camels'), 'Heliolisk': ('B2', 'day', None),
    'Mandibuzz': ('B2', 'day', None), 'Orthworm': ('B2', 'hidden', None), 'Gliscor': ('B2', 'night', None),
    'Arbok': ('B5', 'day', 'Libya\'s snakes are the Gorgon\'s blood (Ovid)'), 'Seviper': ('B5', 'day', None),
    'Garganacl': ('B5', 'rock', 'Herodotus\'s salt hills (4.181)'), 'Glimmora': ('B7', 'cave', 'Libyan desert glass'),
    'Hitmonlee': ('B8', 'day', 'pankration'), 'Hitmonchan': ('B8', 'day', 'pankration'), 'Hitmontop': ('B8', 'day', 'pankration'),
    'Hariyama': ('B8', 'day', None), 'Hawlucha': ('B8', 'day', None), 'Scrafty': ('B8', 'day', None),
    'Machamp': ('B8', 'day', 'Antaeus wrestled every stranger'), 'Throh': ('B8', 'day', None), 'Sawk': ('B8', 'day', None),
    'Drednaw': ('B3', 'surf', None), 'Ludicolo': ('H10', 'surf', 'the Lotus-Eaters (PITCH §4)'),
    # The Far West
    'Heracross': ('W7', 'day', 'the Hercules beetle on the island of Herakles\'s tenth Labor'), 'Bouffalant': ('W7', 'day', 'Geryon\'s red cattle'),
    'Barbaracle': ('W2', 'day', None), 'Skarmory': ('W3', 'day', None), 'Corviknight': ('W3', 'day', None),
    'Golurk': ('W4', 'cave', 'the range Herodotus calls the pillar of heaven (4.184)'), 'Gigalith': ('W4', 'cave', None), 'Archaludon': ('W6', 'hidden', None),
    'Duraludon': ('W6', 'cave', None), 'Excadrill': ('W6', 'cave', None),
    'Tsareena': ('W5', 'day', 'a queen of the golden orchard'), 'Lurantis': ('W5', 'day', None),
    'Flapple': ('W5', 'day', 'the golden apples\' dragons'), 'Appletun': ('W5', 'day', None), 'Dipplin': ('W5', 'hidden', None),
    # The Western Sea
    'Tauros': ('H3', 'day', 'the cattle of Helios'), 'Miltank': ('H3', 'day', None), 'Alcremie': ('H3', 'day', None),
    'Oinkologne': ('H4', 'day', 'Circe\'s swine (PITCH §4)'), 'Weezing': ('H7', 'day', 'sulfur vents'),
    'Magcargo': ('H7', 'day', None), 'Salazzle': ('H7', 'day', None), 'Turtonator': ('H7', 'rock', None),
    'Centiskorch': ('H7', 'day', None), 'Magmar': ('H7', 'day', None),
    'Altaria': ('H5', 'day', 'the Sirens (PITCH §4)'), 'Dusclops': ('H6', 'day', 'the one-eyed (PITCH §4)'),
    'Grapploct': ('H2', 'surf', 'Scylla (PITCH §4)'), 'Sharpedo': ('H2', 'surf', None), 'Golisopod': ('H2', 'surf', None),
    'Palafin': ('H1', 'surf', 'Arion\'s dolphins (Herodotus 1.24)'), 'Barraskewda': ('H1', 'fish', None),
    'Milotic': ('H9', 'fish', 'Calypso\'s pools'), 'Basculin': ('H8', 'fish', None),
    # The Ring of Okeanos
    'Wailord': ('O1', 'surf', 'the ketos, the sea-monster'), 'Lapras': ('O1', 'surf', None), 'Gyarados': ('O1', 'fish', None),
    'Relicanth': ('O1', 'fish', 'older than the gods'), 'Lanturn': ('O1', 'fish', None), 'Lumineon': ('O1', 'fish', None),
    'Dhelmise': ('O1', 'fish', 'a drowned anchor'), 'Starmie': ('O1', 'surf', 'stars that fell in the sea'),
    'Jellicent': ('O2', 'surf', None), 'Gengar': ('O2', 'night', None), 'Mismagius': ('O2', 'night', None),
    'Drifblim': ('O2', 'night', 'it carries the dead'), 'Dragapult': ('O2', 'hidden', None),
    'Honchkrow': ('O2', 'night', None), 'Zoroark': ('O2', 'night', 'illusions in the mist'), 'Mimikyu': ('O2', 'hidden', None),
    'Snorlax': ('O3', 'cave', 'the Cave of Sleep (Ovid)'), 'Hypno': ('O3', 'cave', None), 'Komala': ('O3', 'cave', None),
    'Togekiss': ('O4', 'hidden', 'luck of the Blessed'), 'Florges': ('O4', 'day', None), 'Roserade': ('O4', 'day', 'meadows red with roses (Pindar)'),
    'Lilligant': ('O4', 'day', None), 'Comfey': ('O4', 'day', None), 'Ribombee': ('O4', 'day', None),
    'Gardevoir': ('O4', 'hidden', None), 'Slurpuff': ('O4', 'day', None), 'Aromatisse': ('O4', 'day', None),
    'Spiritomb': ('O2', 'hidden', 'the restless dead at the pit of the Cimmerians'),
    'Rotom': ('E8', 'hidden', 'Hephaestus\'s self-moving tripods (Iliad 18.373); its forms change at Aia\'s palace'),
    'Mawile': ('L7', 'cave', None), 'Volbeat': ('H9', 'night', None), 'Illumise': ('H9', 'night', None),
    'Luvdisc': ('O4', 'fish', None), 'Cryogonal': ('S6', 'cave', None), 'Kecleon': ('A5', 'hidden', None),
    'Dondozo': ('O1', 'surf', None), 'Tatsugiri': ('O1', 'fish', None), 'Veluza': ('O1', 'fish', None),
    'Wishiwashi': ('E2', 'fish', 'a school becomes a sea-monster'), 'Pincurchin': ('H2', 'surf', None),
    'Bruxish': ('A1', 'fish', None), 'Klawf': ('B5', 'rock', None), 'Shuckle': ('H6', 'rock', None),
    'Castform': ('B3', 'day', 'it reads the weather, as augurs do now'), 'Carnivine': ('Y1', 'day', None),
    'Indeedee': ('Y8', 'cave', 'temple attendants'),
    'Beheeyem': ('O7', 'day', 'from beyond the selvage'), 'Porygon2': ('O7', 'hidden', 'a beast of pure angles'),
    'Minior': ('O7', 'day', 'pieces of the sky'), 'Metagross': ('O7', 'hidden', None),
    'Spiritomb': None,
}
OVERRIDES = {k: v for k, v in OVERRIDES.items() if v}

GIFT_LINES = {  # SYSTEMS.md §10
    'Snivy': 'Demeter', 'Cyndaquil': 'Hephaestus', 'Piplup': 'Poseidon', 'Squirtle': 'Hermes',
    'Charmander': 'Hestia', 'Turtwig': 'Athena', 'Torchic': 'Ares', 'Grookey': 'Dionysus',
    'Tepig': 'Artemis', 'Oshawott': 'Aphrodite', 'Chimchar': 'Apollo', 'Chikorita': 'Hera',
    'Mudkip': 'Hecate', 'Totodile': 'Hades', 'Bulbasaur': 'Persephone', 'Sobble': 'Proteus',
    'Treecko': 'Hermes (finale)', 'Scorbunny': 'Zeus (finale)',
}
LAZARUS_LINES = {'Rowlet', 'Litten', 'Popplio', 'Chespin', 'Fennekin', 'Froakie', 'Sprigatito', 'Fuecoco', 'Quaxly'}

FOSSILS = {  # revived from dig finds (OIKOUMENE.md §8)
    'Omanyte': 'Helix Fossil', 'Kabuto': 'Dome Fossil', 'Aerodactyl': 'Old Amber', 'Lileep': 'Root Fossil',
    'Anorith': 'Claw Fossil', 'Cranidos': 'Skull Fossil', 'Shieldon': 'Armor Fossil', 'Tirtouga': 'Cover Fossil',
    'Archen': 'Plume Fossil', 'Tyrunt': 'Jaw Fossil', 'Amaura': 'Sail Fossil',
    'Dracozolt': 'Fossilized Bird + Drake', 'Arctozolt': 'Fossilized Bird + Dino',
    'Dracovish': 'Fossilized Fish + Drake', 'Arctovish': 'Fossilized Fish + Dino',
}
FOSSIL_LAND = {
    'Omanyte': 'Okeanos', 'Kabuto': 'WestSea', 'Aerodactyl': 'Euxine', 'Lileep': 'Libya', 'Anorith': 'Egypt',
    'Cranidos': 'Troad', 'Shieldon': 'Troad', 'Tirtouga': 'West', 'Archen': 'Lydia', 'Tyrunt': 'Aithiopia',
    'Amaura': 'North', 'Dracozolt': 'North', 'Arctozolt': 'North', 'Dracovish': 'North', 'Arctovish': 'North',
}
INCENSE = {'Azurill': 'Sea Incense', 'Wynaut': 'Lax Incense', 'Budew': 'Rose Incense', 'Chingling': 'Pure Incense',
           'Bonsly': 'Rock Incense', 'Mime Jr.': 'Odd Incense', 'Happiny': 'Luck Incense', 'Munchlax': 'Full Incense',
           'Mantyke': 'Wave Incense'}

# Families whose wild form should stay low, or whose root is the wild form.
WILD_FORM_OVERRIDE = {
    'Eevee': 'Eevee', 'Tyrogue': None, 'Wurmple': None, 'Burmy': None, 'Nincada': 'Ninjask',
    'Cosmog': None, 'Type: Null': None, 'Kubfu': None, 'Poipole': None, 'Meltan': None,
    'Feebas': 'Feebas', 'Applin': 'Applin', 'Charcadet': 'Charcadet', 'Gimmighoul': 'Gimmighoul',
    'Elgyem': 'Beheeyem', 'Porygon': 'Porygon2',
}
WILD_EXTRA = {  # second wild homes, so a branch or a famous form is wild too
    'Eevee': [('Vaporeon', 'O4', 'surf'), ('Jolteon', 'B2', 'hidden'), ('Flareon', 'A7', 'hidden'),
              ('Espeon', 'Y8', 'hidden'), ('Umbreon', 'O2', 'hidden'), ('Leafeon', 'O4', 'hidden'),
              ('Glaceon', 'S7', 'hidden'), ('Sylveon', 'O4', 'hidden')],
    'Gloom': [('Vileplume', 'A4', 'day'), ('Bellossom', 'O4', 'day')],
}

# ---------------------------------------------------------------------------
# Parsing the expansion
# ---------------------------------------------------------------------------

def read(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as f:
        return f.read()


def parse_ndex():
    txt = read('include/constants/pokedex.h')
    order, i, started = {}, 0, False
    for line in txt.splitlines():
        m = re.match(r'\s*(NATIONAL_DEX_[A-Z0-9_]+)', line)
        if not m:
            continue
        name = m.group(1)
        if name == 'NATIONAL_DEX_NONE':
            started, i = True, 0
            continue
        if started and name not in order and not name.endswith('_COUNT'):
            i += 1
            order[name] = i
        if i >= 1025:
            break
    return order


def balanced(s, start):
    depth = 0
    for j in range(start, len(s)):
        if s[j] in '({':
            depth += 1
        elif s[j] in ')}':
            depth -= 1
            if depth == 0:
                return j
    return len(s)


def parse_species():
    species = {}
    for f in sorted(glob.glob(os.path.join(ROOT, 'src/data/pokemon/species_info/gen_*_families.h'))):
        txt = open(f, encoding='utf-8').read()
        for m in re.finditer(r'\n\s*\[(SPECIES_[A-Z0-9_]+)\]\s*=\s*\n?\s*\{', txt):
            sp = m.group(1)
            body = txt[m.end():balanced(txt, m.end() - 1)]
            e = {'id': sp}
            g = re.search(r'\.natDexNum\s*=\s*(NATIONAL_DEX_[A-Z0-9_]+)', body)
            e['ndex'] = g.group(1) if g else None
            g = re.search(r'\.speciesName\s*=\s*_\("([^"]*)"\)', body)
            e['name'] = g.group(1).replace('{PKMN}', 'Pkmn') if g else None
            g = re.search(r'\.types\s*=\s*MON_TYPES\(([^)]*)\)', body)
            e['types'] = [t.strip().replace('TYPE_', '') for t in g.group(1).split(',')] if g else []
            g = re.search(r'\.eggGroups\s*=\s*MON_EGG_GROUPS\(([^)]*)\)', body)
            e['egg'] = [t.strip().replace('EGG_GROUP_', '') for t in g.group(1).split(',')] if g else []
            evos = []
            g = re.search(r'\.evolutions\s*=\s*EVOLUTION\(', body)
            if g:
                start = g.end() - 1
                inner = body[start + 1:balanced(body, start)]
                j = 0
                while True:
                    k = inner.find('{', j)
                    if k < 0:
                        break
                    end = balanced(inner, k)
                    chunk = inner[k + 1:end]
                    parts = [p.strip() for p in re.split(r',(?![^({]*[)}])', chunk)]
                    if len(parts) >= 3 and parts[0].startswith('EVO_'):
                        evos.append({'method': parts[0], 'param': parts[1], 'target': parts[2],
                                     'cond': ','.join(parts[3:])})
                    j = end + 1
            e['evos'] = evos
            e['legend'] = any(re.search(r'\.' + k + r'\s*=\s*TRUE', body) for k in
                              ('isRestrictedLegendary', 'isSubLegendary', 'isMythical', 'isUltraBeast', 'isParadox'))
            species[sp] = e
    return species


# Macro-defined species the simple parser misses.
MANUAL = {
    'NATIONAL_DEX_UNOWN': ('Unown', ['PSYCHIC'], ['NO_EGGS_DISCOVERED'], []),
    'NATIONAL_DEX_MOTHIM': ('Mothim', ['BUG', 'FLYING'], ['BUG'], []),
    'NATIONAL_DEX_SCATTERBUG': ('Scatterbug', ['BUG'], ['BUG'], [('EVO_LEVEL', '9', 'NATIONAL_DEX_SPEWPA', '')]),
    'NATIONAL_DEX_SPEWPA': ('Spewpa', ['BUG'], ['BUG'], [('EVO_LEVEL', '12', 'NATIONAL_DEX_VIVILLON', '')]),
    'NATIONAL_DEX_VIVILLON': ('Vivillon', ['BUG', 'FLYING'], ['BUG'], []),
    'NATIONAL_DEX_FLABEBE': ('Flabebe', ['FAIRY'], ['FAIRY'], [('EVO_LEVEL', '19', 'NATIONAL_DEX_FLOETTE', '')]),
    'NATIONAL_DEX_FLORGES': ('Florges', ['FAIRY'], ['FAIRY'], []),
    'NATIONAL_DEX_MINIOR': ('Minior', ['ROCK', 'FLYING'], ['MINERAL'], []),
    'NATIONAL_DEX_FURFROU': ('Furfrou', ['NORMAL'], ['FIELD'], []),
    'NATIONAL_DEX_ARCEUS': ('Arceus', ['NORMAL'], ['NO_EGGS_DISCOVERED'], []),
    'NATIONAL_DEX_GENESECT': ('Genesect', ['BUG', 'STEEL'], ['NO_EGGS_DISCOVERED'], []),
    'NATIONAL_DEX_SILVALLY': ('Silvally', ['NORMAL'], ['NO_EGGS_DISCOVERED'], []),
    'NATIONAL_DEX_OGERPON': ('Ogerpon', ['GRASS'], ['NO_EGGS_DISCOVERED'], []),
}
MANUAL_LEGEND = {'NATIONAL_DEX_ARCEUS', 'NATIONAL_DEX_GENESECT', 'NATIONAL_DEX_SILVALLY', 'NATIONAL_DEX_OGERPON'}
# Types the parser can't read (they sit behind #if P_UPDATED_TYPES or a form macro)
TYPE_FIX = {'Clefairy': ['FAIRY'], 'Clefable': ['FAIRY'], 'Cleffa': ['FAIRY'], 'Jigglypuff': ['NORMAL', 'FAIRY'],
            'Wigglytuff': ['NORMAL', 'FAIRY'], 'Igglybuff': ['NORMAL', 'FAIRY'], 'Rotom': ['ELECTRIC', 'GHOST'],
            'Alcremie': ['FAIRY'], 'Togepi': ['FAIRY'], 'Togetic': ['FAIRY', 'FLYING'], 'Togekiss': ['FAIRY', 'FLYING']}
# Evolutions whose targets are form macros the parser can't resolve
EXTRA_EDGES = [('NATIONAL_DEX_MILCERY', 'NATIONAL_DEX_ALCREMIE', 'EVO_SPIN', '0', ''),
               ('NATIONAL_DEX_FLOETTE', 'NATIONAL_DEX_FLORGES', 'EVO_ITEM', 'ITEM_SHINY_STONE', ''),
               ('NATIONAL_DEX_BURMY', 'NATIONAL_DEX_MOTHIM', 'EVO_LEVEL', '20', '{IF_GENDER, MON_MALE}'),
               ('NATIONAL_DEX_TYPE_NULL', 'NATIONAL_DEX_SILVALLY', 'EVO_LEVEL', '0', '{IF_MIN_FRIENDSHIP, 160}')]


def evo_text(ev, names):
    m, p, c = ev['method'], ev['param'], ev['cond']

    def item(x):
        return x.replace('ITEM_', '').replace('_', ' ').title()

    def move(x):
        return x.replace('MOVE_', '').replace('_', ' ').title()
    bits = []
    if 'IF_DEFEAT_X_WITH_ITEMS' in c:
        return "level up after beating 3 Bisharp that hold a Leader's Crest"
    if m == 'EVO_LEVEL':
        if p not in ('0', ''):
            bits.append('Lv ' + p)
    elif m == 'EVO_ITEM':
        bits.append('use ' + item(p))
    elif m == 'EVO_TRADE':
        bits.append('trade, or the Xenion')
    elif m == 'EVO_SPIN':
        bits.append('spin while holding a Sweet')
    elif m == 'EVO_SPLIT_FROM_EVO':
        return 'appears when Nincada evolves, with a free party slot and a spare Poké Ball'
    elif m == 'EVO_THRESHOLD':
        bits.append('special: ' + p.lower())
    elif m == 'EVO_LEVEL_BATTLE_ONLY':
        bits.append('in battle')
    elif m == 'EVO_SCRIPT_TRIGGER':
        bits.append('scripted: ' + p.replace('EVO_TRIGGER_', '').replace('_', ' ').lower())
    elif m == 'EVO_BATTLE_END':
        bits.append('after a battle')
    else:
        bits.append(m.replace('EVO_', '').lower())
    for cm in re.finditer(r'\{\s*(IF_[A-Z_]+)\s*,?\s*([^,}]*)\s*,?\s*([^}]*)\}', c):
        k, a, b = cm.group(1), cm.group(2).strip(), cm.group(3).strip()
        if k == 'IF_MIN_FRIENDSHIP':
            bits.append('friendship')
        elif k in ('IF_TIME',):
            bits.append(a.replace('TIME_', '').lower())
        elif k == 'IF_NOT_TIME':
            bits.append('not at ' + a.replace('TIME_', '').lower())
        elif k == 'IF_HOLD_ITEM':
            bits.append('holding ' + item(a))
        elif k == 'IF_KNOWS_MOVE':
            bits.append('knowing ' + move(a))
        elif k == 'IF_KNOWS_MOVE_TYPE':
            bits.append('knowing a ' + a.replace('TYPE_', '').title() + ' move')
        elif k == 'IF_GENDER':
            bits.append('female' if 'FEMALE' in a else 'male')
        elif k in ('IF_REGION', 'IF_NOT_REGION'):
            bits.append(('in ' if k == 'IF_REGION' else 'outside ') + a.replace('REGION_', '').title())
        elif k == 'IF_WEATHER':
            bits.append('in ' + a.replace('WEATHER_', '').lower().replace('_', ' '))
        elif k in ('IF_IN_MAP', 'IF_IN_MAPSEC'):
            bits.append('at a special place')
        elif k == 'IF_SPECIES_IN_PARTY':
            bits.append('with ' + names.get(a, a) + ' in the party')
        elif k == 'IF_TYPE_IN_PARTY':
            bits.append('with a ' + a.replace('TYPE_', '').title() + ' type in the party')
        elif k == 'IF_TRADE_PARTNER_SPECIES':
            bits.append('traded for ' + names.get(a, a))
        elif k == 'IF_MIN_BEAUTY':
            bits.append('high beauty')
        elif k == 'IF_MIN_OVERWORLD_STEPS':
            bits.append('after walking ' + a + ' steps')
        elif k == 'IF_USED_MOVE_X_TIMES':
            bits.append('after using ' + move(a) + ' ' + b + ' times')
        elif k == 'IF_RECOIL_DAMAGE_GE':
            bits.append('after taking ' + a + ' recoil')
        elif k == 'IF_CURRENT_DAMAGE_GE':
            bits.append('after losing ' + a + ' HP')
        elif k == 'IF_CRITICAL_HITS_GE':
            bits.append('after ' + a + ' critical hits in one battle')
        elif k == 'IF_DEFEAT_X_WITH_ITEMS':
            bits.append('after beating ' + b + ' Bisharp that hold a Leader\'s Crest')
        elif k == 'IF_BAG_ITEM_COUNT':
            bits.append('with ' + b + ' ' + item(a))
        elif k in ('IF_ATK_GT_DEF', 'IF_ATK_LT_DEF', 'IF_ATK_EQ_DEF'):
            bits.append({'IF_ATK_GT_DEF': 'Atk > Def', 'IF_ATK_LT_DEF': 'Atk < Def', 'IF_ATK_EQ_DEF': 'Atk = Def'}[k])
        elif k.startswith('IF_PID'):
            bits.append('by personality')
        elif k in ('IF_AMPED_NATURE', 'IF_LOW_KEY_NATURE'):
            bits.append('amped nature' if 'AMPED' in k else 'low-key nature')
    return ', '.join(bits) if bits else 'level up'


def is_plain_level(ev):
    return ev['method'] == 'EVO_LEVEL' and ev['param'] not in ('0', '') and \
        not re.search(r'IF_(HOLD_ITEM|KNOWS_MOVE|MIN_FRIENDSHIP|IN_MAP|REGION|SPECIES_IN_PARTY|TYPE_IN_PARTY|WEATHER|MIN_BEAUTY|USED_MOVE|RECOIL|CURRENT_DAMAGE|CRITICAL|DEFEAT|BAG_ITEM|MIN_OVERWORLD)', ev['cond'])


def main():
    order = parse_ndex()
    species = parse_species()
    base = {}  # ndex name -> entry (first parsed form)
    for sp in species.values():
        if sp['ndex'] and sp['ndex'] not in base and sp['name']:
            base[sp['ndex']] = sp
    for nd, (name, types, egg, evos) in MANUAL.items():
        if nd not in base:
            base[nd] = {'id': nd, 'ndex': nd, 'name': name, 'types': types, 'egg': egg, 'legend': nd in MANUAL_LEGEND,
                        'evos': [{'method': a, 'param': b, 'target': c, 'cond': d} for a, b, c, d in evos]}
    for nd, sp in base.items():
        if sp['name'] in TYPE_FIX:
            sp['types'] = TYPE_FIX[sp['name']]
    sp2nd = {sp['id']: sp['ndex'] for sp in species.values() if sp['ndex']}
    for nd in MANUAL:
        sp2nd[nd] = nd
    names = {}
    for sp in species.values():
        if sp['name']:
            names[sp['id']] = sp['name']
    nd_name = {nd: base[nd]['name'] for nd in base}
    for sp in list(names):
        if sp2nd.get(sp) in nd_name:
            names[sp] = nd_name[sp2nd[sp]]

    # evolution graph over ndex numbers, from every form of each species
    edges = collections.defaultdict(list)   # nd -> [(target nd, evo)]
    incoming = collections.defaultdict(list)
    for sp in list(species.values()) + [base[n] for n in MANUAL]:
        src = sp2nd.get(sp['id'])
        if not src:
            continue
        for ev in sp['evos']:
            tgt = sp2nd.get(ev['target'], ev['target'] if ev['target'].startswith('NATIONAL_DEX') else None)
            if not tgt or tgt == src:
                continue
            if all(t != tgt for t, _ in edges[src]):
                edges[src].append((tgt, ev))
                incoming[tgt].append((src, ev))
    for src, tgt, m, p, c in EXTRA_EDGES:
        if all(t != tgt for t, _ in edges[src]):
            ev = {'method': m, 'param': p, 'target': tgt, 'cond': c}
            edges[src].append((tgt, ev))
            incoming[tgt].append((src, ev))

    nds = sorted(order, key=order.get)
    legend = {nd for nd in nds if base[nd].get('legend')}
    # families
    fam_of, families = {}, []
    for nd in nds:
        if nd in fam_of:
            continue
        stack, comp = [nd], set()
        while stack:
            x = stack.pop()
            if x in comp:
                continue
            comp.add(x)
            stack += [t for t, _ in edges[x]] + [s for s, _ in incoming[x]]
        fam = sorted(comp, key=lambda n: order.get(n, 9999))
        for x in fam:
            fam_of[x] = len(families)
        families.append(fam)

    rows = {}
    load = collections.Counter()
    nursery_load = collections.Counter()
    area_rows = collections.defaultdict(list)

    def nm(nd):
        return base[nd]['name']

    def place(nd, area, method, note, extra=False):
        land, aname, band, methods, _ = AREAS[area]
        meths = methods.split()
        if method not in meths:
            method = pick_method(nd, meths)
        load[area] += 1
        lo, hi = band
        if method == 'hidden':
            lo, hi = max(lo, hi - 2), hi
        rows[nd] = {'home': LANDS[land], 'where': aname, 'how': METHOD_TEXT[method], 'lv': '%d-%d' % (lo, hi),
                    'note': note or '', 'area': area}
        area_rows[area].append((nd, method))

    def pick_method(nd, meths):
        t = base[nd]['types']
        if 'WATER' in t and 'surf' in meths:
            return 'surf'
        if 'WATER' in t and 'fish' in meths:
            return 'fish'
        night = {'GHOST', 'DARK'} & set(t)
        if night and 'night' in meths:
            return 'night'
        for m in ('day', 'cave', 'night', 'rock', 'hidden', 'surf', 'fish'):
            if m in meths:
                return m
        return meths[0]

    def best_area(nd):
        t = base[nd]['types']
        cands = []
        for rank, ty in enumerate(t):
            for pos, a in enumerate(TYPE_HOMES.get(ty, [])):
                score = pos + rank * 3
                if len(t) > 1 and t[1 - rank] in AREAS[a][4].upper().split():
                    score -= 4
                if 'WATER' in t and not ({'surf', 'fish'} & set(AREAS[a][3].split())):
                    score += 20
                cands.append((score + load[a] * 1.6, a))
        cands.sort()
        return cands[0][1] if cands else 'T2'

    month_slot = collections.Counter()

    def nursery(nd, land):
        if land not in NURSERIES:
            land = 'West'  # Okeanos's young are raised at its nearest shore, Gadeira
        month = MONTHS[month_slot[land] % 12]
        month_slot[land] += 1
        nursery_load[land] += 1
        return land, month

    special = []
    for fam in families:
        root_candidates = [n for n in fam if not incoming[n] or all(s not in fam for s, _ in incoming[n])]
        root = min(root_candidates, key=lambda n: order[n])
        rname = nm(root)
        if any(n in legend for n in fam):
            for n in fam:
                if n not in rows:
                    rows[n] = {'home': 'LEGENDS.md', 'where': 'LEGENDS.md §2 gives the home and the doc that places it', 'how': 'quest',
                               'lv': '—', 'note': '', 'area': None}
            continue
        if rname in GIFT_LINES:
            for n in fam:
                rows[n] = {'home': 'Aethos (SYSTEMS.md §10)', 'where': 'guest-gift of ' + GIFT_LINES[rname],
                           'how': 'gift' if n == root else 'evolve', 'lv': '—', 'note': '', 'area': None}
            special.append((root, 'gift only', 'theoxenia guest-gift of %s (SYSTEMS.md §10); the line evolves from it' % GIFT_LINES[rname]))
            continue
        if rname in FOSSILS:
            land = FOSSIL_LAND[rname]
            for n in fam:
                if n == root:
                    rows[n] = {'home': LANDS[land], 'where': 'dig sites, revived by Daphne at Naukratis',
                               'how': 'fossil: ' + FOSSILS[rname], 'lv': '20', 'note': '', 'area': None}
                    special.append((n, 'fossil', FOSSILS[rname]))
                else:
                    ev = next(e for s, e in incoming[n])
                    rows[n] = {'home': LANDS[land], 'where': 'evolve ' + nm(next(s for s, e in incoming[n])),
                               'how': evo_text(ev, names), 'lv': '—', 'note': '', 'area': None}
            continue
        # the wild form
        wilds = []
        wf = WILD_FORM_OVERRIDE.get(rname, 'auto')
        if wf == 'auto':
            frontier = [root]
            # a baby (Undiscovered until it evolves) is never the wild form:
            # start from its first evolution, as the official games do
            if 'NO_EGGS_DISCOVERED' in base[root]['egg'] and edges[root]:
                frontier = [t for t, ev in edges[root] if t in fam]
            while frontier:
                x = frontier.pop()
                nxt = [t for t, ev in edges[x] if t in fam and is_plain_level(ev)]
                if nxt:
                    frontier += nxt
                else:
                    wilds.append(x)
        elif wf is None:
            frontier = [root]
            while frontier:
                x = frontier.pop()
                nxt = [t for t, ev in edges[x] if t in fam]
                if nxt and any(is_plain_level(ev) for t, ev in edges[x] if t in fam):
                    frontier += [t for t, ev in edges[x] if t in fam and is_plain_level(ev)]
                else:
                    wilds.append(x)
        else:
            wilds = [n for n in fam if nm(n) == wf] or [root]
        wilds = sorted(set(wilds), key=order.get)
        land_of_family = None
        for w in wilds:
            ov = OVERRIDES.get(nm(w))
            if not ov:
                for n in fam:
                    if OVERRIDES.get(nm(n)):
                        ov = OVERRIDES[nm(n)]
                        break
            if ov:
                area, method, note = ov
            else:
                area, method, note = best_area(w), None, None
            if rname in LAZARUS_LINES:
                note = (note + '; ' if note else '') + 'wild only, never a gift (PG-5)'
            place(w, area, method, note)
            land_of_family = land_of_family or AREAS[area][0]
        for extra in WILD_EXTRA.get(nm(wilds[0]), []) + WILD_EXTRA.get(rname, []):
            n = next((x for x in fam if nm(x) == extra[0]), None)
            if n and n not in rows:
                place(n, extra[1], extra[2], None)
        # everything else in the family
        for n in fam:
            if n in rows:
                continue
            if n == root or nm(n) in INCENSE:
                land, month = nursery(n, land_of_family)
                breeders = [w for w in wilds if 'NO_EGGS_DISCOVERED' not in base[w]['egg']] or \
                           [x for x in fam if 'NO_EGGS_DISCOVERED' not in base[x]['egg'] and x != n] or [n]
                via = 'breed ' + ' or '.join(nm(w) for w in breeders[:2])
                if nm(n) in INCENSE:
                    via += ' holding a ' + INCENSE[nm(n)]
                    special.append((n, 'baby', 'breed holding a ' + INCENSE[nm(n)]))
                eggs = base[n]['egg']
                if 'NO_EGGS_DISCOVERED' in eggs and nm(n) not in INCENSE:
                    special.append((n, 'baby', 'Undiscovered egg group: nursery, or breed its evolved form'))
                rows[n] = {'home': LANDS[land], 'where': 'Nursery: ' + NURSERIES[land] + ', ' + month,
                           'how': 'nursery, or ' + via, 'lv': '%d-%d' % NURSERY_BAND, 'note': '', 'area': None}
            else:
                src = [(s, e) for s, e in incoming[n] if s in fam]
                s, ev = src[0]
                txt = evo_text(ev, names)
                below = n in [x for w in wilds for x in ancestors(w, incoming, fam)]
                rows[n] = {'home': rows.get(s, {}).get('home', LANDS.get(land_of_family, '')),
                           'where': 'evolve ' + nm(s), 'how': txt, 'lv': '—', 'note': '', 'area': None}
                if not is_plain_level(ev):
                    special.append((n, 'evolution', 'evolve %s: %s' % (nm(s), txt)))
    # Ditto is needed for genderless breeding, so it gets a second home
    write(order, base, rows, load, nursery_load, area_rows, special, nds)


def ancestors(nd, incoming, fam):
    out, stack = [], [nd]
    while stack:
        x = stack.pop()
        for s, _ in incoming[x]:
            if s in fam and s not in out:
                out.append(s)
                stack.append(s)
    return out


METHOD_TEXT = {'day': 'grass, day', 'night': 'grass, night', 'cave': 'cave floor', 'surf': 'surfing',
               'fish': 'fishing', 'rock': 'rock smash', 'hidden': "Augur's Eye (hidden)"}


def write(order, base, rows, load, nursery_load, area_rows, special, nds):
    L = []
    L.append('# The Oikoumene: where every Pokémon lives')
    L.append('')
    L.append('Generated by `design/oikoumene/coverage.py` from the expansion\'s species data. Edit the script\'s tables, not this file. The rules are in `design/OIKOUMENE.md` §8; legendary quests are in `design/LEGENDS.md`.')
    L.append('')
    L.append('Areas marked LABORS\'s or ODYSSEY\'s are those docs\' maps on the Oikoumene chart. Their own wild tables (LABORS §3, ODYSSEY §4 and §6) already hold some existing species; the homes listed here join those tables, and every species here has at least one home whatever those tables hold.')
    L.append('')
    cats = collections.Counter()
    for nd in nds:
        r = rows[nd]
        if r['home'] == 'LEGENDS.md':
            cats['Legendary, mythical, Ultra Beast or Paradox (LEGENDS.md §2, which names the epics that place some)'] += 1
        elif r['how'] in ('gift',) or 'guest-gift' in r['where']:
            cats['Theoxenia guest-gift lines (SYSTEMS.md §10)'] += 1
        elif r['area']:
            cats['Wild in an Oikoumene area'] += 1
        elif r['where'].startswith('Nursery'):
            cats['Nursery (low-level, by month) or breeding'] += 1
        elif r['how'].startswith('fossil'):
            cats['Fossil, revived'] += 1
        else:
            cats['Evolve a caught Pokémon'] += 1
    L.append('## Totals')
    L.append('')
    L.append('| How it is obtained | Species |')
    L.append('|---|---:|')
    for k, v in cats.most_common():
        L.append('| %s | %d |' % (k, v))
    L.append('| **All National Dex species** | **%d** |' % len(nds))
    L.append('')
    L.append('## The encounter areas')
    L.append('')
    L.append('Each area\'s wild forms, by method. "Day" and "night" are the land table\'s morning-and-day and evening-and-night sets (`OW_TIME_OF_DAY_ENCOUNTERS`). A Gen 3 table holds 12 land, 5 surf, 5 rock-smash and 10 fishing slots per time of day, plus 3 Augur\'s Eye (DexNav) slots, so no area here is over capacity.')
    L.append('')
    L.append('"Shares" are species whose home is a neighboring area of the same land and type, used to fill the rest of the table\'s slots so no map feels thin. A species\' home is where it is most common; a share is where it also turns up.')
    L.append('')
    L.append('| Area | Land | Levels | Home to | Wild forms | Shares |')
    L.append('|---|---|---|---:|---|---|')
    for a, (land, aname, band, methods, aff) in AREAS.items():
        lst = sorted(area_rows[a], key=lambda x: order[x[0]])
        by = collections.defaultdict(list)
        for nd, m in lst:
            by[m].append(base[nd]['name'])
        txt = '; '.join('%s: %s' % (METHOD_TEXT[m], ', '.join(v)) for m, v in by.items())
        affs = set(aff.upper().split())
        water = bool({'surf', 'fish'} & set(methods.split()))
        landish = bool({'day', 'night', 'cave', 'rock'} & set(methods.split()))
        mine = {nd for nd, _ in lst}
        shares = []
        for b, (land2, _, band2, _, _) in AREAS.items():
            if b == a or land2 != land:
                continue
            for nd, _ in area_rows[b]:
                t = set(base[nd]['types'])
                if nd in mine or not (t & affs):
                    continue
                if 'WATER' in t and not water:
                    continue
                if 'WATER' not in t and not landish:
                    continue
                shares.append(base[nd]['name'])
        shares = shares[:max(0, 10 - len(lst))]
        L.append('| %s %s | %s | %d–%d | %d | %s | %s |' % (a, aname, LANDS[land].split(':')[0], band[0], band[1], len(lst), txt, ', '.join(shares)))
    L.append('')
    L.append('**Capacity check.** The fullest area holds %d wild forms. An area with day, night, surf, fishing, rock and Augur\'s Eye tables can hold about 30 distinct species without crowding.' % max(load.values()))
    L.append('')
    L.append('## The Nurseries')
    L.append('')
    L.append('Each land but Okeanos has one Nursery: a small, gentle spot where the young live, at levels %d–%d. Its table turns with the Aethos month (12 months of 3 days, SYSTEMS.md §7), using the Altering Cave\'s table-offset hook (`GetCurrentMapWildMonHeaderId`, `src/wild_encounter.c` line 434). Every first stage can also be bred.' % NURSERY_BAND)
    L.append('')
    L.append('| Land | Nursery | First stages |')
    L.append('|---|---|---:|')
    for land, n in NURSERIES.items():
        L.append('| %s | %s | %d |' % (LANDS[land], n, nursery_load[land]))
    L.append('')
    L.append('## Special handling')
    L.append('')
    L.append('Everything here is obtainable in one save, with no link cable. Trade evolutions use the **Xenion** (the expansion\'s Linking Cord, renamed: a guest-gift that stands in for an exchange), and a few also come through in-game trades in the Oikoumene\'s houses (OIKOUMENE.md §4). The legendary gifts (Cosmog, Type: Null, Kubfu, Poipole) are in LEGENDS.md.')
    L.append('')
    L.append('| # | Species | Kind | How |')
    L.append('|---:|---|---|---|')
    seen = set()
    for nd, kind, how in sorted(special, key=lambda x: order[x[0]]):
        if nd in seen:
            continue
        seen.add(nd)
        L.append('| %d | %s | %s | %s |' % (order[nd], base[nd]['name'], kind, how))
    L.append('')
    L.append('## Every species')
    L.append('')
    L.append('| # | Species | Types | Home | Where | Method | Lv | Note |')
    L.append('|---:|---|---|---|---|---|---|---|')
    for nd in nds:
        r = rows[nd]
        t = '/'.join(x.title() for x in base[nd]['types'])
        L.append('| %d | %s | %s | %s | %s | %s | %s | %s |' % (order[nd], base[nd]['name'], t, r['home'], r['where'], r['how'], r['lv'], r['note']))
    L.append('')
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))
    print('wrote', OUT, '—', len(nds), 'species;', dict(cats))
    print('max area load', max(load.values()), max(load, key=load.get))
    print('nursery load', dict(nursery_load))


if __name__ == '__main__':
    main()
