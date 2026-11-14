#include "global.h"
#include "main.h"
#include "palette.h"
#include "scanline_effect.h"
#include "task.h"
#include "title_screen.h"
#include "libgcnmultiboot.h"
#include "malloc.h"
#include "gpu_regs.h"
#include "link.h"
#include "multiboot_pokemon_colosseum.h"
#include "load_save.h"
#include "save.h"
#include "new_game.h"
#include "m4a.h"
#include "decompress.h"
#include "constants/songs.h"
#include "trig.h"
#include "intro.h"
#include "graphics.h"
#include "sound.h"
#include "sprite.h"
#include "util.h"
#include "expansion_intro.h"
#include "intro_frlg.h"
#include "constants/rgb.h"
#include "pokemon.h"
#include "data/intro_ichor_layout.h"

/*
    Ichor: the boot sequence (design/phase1/INTRO.md).

    Scene 0. The copyright card (graphics/intro/copyright.png), then, with
             EXPANSION_INTRO, the "powered by" card (src/expansion_intro.c).
    Scene 1. The studio mark: a drop of ichor falls through the dark and blooms
             into ΙΧΩΡ, ringed by the Twelve.
    Scene 2. The frieze: Clotho spins, and her thread runs along a black-figure
             frieze of Aethos as the pot turns: the olive grove of Elaia, where
             the golden thread rises unspun; the sea, the trireme and the ketos;
             the temple of the Twelve; Olympus and Zapdos.
    Scene 3. The loom: Lachesis measures the warp and Atropos cuts it, until the
             shears reach the golden thread, which has no measure, and stop.

    Then a white cut to the title screen, where the three Fates stand painted.
    The art is drawn by tools/ichor/art/intro_screen.py.

    Ichor replaced Emerald's scenes 1-3 (the Game Freak logo, the bike ride and
    the legendary trio) wholesale; the copyright screen code is Emerald's.
*/

static void MainCB2_EndIntro(void);
static void Task_IchorIntro(u8 taskId);

enum {
    COPYRIGHT_INITIALIZE,
    COPYRIGHT_EMULATOR_BLEND,
    COPYRIGHT_START_FADE = 140,
    COPYRIGHT_START_INTRO,
};

#define COLOSSEUM_GAME_CODE 0x65366347 // "Gc6e" in ASCII

COMMON_DATA u32 gIntroFrameCounter = 0;
COMMON_DATA struct GcmbStruct gMultibootProgramStruct = {0};

static void VBlankCB_Intro(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
    ScanlineEffect_InitHBlankDmaTransfer();
}

void MainCB2_Intro(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    UpdatePaletteFade();
    if (gMain.newKeys != 0 && !gPaletteFade.active)
        SetMainCallback2(MainCB2_EndIntro);
    else if (gIntroFrameCounter != -1)
        gIntroFrameCounter++;
}

static void MainCB2_EndIntro(void)
{
    if (!UpdatePaletteFade())
    {
        ScanlineEffect_Stop(); // Ichor: the loom sways its golden thread per scanline
        SetMainCallback2(CB2_InitTitleScreen);
    }
}

static void LoadCopyrightGraphics(u16 tilesetAddress, u16 tilemapAddress, u16 paletteOffset)
{
    DecompressDataWithHeaderVram(gIntroCopyright_Gfx, (void *)(VRAM + tilesetAddress));
    DecompressDataWithHeaderVram(gIntroCopyright_Tilemap, (void *)(VRAM + tilemapAddress));
    LoadPalette(gIntroCopyright_Pal, paletteOffset, PLTT_SIZE_4BPP);
}

static void SerialCB_CopyrightScreen(void)
{
    GameCubeMultiBoot_HandleSerialInterrupt(&gMultibootProgramStruct);
}

static u8 SetUpCopyrightScreen(void)
{
    if (IS_FRLG)
        return SetUpCopyrightScreenFrlg();

    switch (gMain.state)
    {
    case COPYRIGHT_INITIALIZE:
        SetVBlankCallback(NULL);
        SetGpuReg(REG_OFFSET_BLDCNT, 0);
        SetGpuReg(REG_OFFSET_BLDALPHA, 0);
        SetGpuReg(REG_OFFSET_BLDY, 0);
        *(u16 *)PLTT = RGB_WHITE;
        SetGpuReg(REG_OFFSET_DISPCNT, 0);
        SetGpuReg(REG_OFFSET_BG0HOFS, 0);
        SetGpuReg(REG_OFFSET_BG0VOFS, 0);
        CpuFill32(0, (void *)VRAM, VRAM_SIZE);
        CpuFill32(0, (void *)OAM, OAM_SIZE);
        CpuFill16(0, (void *)(PLTT + 2), PLTT_SIZE - 2);
        ResetPaletteFade();
        LoadCopyrightGraphics(0, 0x3800, BG_PLTT_ID(0));
        ScanlineEffect_Stop();
        ResetTasks();
        ResetSpriteData();
        FreeAllSpritePalettes();
        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_WHITEALPHA);
        SetGpuReg(REG_OFFSET_BG0CNT, BGCNT_PRIORITY(0)
                                   | BGCNT_CHARBASE(0)
                                   | BGCNT_SCREENBASE(7)
                                   | BGCNT_16COLOR
                                   | BGCNT_TXT256x256);
        EnableInterrupts(INTR_FLAG_VBLANK);
        SetVBlankCallback(VBlankCB_Intro);
        REG_DISPCNT = DISPCNT_MODE_0 | DISPCNT_OBJ_1D_MAP | DISPCNT_BG0_ON;
        SetSerialCallback(SerialCB_CopyrightScreen);
        GameCubeMultiBoot_Init(&gMultibootProgramStruct);
    // REG_DISPCNT needs to be overwritten the second time, because otherwise the intro won't show up on VBA 1.7.2 and John GBA Lite emulators.
    // The REG_DISPCNT overwrite is NOT needed in m-GBA, No$GBA, VBA 1.8.0, My Boy and Pizza Boy GBA emulators.
    case COPYRIGHT_EMULATOR_BLEND:
        REG_DISPCNT = DISPCNT_MODE_0 | DISPCNT_OBJ_1D_MAP | DISPCNT_BG0_ON;
    default:
        UpdatePaletteFade();
        gMain.state++;
        GameCubeMultiBoot_Main(&gMultibootProgramStruct);
        break;
    case COPYRIGHT_START_FADE:
        GameCubeMultiBoot_Main(&gMultibootProgramStruct);
        if (gMultibootProgramStruct.gcmb_field_2 != 1)
        {
            BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
            gMain.state++;
        }
        break;
    case COPYRIGHT_START_INTRO:
        if (UpdatePaletteFade())
            break;
#if EXPANSION_INTRO == TRUE
        SetMainCallback2(CB2_ExpansionIntro);
        CreateTask(Task_HandleExpansionIntro, 0);
#else
        CreateTask(Task_Scene1_Load, 0);
        SetMainCallback2(MainCB2_Intro);
#endif
        if (gMultibootProgramStruct.gcmb_field_2 != 0)
        {
            if (gMultibootProgramStruct.gcmb_field_2 == 2)
            {
                // check the multiboot ROM header game code to see if we already did this
                if (*(u32 *)(EWRAM_START + 0xAC) == COLOSSEUM_GAME_CODE)
                {
                    CpuCopy16(&gMultiBootProgram_PokemonColosseum_Start, (void *)EWRAM_START, sizeof(gMultiBootProgram_PokemonColosseum_Start));
                    *(u32 *)(EWRAM_START + 0xAC) = COLOSSEUM_GAME_CODE;
                }
                GameCubeMultiBoot_ExecuteProgram(&gMultibootProgramStruct);
            }
        }
        else
        {
            GameCubeMultiBoot_Quit();
            SetSerialCallback(SerialCB);
        }
        return 0;
    }

    return 1;
}

void CB2_InitCopyrightScreenAfterBootup(void)
{
    if (!SetUpCopyrightScreen())
    {
        SetSaveBlocksPointers(GetSaveBlocksPointersBaseOffset());
        ResetMenuAndMonGlobals();
        Save_ResetSaveCounters();
        LoadGameSave(SAVE_NORMAL);
        if (gSaveFileStatus == SAVE_STATUS_EMPTY || gSaveFileStatus == SAVE_STATUS_CORRUPT)
            Sav2_ClearSetDefault();
        SetPokemonCryStereo(gSaveBlock2Ptr->optionsSound);
        InitHeap(gHeap, HEAP_SIZE);
    }
}

void CB2_InitCopyrightScreenAfterTitleScreen(void)
{
    SetUpCopyrightScreen();
}

void PanFadeAndZoomScreen(u16 screenX, u16 screenY, u16 zoom, u16 alpha)
{
    struct BgAffineSrcData src;
    struct BgAffineDstData dest;

    src.texX = 0x8000;
    src.texY = 0x8000;
    src.scrX = screenX;
    src.scrY = screenY;
    src.sx = zoom;
    src.sy = zoom;
    src.alpha = alpha;
    BgAffineSet(&src, &dest, 1);
    SetGpuReg(REG_OFFSET_BG2PA, dest.pa);
    SetGpuReg(REG_OFFSET_BG2PB, dest.pb);
    SetGpuReg(REG_OFFSET_BG2PC, dest.pc);
    SetGpuReg(REG_OFFSET_BG2PD, dest.pd);
    SetGpuReg(REG_OFFSET_BG2X_L, dest.dx);
    SetGpuReg(REG_OFFSET_BG2X_H, dest.dx >> 16);
    SetGpuReg(REG_OFFSET_BG2Y_L, dest.dy);
    SetGpuReg(REG_OFFSET_BG2Y_H, dest.dy >> 16);
}

// ---------------------------------------------------------------------------
// The movie's clock
// ---------------------------------------------------------------------------
// gIntroFrameCounter counts frames from the studio card, where MUS_INTRO
// starts, and every cue below is a frame on that clock. INTRO.md has them as a
// timing sheet. MUS_INTRO is 4/4 at 140 bpm: a beat is 25.6 frames, a bar
// 102.4; its sections change at 1024 (B) and 2048 (C) and it ends near 2355.

// Scene 1: the studio mark
#define T_DROP_FORM        24   // a bead of ichor gathers at the top of the dark
#define T_DROP_FALL        86   // it lets go
#define T_DROP_IMPACT     112   // it lands, and the mark's drop flares
#define T_RING            124   // the ripple reaches the ring of the Twelve
#define T_LETTERS         140   // ΙΧΩΡ gilds in
#define T_STUDIO_OUT      300   // fade to black
#define T_FRIEZE_LOAD     372
// Scene 2: the frieze
#define T_CLOTHO          410   // fade in on Clotho at her spindle (bar 5)
#define T_THREAD_GROW     466   // her thread runs out to the right
#define T_THREAD_DONE     700
#define T_PAN             717   // the pot begins to turn (bar 8), gathering speed into the timpani roll
#define T_GOLD           1024   // the golden thread rises in Elaia's grove (section B)
#define T_GOLD_DONE      1084
#define T_PAN_END        1990   // Olympus
#define T_BOLT_1         1894   // Zapdos's lightning
#define T_BOLT_2         1936
#define T_BOLT_3         1972
#define T_TO_LOOM        2032   // white
// Scene 3: the loom (section C)
#define T_LOOM           2048
#define T_ROD_IN         2050
#define T_ROD_HOP        2061   // Lachesis's rod at the first thread; a thread per eighth note
#define T_ROD_OUT        2142
#define T_SHEARS_IN      2150
#define T_SNIP           2176   // Atropos's first cut; a cut per beat
#define T_SHEARS_GOLD    2253   // the shears open on the golden thread (bar 3, the crash)
#define T_FLASH          2326   // the cut to white
#define T_END            2342

#define ROD_HOP_TIME(k)  (T_ROD_HOP + ((k) * 64) / 5)
#define SNIP_TIME(k)     (T_SNIP + ((k) * 128) / 5)

#define INK_COLOR        RGB(4, 3, 3)

enum {
    SCENE_STUDIO,
    SCENE_FRIEZE,
    SCENE_LOOM,
    SCENE_DONE,
};

// BG palette rows of the painted scenes (tools/ichor/art/intro_screen.py)
#define PAL_PAINT 0
#define PAL_CLAY  1
#define PAL_WHITE 2
#define PAL_GOLD  3

// ---------------------------------------------------------------------------
// Art
// ---------------------------------------------------------------------------
static const u32 sStudioMark_Gfx[]       = INCGFX_U32("graphics/intro/studio_mark.png", ".4bpp.smol");
static const u32 sStudioMark_Tilemap[]   = INCGFX_U32("graphics/intro/studio_mark.bin", ".smolTM");
static const u16 sStudioMark_Pal[]       = INCGFX_U16("graphics/intro/studio_mark.pal", ".gbapal");
static const u32 sStudioDrop_Gfx[]       = INCGFX_U32("graphics/intro/studio_drop.png", ".4bpp.smol");
static const u32 sStudioRipple_Gfx[]     = INCGFX_U32("graphics/intro/studio_ripple.png", ".4bpp.smol");
static const u16 sStudioObj_Pal[]        = INCGFX_U16("graphics/intro/studio_obj.pal", ".gbapal");

static const u32 sFrieze_Gfx[]           = INCGFX_U32("graphics/intro/frieze.png", ".4bpp.smol");
static const u32 sFriezeAux_Gfx[]        = INCGFX_U32("graphics/intro/frieze_aux.png", ".4bpp.smol");
static const u16 sFrieze_Tilemap[]       = INCBIN_U16("graphics/intro/frieze.bin");        // column-major, 20 rows
static const u16 sFriezeWhite_Tilemap[]  = INCBIN_U16("graphics/intro/frieze_white.bin");
static const u16 sFriezeGold_Tilemap[]   = INCBIN_U16("graphics/intro/frieze_gold.bin");
static const u32 sClay_Tilemap[]         = INCGFX_U32("graphics/intro/clay.bin", ".smolTM");

static const u32 sLoom_Gfx[]             = INCGFX_U32("graphics/intro/loom.png", ".4bpp.smol");
static const u32 sLoomAux_Gfx[]          = INCGFX_U32("graphics/intro/loom_aux.png", ".4bpp.smol");
static const u32 sLoom_Tilemap[]         = INCGFX_U32("graphics/intro/loom.bin", ".smolTM");
static const u32 sLoomGold_Tilemap[]     = INCGFX_U32("graphics/intro/loom_gold.bin", ".smolTM");
static const u32 sLoomClay_Tilemap[]     = INCGFX_U32("graphics/intro/loom_clay.bin", ".smolTM");

static const u16 sPaint_Pal[]            = INCGFX_U16("graphics/intro/paint.pal", ".gbapal");
static const u16 sClay_Pal[]             = INCGFX_U16("graphics/intro/clay.pal", ".gbapal");
static const u16 sThreadWhite_Pal[]      = INCGFX_U16("graphics/intro/thread_white.pal", ".gbapal");
static const u16 sThreadGold_Pal[]       = INCGFX_U16("graphics/intro/thread_gold.pal", ".gbapal");
static const u16 sObjFigure_Pal[]        = INCGFX_U16("graphics/intro/obj_figure.pal", ".gbapal");
static const u16 sObjGold_Pal[]          = INCGFX_U16("graphics/intro/obj_gold.pal", ".gbapal");

static const u32 sSpindle_Gfx[]          = INCGFX_U32("graphics/intro/sprites_spindle.png", ".4bpp.smol");
static const u32 sFinizen_Gfx[]          = INCGFX_U32("graphics/intro/sprites_finizen.png", ".4bpp.smol");
static const u32 sFlame_Gfx[]            = INCGFX_U32("graphics/intro/sprites_flame.png", ".4bpp.smol");
static const u32 sBolt_Gfx[]             = INCGFX_U32("graphics/intro/sprites_bolt.png", ".4bpp.smol");
static const u32 sSparkle_Gfx[]          = INCGFX_U32("graphics/intro/sprites_sparkle.png", ".4bpp.smol");
static const u32 sSegments_Gfx[]         = INCGFX_U32("graphics/intro/sprites_segments.png", ".4bpp.smol");
static const u32 sRod_Gfx[]              = INCGFX_U32("graphics/intro/sprites_rod.png", ".4bpp.smol");
static const u32 sRodHand_Gfx[]          = INCGFX_U32("graphics/intro/sprites_rod_hand.png", ".4bpp.smol");
static const u32 sShears_Gfx[]           = INCGFX_U32("graphics/intro/sprites_shears.png", ".4bpp.smol");
static const u32 sArm_Gfx[]              = INCGFX_U32("graphics/intro/sprites_arm.png", ".4bpp.smol");
static const u32 sKnot_Gfx[]             = INCGFX_U32("graphics/intro/sprites_knot.png", ".4bpp.smol");

static const s16 sFinizenLeaps[2][4] = {FRIEZE_FINIZEN_A, FRIEZE_FINIZEN_B};
static const s16 sBolts[3][2] = FRIEZE_BOLTS;
static const u16 sBoltTimes[3] = {T_BOLT_1, T_BOLT_2, T_BOLT_3};
static const u8 sLoomThreadX[] = LOOM_THREAD_X;
static const u8 sLoomKnotY[] = LOOM_KNOT_Y;
static const u8 sLoomCut[] = LOOM_CUT;

// ---------------------------------------------------------------------------
// Sprites: one sheet per tag; frames are chosen by setting the tile number
// ---------------------------------------------------------------------------
enum {
    TAG_STUDIO_DROP = 3000,
    TAG_STUDIO_RIPPLE,
    TAG_SPINDLE,
    TAG_FINIZEN,
    TAG_FLAME,
    TAG_BOLT,
    TAG_SPARKLE,
    TAG_SEGMENTS,
    TAG_ROD,
    TAG_ROD_HAND,
    TAG_SHEARS,
    TAG_ARM,
    TAG_KNOT,
    PALTAG_STUDIO = 3000,
    PALTAG_FIGURE,
    PALTAG_GOLD,
};

#define SHEET(gfx, w, h, frames, tag) {gfx, (w) * (h) / 2 * (frames), tag}

static const struct CompressedSpriteSheet sSheets_Studio[] = {
    SHEET(sStudioDrop_Gfx, 16, 32, 6, TAG_STUDIO_DROP),
    SHEET(sStudioRipple_Gfx, 64, 64, 6, TAG_STUDIO_RIPPLE),
    {},
};
static const struct CompressedSpriteSheet sSheets_Frieze[] = {
    SHEET(sSpindle_Gfx, 8, 16, 7, TAG_SPINDLE),
    SHEET(sFinizen_Gfx, 32, 16, 3, TAG_FINIZEN),
    SHEET(sFlame_Gfx, 16, 16, 3, TAG_FLAME),
    SHEET(sBolt_Gfx, 16, 32, 2, TAG_BOLT),
    SHEET(sSparkle_Gfx, 16, 16, 4, TAG_SPARKLE),
    {},
};
static const struct CompressedSpriteSheet sSheets_Loom[] = {
    SHEET(sSegments_Gfx, 32, 64, 3, TAG_SEGMENTS),
    SHEET(sRod_Gfx, 8, 64, 1, TAG_ROD),
    SHEET(sRodHand_Gfx, 16, 16, 1, TAG_ROD_HAND),
    SHEET(sShears_Gfx, 64, 32, 3, TAG_SHEARS),
    SHEET(sArm_Gfx, 64, 32, 2, TAG_ARM),
    SHEET(sKnot_Gfx, 8, 8, 1, TAG_KNOT),
    SHEET(sSparkle_Gfx, 16, 16, 4, TAG_SPARKLE),
    {},
};

static const struct SpritePalette sSpritePalettes[] = {
    {sStudioObj_Pal, PALTAG_STUDIO},
    {sObjFigure_Pal, PALTAG_FIGURE},
    {sObjGold_Pal, PALTAG_GOLD},
    {},
};

#define OAM_DATA(w, h, prio) {.shape = SPRITE_SHAPE(w##x##h), .size = SPRITE_SIZE(w##x##h), .priority = prio}
static const struct OamData sOam_16x32_1 = OAM_DATA(16, 32, 1);
static const struct OamData sOam_64x64_1 = OAM_DATA(64, 64, 1);
static const struct OamData sOam_8x16_2  = OAM_DATA(8, 16, 2);
static const struct OamData sOam_32x16_3 = OAM_DATA(32, 16, 3);   // behind the painted sea
static const struct OamData sOam_16x16_2 = OAM_DATA(16, 16, 2);
static const struct OamData sOam_16x32_2 = OAM_DATA(16, 32, 2);
static const struct OamData sOam_16x16_0 = OAM_DATA(16, 16, 0);
// The loom's sprites are in front of the golden thread: the blades close round it.
static const struct OamData sOam_32x64_0 = OAM_DATA(32, 64, 0);
static const struct OamData sOam_8x32_0  = OAM_DATA(8, 32, 0);
static const struct OamData sOam_64x32_0 = OAM_DATA(64, 32, 0);
static const struct OamData sOam_8x8_0   = OAM_DATA(8, 8, 0);

#define TEMPLATE(tag, pal, oamData) {.tileTag = tag, .paletteTag = pal, .oam = &oamData, .anims = gDummySpriteAnimTable, \
                                 .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy}
static const struct SpriteTemplate sTemplate_Drop     = TEMPLATE(TAG_STUDIO_DROP, PALTAG_STUDIO, sOam_16x32_1);
static const struct SpriteTemplate sTemplate_Ripple   = TEMPLATE(TAG_STUDIO_RIPPLE, PALTAG_STUDIO, sOam_64x64_1);
static const struct SpriteTemplate sTemplate_Spindle  = TEMPLATE(TAG_SPINDLE, PALTAG_FIGURE, sOam_8x16_2);
static const struct SpriteTemplate sTemplate_Finizen  = TEMPLATE(TAG_FINIZEN, PALTAG_FIGURE, sOam_32x16_3);
static const struct SpriteTemplate sTemplate_Flame    = TEMPLATE(TAG_FLAME, PALTAG_FIGURE, sOam_16x16_2);
static const struct SpriteTemplate sTemplate_Bolt     = TEMPLATE(TAG_BOLT, PALTAG_FIGURE, sOam_16x32_2);
static const struct SpriteTemplate sTemplate_Sparkle  = TEMPLATE(TAG_SPARKLE, PALTAG_GOLD, sOam_16x16_0);
static const struct SpriteTemplate sTemplate_Segment  = TEMPLATE(TAG_SEGMENTS, PALTAG_FIGURE, sOam_32x64_0);
static const struct SpriteTemplate sTemplate_Rod      = TEMPLATE(TAG_ROD, PALTAG_FIGURE, sOam_8x32_0);
static const struct SpriteTemplate sTemplate_RodHand  = TEMPLATE(TAG_ROD_HAND, PALTAG_FIGURE, sOam_16x16_0);
static const struct SpriteTemplate sTemplate_Shears   = TEMPLATE(TAG_SHEARS, PALTAG_FIGURE, sOam_64x32_0);
static const struct SpriteTemplate sTemplate_Arm      = TEMPLATE(TAG_ARM, PALTAG_FIGURE, sOam_64x32_0);
static const struct SpriteTemplate sTemplate_Knot     = TEMPLATE(TAG_KNOT, PALTAG_FIGURE, sOam_8x8_0);

// Sprite ids, by role
enum {
    SPR_DROP,
    SPR_RIPPLE,
    SPR_SPINDLE = 0,
    SPR_FINIZEN_A,
    SPR_FINIZEN_B,
    SPR_FLAME,
    SPR_BOLT_1,
    SPR_BOLT_2,
    SPR_BOLT_3,
    SPR_SPARKLE,
    SPR_SPARKLE_2,
    SPR_SEGMENT_1 = 0,  // the loom
    SPR_SEGMENT_2,
    SPR_SEGMENT_3,
    SPR_KNOT_1,         // one per thread (the golden one's is never shown)
    SPR_ROD_TOP = SPR_KNOT_1 + 7,
    SPR_ROD_BOTTOM,
    SPR_ROD_HAND,
    SPR_ROD_ARM_1,
    SPR_ROD_ARM_2,
    SPR_ROD_ARM_3,
    SPR_SHEARS,
    SPR_SHEARS_ARM_1,
    SPR_SHEARS_ARM_2,
    SPR_SHEARS_ARM_3,
    SPR_LOOM_SPARKLE,
    SPR_COUNT,
};

static EWRAM_DATA u8 sScene = 0;
static EWRAM_DATA u8 sSpriteIds[SPR_COUNT] = {0};
static EWRAM_DATA u16 sNextColumn = 0;
static EWRAM_DATA s16 sFallY[ARRAY_COUNT(sLoomCut)] = {0};   // falling thread ends, 1/16 px
static EWRAM_DATA s16 sFallV[ARRAY_COUNT(sLoomCut)] = {0};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
static u8 AddSprite(const struct SpriteTemplate *template)
{
    u8 id = CreateSprite(template, -64, -64, 0);
    gSprites[id].invisible = TRUE;
    return id;
}

// Show sprite `role` centered at (x, y) on frame `frame` (tilesPerFrame tiles
// each), or hide it if asked to or if it is off screen.
static void ShowSprite(u8 role, s32 x, s32 y, u8 frame, u8 tilesPerFrame, bool32 show)
{
    struct Sprite *sprite = &gSprites[sSpriteIds[role]];

    if (!show || x < -40 || x > DISPLAY_WIDTH + 40 || y < -40 || y > DISPLAY_HEIGHT + 40)
    {
        sprite->invisible = TRUE;
        return;
    }
    sprite->invisible = FALSE;
    sprite->x = x;
    sprite->y = y;
    sprite->oam.tileNum = sprite->sheetTileStart + frame * tilesPerFrame;
}

static void FlipSprite(u8 role, bool32 hFlip)
{
    gSprites[sSpriteIds[role]].oam.matrixNum = hFlip ? ST_OAM_HFLIP : 0;
}

// Linear step from a to b as t runs from t0 to t1.
static s32 Lerp(s32 a, s32 b, s32 t, s32 t0, s32 t1)
{
    if (t <= t0)
        return a;
    if (t >= t1)
        return b;
    return a + (b - a) * (t - t0) / (t1 - t0);
}

// The same, eased in and out.
static s32 Ease(s32 a, s32 b, s32 t, s32 t0, s32 t1)
{
    s32 u;

    if (t <= t0)
        return a;
    if (t >= t1)
        return b;
    u = ((t - t0) << 8) / (t1 - t0);
    u = (u * u * (768 - 2 * u)) >> 16;   // 3u^2 - 2u^3, in 1/256
    return a + (b - a) * u / 256;
}

// Start of frame: the faded buffer begins as the loaded palettes.
static void ResetFadedPalettes(void)
{
    CpuFastCopy(gPlttBufferUnfaded, gPlttBufferFaded, PLTT_SIZE);
}

// End of frame: fade everything toward `color` by coeff/16.
static void FadeAll(u8 coeff, u32 color)
{
    if (coeff != 0)
        BlendPalettesFine(PALETTES_ALL, gPlttBufferFaded, gPlttBufferFaded, coeff > 16 ? 16 : coeff, color);
}

static void ResetIntroGpu(void)
{
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
    SetGpuReg(REG_OFFSET_BG0HOFS, 0);
    SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    SetGpuReg(REG_OFFSET_BG1HOFS, 0);
    SetGpuReg(REG_OFFSET_BG1VOFS, 0);
    SetGpuReg(REG_OFFSET_BG2HOFS, 0);
    SetGpuReg(REG_OFFSET_BG2VOFS, 0);
    SetGpuReg(REG_OFFSET_BG3HOFS, 0);
    SetGpuReg(REG_OFFSET_BG3VOFS, 0);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDALPHA, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
    SetGpuReg(REG_OFFSET_WININ, 0);
    SetGpuReg(REG_OFFSET_WINOUT, 0);
    SetGpuReg(REG_OFFSET_WIN0H, 0);
    SetGpuReg(REG_OFFSET_WIN0V, 0);
    SetGpuReg(REG_OFFSET_WIN1H, 0);
    SetGpuReg(REG_OFFSET_WIN1V, 0);
}

static void ResetIntroSprites(void)
{
    ResetSpriteData();
    FreeAllSpritePalettes();
    LoadSpritePalettes(sSpritePalettes);
}

// ---------------------------------------------------------------------------
// Scene 1: the studio mark
// ---------------------------------------------------------------------------
#define MARK_CX 120
#define MARK_CY 62
// studio_mark.pal: the drop is colors 1-5, the ring of the Twelve 6-7, the letters 8-12
#define MARK_DROP    1, 5
#define MARK_RING    6, 2
#define MARK_LETTERS 8, 5

static void Studio_Load(void)
{
    ResetIntroGpu();
    ResetIntroSprites();
    DmaClear16(3, (void *)BG_SCREEN_ADDR(31), BG_SCREEN_SIZE);
    DecompressDataWithHeaderVram(sStudioMark_Gfx, (void *)BG_CHAR_ADDR(0));
    DecompressDataWithHeaderVram(sStudioMark_Tilemap, (void *)BG_SCREEN_ADDR(31));
    LoadPalette(sStudioMark_Pal, BG_PLTT_ID(0), PLTT_SIZE_4BPP);
    LoadCompressedSpriteSheet(&sSheets_Studio[0]);
    LoadCompressedSpriteSheet(&sSheets_Studio[1]);
    sSpriteIds[SPR_DROP] = AddSprite(&sTemplate_Drop);
    sSpriteIds[SPR_RIPPLE] = AddSprite(&sTemplate_Ripple);
    SetGpuReg(REG_OFFSET_BG0CNT, BGCNT_PRIORITY(2) | BGCNT_CHARBASE(0) | BGCNT_SCREENBASE(31) | BGCNT_16COLOR | BGCNT_TXT256x256);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0 | DISPCNT_OBJ_1D_MAP | DISPCNT_BG0_ON | DISPCNT_OBJ_ON);
}

static void BlendRange(u16 offset, u16 count, u8 coeff, u32 color)
{
    BlendPalette(offset, count, coeff > 16 ? 16 : coeff, color);
}

static void Studio_Update(s32 t)
{
    s32 y;
    u8 coeff;

    ResetFadedPalettes();

    // The drop: a bead swells at the top edge, lets go and falls (frames 0-3
    // hanging, 4 falling), and is gone the moment it lands.
    if (t >= T_DROP_FORM && t < T_DROP_FALL)
        ShowSprite(SPR_DROP, MARK_CX, 18, (t - T_DROP_FORM) * 4 / (T_DROP_FALL - T_DROP_FORM), 8, TRUE);
    else if (t >= T_DROP_FALL && t < T_DROP_IMPACT)
    {
        s32 dt = t - T_DROP_FALL;
        // 0.07 px/frame^2 brings it from the top to the mark in 26 frames
        y = 18 + (dt * dt * 18) / 256;
        ShowSprite(SPR_DROP, MARK_CX, y, 4, 8, TRUE);
    }
    else
        ShowSprite(SPR_DROP, 0, 0, 0, 0, FALSE);

    // The ripple spreads to the ring of the Twelve.
    if (t >= T_DROP_IMPACT && t < T_DROP_IMPACT + 18)
        ShowSprite(SPR_RIPPLE, MARK_CX, MARK_CY, (t - T_DROP_IMPACT) / 3, 64, TRUE);
    else
        ShowSprite(SPR_RIPPLE, 0, 0, 0, 0, FALSE);

    // The mark's drop: dark until the impact, then a white flare cooling to gold.
    if (t < T_DROP_IMPACT)
        BlendRange(BG_PLTT_ID(0) + MARK_DROP, 16, INK_COLOR);
    else if (t < T_DROP_IMPACT + 24)
        BlendRange(BG_PLTT_ID(0) + MARK_DROP, 16 - (t - T_DROP_IMPACT) * 2 / 3, RGB(31, 31, 29));

    // The ring of the Twelve kindles as the ripple reaches it.
    coeff = Lerp(16, 0, t, T_RING, T_RING + 12);
    BlendRange(BG_PLTT_ID(0) + MARK_RING, coeff, INK_COLOR);
    if (t >= T_RING && t < T_RING + 12)
        BlendRange(BG_PLTT_ID(0) + MARK_RING, 16 - (t - T_RING), RGB(31, 31, 29));

    // ΙΧΩΡ gilds in, and its edges glint now and then.
    coeff = Lerp(16, 0, t, T_LETTERS, T_LETTERS + 40);
    BlendRange(BG_PLTT_ID(0) + MARK_LETTERS, coeff, INK_COLOR);
    if (t > T_LETTERS + 40)
    {
        coeff = 4 + Sin(((t - T_LETTERS) * 4) & 0xFF, 4);
        BlendRange(BG_PLTT_ID(0) + 12, 1, coeff, RGB(31, 31, 28));
        BlendRange(BG_PLTT_ID(0) + 5, 1, coeff, RGB(31, 31, 28));
    }

    FadeAll(Lerp(0, 16, t, T_STUDIO_OUT, T_STUDIO_OUT + 32), RGB_BLACK);
}

// ---------------------------------------------------------------------------
// Scene 2: the frieze
// ---------------------------------------------------------------------------
// BG2: the frieze (charblocks 0-1, map 64x32 at screen blocks 24-25)
// BG3: the lit clay band (charblock 2, map at 26), fixed: the pot turns under the light
// BG1: the white thread (charblock 2, map at 28-29)
// BG0: the golden thread (charblock 2, map at 30-31), blended to glow
#define FRIEZE_ROWS 20
#define SB_FRIEZE   24
#define SB_CLAY     26
#define SB_WHITE    28
#define SB_GOLD     30

static void WriteColumn(u8 screenBase, const u16 *map, u16 column)
{
    u16 mapCol = column & 63;
    u16 *dest = (u16 *)BG_SCREEN_ADDR(screenBase + (mapCol >> 5)) + (mapCol & 31);
    const u16 *src = &map[column * FRIEZE_ROWS];
    u32 row;

    for (row = 0; row < FRIEZE_ROWS; row++)
        dest[row * 32] = src[row];
}

// Write the columns that will be on screen at camera x `cam` (plus one).
static void StreamFrieze(s32 cam)
{
    u16 need = (cam + DISPLAY_WIDTH + 8) / 8;

    if (need >= FRIEZE_COLS)
        need = FRIEZE_COLS - 1;
    while (sNextColumn <= need)
    {
        WriteColumn(SB_FRIEZE, sFrieze_Tilemap, sNextColumn);
        WriteColumn(SB_WHITE, sFriezeWhite_Tilemap, sNextColumn);
        WriteColumn(SB_GOLD, sFriezeGold_Tilemap, sNextColumn);
        sNextColumn++;
    }
}

// The pan: at rest on Clotho, then the pot turns, easing in over PAN_ACCEL
// frames and out over PAN_DECEL, to stop with Olympus in frame.
#define PAN_ACCEL 150
#define PAN_DECEL 110
static s32 FriezeCamera(s32 t)
{
    s32 n = T_PAN_END - T_PAN;
    s32 full = n - PAN_ACCEL / 2 - PAN_DECEL / 2;   // frames at full speed, equivalent
    s32 e = t - T_PAN, d;

    if (e <= 0)
        return 0;
    if (e >= n)
        return FRIEZE_CAM_END;
    if (e < PAN_ACCEL)
        d = e * e * 128 / PAN_ACCEL;
    else if (e < n - PAN_DECEL)
        d = PAN_ACCEL * 128 + (e - PAN_ACCEL) * 256;
    else
        d = full * 256 - (n - e) * (n - e) * 128 / PAN_DECEL;
    return d * FRIEZE_CAM_END / (full * 256);
}

static void Frieze_Load(void)
{
    u32 i;

    ResetIntroGpu();
    ResetIntroSprites();
    DmaClear16(3, (void *)BG_SCREEN_ADDR(24), BG_SCREEN_SIZE * 8);
    DecompressDataWithHeaderVram(sFrieze_Gfx, (void *)BG_CHAR_ADDR(0));
    DecompressDataWithHeaderVram(sFriezeAux_Gfx, (void *)BG_CHAR_ADDR(2));
    DecompressDataWithHeaderVram(sClay_Tilemap, (void *)BG_SCREEN_ADDR(SB_CLAY));
    sNextColumn = 0;
    StreamFrieze(0);
    LoadPalette(sPaint_Pal, BG_PLTT_ID(PAL_PAINT), PLTT_SIZE_4BPP);
    LoadPalette(sClay_Pal, BG_PLTT_ID(PAL_CLAY), PLTT_SIZE_4BPP);
    LoadPalette(sThreadWhite_Pal, BG_PLTT_ID(PAL_WHITE), PLTT_SIZE_4BPP);
    LoadPalette(sThreadGold_Pal, BG_PLTT_ID(PAL_GOLD), PLTT_SIZE_4BPP);
    for (i = 0; sSheets_Frieze[i].data != NULL; i++)
        LoadCompressedSpriteSheet(&sSheets_Frieze[i]);
    sSpriteIds[SPR_SPINDLE] = AddSprite(&sTemplate_Spindle);
    sSpriteIds[SPR_FINIZEN_A] = AddSprite(&sTemplate_Finizen);
    sSpriteIds[SPR_FINIZEN_B] = AddSprite(&sTemplate_Finizen);
    sSpriteIds[SPR_FLAME] = AddSprite(&sTemplate_Flame);
    for (i = 0; i < 3; i++)
        sSpriteIds[SPR_BOLT_1 + i] = AddSprite(&sTemplate_Bolt);
    sSpriteIds[SPR_SPARKLE] = AddSprite(&sTemplate_Sparkle);
    sSpriteIds[SPR_SPARKLE_2] = AddSprite(&sTemplate_Sparkle);

    SetGpuReg(REG_OFFSET_BG0CNT, BGCNT_PRIORITY(0) | BGCNT_CHARBASE(2) | BGCNT_SCREENBASE(SB_GOLD) | BGCNT_16COLOR | BGCNT_TXT512x256);
    SetGpuReg(REG_OFFSET_BG1CNT, BGCNT_PRIORITY(1) | BGCNT_CHARBASE(2) | BGCNT_SCREENBASE(SB_WHITE) | BGCNT_16COLOR | BGCNT_TXT512x256);
    SetGpuReg(REG_OFFSET_BG2CNT, BGCNT_PRIORITY(2) | BGCNT_CHARBASE(0) | BGCNT_SCREENBASE(SB_FRIEZE) | BGCNT_16COLOR | BGCNT_TXT512x256);
    SetGpuReg(REG_OFFSET_BG3CNT, BGCNT_PRIORITY(3) | BGCNT_CHARBASE(2) | BGCNT_SCREENBASE(SB_CLAY) | BGCNT_16COLOR | BGCNT_TXT256x256);
    // The threads are revealed through windows: WIN0 is the part of the screen
    // the golden thread has reached, WIN1 the part the white thread has.
    SetGpuReg(REG_OFFSET_WIN0V, WIN_RANGE(0, DISPLAY_HEIGHT));
    SetGpuReg(REG_OFFSET_WIN1V, WIN_RANGE(0, DISPLAY_HEIGHT));
    SetGpuReg(REG_OFFSET_WININ, WININ_WIN0_ALL | WININ_WIN1_BG1 | WININ_WIN1_BG2 | WININ_WIN1_BG3 | WININ_WIN1_OBJ | WININ_WIN1_CLR);
    SetGpuReg(REG_OFFSET_WINOUT, WINOUT_WIN01_BG2 | WINOUT_WIN01_BG3 | WINOUT_WIN01_OBJ | WINOUT_WIN01_CLR);
    // The golden thread glows over what it crosses, as on the title.
    SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT1_BG0 | BLDCNT_EFFECT_BLEND | BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3 | BLDCNT_TGT2_OBJ);
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(12, 8));
}

static void Frieze_Update(s32 t)
{
    s32 cam = FriezeCamera(t);
    s32 whiteX, goldX, x, y, i;
    u16 dispcnt = DISPCNT_MODE_0 | DISPCNT_OBJ_1D_MAP | DISPCNT_BG_ALL_ON | DISPCNT_OBJ_ON | DISPCNT_WIN1_ON;
    u8 coeff;

    ResetFadedPalettes();
    StreamFrieze(cam);
    SetGpuReg(REG_OFFSET_BG0HOFS, cam);
    SetGpuReg(REG_OFFSET_BG1HOFS, cam);
    SetGpuReg(REG_OFFSET_BG2HOFS, cam);

    // Clotho's thread runs out from her hand (the camera is still till T_PAN)...
    whiteX = Lerp(FRIEZE_HAND_X, DISPLAY_WIDTH, t, T_THREAD_GROW, T_THREAD_DONE);
    SetGpuReg(REG_OFFSET_WIN1H, WIN_RANGE(0, whiteX));

    // ...and later the golden one rises from the olive's roots and runs after it.
    if (t >= T_GOLD)
    {
        goldX = Lerp(FRIEZE_GOLD_X - cam, DISPLAY_WIDTH, t, T_GOLD + 8, T_GOLD_DONE);
        if (goldX < 1)
            goldX = 1;
        SetGpuReg(REG_OFFSET_WIN0H, WIN_RANGE(0, goldX));
        dispcnt |= DISPCNT_WIN0_ON;
        if (t < T_GOLD + 16)
            ShowSprite(SPR_SPARKLE, FRIEZE_GOLD_X - cam, FRIEZE_GOLD_Y - 1, (t - T_GOLD) / 4, 4, TRUE);
        else
            ShowSprite(SPR_SPARKLE, 0, 0, 0, 0, FALSE);
        if (t >= T_GOLD + 8 && t < T_GOLD_DONE && goldX < DISPLAY_WIDTH)
            ShowSprite(SPR_SPARKLE_2, goldX, 95 + Sin(((goldX + cam) * 2) & 0xFF, 3), (t >> 2) & 3, 4, TRUE);
        else
            ShowSprite(SPR_SPARKLE_2, 0, 0, 0, 0, FALSE);
    }
    SetGpuReg(REG_OFFSET_DISPCNT, dispcnt);

    // The golden thread's glints pulse, like the title's.
    coeff = 6 + Sin((t * 5) & 0xFF, 6);
    BlendRange(BG_PLTT_ID(PAL_GOLD) + FRIEZE_GOLD_GLINT, 1, coeff, RGB(31, 31, 28));

    // Clotho's spindle turns.
    ShowSprite(SPR_SPINDLE, FRIEZE_SPINDLE_X + 4 - cam, FRIEZE_SPINDLE_Y + 8, (t / 3) % 7, 2, TRUE);

    // Finizen leap round the trireme, one leap every 80 frames.
    for (i = 0; i < 2; i++)
    {
        const s16 *leap = sFinizenLeaps[i];
        s32 p = (t + i * 37) % 80;
        bool32 airborne = p < 36;

        x = leap[0] + (leap[2] - leap[0]) * p / 36 - cam;
        y = leap[1] - Sin((p * 128 / 36) & 0xFF, leap[3]);
        ShowSprite(SPR_FINIZEN_A + i, x, y, p < 12 ? 0 : (p < 24 ? 1 : 2), 8, airborne && t > T_PAN);
    }

    // The altar fire on the temple steps.
    ShowSprite(SPR_FLAME, FRIEZE_FLAME_X + 8 - cam, FRIEZE_FLAME_Y + 8, (t / 6) % 3, 4, TRUE);

    // Zapdos calls the lightning: bolts, and the clay flashes.
    for (i = 0; i < 3; i++)
    {
        s32 dt = t - sBoltTimes[i];
        ShowSprite(SPR_BOLT_1 + i, sBolts[i][0] + 8 - cam, sBolts[i][1] + 16, (t >> 1) & 1, 8, dt >= 0 && dt < 10);
        if (dt >= 0 && dt < 7)
            BlendRange(BG_PLTT_ID(PAL_CLAY), 16, 7 - dt, RGB(31, 27, 20));
    }

    // In from black on Clotho; out to white for the loom.
    if (t < T_CLOTHO + 32)
        FadeAll(Lerp(16, 0, t, T_CLOTHO, T_CLOTHO + 32), RGB_BLACK);
    else
        FadeAll(Lerp(0, 16, t, T_TO_LOOM, T_LOOM), RGB_WHITE);
}

// ---------------------------------------------------------------------------
// Scene 3: the loom
// ---------------------------------------------------------------------------
// BG2: the loom (charblock 0, map at 24)
// BG3: the clay band (charblock 2, map at 26)
// BG0: the golden thread (charblock 2, map at 30), swayed per scanline
#define ROD_TOP      50     // the measuring rod spans rows 50-113
#define GOLD_CUT_Y   84     // where the shears come to the golden thread
#define ROD_OFF_X    (-60)
#define SHEARS_OFF_X 300

static void Loom_Load(void)
{
    u32 i;
    struct ScanlineEffectParams params = {&REG_BG0HOFS, SCANLINE_EFFECT_DMACNT_16BIT, 1};

    ResetIntroGpu();
    ResetIntroSprites();
    DmaClear16(3, (void *)BG_SCREEN_ADDR(24), BG_SCREEN_SIZE * 8);
    DecompressDataWithHeaderVram(sLoom_Gfx, (void *)BG_CHAR_ADDR(0));
    DecompressDataWithHeaderVram(sLoomAux_Gfx, (void *)BG_CHAR_ADDR(2));
    DecompressDataWithHeaderVram(sLoom_Tilemap, (void *)BG_SCREEN_ADDR(SB_FRIEZE));
    DecompressDataWithHeaderVram(sLoomClay_Tilemap, (void *)BG_SCREEN_ADDR(SB_CLAY));
    DecompressDataWithHeaderVram(sLoomGold_Tilemap, (void *)BG_SCREEN_ADDR(SB_GOLD));
    LoadPalette(sPaint_Pal, BG_PLTT_ID(PAL_PAINT), PLTT_SIZE_4BPP);
    LoadPalette(sClay_Pal, BG_PLTT_ID(PAL_CLAY), PLTT_SIZE_4BPP);
    LoadPalette(sThreadGold_Pal, BG_PLTT_ID(PAL_GOLD), PLTT_SIZE_4BPP);
    for (i = 0; sSheets_Loom[i].data != NULL; i++)
        LoadCompressedSpriteSheet(&sSheets_Loom[i]);
    // Created front to back: the knots over the thread ends, the hand over the rod.
    for (i = 0; i < ARRAY_COUNT(sLoomThreadX); i++)
        sSpriteIds[SPR_KNOT_1 + i] = AddSprite(&sTemplate_Knot);
    for (i = 0; i < ARRAY_COUNT(sLoomCut); i++)
    {
        sSpriteIds[SPR_SEGMENT_1 + i] = AddSprite(&sTemplate_Segment);
        sFallY[i] = 0;
        sFallV[i] = 0;
    }
    sSpriteIds[SPR_ROD_HAND] = AddSprite(&sTemplate_RodHand);   // in front of the rod
    sSpriteIds[SPR_ROD_TOP] = AddSprite(&sTemplate_Rod);
    sSpriteIds[SPR_ROD_BOTTOM] = AddSprite(&sTemplate_Rod);
    for (i = 0; i < 3; i++)
        sSpriteIds[SPR_ROD_ARM_1 + i] = AddSprite(&sTemplate_Arm);
    sSpriteIds[SPR_SHEARS] = AddSprite(&sTemplate_Shears);
    for (i = 0; i < 3; i++)
        sSpriteIds[SPR_SHEARS_ARM_1 + i] = AddSprite(&sTemplate_Arm);
    sSpriteIds[SPR_LOOM_SPARKLE] = AddSprite(&sTemplate_Sparkle);
    FlipSprite(SPR_ROD_ARM_1, TRUE);
    FlipSprite(SPR_ROD_ARM_2, TRUE);
    FlipSprite(SPR_ROD_ARM_3, TRUE);

    SetGpuReg(REG_OFFSET_BG0CNT, BGCNT_PRIORITY(0) | BGCNT_CHARBASE(2) | BGCNT_SCREENBASE(SB_GOLD) | BGCNT_16COLOR | BGCNT_TXT256x256);
    SetGpuReg(REG_OFFSET_BG2CNT, BGCNT_PRIORITY(2) | BGCNT_CHARBASE(0) | BGCNT_SCREENBASE(SB_FRIEZE) | BGCNT_16COLOR | BGCNT_TXT256x256);
    SetGpuReg(REG_OFFSET_BG3CNT, BGCNT_PRIORITY(3) | BGCNT_CHARBASE(2) | BGCNT_SCREENBASE(SB_CLAY) | BGCNT_16COLOR | BGCNT_TXT256x256);
    SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT1_BG0 | BLDCNT_EFFECT_BLEND | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3 | BLDCNT_TGT2_OBJ);
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(12, 8));
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0 | DISPCNT_OBJ_1D_MAP | DISPCNT_BG0_ON | DISPCNT_BG2_ON | DISPCNT_BG3_ON | DISPCNT_OBJ_ON);
    CpuFill16(0, gScanlineEffectRegBuffers, sizeof(gScanlineEffectRegBuffers));
    ScanlineEffect_SetParams(params);
}

// Lachesis's rod (with her hand and arm) standing at x, its top at y.
static void ShowRod(s32 x, s32 y, bool32 show)
{
    ShowSprite(SPR_ROD_TOP, x + 1, y + 16, 0, 4, show);
    ShowSprite(SPR_ROD_BOTTOM, x + 1, y + 48, 1, 4, show);
    ShowSprite(SPR_ROD_HAND, x, y + 36, 0, 4, show);
    ShowSprite(SPR_ROD_ARM_1, x - 36, y + 36, 0, 32, show);
    ShowSprite(SPR_ROD_ARM_2, x - 100, y + 36, 1, 32, show);
    ShowSprite(SPR_ROD_ARM_3, x - 164, y + 36, 1, 32, show);
}

// Atropos's shears (with her hand and arm), the blades' meeting point at (x, y).
static void ShowShears(s32 x, s32 y, u8 frame)
{
    s32 cx = x + 32 - LOOM_SHEARS_CUT_X;

    ShowSprite(SPR_SHEARS, cx, y + 16 - LOOM_SHEARS_CUT_Y, frame, 32, TRUE);
    ShowSprite(SPR_SHEARS_ARM_1, cx + 48, y, 0, 32, TRUE);
    ShowSprite(SPR_SHEARS_ARM_2, cx + 112, y, 1, 32, TRUE);
    ShowSprite(SPR_SHEARS_ARM_3, cx + 176, y, 1, 32, TRUE);
}

#define ROD_X(k) (sLoomThreadX[k] + 5)

static void Loom_Update(s32 t)
{
    s32 i, k, y, rodX, rodY, cutX, cutY, amp;
    u8 frame;
    u16 *hofs;

    ResetFadedPalettes();

    // The golden thread sways from the beam, more as the shears come near.
    amp = t < T_SHEARS_GOLD ? 2 : 3;
    hofs = gScanlineEffectRegBuffers[gScanlineEffect.srcBuffer];
    for (y = 0; y < DISPLAY_HEIGHT; y++)
    {
        s32 depth = y - LOOM_BEAM_BOTTOM;
        hofs[y] = depth > 0 ? -(Sin((t * 3) & 0xFF, amp) * depth) / 64 : 0;
    }

    // Lachesis measures: the rod steps along the warp, a thread per eighth
    // note, and ties a red knot where each will be cut. On the golden thread
    // it finds nothing to measure.
    rodY = ROD_TOP;
    if (t < T_ROD_IN)
        rodX = ROD_OFF_X;
    else if (t < ROD_HOP_TIME(0))
        rodX = Ease(ROD_OFF_X, ROD_X(0), t, T_ROD_IN, ROD_HOP_TIME(0));
    else if (t < T_ROD_OUT)
    {
        // k: the thread the rod is at, or hopping to
        k = 0;
        while (k < 6 && t >= ROD_HOP_TIME(k + 1) - 6)
            k++;
        rodX = ROD_X(k);
        if (k > 0 && t < ROD_HOP_TIME(k))
        {
            // mid-hop from thread k-1 to k
            rodX = Ease(ROD_X(k - 1), ROD_X(k), t, ROD_HOP_TIME(k) - 6, ROD_HOP_TIME(k));
            rodY = ROD_TOP - Sin(((t - (ROD_HOP_TIME(k) - 6)) * 128 / 6) & 0xFF, 3);
        }
    }
    else
        rodX = Ease(ROD_X(6), ROD_OFF_X, t, T_ROD_OUT, T_ROD_OUT + 12);
    ShowRod(rodX, rodY, t >= T_ROD_IN && t < T_ROD_OUT + 12);

    for (i = 0; i < (s32)ARRAY_COUNT(sLoomThreadX); i++)
    {
        bool32 tied = (i != LOOM_GOLD) && t >= ROD_HOP_TIME(i) + 2;
        s32 fall = 0;

        for (k = 0; k < (s32)ARRAY_COUNT(sLoomCut); k++)
            if (sLoomCut[k] == i)
                fall = sFallY[k] / 16;
        ShowSprite(SPR_KNOT_1 + i, sLoomThreadX[i] + 1, sLoomKnotY[i] + fall, 0, 1, tied);
    }
    if (t >= ROD_HOP_TIME(LOOM_GOLD) && t < ROD_HOP_TIME(LOOM_GOLD) + 16)
        ShowSprite(SPR_LOOM_SPARKLE, sLoomThreadX[LOOM_GOLD], ROD_TOP + 30, (t - ROD_HOP_TIME(LOOM_GOLD)) / 4, 4, TRUE);
    else if (t < T_SHEARS_GOLD)
        ShowSprite(SPR_LOOM_SPARKLE, 0, 0, 0, 0, FALSE);

    // Atropos cuts: in from the right, a thread per beat. The cut end falls
    // with its weight.
    frame = 0;
    if (t < T_SHEARS_IN)
    {
        cutX = SHEARS_OFF_X;
        cutY = sLoomKnotY[sLoomCut[0]];
    }
    else if (t < SNIP_TIME(0) - 6)
    {
        cutX = Ease(SHEARS_OFF_X, sLoomThreadX[sLoomCut[0]], t, T_SHEARS_IN, SNIP_TIME(0) - 6);
        cutY = sLoomKnotY[sLoomCut[0]];
    }
    else if (t < SNIP_TIME(2) + 6)
    {
        k = 0;
        while (k < 2 && t >= SNIP_TIME(k) + 6)
            k++;
        cutX = sLoomThreadX[sLoomCut[k]];
        cutY = sLoomKnotY[sLoomCut[k]];
        if (k > 0 && t < SNIP_TIME(k) - 6)
        {
            cutX = Ease(sLoomThreadX[sLoomCut[k - 1]], cutX, t, SNIP_TIME(k - 1) + 6, SNIP_TIME(k) - 6);
            cutY = Ease(sLoomKnotY[sLoomCut[k - 1]], cutY, t, SNIP_TIME(k - 1) + 6, SNIP_TIME(k) - 6);
        }
        i = t - SNIP_TIME(k);
        if (i >= -4 && i < -2)
            frame = 1;
        else if (i >= -2 && i < 3)
            frame = 2;
        else if (i >= 3 && i < 6)
            frame = 1;
    }
    else if (t < T_SHEARS_GOLD)
    {
        cutX = Ease(sLoomThreadX[sLoomCut[2]], sLoomThreadX[LOOM_GOLD], t, SNIP_TIME(2) + 6, T_SHEARS_GOLD - 4);
        cutY = Ease(sLoomKnotY[sLoomCut[2]], GOLD_CUT_Y, t, SNIP_TIME(2) + 6, T_SHEARS_GOLD - 4);
        frame = 1;
    }
    else
    {
        // The hesitation: open wide on the golden thread, trembling; one
        // attempt to close, and the blades open again.
        i = t - T_SHEARS_GOLD;
        cutX = sLoomThreadX[LOOM_GOLD] + ((i > 12 && (t & 2)) ? 1 : 0);
        cutY = GOLD_CUT_Y;
        frame = (i >= 40 && i < 50) ? 1 : 0;
        if (i >= 20 && i < 36)
            ShowSprite(SPR_LOOM_SPARKLE, sLoomThreadX[LOOM_GOLD], GOLD_CUT_Y, (i - 20) / 4, 4, TRUE);
        else if (i >= 52 && i < 68)
            ShowSprite(SPR_LOOM_SPARKLE, sLoomThreadX[LOOM_GOLD], GOLD_CUT_Y - 14, (i - 52) / 4, 4, TRUE);
        else
            ShowSprite(SPR_LOOM_SPARKLE, 0, 0, 0, 0, FALSE);
    }
    ShowShears(cutX, cutY, frame);

    for (k = 0; k < (s32)ARRAY_COUNT(sLoomCut); k++)
    {
        i = sLoomCut[k];
        if (t >= SNIP_TIME(k))
        {
            sFallV[k] += 5;
            sFallY[k] += sFallV[k];
        }
        ShowSprite(SPR_SEGMENT_1 + k, sLoomThreadX[i], sLoomKnotY[i] + 32 + sFallY[k] / 16, k, 32,
                   sLoomKnotY[i] + sFallY[k] / 16 < DISPLAY_HEIGHT);
    }

    FadeAll(t < T_LOOM + 16 ? Lerp(16, 0, t, T_LOOM, T_LOOM + 16) : Lerp(0, 16, t, T_FLASH, T_END), RGB_WHITE);
}

// ---------------------------------------------------------------------------
// The movie
// ---------------------------------------------------------------------------
void Task_Scene1_Load(u8 taskId)
{
    SetVBlankCallback(NULL);
    sScene = SCENE_STUDIO;
    Studio_Load();
    gIntroFrameCounter = 0;
    Studio_Update(0);
    SetVBlankCallback(VBlankCB_Intro);
    m4aSongNumStart(MUS_INTRO);
    ResetSerial();
    gTasks[taskId].func = Task_IchorIntro;
}

static void Task_IchorIntro(u8 taskId)
{
    s32 t = gIntroFrameCounter;

    switch (sScene)
    {
    case SCENE_STUDIO:
        if (t >= T_FRIEZE_LOAD)
        {
            Frieze_Load();
            sScene = SCENE_FRIEZE;
            Frieze_Update(t);
        }
        else
        {
            Studio_Update(t);
        }
        break;
    case SCENE_FRIEZE:
        if (t >= T_LOOM)
        {
            Loom_Load();
            sScene = SCENE_LOOM;
        }
        else
        {
            Frieze_Update(t);
            break;
        }
        // fallthrough
    case SCENE_LOOM:
        Loom_Update(t);
        if (t >= T_END)
        {
            sScene = SCENE_DONE;
            DestroyTask(taskId);
            SetMainCallback2(MainCB2_EndIntro);
        }
        break;
    }
}
