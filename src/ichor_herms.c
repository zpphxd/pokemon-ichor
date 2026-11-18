// Ichor: herm waystones (design/SYSTEMS.md §4).
//
// Every route has one great herm. Anointing it with olive oil costs one Olive
// Oil, gives Hermes +1 Favor once, and registers it; anointing every herm gives
// Hermes +10 more. With Daedalus's Wings, every anointed herm's route is a fly
// target on the region map, landing on the tile south of the herm. The rows
// are in src/data/ichor_herms.h; data/scripts/ichor_herms.pory has the script.
#include "global.h"
#include "event_data.h"
#include "field_screen_effect.h"
#include "heal_location.h"
#include "ichor_herms.h"
#include "ichor_relics.h"
#include "ichor_rites.h"
#include "item.h"
#include "list_menu.h"
#include "malloc.h"
#include "overworld.h"
#include "script_menu.h"
#include "string_util.h"
#include "constants/heal_locations.h"
#include "constants/items.h"
#include "constants/maps.h"
#include "constants/region_map_sections.h"

#include "data/ichor_herms.h"
#include "data/ichor_town_herms.h"

STATIC_ASSERT(TOWN_HERM_COUNT <= TOWN_HERM_MAX, TownHermsFitTheirFlags);
STATIC_ASSERT(FLAG_ICHOR_TOWN_HERM_OLYMPUS == FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_OLYMPUS, TownHermFlagsInOrder);
STATIC_ASSERT(FLAG_ICHOR_TOWN_HERM_SPARE_31 == FLAG_ICHOR_TOWN_HERMS_START + TOWN_HERM_MAX - 1, TownHermFlagsAreOneRun);

STATIC_ASSERT(HERM_COUNT <= HERM_AETHOS_MAX, AethosHermsFitTheirFlags);
STATIC_ASSERT(HERM_MAX - HERM_OIKOUMENE_FIRST <= 32, WaystonesFitTheirFlags);

#define HERM_NONE 0xFF

// Aethos's herms flag in FLAG_ICHOR_HERMS_START's range; the Oikoumene's
// waystones (ids from HERM_OIKOUMENE_FIRST) in FLAG_ICHOR_WAYSTONES_START's.
u16 Ichor_GetHermFlag(u32 herm)
{
    if (herm < HERM_OIKOUMENE_FIRST)
        return FLAG_ICHOR_HERMS_START + herm;
    return FLAG_ICHOR_WAYSTONES_START + (herm - HERM_OIKOUMENE_FIRST);
}
#define HERM_FLAG(herm) Ichor_GetHermFlag(herm)

static bool32 IsPlaced(u32 herm)
{
    return herm < HERM_MAX && gIchorHerms[herm].map != 0;
}

static u32 GetHermOnThisMap(void)
{
    u32 herm;
    u16 map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
    for (herm = 0; herm < HERM_MAX; herm++)
    {
        if (IsPlaced(herm) && gIchorHerms[herm].map == map)
            return herm;
    }
    return HERM_NONE;
}

static bool32 IsAnointed(u32 herm)
{
    return FlagGet(HERM_FLAG(herm));
}

u32 Ichor_CountAnointedHerms(void)
{
    return Ichor_CountFlags(FLAG_ICHOR_HERMS_START, HERM_COUNT);
}

// specialvar Ichor_CountHerms: anointed herms, for the Scroll of Deeds. VAR_0x8004 gets HERM_COUNT.
u16 Ichor_CountHerms(void)
{
    gSpecialVar_0x8004 = HERM_COUNT;
    return Ichor_CountAnointedHerms();
}

enum { HERM_STATE_NONE, HERM_STATE_ANOINTED, HERM_STATE_DRY };

// specialvar Ichor_GetHermState: this map's great herm: HERM_STATE_NONE (no
// herm row for this map), _ANOINTED or _DRY. STR_VAR_1 is the Olive Oil carried.
u16 Ichor_GetHermState(void)
{
    u32 herm = GetHermOnThisMap();
    ConvertIntToDecimalStringN(gStringVar1, CountTotalItemQuantityInBag(ITEM_OLIVE_OIL), STR_CONV_MODE_LEFT_ALIGN, 3);
    if (herm == HERM_NONE)
        return HERM_STATE_NONE;
    return IsAnointed(herm) ? HERM_STATE_ANOINTED : HERM_STATE_DRY;
}

// special Ichor_AnointHerm: takes one Olive Oil and registers this map's herm.
// VAR_RESULT is TRUE when it was the last of them (Hermes's +10).
void Ichor_AnointHerm(void)
{
    u32 herm = GetHermOnThisMap();

    gSpecialVar_Result = FALSE;
    if (herm == HERM_NONE || IsAnointed(herm) || !RemoveBagItem(ITEM_OLIVE_OIL, 1))
        return;
    FlagSet(HERM_FLAG(herm));
    Ichor_AddFavorTo(ICHOR_GOD_HERMES, 1);
    if (herm < HERM_COUNT && Ichor_CountAnointedHerms() == HERM_COUNT && !FlagGet(FLAG_ICHOR_ALL_HERMS_REWARD))
    {
        FlagSet(FLAG_ICHOR_ALL_HERMS_REWARD);
        Ichor_AddFavorTo(ICHOR_GOD_HERMES, 10);
        gSpecialVar_Result = TRUE;
    }
}

static u32 GetHermForMapsec(u32 mapsec)
{
    u32 herm;
    for (herm = 0; herm < HERM_MAX; herm++)
    {
        if (IsPlaced(herm) && gIchorHerms[herm].mapsec == mapsec)
            return herm;
    }
    return HERM_NONE;
}

// A route is a fly target once its herm is anointed (the fly map itself needs the Wings).
bool32 Ichor_IsHermFlyTarget(u32 mapsec)
{
    u32 herm = GetHermForMapsec(mapsec);
    return herm != HERM_NONE && IsAnointed(herm) && gIchorHerms[herm].healLocation != HEAL_LOCATION_NONE;
}

u32 Ichor_GetHermHealLocation(u32 mapsec)
{
    if (!Ichor_IsHermFlyTarget(mapsec))
        return HEAL_LOCATION_NONE;
    return gIchorHerms[GetHermForMapsec(mapsec)].healLocation;
}

// The map section of herm `herm` if it's anointed (its fly map icon), else MAPSEC_NONE.
u32 Ichor_GetAnointedHermMapsec(u32 herm)
{
    if (!IsPlaced(herm) || !IsAnointed(herm))
        return MAPSEC_NONE;
    return gIchorHerms[herm].mapsec;
}

// ---------------------------------------------------------------------------
// Travel herms (SYSTEMS §4). Every town's entrance herm is registered the first
// time the player uses the town's Asclepeion or healer, or touches the herm.
// From then on any herm offers TRAVEL to every registered town, from the start
// of the game: no Olive Oil, no Wings. Registration lives in the Ichor flag
// bank (FLAG_ICHOR_TOWN_HERMS_START + id), not in the engine's FLAG_VISITED_*
// flags, because those are set on entering a town, not on using its healer,
// and only a few of Aethos's towns have one.
// ---------------------------------------------------------------------------

#define TOWN_HERM_NONE 0xFF

static bool32 IsTownPlaced(u32 townHerm)
{
    return townHerm < TOWN_HERM_MAX && gIchorTownHerms[townHerm].map != 0;
}

bool32 Ichor_IsTownHermRegistered(u32 townHerm)
{
    return IsTownPlaced(townHerm) && FlagGet(FLAG_ICHOR_TOWN_HERMS_START + townHerm);
}

// Sets the flag; TRUE if it wasn't set before.
static bool32 RegisterTownHerm(u32 townHerm)
{
    if (!IsTownPlaced(townHerm) || Ichor_IsTownHermRegistered(townHerm))
        return FALSE;
    FlagSet(FLAG_ICHOR_TOWN_HERMS_START + townHerm);
    return TRUE;
}

static u32 GetTownHermOnThisMap(void)
{
    u32 i;
    u16 map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
    for (i = 0; i < TOWN_HERM_MAX; i++)
    {
        if (IsTownPlaced(i) && gIchorTownHerms[i].map == map)
            return i;
    }
    return TOWN_HERM_NONE;
}

static void BufferTownHermName(u32 townHerm)
{
    if (IsTownPlaced(townHerm))
        StringCopy(gStringVar1, gIchorTownHerms[townHerm].name);
    else
        gStringVar1[0] = EOS;
}

// specialvar Ichor_TouchTownHerm: the herm object's script. Registers this
// map's town herm and puts its town in STR_VAR_1. Returns TOWN_HERM_TOUCH_*.
u16 Ichor_TouchTownHerm(void)
{
    u32 townHerm = GetTownHermOnThisMap();
    BufferTownHermName(townHerm);
    if (townHerm == TOWN_HERM_NONE)
        return TOWN_HERM_TOUCH_NONE;
    return RegisterTownHerm(townHerm) ? TOWN_HERM_TOUCH_NEW : TOWN_HERM_TOUCH_KNOWN;
}

// special Ichor_BufferTownHermName: this map's town in STR_VAR_1, for the plaque.
void Ichor_BufferTownHermName(void)
{
    BufferTownHermName(GetTownHermOnThisMap());
}

// specialvar Ichor_RegisterHealerTownHerm: called after an Asclepeion or healer
// heals. Every healer's map sets its town as the respawn point (setrespawn), so
// the last heal location says which town this is. TRUE if newly registered;
// the town is in STR_VAR_1.
u16 Ichor_RegisterHealerTownHerm(void)
{
    u32 i, heal = GetHealLocationIndexByWarpData(&gSaveBlock1Ptr->lastHealLocation);
    if (heal == HEAL_LOCATION_NONE)
        return FALSE;
    for (i = 0; i < TOWN_HERM_MAX; i++)
    {
        if (IsTownPlaced(i) && gIchorTownHerms[i].healLocation == heal)
        {
            BufferTownHermName(i);
            return RegisterTownHerm(i);
        }
    }
    return FALSE;
}

// special Ichor_RegisterTownHerm: registers TOWN_HERM_* VAR_0x8004, for a town
// healed by an inn rather than an Asclepeion. VAR_RESULT is TRUE if it's new.
void Ichor_RegisterTownHerm(void)
{
    gSpecialVar_Result = RegisterTownHerm(gSpecialVar_0x8004);
}

// specialvar Ichor_CountTravelHerms: registered towns other than this map's.
u16 Ichor_CountTravelHerms(void)
{
    u32 i, here = GetTownHermOnThisMap(), count = 0;
    for (i = 0; i < TOWN_HERM_MAX; i++)
    {
        if (i != here && Ichor_IsTownHermRegistered(i))
            count++;
    }
    return count;
}

static void PushTravelEntry(const u8 *text, u16 id)
{
    struct ListMenuItem item;
    u8 *name = Alloc(24); // freed by the menu
    StringCopy(name, text);
    item.name = name;
    item.id = id;
    MultichoiceDynamic_PushElement(item);
}

// special Ichor_BuildTravelMenu: every registered town but this one, in story
// order, each with its TOWN_HERM_* id, then "Stay here" (TOWN_HERM_STAY), for
// dynmultistack.
void Ichor_BuildTravelMenu(void)
{
    u32 i, here = GetTownHermOnThisMap();
    for (i = 0; i < TOWN_HERM_MAX; i++)
    {
        if (i != here && Ichor_IsTownHermRegistered(i))
            PushTravelEntry(gIchorTownHerms[i].name, i);
    }
    PushTravelEntry(COMPOUND_STRING("Stay here"), TOWN_HERM_STAY);
}

// specialvar Ichor_TravelToTownHerm: Hermes carries the player to TOWN_HERM_*
// VAR_0x8004's landing tile, through a white flash. Returns TRUE when the warp
// has started; the script then waits with waitstate, as after warp.
u16 Ichor_TravelToTownHerm(void)
{
    const struct IchorTownHerm *dest;
    if (!Ichor_IsTownHermRegistered(gSpecialVar_0x8004))
        return FALSE;
    dest = &gIchorTownHerms[gSpecialVar_0x8004];
    SetWarpDestination(dest->map >> 8, dest->map & 0xFF, WARP_ID_NONE, dest->x, dest->y);
    DoWhiteFadeWarp();
    ResetInitialPlayerAvatarState();
    return TRUE;
}
