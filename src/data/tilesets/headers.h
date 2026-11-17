#include "fieldmap.h"

// Whether a palette has a night version, located at ((x + 9) % 16).pal
#define SWAP_PAL(x) ((x) < NUM_PALS_IN_PRIMARY ? 1 << (x) : 1 << ((x) - NUM_PALS_IN_PRIMARY))

// Ichor: tilesets whose maps were cut (hoenn-cut batch 2) but that upstream code
// still names, mostly field_door.c's door table. Their graphics are gone; these
// empty structs only keep those references linking.
const struct Tileset gTileset_BattleTent = { .isSecondary = TRUE };
const struct Tileset gTileset_BikeShop = { .isSecondary = TRUE };
const struct Tileset gTileset_BrendansMaysHouse = { .isSecondary = TRUE };
const struct Tileset gTileset_BuildingFrlg = { .isSecondary = FALSE };
const struct Tileset gTileset_Cave = { .isSecondary = TRUE };
const struct Tileset gTileset_CeladonCity = { .isSecondary = TRUE };
const struct Tileset gTileset_CeruleanCity = { .isSecondary = TRUE };
const struct Tileset gTileset_CinnabarGym = { .isSecondary = TRUE };
const struct Tileset gTileset_CinnabarIsland = { .isSecondary = TRUE };
const struct Tileset gTileset_Contest = { .isSecondary = TRUE };
const struct Tileset gTileset_DepartmentStore = { .isSecondary = TRUE };
const struct Tileset gTileset_Dewford = { .isSecondary = TRUE };
const struct Tileset gTileset_EliteFour = { .isSecondary = TRUE };
const struct Tileset gTileset_EverGrande = { .isSecondary = TRUE };
const struct Tileset gTileset_Facility = { .isSecondary = TRUE };
const struct Tileset gTileset_Fallarbor = { .isSecondary = TRUE };
const struct Tileset gTileset_Fortree = { .isSecondary = TRUE };
const struct Tileset gTileset_FuchsiaCity = { .isSecondary = TRUE };
const struct Tileset gTileset_GameCorner = { .isSecondary = TRUE };
const struct Tileset gTileset_General_Frlg = { .isSecondary = FALSE };
const struct Tileset gTileset_GenericBuilding = { .isSecondary = TRUE };
const struct Tileset gTileset_GenericBuilding1 = { .isSecondary = TRUE };
const struct Tileset gTileset_InsideOfTruck = { .isSecondary = TRUE };
const struct Tileset gTileset_InsideShip = { .isSecondary = TRUE };
const struct Tileset gTileset_Lavaridge = { .isSecondary = TRUE };
const struct Tileset gTileset_LavenderTown = { .isSecondary = TRUE };
const struct Tileset gTileset_Lilycove = { .isSecondary = TRUE };
const struct Tileset gTileset_LilycoveMuseum = { .isSecondary = TRUE };
const struct Tileset gTileset_Mart = { .isSecondary = TRUE };
const struct Tileset gTileset_Mauville = { .isSecondary = TRUE };
const struct Tileset gTileset_MauvilleGym = { .isSecondary = TRUE };
const struct Tileset gTileset_MeteorFalls = { .isSecondary = TRUE };
const struct Tileset gTileset_MirageTower = { .isSecondary = TRUE };
const struct Tileset gTileset_Mossdeep = { .isSecondary = TRUE };
const struct Tileset gTileset_MossdeepGameCorner = { .isSecondary = TRUE };
const struct Tileset gTileset_MossdeepGym = { .isSecondary = TRUE };
const struct Tileset gTileset_MtEmber = { .isSecondary = TRUE };
const struct Tileset gTileset_Pacifidlog = { .isSecondary = TRUE };
const struct Tileset gTileset_PalletTown = { .isSecondary = TRUE };
const struct Tileset gTileset_Petalburg = { .isSecondary = TRUE };
const struct Tileset gTileset_PetalburgGym = { .isSecondary = TRUE };
const struct Tileset gTileset_PewterCity = { .isSecondary = TRUE };
const struct Tileset gTileset_PokemonCenterFrlg = { .isSecondary = TRUE };
const struct Tileset gTileset_PokemonLeague = { .isSecondary = TRUE };
const struct Tileset gTileset_PokemonMansion = { .isSecondary = TRUE };
const struct Tileset gTileset_Rustboro = { .isSecondary = TRUE };
const struct Tileset gTileset_SSAnne = { .isSecondary = TRUE };
const struct Tileset gTileset_SaffronCity = { .isSecondary = TRUE };
const struct Tileset gTileset_SeaCottage = { .isSecondary = TRUE };
const struct Tileset gTileset_SeafoamIslands = { .isSecondary = TRUE };
const struct Tileset gTileset_SecretBase = { .isSecondary = FALSE };
const struct Tileset gTileset_SecretBaseRedCave = { .isSecondary = TRUE };
const struct Tileset gTileset_SeviiIslands123 = { .isSecondary = TRUE };
const struct Tileset gTileset_SeviiIslands45 = { .isSecondary = TRUE };
const struct Tileset gTileset_SeviiIslands67 = { .isSecondary = TRUE };
const struct Tileset gTileset_SilphCo = { .isSecondary = TRUE };
const struct Tileset gTileset_Slateport = { .isSecondary = TRUE };
const struct Tileset gTileset_Sootopolis = { .isSecondary = TRUE };
const struct Tileset gTileset_SootopolisGym = { .isSecondary = TRUE };
const struct Tileset gTileset_TrainerTower = { .isSecondary = TRUE };
const struct Tileset gTileset_TrickHousePuzzle = { .isSecondary = TRUE };
const struct Tileset gTileset_Underwater = { .isSecondary = TRUE };
const struct Tileset gTileset_VermilionCity = { .isSecondary = TRUE };
const struct Tileset gTileset_VermilionGym = { .isSecondary = TRUE };
const struct Tileset gTileset_ViridianCity = { .isSecondary = TRUE };
const struct Tileset gTileset_ViridianForest = { .isSecondary = TRUE };

const struct Tileset *const gTilesetPointer_SecretBase = &gTileset_SecretBase;
const struct Tileset *const gTilesetPointer_SecretBaseRedCave = &gTileset_SecretBaseRedCave;

#if !IS_FRLG

const struct Tileset gTileset_General =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_General,
    .palettes = gTilesetPalettes_General,
    .metatiles = gMetatiles_General,
    .metatileAttributes = gMetatileAttributes_General,
    .callback = InitTilesetAnim_General,
};

const struct Tileset gTileset_BattleFrontierOutsideWest =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattleFrontierOutsideWest,
    .palettes = gTilesetPalettes_BattleFrontierOutsideWest,
    .metatiles = gMetatiles_BattleFrontierOutsideWest,
    .metatileAttributes = gMetatileAttributes_BattleFrontierOutsideWest,
    .callback = InitTilesetAnim_BattleFrontierOutsideWest,
};

const struct Tileset gTileset_BattleFrontierOutsideEast =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattleFrontierOutsideEast,
    .palettes = gTilesetPalettes_BattleFrontierOutsideEast,
    .metatiles = gMetatiles_BattleFrontierOutsideEast,
    .metatileAttributes = gMetatileAttributes_BattleFrontierOutsideEast,
    .callback = InitTilesetAnim_BattleFrontierOutsideEast,
};

const struct Tileset gTileset_Building =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_InsideBuilding,
    .palettes = gTilesetPalettes_InsideBuilding,
    .metatiles = gMetatiles_InsideBuilding,
    .metatileAttributes = gMetatileAttributes_InsideBuilding,
    .callback = InitTilesetAnim_Building,
};

const struct Tileset gTileset_Shop =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_Shop,
    .palettes = gTilesetPalettes_Shop,
    .metatiles = gMetatiles_Shop,
    .metatileAttributes = gMetatileAttributes_Shop,
    .callback = NULL,
};

const struct Tileset gTileset_PokemonCenter =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PokemonCenter,
    .palettes = gTilesetPalettes_PokemonCenter,
    .metatiles = gMetatiles_PokemonCenter,
    .metatileAttributes = gMetatileAttributes_PokemonCenter,
    .callback = NULL,
};

const struct Tileset gTileset_BattleFrontier =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattleFrontier,
    .palettes = gTilesetPalettes_BattleFrontier,
    .metatiles = gMetatiles_BattleFrontier,
    .metatileAttributes = gMetatileAttributes_BattleFrontier,
    .callback = NULL,
};

const struct Tileset gTileset_BattlePalace =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattlePalace,
    .palettes = gTilesetPalettes_BattlePalace,
    .metatiles = gMetatiles_BattlePalace,
    .metatileAttributes = gMetatileAttributes_BattlePalace,
    .callback = NULL,
};

const struct Tileset gTileset_BattleDome =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattleDome,
    .palettes = gTilesetPalettes_BattleDome,
    .metatiles = gMetatiles_BattleDome,
    .metatileAttributes = gMetatileAttributes_BattleDome,
    .callback = InitTilesetAnim_BattleDome,
};

const struct Tileset gTileset_BattleFactory =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattleFactory,
    .palettes = gTilesetPalettes_BattleFactory,
    .metatiles = gMetatiles_BattleFactory,
    .metatileAttributes = gMetatileAttributes_BattleFactory,
    .callback = NULL,
};

const struct Tileset gTileset_BattlePike =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattlePike,
    .palettes = gTilesetPalettes_BattlePike,
    .metatiles = gMetatiles_BattlePike,
    .metatileAttributes = gMetatileAttributes_BattlePike,
    .callback = NULL,
};

const struct Tileset gTileset_BattleArena =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattleArena,
    .palettes = gTilesetPalettes_BattleArena,
    .metatiles = gMetatiles_BattleArena,
    .metatileAttributes = gMetatileAttributes_BattleArena,
    .callback = NULL,
};

const struct Tileset gTileset_BattlePyramid =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattlePyramid,
    .palettes = gTilesetPalettes_BattlePyramid,
    .metatiles = gMetatiles_BattlePyramid,
    .metatileAttributes = gMetatileAttributes_BattlePyramid,
    .callback = InitTilesetAnim_BattlePyramid,
};

const struct Tileset gTileset_TrainerHill =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_TrainerHill,
    .palettes = gTilesetPalettes_TrainerHill,
    .metatiles = gMetatiles_TrainerHill,
    .metatileAttributes = gMetatileAttributes_TrainerHill,
    .callback = NULL,
};

const struct Tileset gTileset_BattleFrontierRankingHall =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_BattleFrontierRankingHall,
    .palettes = gTilesetPalettes_BattleFrontierRankingHall,
    .metatiles = gMetatiles_BattleFrontierRankingHall,
    .metatileAttributes = gMetatileAttributes_BattleFrontierRankingHall,
    .callback = NULL,
};

// Ichor: Aethos, the Greek primary. It keeps General's metatile ids, so Hoenn
// layouts render against it. Managed by Porytiles (tools/ichor/art/).
const struct Tileset gTileset_Aethos =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_PorytilesManaged_Aethos,
    .palettes = gTilesetPalettes_PorytilesManaged_Aethos,
    .metatiles = gMetatiles_PorytilesManaged_Aethos,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Aethos,
    .callback = InitTilesetAnim_PorytilesManaged_Aethos,
};

#else

// FRLG tilesets

#endif // IS_FRLG

const struct Tileset gTileset_Kalliste =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Kalliste,
    .palettes = gTilesetPalettes_PorytilesManaged_Kalliste,
    .metatiles = gMetatiles_PorytilesManaged_Kalliste,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Kalliste,
    .callback = NULL,
};

const struct Tileset gTileset_TempleHestia =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_TempleHestia,
    .palettes = gTilesetPalettes_PorytilesManaged_TempleHestia,
    .metatiles = gMetatiles_PorytilesManaged_TempleHestia,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_TempleHestia,
    .callback = NULL,
};

// Ichor: Oikos ("household"), the Greek interior primary. It keeps Building's
// metatile ids and every tile the Hoenn interior secondaries point at, so they
// still render on it. Managed by Porytiles (tools/ichor/art/oikos_paint.py).
// No tile animation: Building's TV-on frames would paint Hoenn art over it.
const struct Tileset gTileset_Oikos =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_PorytilesManaged_Oikos,
    .palettes = gTilesetPalettes_PorytilesManaged_Oikos,
    .metatiles = gMetatiles_PorytilesManaged_Oikos,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Oikos,
    .callback = NULL,
};

// Ichor: oikia, furnishings of a Greek house. A secondary that uses only its
// own tiles and palettes 6-12, so it works on any primary. Built by
// tools/ichor/art/oikia_build.py.
const struct Tileset gTileset_Oikia =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Oikia,
    .palettes = gTilesetPalettes_PorytilesManaged_Oikia,
    .metatiles = gMetatiles_PorytilesManaged_Oikia,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Oikia,
    .callback = NULL,
};

// Ichor: civic, the Greek public halls (Asclepeion, Agora, Akademia). A
// Porytiles-managed secondary built by tools/ichor/art/civic_tiles.py; it uses
// only its own tiles and palettes 6-12, so it works on any primary.
const struct Tileset gTileset_Civic =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Civic,
    .palettes = gTilesetPalettes_PorytilesManaged_Civic,
    .metatiles = gMetatiles_PorytilesManaged_Civic,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Civic,
    .callback = NULL,
};

// Ichor: akti, Akti Town's harbor. A Porytiles-managed secondary built by
// tools/ichor/art/akti_build.py for the aethos primary: its ground cells borrow
// aethos's grass, sand and animated sea, so rebuild it whenever aethos changes.
const struct Tileset gTileset_Akti =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Akti,
    .palettes = gTilesetPalettes_PorytilesManaged_Akti,
    .metatiles = gMetatiles_PorytilesManaged_Akti,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Akti,
    .callback = NULL,
};

// Porytiles-managed secondary built by tools/ichor/art/agros_build.py: the
// countryside (Route 1, Kronion Hill). It uses only its own tiles and
// palettes 6-12, so it works on any primary; its ground matches aethos.
const struct Tileset gTileset_Agros =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Agros,
    .palettes = gTilesetPalettes_PorytilesManaged_Agros,
    .metatiles = gMetatiles_PorytilesManaged_Agros,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Agros,
    .callback = NULL,
};

// Ichor: eleusa, Eleusa Village (Eleusis): wheat fields, farms and the
// sanctuary of the Mysteries. Porytiles-managed, built by
// tools/ichor/art/eleusa_build.py for the aethos primary: its ground cells
// borrow aethos's grass, path and animated sea, so rebuild it whenever aethos
// changes.
const struct Tileset gTileset_Eleusa =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Eleusa,
    .palettes = gTilesetPalettes_PorytilesManaged_Eleusa,
    .metatiles = gMetatiles_PorytilesManaged_Eleusa,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Eleusa,
    .callback = NULL,
};

// Ichor: temple_demeter, the Temple of Demeter's underground megaron (the
// Lesser Mysteries). Porytiles-managed, built by
// tools/ichor/art/temple_demeter_build.py; it uses only its own tiles and
// palettes 6-12, so it works on any interior primary (oikos). Its doused
// palette set is gTilesetPalettes_TempleDemeterGlow (graphics.h).
const struct Tileset gTileset_TempleDemeter =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_TempleDemeter,
    .palettes = gTilesetPalettes_PorytilesManaged_TempleDemeter,
    .metatiles = gMetatiles_PorytilesManaged_TempleDemeter,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_TempleDemeter,
    .callback = NULL,
};

// Ichor: ergasteria, Phase 2's working interiors (Aegina's inn, mint and homes;
// Emporion's workshops next). A secondary that uses only its own tiles and
// palettes 6-12, so it works on any primary. Built by
// tools/ichor/art/ergasteria_build.py.
const struct Tileset gTileset_Ergasteria =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Ergasteria,
    .palettes = gTilesetPalettes_PorytilesManaged_Ergasteria,
    .metatiles = gMetatiles_PorytilesManaged_Ergasteria,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Ergasteria,
    .callback = NULL,
};

// Ichor: limen, Emporion's harbor-town interiors (the Deigma, the Dolphin,
// Philoxenos's andron, the widow's room, the runners' house, Euphronios's
// workshop and the hiring hall). Like ergasteria, it uses only its own tiles
// and palettes 6-12. Built by tools/ichor/art/limen_build.py.
const struct Tileset gTileset_Limen =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Limen,
    .palettes = gTilesetPalettes_PorytilesManaged_Limen,
    .metatiles = gMetatiles_PorytilesManaged_Limen,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Limen,
    .callback = NULL,
};

// Ichor: domos, limen's twin for Emporion's town households and workshops
// (Philoxenos's andron, the runners' house, Euphronios's workshop): the same
// art and palettes, in a second set because seven rooms didn't fit one.
// Built by tools/ichor/art/limen_build.py.
const struct Tileset gTileset_Domos =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Domos,
    .palettes = gTilesetPalettes_PorytilesManaged_Domos,
    .metatiles = gMetatiles_PorytilesManaged_Domos,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Domos,
    .callback = NULL,
};

// Porytiles-managed secondary built by tools/ichor/art/emporion_build.py: Emporion
// City (streets, the house kit, the Agora, the Temple of Hermes and the monuments,
// Acrocorinth, the workshops). It uses only its own tiles and palettes 6-12; cells
// on grass borrow aethos's, so rebuild it whenever aethos changes.
const struct Tileset gTileset_Emporion =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Emporion,
    .palettes = gTilesetPalettes_PorytilesManaged_Emporion,
    .metatiles = gMetatiles_PorytilesManaged_Emporion,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Emporion,
    .callback = NULL,
};

// Porytiles-managed secondary built by tools/ichor/art/emporion_build.py: Emporion's
// harbor and the Isthmus (the port of Lechaion, the Diolkos, Isthmia), with the
// city's paving and house kit. Its cells on grass, sand, sea and path borrow
// aethos's, so rebuild it whenever aethos changes.
const struct Tileset gTileset_Isthmos =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Isthmos,
    .palettes = gTilesetPalettes_PorytilesManaged_Isthmos,
    .metatiles = gMetatiles_PorytilesManaged_Isthmos,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Isthmos,
    .callback = NULL,
};

// Porytiles-managed secondary built by tools/ichor/art/emporion_build.py: the Temple
// of Hermes's interior and the Herald's Run. It uses only its own tiles and palettes
// 6-12, with opaque floors, so it works on any primary (drawn for oikos).
const struct Tileset gTileset_TempleHermes =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_TempleHermes,
    .palettes = gTilesetPalettes_PorytilesManaged_TempleHermes,
    .metatiles = gMetatiles_PorytilesManaged_TempleHermes,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_TempleHermes,
    .callback = NULL,
};

// Ichor: aegina, the island secondary for Aegina Town and the Aegina detour. A
// Porytiles-managed secondary built by tools/ichor/art/aegina_build.py for the
// aethos primary: its ground cells borrow aethos's grass, sand, sea and path, so
// rebuild it whenever aethos changes.
const struct Tileset gTileset_Aegina =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Aegina,
    .palettes = gTilesetPalettes_PorytilesManaged_Aegina,
    .metatiles = gMetatiles_PorytilesManaged_Aegina,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Aegina,
    .callback = NULL,
};

// Porytiles-managed secondary built by tools/ichor/art/skiron_build.py: Act I's
// mainland road, Route 4's kilns, tombs, rockslide and camp and Route 5's Skironian
// cliffs. Its cells on grass, path and sea borrow aethos's, so rebuild it whenever
// aethos's ground changes.
const struct Tileset gTileset_Skiron =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Skiron,
    .palettes = gTilesetPalettes_PorytilesManaged_Skiron,
    .metatiles = gMetatiles_PorytilesManaged_Skiron,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Skiron,
    .callback = NULL,
};

// Ichor: trireme, the Euploia's deck and hold. A Porytiles-managed secondary
// built by tools/ichor/art/trireme_build.py for the aethos primary: its sea
// cells borrow aethos's animated sea, so rebuild it whenever aethos changes.
const struct Tileset gTileset_Trireme =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Trireme,
    .palettes = gTilesetPalettes_PorytilesManaged_Trireme,
    .metatiles = gMetatiles_PorytilesManaged_Trireme,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Trireme,
    .callback = NULL,
};

// Porytiles-managed secondary built by tools/ichor/art/cave_dark_build.py: the
// dark places (Hecate's Hollow, the Salt Grotto, Akti's Sea Grotto, the Kronion
// Crypt). It uses only its own tiles and palettes 6-12, so it works on any
// primary; the maps pair it with aethos.
const struct Tileset gTileset_CaveDark =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_CaveDark,
    .palettes = gTilesetPalettes_PorytilesManaged_CaveDark,
    .metatiles = gMetatiles_PorytilesManaged_CaveDark,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_CaveDark,
    .callback = InitTilesetAnim_PorytilesManaged_CaveDark,
};

// Ichor: labyrinth, Daedalus's Labyrinth under Knossa (LABYRINTH.md §11). Porytiles-managed,
// built by tools/ichor/art/labyrinth_build.py; so far it holds the house's masonry and
// Daedalus's workshop. It uses only its own tiles and palettes 6-12, with opaque floors,
// so it works on any interior primary (drawn for oikos). Its variant palette sets,
// gTilesetPalettes_LabyrinthGlow (the doused torch) and gTilesetPalettes_LabyrinthDawn
// (scene L), are in graphics.h. No layout uses it yet.
const struct Tileset gTileset_Labyrinth =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Labyrinth,
    .palettes = gTilesetPalettes_PorytilesManaged_Labyrinth,
    .metatiles = gMetatiles_PorytilesManaged_Labyrinth,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Labyrinth,
    .callback = NULL,
};

// Ichor: the Mystery sanctum under Eleusa (tools/ichor/maps/sanctum.py). Two derived
// secondaries, drawn from nothing new: each shares a base set's tiles, palettes and
// animation, and has its own metatiles: the base set's, then a few composed from
// existing tiles (braziers, pithoi and lamps on the crypt's flagstones, grain pits, the
// spring basin, the hall's rimmed pits and glowing chasm). Re-run the builder after
// cave_dark or temple_demeter is rebuilt.
const struct Tileset gTileset_EleusaSanctumRock =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_CaveDark,
    .palettes = gTilesetPalettes_PorytilesManaged_CaveDark,
    .metatiles = gMetatiles_EleusaSanctumRock,
    .metatileAttributes = gMetatileAttributes_EleusaSanctumRock,
    .callback = InitTilesetAnim_PorytilesManaged_CaveDark,
};

const struct Tileset gTileset_EleusaSanctumHall =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_TempleDemeter,
    .palettes = gTilesetPalettes_PorytilesManaged_TempleDemeter,
    .metatiles = gMetatiles_EleusaSanctumHall,
    .metatileAttributes = gMetatileAttributes_EleusaSanctumHall,
    .callback = NULL,
};

// Porytiles-managed secondary, ported from claude/world-act2-0a92e7 (its generator,
// tools/ichor/art/thyrsa_build.py, stays on that branch; porytiles_src is here): Thyrsa City
// (its Cyclopean walls and gates, streets, houses, the Agora, the Temple of Dionysus's
// front, the Asclepeion, Semele's chamber and the vineyards). It uses only its own
// tiles and palettes 6-12; cells on grass borrow aethos's, so rebuild it whenever
// aethos changes.
const struct Tileset gTileset_Thyrsa =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Thyrsa,
    .palettes = gTilesetPalettes_PorytilesManaged_Thyrsa,
    .metatiles = gMetatiles_PorytilesManaged_Thyrsa,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Thyrsa,
    .callback = InitTilesetAnim_Thyrsa,     // Semele's smoke (src/tileset_anims.c)
};

// Ichor (Act II rooms): Thyrsa's plastered rooms: the Asclepeion, the Agora, Pindaros's and Polos's houses. A Porytiles-managed secondary for the oikos
// primary, ported from claude/world-act2-0a92e7 (generator tools/ichor/maps/thyrsa_rooms.py stays there).
// It uses only its own tiles and palettes 6-12.
const struct Tileset gTileset_ThyrsaRooms =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_ThyrsaRooms,
    .palettes = gTilesetPalettes_PorytilesManaged_ThyrsaRooms,
    .metatiles = gMetatiles_PorytilesManaged_ThyrsaRooms,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_ThyrsaRooms,
    .callback = NULL,
};

// Ichor (Act II rooms): Thyrsa's households: Staphylos's, Eudora's, Euthykles's workshop and Manto's. A Porytiles-managed secondary for the oikos
// primary, ported from claude/world-act2-0a92e7 (generator tools/ichor/maps/thyrsa_rooms.py stays there).
// It uses only its own tiles and palettes 6-12.
const struct Tileset gTileset_ThyrsaHomes =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_ThyrsaHomes,
    .palettes = gTilesetPalettes_PorytilesManaged_ThyrsaHomes,
    .metatiles = gMetatiles_PorytilesManaged_ThyrsaHomes,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_ThyrsaHomes,
    .callback = NULL,
};

// Ichor (Act II rooms): the stone rooms: Eleutherai's watch-house and homes, the Kantharos tavern and Chthonia's house. A Porytiles-managed secondary for the oikos
// primary, ported from claude/world-act2-0a92e7 (generator tools/ichor/maps/thyrsa_rooms.py stays there).
// It uses only its own tiles and palettes 6-12.
const struct Tileset gTileset_ThyrsaStone =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_ThyrsaStone,
    .palettes = gTilesetPalettes_PorytilesManaged_ThyrsaStone,
    .metatiles = gMetatiles_PorytilesManaged_ThyrsaStone,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_ThyrsaStone,
    .callback = NULL,
};

// Ichor: arkadia, Arkadia, the hunters' town (Act II, beat 41). Porytiles-managed, ported from claude/world-act2-0a92e7, where it is built by
// tools/ichor/art/arkadia_build.py for the aethos primary: its cells on grass borrow
// aethos's grass, so rebuild it whenever aethos changes. It uses only its own
// tiles and palettes 6-12.
const struct Tileset gTileset_Arkadia =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Arkadia,
    .palettes = gTilesetPalettes_PorytilesManaged_Arkadia,
    .metatiles = gMetatiles_PorytilesManaged_Arkadia,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Arkadia,
    .callback = NULL,
};

// Ichor: styx_falls, the Arkadian climb: Styx Falls and Nonakris. Porytiles-managed, ported from claude/world-act2-0a92e7, where it is built by
// tools/ichor/art/heights_build.py for the aethos primary; it shares its core section
// with gTileset_ArkadiaHeights at the same ids. Its ground cells borrow aethos's, so
// rebuild it whenever aethos changes.
const struct Tileset gTileset_StyxFalls =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_StyxFalls,
    .palettes = gTilesetPalettes_PorytilesManaged_StyxFalls,
    .metatiles = gMetatiles_PorytilesManaged_StyxFalls,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_StyxFalls,
    .callback = NULL,
};

// Ichor: kyllene, the Arkadian climb: Route 12, the cypress road over Kyllene. Porytiles-managed, ported from claude/world-act2-0a92e7, where it is built by
// tools/ichor/art/heights_build.py for the aethos primary; it shares its core section
// with gTileset_ArkadiaHeights at the same ids. Its ground cells borrow aethos's, so
// rebuild it whenever aethos changes.
const struct Tileset gTileset_Kyllene =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Kyllene,
    .palettes = gTilesetPalettes_PorytilesManaged_Kyllene,
    .metatiles = gMetatiles_PorytilesManaged_Kyllene,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Kyllene,
    .callback = NULL,
};

// Porytiles-managed secondary ported from claude/world-act2-0a92e7, where it is built by tools/ichor/art/temple_artemis_build.py: the Temple
// of Artemis at Arkadia, the goddess's night garden and the Hunt for the Hind. It uses only
// its own tiles and palettes 6-12, with opaque floors, so it works on any primary (drawn for
// oikos: an indoor map, so the clock's tint never touches its night).
const struct Tileset gTileset_TempleArtemis =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_TempleArtemis,
    .palettes = gTilesetPalettes_PorytilesManaged_TempleArtemis,
    .metatiles = gMetatiles_PorytilesManaged_TempleArtemis,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_TempleArtemis,
    .callback = NULL,
};

// Ichor (Act II batch 3 rooms): Arkadia's public rooms: the Asclepeion, the Agora stall, and Klymene's upper room. A Porytiles-managed secondary for the oikos
// primary, ported from claude/world-act2-0a92e7, where it is built by tools/ichor/maps/arkrooms.py (art in tools/ichor/art/arkrooms_*.py).
// It uses only its own tiles and palettes 6-12.
const struct Tileset gTileset_ArkadiaRooms =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_ArkadiaRooms,
    .palettes = gTilesetPalettes_PorytilesManaged_ArkadiaRooms,
    .metatiles = gMetatiles_PorytilesManaged_ArkadiaRooms,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_ArkadiaRooms,
    .callback = NULL,
};

// Ichor (Act II batch 3 rooms): Arkadia's homes: Nyktimos's hall, Hippothoos's charcoal hut and Krotos's house and byre. A Porytiles-managed secondary for the oikos
// primary, ported from claude/world-act2-0a92e7, where it is built by tools/ichor/maps/arkrooms.py (art in tools/ichor/art/arkrooms_*.py).
// It uses only its own tiles and palettes 6-12.
const struct Tileset gTileset_ArkadiaHomes =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_ArkadiaHomes,
    .palettes = gTilesetPalettes_PorytilesManaged_ArkadiaHomes,
    .metatiles = gMetatiles_PorytilesManaged_ArkadiaHomes,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_ArkadiaHomes,
    .callback = NULL,
};

// Ichor (Act II batch 3 rooms): Styx Falls's rooms: the Inn at the Falls, Horkia's house of oaths and Kepheus's house. A Porytiles-managed secondary for the oikos
// primary, ported from claude/world-act2-0a92e7, where it is built by tools/ichor/maps/arkrooms.py (art in tools/ichor/art/arkrooms_*.py).
// It uses only its own tiles and palettes 6-12.
const struct Tileset gTileset_StyxRooms =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_StyxRooms,
    .palettes = gTilesetPalettes_PorytilesManaged_StyxRooms,
    .metatiles = gMetatiles_PorytilesManaged_StyxRooms,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_StyxRooms,
    .callback = NULL,
};

// Ichor: maia_cave, the Arkadian climb: the Cave of Maia on Route 12. Porytiles-managed, ported from claude/world-act2-0a92e7, where it is built by
// tools/ichor/art/heights_build.py for the aethos primary: its ground cells borrow
// aethos's grass, road, sea, tall grass, shade and waterfall, so rebuild it whenever aethos changes.
const struct Tileset gTileset_MaiaCave =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_MaiaCave,
    .palettes = gTilesetPalettes_PorytilesManaged_MaiaCave,
    .metatiles = gMetatiles_PorytilesManaged_MaiaCave,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_MaiaCave,
    .callback = NULL,
};

// Ichor: arkadia_wood, the Cypress Wood and the Pool of Mnemosyne (Act II, beats 42-43). Porytiles-managed, ported from claude/world-act2-0a92e7, where it is built by
// tools/ichor/art/arkadia_build.py for the aethos primary: its cells on grass borrow
// aethos's grass, so rebuild it whenever aethos changes. It uses only its own
// tiles and palettes 6-12.
const struct Tileset gTileset_ArkadiaWood =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_ArkadiaWood,
    .palettes = gTilesetPalettes_PorytilesManaged_ArkadiaWood,
    .metatiles = gMetatiles_PorytilesManaged_ArkadiaWood,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_ArkadiaWood,
    .callback = NULL,
};
