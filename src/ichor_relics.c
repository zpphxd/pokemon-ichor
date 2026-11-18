// Ichor: relics, the key items that replace HMs (design/SYSTEMS.md §1, §2).
//
// No Pokémon ever needs a field move. Obstacle scripts check the bag
// (data/scripts/ichor_relics.pory), the water checks in field_control_avatar.c
// check the Conch, the Horn and the Pearl, and dark maps light up from the Torch.
// The relic's own pose replaces the Pokémon cut-in: a field effect started with
// ICHOR_FIELD_EFFECT_RELIC | item shows the relic's icon over the player.
// SELECT opens the Relic Ring once the player owns a free relic.
#include "global.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_control_avatar.h"
#include "field_effect.h"
#include "field_player_avatar.h"
#include "field_screen_effect.h"
#include "field_weather.h"
#include "fieldmap.h"
#include "gpu_regs.h"
#include "fldeff.h"
#include "follower_npc.h"
#include "ichor_frozen.h"
#include "ichor_hunt.h"
#include "ichor_labyrinth.h"
#include "ichor_omen.h"
#include "ichor_relics.h"
#include "ichor_theoxenia.h"
#include "ichor_save.h"
#include "item.h"
#include "item_icon.h"
#include "item_menu.h"
#include "item_use.h"
#include "list_menu.h"
#include "malloc.h"
#include "metatile_behavior.h"
#include "overworld.h"
#include "party_menu.h"
#include "palette.h"
#include "region_map.h"
#include "script.h"
#include "script_menu.h"
#include "sound.h"
#include "sprite.h"
#include "string_util.h"
#include "task.h"
#include "text.h"
#include "constants/field_effects.h"
#include "constants/metatile_behaviors.h"
#include "constants/ichor.h"
#include "constants/items.h"
#include "constants/songs.h"
#include "constants/weather.h"

extern const u8 EventScript_UseSurf[];
extern const u8 EventScript_UseWaterfall[];
extern const u8 EventScript_UseRockClimb[];
extern const u8 EventScript_UseDive[];
extern const u8 EventScript_UseDiveUnderwater[];
extern const u8 EventScript_CutTree[];
extern const u8 EventScript_RockSmash[];
extern const u8 EventScript_StrengthBoulder[];
extern const u8 EventScript_IchorCobweb[];
extern const u8 EventScript_IchorThornweb[];
extern const u8 EventScript_IchorGreatBoulder[];
extern const u8 EventScript_IchorLabrysSeal[];
extern const u8 EventScript_IchorThreadMenu[];
extern const u8 EventScript_IchorFlameGutters[];
extern const u8 EventScript_IchorFlameSpent[];
extern const u8 EventScript_IchorFlameDrowned[];
extern const u8 EventScript_IchorRelicRing[];
extern const u8 EventScript_IchorTorchDoused[];
extern const u8 EventScript_IchorTorchRelit[];
extern const u8 EventScript_IchorAeolusBag[];
extern const u8 EventScript_IchorHearthfire[];

// The free relics the Relic Ring offers, in its fixed order.
static const u16 sRingRelics[] = {
    ITEM_DAEDALUS_WINGS,
    ITEM_HECATES_TORCH,
    ITEM_HELM_OF_DARKNESS,
    ITEM_ARIADNES_THREAD,
};

// --- Ownership --------------------------------------------------------------

u16 Ichor_GetRelicFlag(u16 itemId)
{
    if (itemId == ITEM_TALARIA)
        return FLAG_ICHOR_GOT_TALARIA;
    if (itemId > ICHOR_RELIC_FIRST && itemId <= ICHOR_RELIC_LAST)
        return FLAG_ICHOR_RELICS_START + (itemId - ICHOR_RELIC_FIRST);
    if (itemId == ITEM_PANS_CROOK)
        return FLAG_ICHOR_GOT_PANS_CROOK;
    return 0;
}

bool32 Ichor_HasRelic(u16 itemId)
{
    u16 flag = Ichor_GetRelicFlag(itemId);
    return (flag != 0 && FlagGet(flag)) || CheckBagHasItem(itemId, 1);
}

// Owned, and this place allows outside tools.
bool32 Ichor_CanUseRelicHere(u16 itemId)
{
    return Ichor_HasRelic(itemId) && !FlagGet(FLAG_ICHOR_NO_RELICS);
}

bool32 Ichor_IsBlessed(u32 god)
{
    return gIchorSave.blessing.god == god && gIchorSave.blessing.steps != 0;
}

void Ichor_OnItemAdded(u16 itemId)
{
    u16 flag = Ichor_GetRelicFlag(itemId);
    if (flag != 0)
        FlagSet(flag);
}

static bool32 FlameTravels(u32 kind);
static void PutOutFlame(void);
static EWRAM_DATA struct { u16 steps; u8 kind; } sCarriedFlame = {0};

void Ichor_OnMapTransition(void)
{
    if (!FlameTravels(sCarriedFlame.kind))
        PutOutFlame();  // the flame dies when you leave, unless its kind travels
    FlagClear(FLAG_ICHOR_NO_RELICS);
    Ichor_FrozenHourOnMapTransition();
    Ichor_LabyrinthOnMapTransition();
}

// overworld.c, OverworldBasic: once a field frame, before the palette fade.
void Ichor_OnFieldFrame(void)
{
    Ichor_OmenFieldFrame();
    Ichor_FrozenHourFrame();
    Ichor_LabyrinthFrame();
    Ichor_TheoxeniaFrame();
    Ichor_HuntFrame();
}

// --- Light (SYSTEMS §2) -------------------------------------------------------

// The light radius on a dark map, from the Torch, its upgrade and Hecate's blessing.
u8 Ichor_GetTorchFlashLevel(void)
{
    u32 level;

    if (FlagGet(FLAG_SYS_USE_FLASH)) // vanilla Flash, for the maps that still use it
        return 1;
    if (!Ichor_CanUseRelicHere(ITEM_HECATES_TORCH))
        return ICHOR_FLASH_NO_TORCH;
    if (FlagGet(FLAG_ICHOR_TORCH_DOUSED))
        return ICHOR_FLASH_DOUSED;
    level = ICHOR_FLASH_TORCH;
    if (FlagGet(FLAG_ICHOR_THREE_FLAMED_TORCH))
        level--;
    if (Ichor_IsBlessed(ICHOR_GOD_HECATE))
        level--;
    return level;
}

#define tTimer data[0]

static void Task_EnableScriptNextFrame(u8 taskId)
{
    ScriptContext_Enable();
    DestroyTask(taskId);
}

// special Ichor_AnimateTorchFlash (waitstate): ease a dark map's light to the
// torch's radius, e.g. after dousing or relighting, or on leaving a lit zone.
void Ichor_AnimateTorchFlash(void)
{
    u8 level = Ichor_GetTorchFlashLevel();
    if (gMapHeader.cave && GetFlashLevel() != level)
    {
        AnimateFlash(level);   // eases the radius; like `animateflash`, it doesn't store the level
        SetFlashLevel(level);
    }
    else
    {
        CreateTask(Task_EnableScriptNextFrame, 80);
    }
}

// --- Glow-paint (SYSTEMS §2: douse to see glow-paint) ------------------------------

#include "data/ichor_glow.h"

// The in-game check's stand-in for a row of src/data/ichor_glow.h (tools/ichor/tests)
static EWRAM_DATA const u16 (*sGlowForTest)[16] = NULL;
static EWRAM_DATA bool8 sGlowShown = FALSE;

static const u16 (*FindGlow(const struct MapLayout *layout))[16]
{
    u32 i;
    if (!gMapHeader.cave || !FlagGet(FLAG_ICHOR_TORCH_DOUSED) || layout == NULL)
        return NULL;
    if (sGlowForTest != NULL)
        return sGlowForTest;
    for (i = 0; sGlowTilesets[i].tileset != NULL; i++)
    {
        if (sGlowTilesets[i].tileset == layout->secondaryTileset)
            return sGlowTilesets[i].palettes;
    }
    return NULL;
}

// After a map's tileset palettes load (fieldmap.c), and when the torch is
// doused: on a doused dark map with glow copies, the glow palettes replace the
// map's, and the map's layers show outside the light (its sprites don't).
void Ichor_UpdateGlow(const struct MapLayout *layout, bool32 skipFaded)
{
    const u16 (*glow)[16] = FindGlow(layout);
    if (glow != NULL)
    {
        if (skipFaded)
            CpuCopy16(glow, gPlttBufferUnfaded, NUM_PALS_TOTAL * PLTT_SIZE_4BPP);
        else
            LoadPalette(glow, BG_PLTT_ID(0), NUM_PALS_TOTAL * PLTT_SIZE_4BPP);
        SetGpuReg(REG_OFFSET_WINOUT, WINOUT_WIN01_BG_ALL | WINOUT_WINOBJ_BG0);
        sGlowShown = TRUE;
    }
    else if (sGlowShown)
    {
        SetGpuReg(REG_OFFSET_WINOUT, WINOUT_WIN01_BG0 | WINOUT_WINOBJ_BG0);  // the overworld's own
        sGlowShown = FALSE;
    }
}

// specialvar Ichor_IsInDarkMap: TRUE on a map whose header asks for a light.
bool8 Ichor_IsInDarkMap(void)
{
    return gMapHeader.cave;
}

// --- The relic pose ---------------------------------------------------------------

#define ICHOR_RELIC_ICON_TAG 0x7A10
#define RELIC_SHOW_FRAMES    44

// ICHOR_FIELD_EFFECT_RELIC | item: any item's icon, or none for ITEM_NONE (a
// gift with no item just raises a hand).
bool32 Ichor_IsRelicShowArg(u32 arg)
{
    u32 value = arg & 0xFFFF;
    return (value & ICHOR_FIELD_EFFECT_RELIC) && (value & ~ICHOR_FIELD_EFFECT_RELIC) < ITEMS_COUNT;
}

#define tSpriteId data[1]

static void Task_RelicShow(u8 taskId)
{
    struct Task *task = &gTasks[taskId];
    struct Sprite *player = &gSprites[gPlayerAvatar.spriteId];
    struct Sprite *icon = &gSprites[task->tSpriteId];

    // the icon rises from the player's hands and hangs over their head
    icon->x = player->x + player->x2;
    icon->y = player->y + player->y2 - 26 - min(task->tTimer, 6);
    if (++task->tTimer >= RELIC_SHOW_FRAMES)
    {
        DestroySpriteAndFreeResources(icon);
        FieldEffectActiveListRemove(FLDEFF_FIELD_MOVE_SHOW_MON);
        DestroyTask(taskId);
    }
}

// Shown where a Pokémon's cut-in would be: FLDEFF_FIELD_MOVE_SHOW_MON stays
// active until it ends, so every field effect that waits on the cut-in waits on
// this instead.
void Ichor_StartRelicShow(u16 itemId)
{
    u8 spriteId, taskId;

    FieldEffectActiveListAdd(FLDEFF_FIELD_MOVE_SHOW_MON);
    PlaySE(SE_M_HEAL_BELL);
    spriteId = itemId == ITEM_NONE ? MAX_SPRITES : AddItemIconSprite(ICHOR_RELIC_ICON_TAG, ICHOR_RELIC_ICON_TAG, itemId);
    taskId = CreateTask(Task_RelicShow, 80);
    if (spriteId == MAX_SPRITES)
    {
        gTasks[taskId].tTimer = RELIC_SHOW_FRAMES - 1;
        gTasks[taskId].tSpriteId = 0;
        return;
    }
    gSprites[spriteId].oam.priority = 1;
    gSprites[spriteId].coordOffsetEnabled = TRUE; // the camera's coordinates, as object sprites use
    gTasks[taskId].tSpriteId = spriteId;
    Task_RelicShow(taskId);
}

#undef tSpriteId

// Called through the vanilla field-move task: the pose, the icon, then back to the script.
static void RelicPoseDone(void)
{
    ScriptContext_Enable();
}

// special Ichor_RelicPose (waitstate): the player raises the relic in VAR_0x8004.
void Ichor_RelicPose(void)
{
    u8 taskId;

    gFieldEffectArguments[0] = ICHOR_FIELD_EFFECT_RELIC | gSpecialVar_0x8004;
    gFieldEffectArguments[3] = 0;
    taskId = CreateFieldMoveTask();
    gTasks[taskId].data[8] = (u32)RelicPoseDone >> 16;
    gTasks[taskId].data[9] = (u32)RelicPoseDone;
}

// special Ichor_FollowerHop: a visible follower hops in place beside the player.
void Ichor_FollowerHop(void)
{
    struct ObjectEvent *follower = GetFollowerObject();
    if (follower != NULL && !follower->invisible)
        ObjectEventSetHeldMovement(follower, GetJumpInPlaceMovementAction(follower->facingDirection));
}

// The Winged Talaria (Hermes's gift II): running into a one-tile gap
// (MB_ICHOR_GAP) leaps it, as a ledge jump does, if the far side is open.
bool32 Ichor_CanLeapGap(struct ObjectEvent *objectEvent, s16 x, s16 y, u32 direction)
{
    s16 landX = x, landY = y;

    if (objectEvent != &gObjectEvents[gPlayerAvatar.objectEventId])
        return FALSE;
    if (!FlagGet(FLAG_ICHOR_WINGED_TALARIA) || FlagGet(FLAG_ICHOR_NO_RELICS) || !JOY_HELD(B_BUTTON))
        return FALSE;
    if (MapGridGetMetatileBehaviorAt(x, y) != MB_ICHOR_GAP)
        return FALSE;
    MoveCoords(direction, &landX, &landY);
    return GetCollisionAtCoords(objectEvent, landX, landY, direction) == COLLISION_NONE;
}

u16 Ichor_GetFlyEffectArg(void)
{
    return ICHOR_FIELD_EFFECT_RELIC | ITEM_DAEDALUS_WINGS;
}

// --- Specials for the relic scripts ------------------------------------------------

// specialvar Ichor_CanUseRelic: can the player use the relic in VAR_0x8004 here?
// ICHOR_RELIC_OK, _MISSING, _FORBIDDEN, or _TOO_WEAK when VAR_0x8005 names an
// upgrade flag that isn't set.
u16 Ichor_CanUseRelic(void)
{
    if (!Ichor_HasRelic(gSpecialVar_0x8004))
        return ICHOR_RELIC_MISSING;
    if (FlagGet(FLAG_ICHOR_NO_RELICS))
        return ICHOR_RELIC_FORBIDDEN;
    if (gSpecialVar_0x8005 != 0 && !FlagGet(gSpecialVar_0x8005))
        return ICHOR_RELIC_TOO_WEAK;
    return ICHOR_RELIC_OK;
}

// specialvar Ichor_RelicPromptsAuto: TRUE when the "Relic prompts" option is AUTO.
bool8 Ichor_RelicPromptsAuto(void)
{
    return (gIchorSave.options & ICHOR_OPTION_RELIC_AUTO) != 0;
}

// specialvar Ichor_CheckFlagInVar / special Ichor_SetFlagInVar: the flag whose id is in VAR_0x8004.
bool8 Ichor_CheckFlagInVar(void)
{
    return FlagGet(gSpecialVar_0x8004);
}

void Ichor_SetFlagInVar(void)
{
    FlagSet(gSpecialVar_0x8004);
}

// special Ichor_ClearFog: Aeolus's Bag blows the fog off this map until you leave it.
void Ichor_ClearFog(void)
{
    SetWeather(WEATHER_NONE);
}

static bool32 IsFoggy(void)
{
    u8 weather = GetCurrentWeather();
    return weather == WEATHER_FOG_HORIZONTAL || weather == WEATHER_FOG_DIAGONAL;
}

// --- From the bag (or SELECT) -------------------------------------------------------

static const u8 sText_CantUseHere[] = _("There's nothing to use it on here.");
static const u8 sText_Forbidden[] = _("This place forbids outside tools.");
static const u8 sText_HoldB[] = _("Hold the B Button to run.");
static const u8 sText_LightEnough[] = _("It's light enough here already.");
static const u8 sText_NoSky[] = _("There's no open sky to fly in here.");
static const u8 sText_HelmOn[] = _("{PLAYER} put on the Helm of Darkness.");
static const u8 sText_HelmOff[] = _("{PLAYER} took off the Helm of Darkness.");
static const u8 sText_NoFog[] = _("There's no fog here to blow away.");

void ItemUseOutOfBattle_IchorTalaria(u8 taskId)
{
    ItemUse_IchorMessage(taskId, sText_HoldB);
}

// The obstacle in front of the player that this relic works on, if any.
static const u8 *GetContextualScript(u16 itemId)
{
    s16 x, y;
    u8 objId;
    const u8 *script;

    GetXYCoordsOneStepInFrontOfPlayer(&x, &y);
    objId = GetObjectEventIdByPosition(x, y, PlayerGetElevation());
    if (objId < OBJECT_EVENTS_COUNT)
    {
        script = GetObjectEventScriptPointerByObjectEventId(objId);
        if ((itemId == ITEM_DEMETERS_SICKLE && script == EventScript_CutTree)
         || (itemId == ITEM_BRONZE_HAMMER && (script == EventScript_RockSmash || script == EventScript_IchorGreatBoulder))
         || (itemId == ITEM_GIRDLE_OF_HERAKLES && script == EventScript_StrengthBoulder)
         || (itemId == ITEM_LABRYS && script == EventScript_IchorLabrysSeal))
        {
            gSpecialVar_LastTalked = gObjectEvents[objId].localId;
            gSpecialVar_Facing = GetPlayerFacingDirection();
            return script;
        }
    }
    switch (itemId)
    {
    case ITEM_POSEIDONS_CONCH:
        if (!TestPlayerAvatarFlags(PLAYER_AVATAR_FLAG_SURFING) && IsPlayerFacingSurfableFishableWater())
            return EventScript_UseSurf;
        break;
    case ITEM_HORN_OF_ACHELOUS:
        if (IsPlayerSurfingNorth() && MetatileBehavior_IsWaterfall(MapGridGetMetatileBehaviorAt(x, y)))
            return EventScript_UseWaterfall;
        break;
    case ITEM_PANS_CROOK:
        if (!TestPlayerAvatarFlags(PLAYER_AVATAR_FLAG_SURFING)
         && MetatileBehavior_IsRockClimbable(MapGridGetMetatileBehaviorAt(x, y)))
            return EventScript_UseRockClimb;
        break;
    case ITEM_NEREID_PEARL:
        if (gMapHeader.mapType == MAP_TYPE_UNDERWATER)
        {
            if (TrySetDiveWarp() == 1)
                return EventScript_UseDiveUnderwater;
        }
        else if (TrySetDiveWarp() == 2)
        {
            return EventScript_UseDive;
        }
        break;
    }
    return NULL;
}

void ItemUseOutOfBattle_IchorContextual(u8 taskId)
{
    const u8 *script;

    if (FlagGet(FLAG_ICHOR_NO_RELICS))
    {
        ItemUse_IchorMessage(taskId, sText_Forbidden);
        return;
    }
    script = GetContextualScript(gSpecialVar_ItemId);
    if (script == NULL)
        ItemUse_IchorMessage(taskId, sText_CantUseHere);
    else
        ItemUse_IchorRunFieldScript(taskId, script);
}

void ItemUseOutOfBattle_IchorTorch(u8 taskId)
{
    if (FlagGet(FLAG_ICHOR_NO_RELICS))
        ItemUse_IchorMessage(taskId, sText_Forbidden);
    else if (!gMapHeader.cave)
        ItemUse_IchorMessage(taskId, sText_LightEnough);
    else if (FlagGet(FLAG_ICHOR_TORCH_DOUSED))
        ItemUse_IchorRunFieldScript(taskId, EventScript_IchorTorchRelit);
    else
        ItemUse_IchorRunFieldScript(taskId, EventScript_IchorTorchDoused);
}

// special Ichor_SetTorchDoused: VAR_0x8004 TRUE douses, FALSE relights.
// --- Carried flames (SYSTEMS §2) ---------------------------------------------------

static const u8 *const sFlameNames[FLAME_COUNT] =
{
    [FLAME_HEARTH]    = COMPOUND_STRING("Hearth fire"),
    [FLAME_SANCTUM]   = COMPOUND_STRING("Sanctum fire"),
    [FLAME_THRESHOLD] = COMPOUND_STRING("Threshold fire"),
    [FLAME_HESTIA_SHIP] = COMPOUND_STRING("Hestia's fire"),
    [FLAME_LERNA]     = COMPOUND_STRING("Kleon's fire"),
    [FLAME_PANATHENAIA] = COMPOUND_STRING("Race torch"),
};

// Kinds that survive a door or an edge: the rest die when you leave the map.
static const bool8 sFlameTravels[FLAME_COUNT] =
{
    [FLAME_HESTIA_SHIP] = TRUE,  // Akti's temple, its streets, the quay, the Euploia
    [FLAME_PANATHENAIA] = TRUE,  // the Kerameikos's Dipylon, through Astyra, up to the Akropolis
};

static bool32 FlameTravels(u32 kind)
{
    return kind < FLAME_COUNT && sFlameTravels[kind];
}

// The carried flame lives here, not in the map's temp vars, which map scripts
// use for their own ends. EWRAM: a save and CONTINUE puts it out.
bool32 Ichor_IsCarryingFlame(void)
{
    return sCarriedFlame.kind != FLAME_NONE && sCarriedFlame.steps != 0;
}

void Ichor_SetCarriedFlame(u32 kind, u32 steps)
{
    sCarriedFlame.kind = steps != 0 ? kind : FLAME_NONE;
    sCarriedFlame.steps = kind != FLAME_NONE ? steps : 0;
}

static void PutOutFlame(void)
{
    Ichor_SetCarriedFlame(FLAME_NONE, 0);
}

// specialvar Ichor_GetFlameKind: the carried flame's FLAME_* kind, or FLAME_NONE.
u16 Ichor_GetFlameKind(void)
{
    return Ichor_IsCarryingFlame() ? sCarriedFlame.kind : FLAME_NONE;
}

// specialvar Ichor_GetFlameSteps: its steps left (0 without one).
u16 Ichor_GetFlameSteps(void)
{
    return Ichor_IsCarryingFlame() ? sCarriedFlame.steps : 0;
}

// special Ichor_TakeFlame: the torch takes fire VAR_0x8004 (FLAME_*) for VAR_0x8005
// steps. VAR_RESULT is FALSE without a lit Hecate's Torch.
void Ichor_TakeFlame(void)
{
    gSpecialVar_Result = FALSE;
    if (!Ichor_HasRelic(ITEM_HECATES_TORCH) || FlagGet(FLAG_ICHOR_TORCH_DOUSED) || gSpecialVar_0x8005 == 0)
        return;
    Ichor_SetCarriedFlame(gSpecialVar_0x8004, gSpecialVar_0x8005);
    gSpecialVar_Result = TRUE;
}

// special Ichor_PutOutFlame: a draught, or a script's own reason.
void Ichor_PutOutFlame(void)
{
    PutOutFlame();
}

// world-postgame's sailing flag, claimed on its branch; its own define wins once merged.
#ifndef FLAG_ICHOR_ON_SHIP
#define FLAG_ICHOR_ON_SHIP (FLAG_ICHOR_GENERAL_START + 0x302)
#endif

static bool32 IsRaining(void)
{
    u32 weather = GetCurrentWeather();
    return weather == WEATHER_RAIN || weather == WEATHER_RAIN_THUNDERSTORM || weather == WEATHER_DOWNPOUR;
}

// Ichor_OnStep: the carried flame burns down a step, two in the rain (scripts
// always give the dry count). Water puts it out. Passing 5 steps left it
// gutters; at 0 it is the torch's ordinary flame again. Scripts only start
// when `canTalk` (the blessing's step didn't start one).
bool32 Ichor_CarriedFlameStep(bool32 canTalk)
{
    u32 steps, before, cost = IsRaining() ? 2 : 1;

    if (!Ichor_IsCarryingFlame())
        return FALSE;
    if (TestPlayerAvatarFlags(PLAYER_AVATAR_FLAG_SURFING) && !FlagGet(FLAG_ICHOR_ON_SHIP)) // sailing isn't swimming
    {
        PutOutFlame();
        if (canTalk)
            ScriptContext_SetupScript(EventScript_IchorFlameDrowned);
        return canTalk;
    }
    before = sCarriedFlame.steps;
    steps = before > cost ? before - cost : 0;
    sCarriedFlame.steps = steps;
    if (steps == 0)
        sCarriedFlame.kind = FLAME_NONE;
    if (!canTalk || (steps != 0 && !(before > ICHOR_FLAME_GUTTER_STEPS && steps <= ICHOR_FLAME_GUTTER_STEPS)))
        return FALSE;
    ScriptContext_SetupScript(steps == 0 ? EventScript_IchorFlameSpent : EventScript_IchorFlameGutters);
    return TRUE;
}

// The start menu's panel: "Hearth fire: 12 steps".
void Ichor_BufferFlamePanel(u8 *dst)
{
    u32 kind = sCarriedFlame.kind;
    dst = StringCopy(dst, kind < FLAME_COUNT && sFlameNames[kind] ? sFlameNames[kind] : COMPOUND_STRING("Carried fire"));
    dst = StringCopy(dst, COMPOUND_STRING(": "));
    dst = ConvertIntToDecimalStringN(dst, sCarriedFlame.steps, STR_CONV_MODE_LEFT_ALIGN, 3);
    StringCopy(dst, sCarriedFlame.steps == 1 ? COMPOUND_STRING(" step") : COMPOUND_STRING(" steps"));
}

void Ichor_SetTorchDoused(void)
{
    if (gSpecialVar_0x8004)
    {
        FlagSet(FLAG_ICHOR_TORCH_DOUSED);
        PutOutFlame();  // a doused torch carries no fire
        Ichor_UpdateGlow(gMapHeader.mapLayout, FALSE);
    }
    else
    {
        FlagClear(FLAG_ICHOR_TORCH_DOUSED);
        if (sGlowShown)
            LoadMapTilesetPalettes(gMapHeader.mapLayout);  // the map's own colors, and the window back
    }
}

// Where the fly map goes back to if the player cancels: the party menu after a
// Pokémon's Fly (vanilla), the bag or the field after the Wings.
static MainCallback sFlyMapCancelCallback;

MainCallback Ichor_GetFlyMapCancelCallback(void)
{
    MainCallback callback = sFlyMapCancelCallback;
    sFlyMapCancelCallback = NULL;
    return callback != NULL ? callback : CB2_ReturnToPartyMenuFromFlyMap;
}

static void Task_OpenFlyMapFromField(u8 taskId)
{
    if (!gPaletteFade.active)
    {
        CleanupOverworldWindowsAndTilemaps();
        SetMainCallback2(CB2_OpenFlyMap);
        DestroyTask(taskId);
    }
}

void ItemUseOutOfBattle_IchorWings(u8 taskId)
{
    if (FlagGet(FLAG_ICHOR_NO_RELICS))
    {
        ItemUse_IchorMessage(taskId, sText_Forbidden);
    }
    else if (!Overworld_MapTypeAllowsTeleportAndFly(gMapHeader.mapType))
    {
        ItemUse_IchorMessage(taskId, sText_NoSky);
    }
    else if (ItemUse_IchorIsFromField(taskId))
    {
        sFlyMapCancelCallback = CB2_ReturnToField;
        FadeScreen(FADE_TO_BLACK, 0);
        gTasks[taskId].func = Task_OpenFlyMapFromField;
    }
    else
    {
        sFlyMapCancelCallback = CB2_ReturnToBagMenuPocket;
        ItemUse_IchorOpenScreenFromBag(taskId, CB2_OpenFlyMap);
    }
}

void ItemUseOutOfBattle_IchorThread(u8 taskId)
{
    // In the Labyrinth: TIE OFF, RETURN TO…, WIND IN (src/ichor_labyrinth.c).
    // Elsewhere the Thread leads back to a dungeon's entrance, like the Escape Rope.
    if (Ichor_IsThreadedMap())
        ItemUse_IchorRunFieldScript(taskId, EventScript_IchorThreadMenu);
    else
        ItemUseOutOfBattle_EscapeRope(taskId);
}

void ItemUseOutOfBattle_IchorHelm(u8 taskId)
{
    if (FlagGet(FLAG_ICHOR_HELM_ON))
    {
        FlagClear(FLAG_ICHOR_HELM_ON);
        ItemUse_IchorMessage(taskId, sText_HelmOff);
    }
    else
    {
        FlagSet(FLAG_ICHOR_HELM_ON);
        ItemUse_IchorMessage(taskId, sText_HelmOn);
    }
}

void ItemUseOutOfBattle_IchorAeolusBag(u8 taskId)
{
    if (IsFoggy())
        ItemUse_IchorRunFieldScript(taskId, EventScript_IchorAeolusBag);
    else
        ItemUse_IchorMessage(taskId, sText_NoFog);
}

// --- The Relic Ring ---------------------------------------------------------------

// IchorSave.relicRingCursor: 0 = the registered item, else a relic's index + 1,
// or RING_HEARTHFIRE.
#define RING_REGISTERED  0
#define RING_HEARTHFIRE  0xFF

static bool32 HasRingRelic(void)
{
    u32 i;
    for (i = 0; i < ARRAY_COUNT(sRingRelics); i++)
    {
        if (Ichor_HasRelic(sRingRelics[i]))
            return TRUE;
    }
    return FALSE;
}

bool32 Ichor_TryOpenRelicRing(void)
{
    if (!HasRingRelic() && !Ichor_IsBlessed(ICHOR_GOD_HESTIA))
        return FALSE;
    ScriptContext_SetupScript(EventScript_IchorRelicRing);
    return TRUE;
}

static void PushRingEntry(const u8 *label, u16 id)
{
    struct ListMenuItem item;
    u8 *name = Alloc(32); // freed by the menu, as dynmultipush's are

    StringCopy(name, label);
    item.name = name;
    item.id = id;
    MultichoiceDynamic_PushElement(item);
}

// The registered item's name in capitals, as menu labels are (design/TERMS.md).
static void CopyItemNameUpper(u8 *dst, u16 itemId)
{
    CopyItemName(itemId, dst);
    for (; *dst != EOS; dst++)
    {
        if (*dst >= CHAR_a && *dst <= CHAR_z)
            *dst = *dst - CHAR_a + CHAR_A;
    }
}

// special Ichor_BuildRelicRing: pushes the ring's entries for dynmultistack.
// Ids are item ids. VAR_0x8000 is the entry to start on and VAR_0x8001 the
// left column, which puts the box in the top-right corner.
void Ichor_BuildRelicRing(void)
{
    static const u8 sLabelFly[] = _("FLY");
    static const u8 sLabelDouse[] = _("DOUSE TORCH");
    static const u8 sLabelLight[] = _("LIGHT TORCH");
    static const u8 sLabelHelmOn[] = _("WEAR HELM");
    static const u8 sLabelHelmOff[] = _("REMOVE HELM");
    static const u8 sLabelThread[] = _("THREAD");
    static const u8 sLabelHearthfire[] = _("HEARTHFIRE");
    u32 i, cursor = gIchorSave.relicRingCursor;
    u16 registered = gSaveBlock1Ptr->registeredItem;
    u8 name[ITEM_NAME_LENGTH + 1];

    gSpecialVar_0x8000 = ITEM_NONE;
    if (registered != ITEM_NONE && CheckBagHasItem(registered, 1))
    {
        CopyItemNameUpper(name, registered);
        PushRingEntry(name, registered);
        gSpecialVar_0x8000 = registered;
    }
    for (i = 0; i < ARRAY_COUNT(sRingRelics); i++)
    {
        u16 relic = sRingRelics[i];
        const u8 *label;
        if (!Ichor_HasRelic(relic))
            continue;
        switch (relic)
        {
        case ITEM_DAEDALUS_WINGS:   label = sLabelFly; break;
        case ITEM_HECATES_TORCH:    label = FlagGet(FLAG_ICHOR_TORCH_DOUSED) ? sLabelLight : sLabelDouse; break;
        case ITEM_HELM_OF_DARKNESS: label = FlagGet(FLAG_ICHOR_HELM_ON) ? sLabelHelmOff : sLabelHelmOn; break;
        default:                    label = sLabelThread; break;
        }
        PushRingEntry(label, relic);
        if (gSpecialVar_0x8000 == ITEM_NONE || cursor == relic - ICHOR_RELIC_FIRST + 1)
            gSpecialVar_0x8000 = relic;
    }
    if (Ichor_IsBlessed(ICHOR_GOD_HESTIA)) // her stored heal (SYSTEMS §3)
    {
        PushRingEntry(sLabelHearthfire, ICHOR_RING_HEARTHFIRE);
        if (gSpecialVar_0x8000 == ITEM_NONE || cursor == RING_HEARTHFIRE)
            gSpecialVar_0x8000 = ICHOR_RING_HEARTHFIRE;
    }
    if (cursor == RING_REGISTERED && registered != ITEM_NONE && CheckBagHasItem(registered, 1))
        gSpecialVar_0x8000 = registered;
    // the menu snaps a box this far right against the screen's right edge
    gSpecialVar_0x8001 = DISPLAY_TILE_WIDTH - 2;
}

// special Ichor_UseRingChoice: the entry in VAR_RESULT runs as if it were the
// registered item, so each relic's logic lives only in its field-use function.
// Call it after releaseall, then end the script.
void Ichor_UseRingChoice(void)
{
    u16 itemId = gSpecialVar_Result;
    u8 taskId;

    if (itemId == ICHOR_RING_HEARTHFIRE)
    {
        gIchorSave.relicRingCursor = RING_HEARTHFIRE;
        ScriptContext_SetupScript(EventScript_IchorHearthfire);
        return;
    }
    if (itemId >= ICHOR_RELIC_FIRST && itemId <= ICHOR_RELIC_LAST)
        gIchorSave.relicRingCursor = itemId - ICHOR_RELIC_FIRST + 1;
    else
        gIchorSave.relicRingCursor = RING_REGISTERED;
    if (itemId == ITEM_NONE || !CheckBagHasItem(itemId, 1) || GetItemFieldFunc(itemId) == NULL)
        return;
    LockPlayerFieldControls();
    FreezeObjectEvents();
    PlayerFreeze();
    StopPlayerAvatar();
    gSpecialVar_ItemId = itemId;
    taskId = CreateTask(GetItemFieldFunc(itemId), 8);
    gTasks[taskId].data[3] = TRUE; // tUsingRegisteredKeyItem (item_menu.c, item_use.c)
}
