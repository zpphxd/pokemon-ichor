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

// Ichor: kithairon, the Kithairon crossing: Route 6, Eleutherai and Mt. Kithairon. Porytiles-managed, built by
// tools/ichor/art/kithairon_build.py for the aethos primary: its ground cells borrow
// aethos's grass, road, sea and tall grass, so rebuild it whenever aethos changes.
const struct Tileset gTileset_Kithairon =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Kithairon,
    .palettes = gTilesetPalettes_PorytilesManaged_Kithairon,
    .metatiles = gMetatiles_PorytilesManaged_Kithairon,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Kithairon,
    .callback = NULL,
};

// Ichor: kronia, the Kithairon crossing: Route 7 and the Kronia grounds. Porytiles-managed, built by
// tools/ichor/art/kithairon_build.py for the aethos primary: its ground cells borrow
// aethos's grass, road, sea and tall grass, so rebuild it whenever aethos changes.
const struct Tileset gTileset_Kronia =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Kronia,
    .palettes = gTilesetPalettes_PorytilesManaged_Kronia,
    .metatiles = gMetatiles_PorytilesManaged_Kronia,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Kronia,
    .callback = NULL,
};

// Ichor: kithairon_cave, the Kithairon crossing: Antiope's cave. Porytiles-managed, built by
// tools/ichor/art/kithairon_build.py for the aethos primary: its ground cells borrow
// aethos's grass, road, sea and tall grass, so rebuild it whenever aethos changes.
const struct Tileset gTileset_KithaironCave =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_KithaironCave,
    .palettes = gTilesetPalettes_PorytilesManaged_KithaironCave,
    .metatiles = gMetatiles_PorytilesManaged_KithaironCave,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_KithaironCave,
    .callback = NULL,
};

// Ichor: theater, Thyrsa's theater (Act II, beats 32-34): the cavea and its
// seated crowd, the orchestra, the skene's painted front and doors, the god-machine.
// Porytiles-managed, built by tools/ichor/art/theater_build.py. It uses only its own
// tiles and palettes 6-12; palettes 10-12 are copies of the crowd's, one per pair of
// blocks of seats, so the trance's pulse can stop pair by pair (src/ichor_act2_scene.c).
// Cells on grass borrow aethos's, so rebuild it whenever aethos changes.
const struct Tileset gTileset_Theater =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Theater,
    .palettes = gTilesetPalettes_PorytilesManaged_Theater,
    .metatiles = gMetatiles_PorytilesManaged_Theater,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Theater,
    .callback = NULL,
};

// Ichor: skene, the theater's stage building inside: the backstage corridor behind
// the three doors and Silenos's prop room. Porytiles-managed, built by
// tools/ichor/art/theater_build.py; it uses only its own tiles and palettes 6-12,
// and is meant for the oikos primary.
const struct Tileset gTileset_Skene =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Skene,
    .palettes = gTilesetPalettes_PorytilesManaged_Skene,
    .metatiles = gMetatiles_PorytilesManaged_Skene,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Skene,
    .callback = NULL,
};

// Porytiles-managed secondary built by tools/ichor/art/thyrsa_build.py: Thyrsa City
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

// Porytiles-managed secondary built by tools/ichor/art/temple_dionysus_build.py: the Temple
// of Dionysus at Thyrsa and the Three-Act Play. It uses only its own tiles and palettes
// 6-12, with opaque floors, so it works on any primary (drawn for oikos).
const struct Tileset gTileset_TempleDionysus =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_TempleDionysus,
    .palettes = gTilesetPalettes_PorytilesManaged_TempleDionysus,
    .metatiles = gMetatiles_PorytilesManaged_TempleDionysus,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_TempleDionysus,
    .callback = NULL,
};

// Ichor (Act II rooms): Thyrsa's plastered rooms: the Asclepeion, the Agora, Pindaros's and Polos's houses. A Porytiles-managed secondary for the oikos
// primary, built by tools/ichor/maps/thyrsa_rooms.py (art in tools/ichor/art/thyrsa_rooms_*.py).
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
// primary, built by tools/ichor/maps/thyrsa_rooms.py (art in tools/ichor/art/thyrsa_rooms_*.py).
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
// primary, built by tools/ichor/maps/thyrsa_rooms.py (art in tools/ichor/art/thyrsa_rooms_*.py).
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

// Ichor (Act II batch 2): Trophonios's cave under Lebadeia (SCRIPT.md Part 5, beats 35B-35C).
// A Porytiles-managed secondary for the aethos primary, built by tools/ichor/art/trophonios_build.py.
// It uses only its own tiles and palettes 6-12.
const struct Tileset gTileset_Trophonios =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_Trophonios,
    .palettes = gTilesetPalettes_PorytilesManaged_Trophonios,
    .metatiles = gMetatiles_PorytilesManaged_Trophonios,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_Trophonios,
    .callback = NULL,
};

// Ichor (Act II rooms, the road west): Lebadeia's pilgrims' hall and the mason's house: living rock, rubble, cut stone. A Porytiles-managed secondary for the oikos
// primary, built by tools/ichor/maps/westrooms.py (art in tools/ichor/art/westrooms_*.py).
// It uses only its own tiles and palettes 6-12.
const struct Tileset gTileset_WestStone =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_WestStone,
    .palettes = gTilesetPalettes_PorytilesManaged_WestStone,
    .metatiles = gMetatiles_PorytilesManaged_WestStone,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_WestStone,
    .callback = NULL,
};

// Ichor (Act II rooms, the road west): Kirrha's pilgrims' inn, Agora stall, the muleteer's and the old sweeper's houses. A Porytiles-managed secondary for the oikos
// primary, built by tools/ichor/maps/westrooms.py (art in tools/ichor/art/westrooms_*.py).
// It uses only its own tiles and palettes 6-12.
const struct Tileset gTileset_WestHarbor =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_WestHarbor,
    .palettes = gTilesetPalettes_PorytilesManaged_WestHarbor,
    .metatiles = gMetatiles_PorytilesManaged_WestHarbor,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_WestHarbor,
    .callback = NULL,
};

// Ichor (Act II rooms, the road west): Herkyna's river house in Lebadeia, and Aigion's old Achaean's and goatherd's houses. A Porytiles-managed secondary for the oikos
// primary, built by tools/ichor/maps/westrooms.py (art in tools/ichor/art/westrooms_*.py).
// It uses only its own tiles and palettes 6-12.
const struct Tileset gTileset_WestHomes =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_PorytilesManaged_WestHomes,
    .palettes = gTilesetPalettes_PorytilesManaged_WestHomes,
    .metatiles = gMetatiles_PorytilesManaged_WestHomes,
    .metatileAttributes = gMetatileAttributes_PorytilesManaged_WestHomes,
    .callback = NULL,
};

// Porytiles-managed secondary built by tools/ichor/art/temple_artemis_build.py: the Temple
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
