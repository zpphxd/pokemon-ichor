// Ichor: omens (design/SYSTEMS.md §6; design/ENGINE_API.md §7).
//
// Today's omen is IchorSave.omenKind (an OMEN_* kind) and omenEntry (an entry
// within that kind, e.g. OMEN_WEATHER_LERNIP). Each new day draws one from
// src/data/ichor_omens.h, filtered by story progress, unless a script forced
// it the day before (as when Akanthis first tells the Lernip rumor). Swarms
// start the expansion's mass outbreak; visitors show their objects.
#include "global.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "field_weather.h"
#include "fieldmap.h"
#include "ichor_frozen.h"
#include "ichor_omen.h"
#include "mass_outbreak.h"
#include "palette.h"
#include "random.h"
#include "script.h"
#include "constants/flags.h"
#include "constants/ichor.h"
#include "constants/map_groups.h"
#include "constants/species.h"
#include "constants/weather.h"

#include "data/ichor_omens.h"

#define ICHOR_OMEN_SALT   0x0BE5A1D5
#define SWARM_SHARE       50   // percent of the map's land encounters

static EWRAM_DATA bool8 sMapRefreshPending = FALSE;

// SYSTEMS §6's weights, by kind. The swarm's 35 is 45 until strangers walk.
static const u8 sKindWeights[] =
{
    [OMEN_SWARM]     = 35,
    [OMEN_VISITOR]   = 25,
    [OMEN_WEATHER]   = 20,
    [OMEN_GOOD_SIGN] = 10,
    [OMEN_STRANGER]  = 10,
};

static bool32 IsEntryOpen(const struct IchorOmenEntry *e)
{
    return (e->unlockFlag == 0 || FlagGet(e->unlockFlag))
        && (e->lockFlag == 0 || !FlagGet(e->lockFlag));
}

static u32 CountOpenEntries(u32 kind)
{
    u32 i, n = 0;
    for (i = 0; i < ARRAY_COUNT(sOmenEntries); i++)
    {
        if (sOmenEntries[i].kind == kind && IsEntryOpen(&sOmenEntries[i]))
            n++;
    }
    return n;
}

static const struct IchorOmenEntry *FindEntry(u32 kind, u32 entry)
{
    u32 i;
    for (i = 0; i < ARRAY_COUNT(sOmenEntries); i++)
    {
        if (sOmenEntries[i].kind == kind && sOmenEntries[i].entry == entry)
            return &sOmenEntries[i];
    }
    return NULL;
}

// Today's omen happens: a swarm's outbreak starts, and only today's visitor shows.
static void ApplyOmen(void)
{
    u32 i;
    const struct IchorOmenEntry *e = FindEntry(gIchorSave.omenKind, gIchorSave.omenEntry);

    sMapRefreshPending = TRUE;
    for (i = 0; i < ARRAY_COUNT(sOmenEntries); i++)
    {
        if (sOmenEntries[i].kind == OMEN_VISITOR && sOmenEntries[i].hideFlag != 0 && &sOmenEntries[i] != e)
            FlagSet(sOmenEntries[i].hideFlag);
    }
    if (e == NULL)
        return;
    if (e->kind == OMEN_VISITOR && e->hideFlag != 0)
    {
        FlagClear(e->hideFlag);
    }
    else if (e->kind == OMEN_SWARM && e->species != SPECIES_NONE)
    {
        struct MassOutbreak outbreak = {
            .species = e->species,
            .moves = {MOVE_NONE},  // the species' own moves at its level (mass_outbreak.c)
            .level = e->level,
            .probability = SWARM_SHARE,
            .duration = 1,
            .location = e->map,
        };
        StartMassOutbreak(outbreak);
    }
}

void Ichor_SetOmenWeather(void)
{
    if (gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_ELEUSA_VILLAGE)
     && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_ELEUSA_VILLAGE))
    {
        SetSavedWeather(gIchorSave.omenKind == OMEN_WEATHER
                     && gIchorSave.omenEntry == OMEN_WEATHER_ELEUSA_SUN
                      ? WEATHER_DROUGHT : WEATHER_NONE);
    }
}

static bool32 IsVisitorFlag(u16 flag)
{
    u32 i;

    if (flag == 0)
        return FALSE;
    for (i = 0; i < ARRAY_COUNT(sOmenEntries); i++)
    {
        if (sOmenEntries[i].kind == OMEN_VISITOR && sOmenEntries[i].hideFlag == flag)
            return TRUE;
    }
    return FALSE;
}

void Ichor_OmenFieldFrame(void)
{
    u32 i;
    struct ObjectEvent *player;
    u8 mapNum = gSaveBlock1Ptr->location.mapNum;
    u8 mapGroup = gSaveBlock1Ptr->location.mapGroup;

    if (!sMapRefreshPending || ScriptContext_IsEnabled() || gPaletteFade.active || Ichor_IsFrozenHour()
     || gPlayerAvatar.tileTransitionState != T_NOT_MOVING
     || gPlayerAvatar.objectEventId >= OBJECT_EVENTS_COUNT
     || !gObjectEvents[gPlayerAvatar.objectEventId].active)
        return;

    player = &gObjectEvents[gPlayerAvatar.objectEventId];
    if (gMapHeader.events != NULL)
    {
        for (i = 0; i < gMapHeader.events->objectEventCount; i++)
        {
            const struct ObjectEventTemplate *template = &gSaveBlock1Ptr->objectEventTemplates[i];
            u8 objectId;

            if (!IsVisitorFlag(template->flagId))
                continue;
            if (FlagGet(template->flagId))
                RemoveObjectEventByLocalIdAndMap(template->localId, mapNum, mapGroup);
            else if (template->x + MAP_OFFSET == player->currentCoords.x
                  && template->y + MAP_OFFSET == player->currentCoords.y
                  && TryGetObjectEventIdByLocalIdAndMap(template->localId, mapNum, mapGroup, &objectId))
                return; // A new arrival waits until the player leaves its tile.
        }
        // The stationary field has no moving-camera offset.
        TrySpawnObjectEvents(0, 0);
    }
    Ichor_SetOmenWeather();
    if (gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_ELEUSA_VILLAGE)
     && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_ELEUSA_VILLAGE))
        SetNextWeather(GetSavedWeather());
    sMapRefreshPending = FALSE;
}

// The day's draw: a kind by weight among the kinds with an open entry, then
// one of its open entries. Good signs are the augur's blessing half the time,
// otherwise a lucky number from 1 to 6.
void Ichor_DrawOmen(u32 seed)
{
    u32 kind, weights[ARRAY_COUNT(sKindWeights)] = {0}, total = 0, roll, i, n;
    rng_value_t rng = LocalRandomSeed(seed ^ ICHOR_OMEN_SALT);
    bool32 strangers = CountOpenEntries(OMEN_STRANGER) != 0;

    for (kind = OMEN_SWARM; kind < ARRAY_COUNT(sKindWeights); kind++)
    {
        if (kind == OMEN_GOOD_SIGN || CountOpenEntries(kind) != 0)
            weights[kind] = sKindWeights[kind];
        if (kind == OMEN_SWARM && weights[kind] != 0 && !strangers)
            weights[kind] += sKindWeights[OMEN_STRANGER];
        total += weights[kind];
    }
    roll = LocalRandom(&rng) % total;
    for (kind = OMEN_SWARM; roll >= weights[kind]; kind++)
        roll -= weights[kind];

    gIchorSave.omenKind = kind;
    if (kind == OMEN_GOOD_SIGN)
    {
        n = LocalRandom(&rng) % 12;
        gIchorSave.omenEntry = n < 6 ? OMEN_SIGN_BLESSING : OMEN_SIGN_LUCKY(n - 5);
        return;
    }
    n = LocalRandom(&rng) % CountOpenEntries(kind);
    for (i = 0; i < ARRAY_COUNT(sOmenEntries); i++)
    {
        if (sOmenEntries[i].kind == kind && IsEntryOpen(&sOmenEntries[i]) && n-- == 0)
        {
            gIchorSave.omenEntry = sOmenEntries[i].entry;
            return;
        }
    }
}

void Ichor_OmenNewDay(void)
{
    if (gIchorSave.forcedOmenKind != OMEN_NONE)
    {
        gIchorSave.omenKind = gIchorSave.forcedOmenKind;
        gIchorSave.omenEntry = gIchorSave.forcedOmenEntry;
        gIchorSave.forcedOmenKind = OMEN_NONE;
        gIchorSave.forcedOmenEntry = 0;
    }
    else
    {
        Ichor_DrawOmen(gSaveBlock1Ptr->dailySeed);
    }
    ApplyOmen();
}

// special Ichor_ForceOmen: tomorrow's omen is kind VAR_0x8004, entry VAR_0x8005.
void Ichor_ForceOmen(void)
{
    gIchorSave.forcedOmenKind = gSpecialVar_0x8004;
    gIchorSave.forcedOmenEntry = gSpecialVar_0x8005;
}

// specialvar Ichor_CheckOmen: TRUE if today's omen is kind VAR_0x8004, entry
// VAR_0x8005. A map's ON_TRANSITION uses it to set the omen's weather.
u16 Ichor_CheckOmen(void)
{
    return gIchorSave.omenKind != OMEN_NONE
        && gIchorSave.omenKind == gSpecialVar_0x8004
        && gIchorSave.omenEntry == gSpecialVar_0x8005;
}

// specialvar Ichor_GetOmen: today's omen kind (OMEN_NONE if none); its entry in VAR_0x8004.
u16 Ichor_GetOmen(void)
{
    gSpecialVar_0x8004 = gIchorSave.omenEntry;
    return gIchorSave.omenKind;
}
