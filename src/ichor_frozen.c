// Ichor: the Frozen Hour (design/phase4/SCRIPT.md Part 11, E1-E6).
//
// The tint is applied to the unfaded palette buffer, which every fade, weather
// color map and blend reads from, so it survives them all:
// - tileset (BG) palettes are tinted as they load (fieldmap.c), and reloaded to
//   change the tint;
// - sprite (OBJ) palettes are tinted once a frame, from a copy of each slot's
//   original colors taken when it loaded (sprite.c marks it).
// A slot used by the player, the follower or an unfrozen object stays in color.
// Objects are held with the vanilla freeze, and releaseall can't thaw them
// (UnfreezeObjectEvent asks Ichor_KeepsObjectFrozen).
#include "global.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "field_weather.h"
#include "fieldmap.h"
#include "ichor_frozen.h"
#include "overworld.h"
#include "palette.h"
#include "script.h"
#include "sound.h"
#include "sprite.h"
#include "task.h"
#include "constants/event_objects.h"
#include "constants/field_weather.h"
#include "constants/rgb.h"
#include "constants/songs.h"

extern const u8 EventScript_IchorFrozenGeneric[];

#define TINT_FULL      192   // all the way to gray (or sepia)
#define TINT_STEPS     12    // the Stair's twelve steps back to color
#define BLEND_IN_SPEED 12    // TINT_FULL / 16: an unfrozen object's color runs in over 16 frames
#define SPREAD_DELAY   6     // frames per palette as the gray spreads from the Loom
#define MAX_UNFROZEN   8
#define NO_DISTANCE    0xFFFF

enum { TINT_GRAY, TINT_SEPIA };

struct IchorObjPalette
{
    u16 tag;        // the tag the slot held when its colors were saved
    u8 amount;      // how far it is tinted now, 0..TINT_FULL
    u8 mode;        // TINT_GRAY or TINT_SEPIA
    u16 original[16];
};

static EWRAM_DATA struct
{
    struct IchorObjPalette obj[16];
    u16 dirty;            // OBJ slots loaded since the last frame
    u16 blendIn;          // OBJ slots fading back to color (Ichor_UnfreezeObject)
    u16 heldObjects;      // object events the hour is holding still
    u16 spreadReached;    // OBJ slots the spreading gray has reached
    u8 unfrozenLocalIds[MAX_UNFROZEN];
    u8 unfrozenCount;
    u8 unfrozenMapNum, unfrozenMapGroup;
    bool8 sepia;
    bool8 spreading;
    bool8 mapHasScripts;  // this map's own scripts answer frozen people (Ichor_FrozenScriptsHere)
    bool8 anyTinted;
    u8 spreadOrder[NUM_PALS_TOTAL + 16];  // BG slots, then 16 + OBJ slot
    u8 spreadCount;
} sFrozen = {0};

bool32 Ichor_IsFrozenHour(void)
{
    return FlagGet(FLAG_ICHOR_FROZEN_HOUR);
}

// The day-and-night tint stays off while the world is gray or sepia.
bool32 Ichor_SuspendsDayNight(void)
{
    return Ichor_IsFrozenHour() || sFrozen.sepia;
}

static u32 GetTintMode(void)
{
    return sFrozen.sepia ? TINT_SEPIA : TINT_GRAY;
}

// How far the map is tinted now: all the way, or less on the Stair.
static u32 GetTintAmount(void)
{
    if (sFrozen.sepia)
        return TINT_FULL;
    if (Ichor_IsFrozenHour())
        return (TINT_STEPS - min(gIchorSave.frozenHourStep, TINT_STEPS)) * (TINT_FULL / TINT_STEPS);
    return 0;
}

static void TintColors(u16 *dst, const u16 *src, u32 count, u32 amount, u32 mode)
{
    u32 i;
    for (i = 0; i < count; i++)
    {
        u16 color = src[i], tinted = color;
        s32 r = GET_R(color), g = GET_G(color), b = GET_B(color);

        if (mode == TINT_SEPIA)
            TintPalette_SepiaTone(&tinted, 1);
        else
            TintPalette_GrayScale(&tinted, 1);
        r += (GET_R(tinted) - r) * (s32)amount / TINT_FULL;
        g += (GET_G(tinted) - g) * (s32)amount / TINT_FULL;
        b += (GET_B(tinted) - b) * (s32)amount / TINT_FULL;
        dst[i] = RGB2(r, g, b);
    }
}

static bool32 IsPaletteIdle(void)
{
    return !gPaletteFade.active && gWeatherPtr->palProcessingState == WEATHER_PAL_STATE_IDLE;
}

// fieldmap.c, LoadTilesetPalette: tint a tileset palette range as it loads.
void Ichor_TintBgPalettes(u32 offset, u32 count, bool32 alsoFaded)
{
    u32 amount = GetTintAmount();
    if (amount == 0)
        return;
    TintColors(&gPlttBufferUnfaded[offset], &gPlttBufferUnfaded[offset], count, amount, GetTintMode());
    if (alsoFaded)
        CpuCopy16(&gPlttBufferUnfaded[offset], &gPlttBufferFaded[offset], count * sizeof(u16));
}

// sprite.c: a sprite palette was loaded into `slot`; save its colors next frame.
void Ichor_OnSpritePaletteLoaded(u32 slot)
{
    if (slot < 16)
        sFrozen.dirty |= 1 << slot;
}

// --- Who stays in color -------------------------------------------------------------

static bool32 IsUnfrozen(const struct ObjectEvent *objectEvent)
{
    u32 i;
    if (objectEvent->isPlayer || objectEvent->localId == OBJ_EVENT_ID_FOLLOWER)
        return TRUE;
    if (objectEvent->mapNum != sFrozen.unfrozenMapNum || objectEvent->mapGroup != sFrozen.unfrozenMapGroup)
        return FALSE;
    for (i = 0; i < sFrozen.unfrozenCount; i++)
    {
        if (sFrozen.unfrozenLocalIds[i] == objectEvent->localId)
            return TRUE;
    }
    return FALSE;
}

static bool32 HourHolds(struct ObjectEvent *objectEvent)
{
    if (IsUnfrozen(objectEvent))
        return FALSE;
    if (Ichor_IsFrozenHour())
        return TRUE;
    return sFrozen.spreading && (sFrozen.spreadReached & (1 << gSprites[objectEvent->spriteId].oam.paletteNum));
}

bool32 Ichor_IsHeldByFrozenHour(struct ObjectEvent *objectEvent)
{
    return (sFrozen.heldObjects & (1 << (objectEvent - gObjectEvents))) && HourHolds(objectEvent);
}

// UnfreezeObjectEvent: releaseall doesn't thaw the people the hour holds.
bool32 Ichor_KeepsObjectFrozen(struct ObjectEvent *objectEvent)
{
    return Ichor_IsHeldByFrozenHour(objectEvent);
}

void Ichor_FrozenHourOnMapTransition(void)
{
    sFrozen.mapHasScripts = FALSE;
    sFrozen.heldObjects = 0;
    sFrozen.blendIn = 0;
    sFrozen.unfrozenCount = 0;
    sFrozen.unfrozenMapNum = gSaveBlock1Ptr->location.mapNum;
    sFrozen.unfrozenMapGroup = gSaveBlock1Ptr->location.mapGroup;
}

// --- Every field frame -----------------------------------------------------------------

// Freezes the people the hour holds, and returns the OBJ slots that stay in color.
static u32 UpdateObjects(void)
{
    u32 i, inColor = 0;

    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
    {
        struct ObjectEvent *objectEvent = &gObjectEvents[i];
        if (!objectEvent->active)
        {
            sFrozen.heldObjects &= ~(1 << i);
            continue;
        }
        if (IsUnfrozen(objectEvent))
            inColor |= 1 << gSprites[objectEvent->spriteId].oam.paletteNum;

        if (HourHolds(objectEvent))
        {
            if (!(sFrozen.heldObjects & (1 << i)))
            {
                FreezeObjectEvent(objectEvent); // refused mid-step: try again next frame
                if (objectEvent->frozen)
                    sFrozen.heldObjects |= 1 << i;
            }
        }
        else if ((sFrozen.heldObjects & (1 << i)) && !ArePlayerFieldControlsLocked())
        {
            // Thawed once no script holds the field (a script's own releaseall may do it first)
            sFrozen.heldObjects &= ~(1 << i);
            UnfreezeObjectEvent(objectEvent);
        }
    }
    return inColor;
}

static void UpdateObjPalettes(u32 inColor, bool32 force)
{
    u32 i, amount = GetTintAmount(), mode = GetTintMode();
    bool32 idle = IsPaletteIdle();

    sFrozen.anyTinted = FALSE;
    for (i = 0; i < 16; i++)
    {
        struct IchorObjPalette *slot = &sFrozen.obj[i];
        u16 *colors = &gPlttBufferUnfaded[OBJ_PLTT_ID(i)];
        u16 tag = GetSpritePaletteTagByPaletteNum(i);
        u32 target;

        if (tag == TAG_NONE)
        {
            slot->tag = TAG_NONE;
            continue;
        }
        if ((sFrozen.dirty & (1 << i)) || slot->tag != tag)
        {
            CpuCopy16(colors, slot->original, sizeof(slot->original));
            slot->tag = tag;
            slot->amount = 0;
            slot->mode = mode;
        }

        if (inColor & (1 << i))
            target = 0;
        else if (sFrozen.spreading)
            target = (sFrozen.spreadReached & (1 << i)) ? TINT_FULL : 0;
        else
            target = amount;
        if (target == 0 && (sFrozen.blendIn & (1 << i)))
        {
            if (slot->amount > BLEND_IN_SPEED)
                target = slot->amount - BLEND_IN_SPEED;
            else
                sFrozen.blendIn &= ~(1 << i);
        }

        if (force || target != slot->amount || mode != slot->mode)
        {
            TintColors(colors, slot->original, 16, target, mode);
            slot->amount = target;
            slot->mode = mode;
            if (idle)
                CpuCopy16(colors, &gPlttBufferFaded[OBJ_PLTT_ID(i)], PLTT_SIZE_4BPP);
        }
        if (slot->amount != 0)
            sFrozen.anyTinted = TRUE;
    }
    sFrozen.dirty = 0;
}

// overworld.c, OverworldBasic: before the palette fade and the frame's transfer.
void Ichor_FrozenHourFrame(void)
{
    bool32 active = Ichor_IsFrozenHour() || sFrozen.sepia || sFrozen.spreading;

    if (!active && !sFrozen.anyTinted && !sFrozen.heldObjects)
    {
        sFrozen.dirty = 0;
        return;
    }
    UpdateObjPalettes(UpdateObjects(), FALSE);
}

// Re-tints everything after the tint itself changed (sepia, a step of the Stair).
static void RefreshAllPalettes(void)
{
    LoadMapTilesetPalettes(gMapHeader.mapLayout);  // Ichor_TintBgPalettes tints them
    UpdateObjPalettes(UpdateObjects(), TRUE);
    if (!Ichor_SuspendsDayNight())
        ApplyWeatherColorMapIfIdle(gWeatherPtr->colorMapIndex);  // the day-and-night tint again
}

// --- E2: the gray spreads from the Loom -------------------------------------------------------

static const u16 *GetMetatileTiles(u32 metatileId)
{
    const struct MapLayout *layout = gMapHeader.mapLayout;
    u32 numPrimary = GetNumMetatilesInPrimary(layout);

    if (metatileId < numPrimary)
        return &layout->primaryTileset->metatiles[metatileId * NUM_TILES_PER_METATILE];
    return &layout->secondaryTileset->metatiles[(metatileId - numPrimary) * NUM_TILES_PER_METATILE];
}

// Orders the palettes by how near the Loom they show on screen: BG slots by the
// nearest metatile drawn with them, OBJ slots by the nearest frozen person
// wearing them. Palettes not on screen go last.
static void BuildSpreadOrder(s32 loomX, s32 loomY)
{
    u16 distance[NUM_PALS_TOTAL + 16];
    bool8 placed[NUM_PALS_TOTAL + 16] = {0};
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    s32 x, y;
    u32 i, j, k;

    for (i = 0; i < ARRAY_COUNT(distance); i++)
        distance[i] = NO_DISTANCE;

    for (y = player->currentCoords.y - 6; y <= player->currentCoords.y + 6; y++)
    {
        for (x = player->currentCoords.x - 8; x <= player->currentCoords.x + 8; x++)
        {
            const u16 *tiles = GetMetatileTiles(MapGridGetMetatileIdAt(x, y));
            u16 d = abs(x - loomX) + abs(y - loomY);
            for (k = 0; k < NUM_TILES_PER_METATILE; k++)
            {
                u32 pal = tiles[k] >> 12;
                if (pal < NUM_PALS_TOTAL && d < distance[pal])
                    distance[pal] = d;
            }
        }
    }
    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
    {
        struct ObjectEvent *objectEvent = &gObjectEvents[i];
        if (objectEvent->active && !IsUnfrozen(objectEvent))
        {
            u32 pal = NUM_PALS_TOTAL + gSprites[objectEvent->spriteId].oam.paletteNum;
            u16 d = abs(objectEvent->currentCoords.x - loomX) + abs(objectEvent->currentCoords.y - loomY);
            if (d < distance[pal])
                distance[pal] = d;
        }
    }

    // A stable selection sort: the nearest first; ties keep BG before OBJ.
    sFrozen.spreadCount = 0;
    for (k = 0; k < ARRAY_COUNT(distance); k++)
    {
        u32 best = ARRAY_COUNT(distance);
        for (j = 0; j < ARRAY_COUNT(distance); j++)
        {
            if (!placed[j] && (best == ARRAY_COUNT(distance) || distance[j] < distance[best]))
                best = j;
        }
        placed[best] = TRUE;
        if (best < NUM_PALS_TOTAL)
            sFrozen.spreadOrder[sFrozen.spreadCount++] = best;
        else if (distance[best] != NO_DISTANCE)  // OBJ slots nobody frozen wears wait for the end
            sFrozen.spreadOrder[sFrozen.spreadCount++] = 16 + (best - NUM_PALS_TOTAL);
    }
}

static void Task_FrozenHourSpread(u8 taskId)
{
    s16 *data = gTasks[taskId].data;

    if (++data[0] < SPREAD_DELAY)
        return;
    data[0] = 0;

    if (data[1] < sFrozen.spreadCount)
    {
        u32 pal = sFrozen.spreadOrder[data[1]++];
        if (pal < 16)
        {
            TintColors(&gPlttBufferUnfaded[PLTT_ID(pal)], &gPlttBufferUnfaded[PLTT_ID(pal)], 16, TINT_FULL, TINT_GRAY);
            CpuCopy16(&gPlttBufferUnfaded[PLTT_ID(pal)], &gPlttBufferFaded[PLTT_ID(pal)], PLTT_SIZE_4BPP);
        }
        else
        {
            sFrozen.spreadReached |= 1 << (pal - 16);
        }
        return;
    }

    gIchorSave.frozenHourStep = 0;
    FlagSet(FLAG_ICHOR_FROZEN_HOUR);
    sFrozen.spreading = FALSE;
    RefreshAllPalettes();  // the OBJ slots nobody wore, and the field effects
    Overworld_ChangeMusicToDefault();  // the music box
    DestroyTask(taskId);
    ScriptContext_Enable();
}

// special Ichor_FrozenHourBegin (waitstate): the gray spreads out from the Loom
// at (VAR_0x8004, VAR_0x8005), one palette every 6 frames, freezing people as
// it reaches them. Then FLAG_ICHOR_FROZEN_HOUR is set and the music box plays.
void Ichor_FrozenHourBegin(void)
{
    BuildSpreadOrder(gSpecialVar_0x8004 + MAP_OFFSET, gSpecialVar_0x8005 + MAP_OFFSET);
    sFrozen.spreadReached = 0;
    sFrozen.spreading = TRUE;
    CreateTask(Task_FrozenHourSpread, 80);
}

// --- E3: unfrozen objects -------------------------------------------------------------------

// special Ichor_UnfreezeObject: object VAR_0x8004 (a local id on this map) keeps
// its color and moves freely in the Frozen Hour. From ON_TRANSITION it spawns in
// color; called while it stands frozen, its color runs back in over 16 frames.
void Ichor_UnfreezeObject(void)
{
    u8 localId = gSpecialVar_0x8004;
    u8 objectEventId;
    struct ObjectEvent *objectEvent;

    sFrozen.unfrozenMapNum = gSaveBlock1Ptr->location.mapNum;
    sFrozen.unfrozenMapGroup = gSaveBlock1Ptr->location.mapGroup;
    if (sFrozen.unfrozenCount < MAX_UNFROZEN)
        sFrozen.unfrozenLocalIds[sFrozen.unfrozenCount++] = localId;

    objectEventId = GetObjectEventIdByLocalIdAndMap(localId, gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup);
    if (objectEventId >= OBJECT_EVENTS_COUNT)
        return;
    objectEvent = &gObjectEvents[objectEventId];
    sFrozen.blendIn |= 1 << gSprites[objectEvent->spriteId].oam.paletteNum;
    if (sFrozen.heldObjects & (1 << objectEventId))
    {
        sFrozen.heldObjects &= ~(1 << objectEventId);
        UnfreezeObjectEvent(objectEvent);
    }
}

// --- E5: sepia memory -------------------------------------------------------------------

// special Ichor_SepiaMemoryBegin / Ichor_SepiaMemoryEnd: a memory plays in sepia,
// then the present comes back gray. The two are never on screen together.
void Ichor_SepiaMemoryBegin(void)
{
    sFrozen.sepia = TRUE;
    RefreshAllPalettes();
}

void Ichor_SepiaMemoryEnd(void)
{
    sFrozen.sepia = FALSE;
    RefreshAllPalettes();
}

// --- E6: the color returns ---------------------------------------------------------------

// special Ichor_ColorReturnStep: step VAR_0x8004 (1-12) of the Stair. Each step
// brings a twelfth of the color back, and survives a map load. Step 12 ends the
// Frozen Hour: the day-and-night tint, the people and the map's music return.
void Ichor_ColorReturnStep(void)
{
    u32 step = gSpecialVar_0x8004;

    if (step >= TINT_STEPS)
    {
        gIchorSave.frozenHourStep = 0;
        FlagClear(FLAG_ICHOR_FROZEN_HOUR);
    }
    else
    {
        gIchorSave.frozenHourStep = step;
    }
    RefreshAllPalettes();
    if (step >= TINT_STEPS)
        Overworld_ChangeMusicToDefault();
}

// --- Talking to frozen people ----------------------------------------------------------------

// field_control_avatar.c: on a map with no frozen scripts of its own, talking
// to someone the hour holds gets a generic line instead of their script, so
// frozen trainers don't battle (Phase 4 SCRIPT.md Part 2, "The generic rule").
// Inanimate objects (item balls, rocks) keep their scripts.
const u8 *Ichor_FrozenTalkScript(u32 objectEventId, const u8 *script)
{
    struct ObjectEvent *objectEvent = &gObjectEvents[objectEventId];

    if (!Ichor_IsFrozenHour() || sFrozen.mapHasScripts || objectEvent->inanimate || !HourHolds(objectEvent))
        return script;
    return EventScript_IchorFrozenGeneric;
}

// special Ichor_FrozenScriptsHere: this map's own scripts answer its frozen
// people (call it in ON_TRANSITION). Each script checks FLAG_ICHOR_FROZEN_HOUR
// itself, and can goto(EventScript_IchorFrozenGeneric) for the generic line.
void Ichor_FrozenScriptsHere(void)
{
    sFrozen.mapHasScripts = TRUE;
}

// specialvar Ichor_FrozenGenericLine: the line for the object last talked to:
// 0-2 by its local id, or 3 for a Pokémon.
u16 Ichor_FrozenGenericLine(void)
{
    struct ObjectEvent *objectEvent = &gObjectEvents[gSelectedObjectEvent];
    if (objectEvent->graphicsId & OBJ_EVENT_MON)
        return 3;
    return objectEvent->localId % 3;
}
