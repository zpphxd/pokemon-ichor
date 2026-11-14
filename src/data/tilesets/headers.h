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
