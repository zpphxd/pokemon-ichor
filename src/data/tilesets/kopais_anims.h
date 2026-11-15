// Ichor: gTileset_Kopais's tile animation (Route 8): the reeds sway, the marsh
// water glints, the eel-smoker's fire flickers. Written by
// tools/ichor/art/kopais_build.py, which finds the compiled tiles of every
// animated piece; included at the end of src/tileset_anims.c. Do not edit.
#ifndef GUARD_KOPAIS_ANIMS_H
#define GUARD_KOPAIS_ANIMS_H

static const u16 sKopaisAnim_Run0_0[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run00_0.4bpp");
static const u16 sKopaisAnim_Run0_1[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run00_1.4bpp");
static const u16 sKopaisAnim_Run0_2[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run00_2.4bpp");
static const u16 sKopaisAnim_Run0_3[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run00_3.4bpp");
static const u16 *const sKopaisAnim_Run0[] = {sKopaisAnim_Run0_0, sKopaisAnim_Run0_1, sKopaisAnim_Run0_2, sKopaisAnim_Run0_3};
static const u16 sKopaisAnim_Run1_0[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run01_0.4bpp");
static const u16 sKopaisAnim_Run1_1[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run01_1.4bpp");
static const u16 sKopaisAnim_Run1_2[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run01_2.4bpp");
static const u16 sKopaisAnim_Run1_3[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run01_3.4bpp");
static const u16 *const sKopaisAnim_Run1[] = {sKopaisAnim_Run1_0, sKopaisAnim_Run1_1, sKopaisAnim_Run1_2, sKopaisAnim_Run1_3};
static const u16 sKopaisAnim_Run2_0[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run02_0.4bpp");
static const u16 sKopaisAnim_Run2_1[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run02_1.4bpp");
static const u16 sKopaisAnim_Run2_2[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run02_2.4bpp");
static const u16 sKopaisAnim_Run2_3[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run02_3.4bpp");
static const u16 *const sKopaisAnim_Run2[] = {sKopaisAnim_Run2_0, sKopaisAnim_Run2_1, sKopaisAnim_Run2_2, sKopaisAnim_Run2_3};
static const u16 sKopaisAnim_Run3_0[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run03_0.4bpp");
static const u16 sKopaisAnim_Run3_1[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run03_1.4bpp");
static const u16 sKopaisAnim_Run3_2[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run03_2.4bpp");
static const u16 sKopaisAnim_Run3_3[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run03_3.4bpp");
static const u16 *const sKopaisAnim_Run3[] = {sKopaisAnim_Run3_0, sKopaisAnim_Run3_1, sKopaisAnim_Run3_2, sKopaisAnim_Run3_3};
static const u16 sKopaisAnim_Run4_0[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run04_0.4bpp");
static const u16 sKopaisAnim_Run4_1[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run04_1.4bpp");
static const u16 sKopaisAnim_Run4_2[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run04_2.4bpp");
static const u16 sKopaisAnim_Run4_3[] = INCBIN_U16("data/tilesets/secondary/kopais/anim/run04_3.4bpp");
static const u16 *const sKopaisAnim_Run4[] = {sKopaisAnim_Run4_0, sKopaisAnim_Run4_1, sKopaisAnim_Run4_2, sKopaisAnim_Run4_3};

struct KopaisAnimRun { const u16 *const *frames; u16 tile; u16 count; };
static const struct KopaisAnimRun sKopaisAnimRuns[] = {
    {sKopaisAnim_Run0, 1, 73},
    {sKopaisAnim_Run1, 260, 2},
    {sKopaisAnim_Run2, 308, 6},
    {sKopaisAnim_Run3, 325, 6},
    {sKopaisAnim_Run4, 348, 11},
};

#define KOPAIS_ANIM_PERIOD 24
#define KOPAIS_ANIM_BATCH 6

// Each phase change copies the runs a few at a time over consecutive frames,
// so the transfer buffer (20 slots) never fills.
static void TilesetAnim_Kopais(u16 timer)
{
    u16 step = timer % KOPAIS_ANIM_PERIOD;
    u16 phase = (timer / KOPAIS_ANIM_PERIOD) % 4;
    u16 i;
    for (i = step * KOPAIS_ANIM_BATCH; i < (step + 1) * KOPAIS_ANIM_BATCH && i < ARRAY_COUNT(sKopaisAnimRuns); i++)
        AppendTilesetAnimToBuffer(sKopaisAnimRuns[i].frames[phase],
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + sKopaisAnimRuns[i].tile)),
                                  sKopaisAnimRuns[i].count * TILE_SIZE_4BPP);
}

void InitTilesetAnim_Kopais(void)
{
    sSecondaryTilesetAnimCounter = 0;
    sSecondaryTilesetAnimCounterMax = KOPAIS_ANIM_PERIOD * 4 * 2;
    sSecondaryTilesetAnimCallback = TilesetAnim_Kopais;
}

#endif // GUARD_KOPAIS_ANIMS_H
