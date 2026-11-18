// Ichor: glow-paint (design/SYSTEMS.md §2; design/ENGINE_API.md §2).
//
// With the torch doused on a dark map, a secondary tileset listed here shows
// its glow copies: the map's palettes go black but for what glows (chalk,
// glowing seeds), and the map shows in the dark while its people don't.
//
// A tileset's glow copies are data/tilesets/secondary/<name>/glow/00.pal-15.pal,
// the same slots in the same order as its palettes/, every color black but
// the glowing ones. Slots 0-12 load (the primary's six go black with them).
// Declare them beside the tileset's palettes in src/data/tilesets/graphics.h:
//
//   const u16 ALIGNED(4) gTilesetPalettes_TrophoniosGlow[][16] =
//   {
//       INCGFX_U16("data/tilesets/secondary/trophonios/glow/00.pal", ".gbapal"),
//       ... through 15.pal
//   };
//
// then add a row here: { &gTileset_..., gTilesetPalettes_TrophoniosGlow }.

extern const struct Tileset gTileset_Labyrinth;
extern const u16 gTilesetPalettes_LabyrinthGlowFull[][16];

struct IchorGlow
{
    const struct Tileset *tileset;
    const u16 (*palettes)[16];
};

static const struct IchorGlow sGlowTilesets[] =
{
    { &gTileset_Labyrinth, gTilesetPalettes_LabyrinthGlowFull },  // Ring III's glow-marks, the faint thread
    { NULL, NULL },  // the end
};
