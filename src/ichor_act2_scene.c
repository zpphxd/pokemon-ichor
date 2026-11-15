// Ichor: Act II's scenes that need the engine: the Dionysia in Thyrsa's theater
// (design/phase3/SCRIPT.md, beat 32). See include/ichor_act2_scene.h.
//
// The trance. The theater's seats are drawn on four copies of one palette
// (tools/ichor/art/theater_build.py): the empty seats on the crowd's own, and
// the audience of each pair of blocks on a copy of its own, so each pair's
// pulse can stop when its blocks laugh. The pulse tints a pair's palette
// toward violet and back, slowly. It is worked out from the unfaded palette
// every frame and passed through the day-and-night tint like every other
// outdoor palette, so it sits under the dusk the play is held at.
#include "global.h"
#include "event_data.h"
#include "field_weather.h"
#include "fieldmap.h"
#include "ichor_act2_scene.h"
#include "menu.h"
#include "overworld.h"
#include "palette.h"
#include "script.h"
#include "script_menu.h"
#include "sprite.h"
#include "task.h"
#include "trig.h"
#include "constants/field_weather.h"
#include "constants/rgb.h"
#include "constants/rtc.h"

#include "data/ichor_act2_theater.h"

// --------------------------------------------------------------------------
// Dusk and the audience
// --------------------------------------------------------------------------

// The play is held at dusk, whatever the clock says: the start of the
// evening-to-night blend, the evening's tint at its fullest. The override lasts
// until the next warp (overworld.c clears it), so the theater's ON_TRANSITION and
// ON_RESUME scripts call this while the play runs.
void Ichor_TheaterDusk(void)
{
    SetTimeOfDay(NIGHT_HOUR_BEGIN);
    UpdateTimeOfDay(TRUE);
}

// Every seat cell becomes its crowd cell (src/data/ichor_act2_theater.h, written
// by tools/ichor/maps/theater.py). Seats stay impassable.
void Ichor_TheaterFillSeats(void)
{
    u32 i;

    for (i = 0; i < THEATER_CROWD_CELLS; i++)
        MapGridSetMetatileIdAt(sTheaterCrowd[i].x + MAP_OFFSET, sTheaterCrowd[i].y + MAP_OFFSET,
                               sTheaterCrowd[i].metatile | MAPGRID_COLLISION_MASK);
}

// --------------------------------------------------------------------------
// The trance's pulse
// --------------------------------------------------------------------------

#define TRANCE_MAX        16          // a pair's strength when fully entranced
#define TRANCE_COLOR      RGB(14, 4, 20)
#define GAZE_COLOR        RGB(31, 27, 16)
#define GAZE_FRAMES       28          // the masks' eyes rest on each pair this long

enum {
    PAIR_OFF,        // not entranced: its palette is left alone
    PAIR_RISING,     // the trance takes it
    PAIR_HELD,       // entranced
    PAIR_DRAINING,   // its blocks laughed: the purple drains away
};

struct TheaterTrance
{
    u8 taskId;
    u8 state[THEATER_PAIR_COUNT];
    u8 strength[THEATER_PAIR_COUNT];   // 0..TRANCE_MAX
    u16 delay[THEATER_PAIR_COUNT];     // frames before a draining pair starts to drain
    u8 phase;                          // the pulse's sine index
    u8 frame;
    bool8 waitingScript;               // a waitstate special is running
    s8 gazePair;                       // the pair the masks look at, or -1
    u8 gazeTimer;
};

static EWRAM_DATA struct TheaterTrance sTrance = {0};

static const u8 sPairPalettes[THEATER_PAIR_COUNT] =
{
    [THEATER_PAIR_LOW] = THEATER_PAL_PAIR_LOW,
    [THEATER_PAIR_MID] = THEATER_PAL_PAIR_MID,
    [THEATER_PAIR_TOP] = THEATER_PAL_PAIR_TOP,
};

static void Task_TheaterTrance(u8 taskId);

static u16 BlendColor(u16 c, u16 to, u32 coeff)
{
    s32 r = GET_R(c), g = GET_G(c), b = GET_B(c);

    r += ((GET_R(to) - r) * (s32)coeff) >> 4;
    g += ((GET_G(to) - g) * (s32)coeff) >> 4;
    b += ((GET_B(to) - b) * (s32)coeff) >> 4;
    return RGB2(r, g, b) | (c & RGB_ALPHA);
}

// Writes pair p's palette into the faded buffer: the unfaded colors tinted by
// `trance` (0..16) toward violet and by `glint` toward the masks' gold, then
// through the day-and-night tint.
static void DrawPairPalette(u32 pair, u32 trance, u32 glint)
{
    u16 tinted[16];
    u32 pal = sPairPalettes[pair];
    const u16 *src = &gPlttBufferUnfaded[BG_PLTT_ID(pal)];
    u32 i;

    tinted[0] = src[0];
    for (i = 1; i < 16; i++)
    {
        u16 c = src[i];
        if (trance)
            c = BlendColor(c, TRANCE_COLOR, trance);
        if (glint)
            c = BlendColor(c, GAZE_COLOR, glint);
        tinted[i] = c;
    }
    if (MapHasNaturalLight(gMapHeader.mapType))
        TimeMixPalettes(1, tinted, &gPlttBufferFaded[BG_PLTT_ID(pal)],
                        &gTimeBlend.startBlend, &gTimeBlend.endBlend, gTimeBlend.weight);
    else
        CpuCopy16(tinted, &gPlttBufferFaded[BG_PLTT_ID(pal)], sizeof(tinted));
}

static bool32 TranceSettled(void)
{
    u32 p;

    for (p = 0; p < THEATER_PAIR_COUNT; p++)
    {
        if (sTrance.state[p] == PAIR_DRAINING || sTrance.state[p] == PAIR_RISING)
            return FALSE;
    }
    return sTrance.gazePair < 0;
}

static void EnsureTranceTask(void)
{
    if (!FuncIsActiveTask(Task_TheaterTrance))
    {
        sTrance.taskId = CreateTask(Task_TheaterTrance, 80);
        sTrance.gazePair = -1;
        sTrance.waitingScript = FALSE;
    }
}

static void Task_TheaterTrance(u8 taskId)
{
    u32 p;
    bool32 idle;

    // Leave the palettes to a screen fade or a weather change while one runs.
    idle = !gPaletteFade.active && gWeatherPtr->palProcessingState == WEATHER_PAL_STATE_IDLE;
    sTrance.frame++;
    sTrance.phase += 2;   // one slow breath every 128 frames

    for (p = 0; p < THEATER_PAIR_COUNT; p++)
    {
        switch (sTrance.state[p])
        {
        case PAIR_RISING:
            if ((sTrance.frame & 3) == 0 && ++sTrance.strength[p] >= TRANCE_MAX)
                sTrance.state[p] = PAIR_HELD;
            break;
        case PAIR_DRAINING:
            if (sTrance.delay[p])
            {
                sTrance.delay[p]--;
            }
            else if ((sTrance.frame & 1) == 0)
            {
                if (sTrance.strength[p])
                    sTrance.strength[p]--;
                if (sTrance.strength[p] == 0)
                {
                    sTrance.state[p] = PAIR_OFF;
                    if (idle)
                        DrawPairPalette(p, 0, 0);   // put the pair back exactly
                }
            }
            break;
        }
    }

    if (sTrance.gazePair >= 0 && ++sTrance.gazeTimer >= GAZE_FRAMES)
    {
        sTrance.gazeTimer = 0;
        if (++sTrance.gazePair >= THEATER_PAIR_COUNT)
        {
            sTrance.gazePair = -1;
            for (p = 0; p < THEATER_PAIR_COUNT; p++)
            {
                if (idle && sTrance.state[p] == PAIR_OFF)
                    DrawPairPalette(p, 0, 0);
            }
        }
    }

    if (idle)
    {
        for (p = 0; p < THEATER_PAIR_COUNT; p++)
        {
            u32 trance = 0, glint = 0;

            if (sTrance.state[p] != PAIR_OFF)
                trance = (sTrance.strength[p] * (7 + Sin(sTrance.phase, 3))) >> 4;
            if (sTrance.gazePair == (s8)p)
                glint = 6 - abs((s32)sTrance.gazeTimer - GAZE_FRAMES / 2) * 6 / (GAZE_FRAMES / 2);
            if (sTrance.state[p] != PAIR_OFF || glint)
                DrawPairPalette(p, trance, glint);
        }
    }

    if (sTrance.waitingScript && TranceSettled())
    {
        sTrance.waitingScript = FALSE;
        ScriptContext_Enable();
    }
}

static void HoldPair(u32 p, bool32 instantly)
{
    sTrance.state[p] = instantly ? PAIR_HELD : PAIR_RISING;
    sTrance.strength[p] = instantly ? TRANCE_MAX : 0;
    sTrance.delay[p] = 0;
}

// ON_RESUME: after a warp or a battle, the pairs still entranced pulse again at
// full strength (each correct entrance has released one more pair).
void Ichor_TheaterTranceResume(void)
{
    u32 stage = VarGet(VAR_ICHOR_DIONYSIA), p;

    if (stage < DIONYSIA_ENTRANCE_1 || stage > DIONYSIA_ENTRANCE_3)
        return;
    EnsureTranceTask();
    for (p = 0; p < THEATER_PAIR_COUNT; p++)
    {
        if (p >= stage - DIONYSIA_ENTRANCE_1)
            HoldPair(p, TRUE);
        else
            sTrance.state[p] = PAIR_OFF;
    }
}

// The play's last scene: the pulse begins on every pair and grows.
void Ichor_TheaterTranceStart(void)
{
    u32 p;

    EnsureTranceTask();
    for (p = 0; p < THEATER_PAIR_COUNT; p++)
        HoldPair(p, FALSE);
}

// A right entrance: pair gSpecialVar_0x8004's blocks laugh and its purple drains.
void Ichor_TheaterTranceRelease(void)
{
    u32 p = gSpecialVar_0x8004;

    if (p >= THEATER_PAIR_COUNT || !FuncIsActiveTask(Task_TheaterTrance))
        return;
    if (sTrance.state[p] != PAIR_OFF)
    {
        sTrance.state[p] = PAIR_DRAINING;
        sTrance.delay[p] = 0;
    }
}

// The satyrs: the laugh starts in the top blocks and runs down and round, and
// the purple drains out of the stone pair by pair. The script waits.
void Ichor_TheaterTranceWake(void)
{
    static const u16 sDelays[THEATER_PAIR_COUNT] = {
        [THEATER_PAIR_TOP] = 0, [THEATER_PAIR_MID] = 36, [THEATER_PAIR_LOW] = 72,
    };
    u32 p;

    EnsureTranceTask();
    for (p = 0; p < THEATER_PAIR_COUNT; p++)
    {
        if (sTrance.state[p] != PAIR_OFF)
        {
            sTrance.state[p] = PAIR_DRAINING;
            sTrance.delay[p] = sDelays[p];
        }
    }
    sTrance.waitingScript = TRUE;   // def_special ..., waitstate=1: the script waits for the task
}

// The masks' painted eyes pass along the tiers, block by block: a gold glint runs
// over each pair in turn, from the parodoi round to the back. The script waits.
void Ichor_TheaterGaze(void)
{
    EnsureTranceTask();
    sTrance.gazePair = THEATER_PAIR_LOW;
    sTrance.gazeTimer = 0;
    sTrance.waitingScript = TRUE;   // def_special ..., waitstate=1: the script waits for the task
}

// --------------------------------------------------------------------------
// The picture window: a 64x64 image in a picture box. The Dionysia's program
// (beat 32), and Astyra's decree, forged order and practice tablets (beats
// 52-55). One shows at a time, so they share a tag.
// --------------------------------------------------------------------------

#define TAG_PICTURE  0x4A31

static const u32 sPictureGfx_Program[] = INCBIN_U32("graphics/ichor/act2/program.4bpp");
static const u16 sPicturePal_Program[] = INCBIN_U16("graphics/ichor/act2/program.gbapal");
static const u32 sPictureGfx_Decree[] = INCBIN_U32("graphics/ichor/act2/decree.4bpp");
static const u16 sPicturePal_Decree[] = INCBIN_U16("graphics/ichor/act2/decree.gbapal");
static const u32 sPictureGfx_ForgedOrder[] = INCBIN_U32("graphics/ichor/act2/forged_order.4bpp");
static const u16 sPicturePal_ForgedOrder[] = INCBIN_U16("graphics/ichor/act2/forged_order.gbapal");
static const u32 sPictureGfx_PracticeTablets[] = INCBIN_U32("graphics/ichor/act2/practice_tablets.4bpp");
static const u16 sPicturePal_PracticeTablets[] = INCBIN_U16("graphics/ichor/act2/practice_tablets.gbapal");

static const struct SpriteSheet sPictureSheets[ICHOR_PICTURE_COUNT] =
{
    [ICHOR_PICTURE_PROGRAM]          = {sPictureGfx_Program, sizeof(sPictureGfx_Program), TAG_PICTURE},
    [ICHOR_PICTURE_DECREE]           = {sPictureGfx_Decree, sizeof(sPictureGfx_Decree), TAG_PICTURE},
    [ICHOR_PICTURE_FORGED_ORDER]     = {sPictureGfx_ForgedOrder, sizeof(sPictureGfx_ForgedOrder), TAG_PICTURE},
    [ICHOR_PICTURE_PRACTICE_TABLETS] = {sPictureGfx_PracticeTablets, sizeof(sPictureGfx_PracticeTablets), TAG_PICTURE},
};

static const struct SpritePalette sPicturePalettes[ICHOR_PICTURE_COUNT] =
{
    [ICHOR_PICTURE_PROGRAM]          = {sPicturePal_Program, TAG_PICTURE},
    [ICHOR_PICTURE_DECREE]           = {sPicturePal_Decree, TAG_PICTURE},
    [ICHOR_PICTURE_FORGED_ORDER]     = {sPicturePal_ForgedOrder, TAG_PICTURE},
    [ICHOR_PICTURE_PRACTICE_TABLETS] = {sPicturePal_PracticeTablets, TAG_PICTURE},
};

static const struct OamData sOam_Picture =
{
    .shape = SPRITE_SHAPE(64x64),
    .size = SPRITE_SIZE(64x64),
    .priority = 0,
};

static const struct SpriteTemplate sSpriteTemplate_Picture =
{
    .tileTag = TAG_PICTURE,
    .paletteTag = TAG_PICTURE,
    .oam = &sOam_Picture,
    .anims = gDummySpriteAnimTable,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};

#define PICTURE_X 10   // the box's tile position, as ScriptMenu_ShowPokemonPic takes it
#define PICTURE_Y 2

static EWRAM_DATA u8 sPictureWindowId = 0;
static EWRAM_DATA u8 sPictureSpriteId = 0;
static EWRAM_DATA bool8 sPictureShown = FALSE;

static void ShowPicture(u32 picture)
{
    if (sPictureShown)
        return;
    if (picture >= ICHOR_PICTURE_COUNT)
        picture = ICHOR_PICTURE_PROGRAM;
    LoadSpriteSheet(&sPictureSheets[picture]);
    LoadSpritePalette(&sPicturePalettes[picture]);
    sPictureSpriteId = CreateSprite(&sSpriteTemplate_Picture, PICTURE_X * 8 + 40, PICTURE_Y * 8 + 40, 0);
    sPictureWindowId = CreateWindowFromRect(PICTURE_X, PICTURE_Y, 8, 8);
    SetStandardWindowBorderStyle(sPictureWindowId, TRUE);
    ScheduleBgCopyTilemapToVram(0);
    sPictureShown = TRUE;
}

// special(Ichor_ShowPicture) with VAR_0x8004 = ICHOR_PICTURE_*
void Ichor_ShowPicture(void)
{
    ShowPicture(gSpecialVar_0x8004);
}

void Ichor_HidePicture(void)
{
    if (!sPictureShown)
        return;
    DestroySprite(&gSprites[sPictureSpriteId]);
    FreeSpriteTilesByTag(TAG_PICTURE);
    FreeSpritePaletteByTag(TAG_PICTURE);
    ClearToTransparentAndRemoveWindow(sPictureWindowId);
    sPictureShown = FALSE;
}

// The Dionysia's own calls (ThyrsaTheater), which leave VAR_0x8004 alone.
void Ichor_ShowProgram(void)
{
    ShowPicture(ICHOR_PICTURE_PROGRAM);
}

void Ichor_HideProgram(void)
{
    Ichor_HidePicture();
}
