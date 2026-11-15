// Ichor postgame: the sailing layer (design/postgame/ENGINE.md; design/ODYSSEY.md
// §2 and §4).
//
// While FLAG_ICHOR_ON_SHIP is set and the player is surfing, the avatar is the
// Euploia: the surf state, with the ship's 64x64 graphics, no surf blob and the
// follower stowed (followers already hide while surfing). The flag stays set from
// the moment she puts out until you go ashore, including while you're below deck
// from the sea. Her speed and her sail come from the day's wind
// (IchorEpics.wind), which the daily reset rolls. The helm's voyages are
// src/data/ichor_voyages.h; the scripts are data/scripts/ichor_postgame_sailing.pory.
//
// Upstream hooks, each marked "Ichor postgame:": field_player_avatar.c (the
// graphics, the step, the push, no stepping ashore), field_effect_helpers.c (no
// surf blob), wild_encounter.c (the rate), start_menu.c (the wind line),
// overworld.c (the Great Bear), field_region_map.c (the Town Map's R at sea), and
// in ichor-engine's files ichor_save.c (the daily wind) and ichor_relics.c (the
// Wings at sea, the Relic Ring's DECK).
#include "global.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "field_screen_effect.h"
#include "field_weather.h"
#include "fieldmap.h"
#include "ichor_sailing.h"
#include "ichor_save.h"
#include "list_menu.h"
#include "main.h"
#include "malloc.h"
#include "overworld.h"
#include "palette.h"
#include "rtc.h"
#include "script.h"
#include "script_menu.h"
#include "sprite.h"
#include "string_util.h"
#include "task.h"
#include "constants/event_objects.h"
#include "constants/ichor_sailing.h"
#include "constants/map_types.h"
#include "constants/maps.h"
#include "constants/rtc.h"

struct IchorVoyage
{
    const u8 *name;
    const u8 *crossing;
    u16 gateFlag;
    u16 quayMap;
    u8 quayX, quayY;
    u16 seaMap;
    u8 seaX, seaY;
    u8 seaDir;
};

#include "data/ichor_voyages.h"

#define sEpics (gIchorSave.epics)

static void RefreshSail(void);

static const struct IchorVoyage *GetVoyage(u32 port)
{
    if (port >= ARRAY_COUNT(sIchorVoyages))
        port = VOYAGE_NONE;
    return &sIchorVoyages[port];
}

static bool32 HasQuay(const struct IchorVoyage *voyage)
{
    return voyage->quayMap != MAP_UNDEFINED;
}

static bool32 HasSea(const struct IchorVoyage *voyage)
{
    return voyage->seaMap != MAP_UNDEFINED;
}

static bool32 IsPortOpen(u32 port)
{
    const struct IchorVoyage *voyage = GetVoyage(port);
    return port != VOYAGE_NONE && voyage->gateFlag != 0 && FlagGet(voyage->gateFlag)
        && (HasQuay(voyage) || HasSea(voyage));
}

// --- Wind -------------------------------------------------------------------------------

u32 Ichor_GetWindDirection(void)
{
    return sEpics.wind & ICHOR_WIND_DIR_MASK;
}

// The strength that counts: an event calm stills any wind; Poseidon's grudge
// never lets it drop to nothing.
u32 Ichor_GetWindStrength(void)
{
    u32 strength = (sEpics.wind & ICHOR_WIND_STRENGTH_MASK) >> ICHOR_WIND_STRENGTH_SHIFT;

    if (sEpics.wind & ICHOR_WIND_BECALMED_BIT)
        return ICHOR_WIND_CALM;
    if (strength > ICHOR_WIND_STRONG)
        strength = ICHOR_WIND_STRONG;
    if ((sEpics.wind & ICHOR_WIND_GRUDGE_BIT) && strength == ICHOR_WIND_CALM)
        strength = ICHOR_WIND_FRESH;
    return strength;
}

static void SetWind(u32 direction, u32 strength)
{
    u32 keep = sEpics.wind & ICHOR_WIND_GRUDGE_BIT;

    if (strength == ICHOR_WIND_BECALMED)
        keep |= ICHOR_WIND_BECALMED_BIT;
    else if (strength > ICHOR_WIND_STRONG)
        strength = ICHOR_WIND_STRONG;
    if (strength == ICHOR_WIND_BECALMED)
        strength = ICHOR_WIND_CALM;
    sEpics.wind = keep | (direction & ICHOR_WIND_DIR_MASK) | (strength << ICHOR_WIND_STRENGTH_SHIFT);
}

// A heading (DIR_*) as a point of the wind's compass.
static u32 HeadingToCompass(u32 direction)
{
    switch (direction)
    {
    case DIR_NORTH: return ICHOR_WIND_N;
    case DIR_EAST:  return ICHOR_WIND_E;
    case DIR_WEST:  return ICHOR_WIND_W;
    default:        return ICHOR_WIND_S;
    }
}

static u32 CompassDistance(u32 a, u32 b)
{
    u32 d = (a - b) & 7;
    return d > 4 ? 8 - d : d;
}

// The ship's heading against the wind: ICHOR_SAIL_*. Poseidon's grudge turns the
// wind against whatever heading you take (ODYSSEY §4).
u32 Ichor_GetSailing(u32 direction)
{
    u32 heading, from;

    if (Ichor_GetWindStrength() == ICHOR_WIND_CALM)
        return ICHOR_SAIL_CALM;
    if (sEpics.wind & ICHOR_WIND_GRUDGE_BIT)
        return ICHOR_SAIL_UPWIND;
    heading = HeadingToCompass(direction);
    from = Ichor_GetWindDirection();
    if (CompassDistance(from, (heading + 4) & 7) <= 1)
        return ICHOR_SAIL_DOWNWIND;
    if (CompassDistance(from, heading) <= 1)
        return ICHOR_SAIL_UPWIND;
    return ICHOR_SAIL_CROSSWIND;
}

// The daily reset (ichor_save.c's Ichor_DoDailyEvents, after the daily seed
// turns): a new direction and strength from the day's seed. Poseidon's grudge and
// an event calm hold until an event lifts them; while the grudge holds, every day
// blows strong.
void Ichor_RollDailyWind(void)
{
    u32 seed = gSaveBlock1Ptr->dailySeed;
    u32 roll = ((seed >> 11) ^ (seed >> 23)) % 100;
    u32 strength;

    if (roll < 20)
        strength = ICHOR_WIND_CALM;
    else if (roll < 75)
        strength = ICHOR_WIND_FRESH;
    else
        strength = ICHOR_WIND_STRONG;
    if (sEpics.wind & ICHOR_WIND_GRUDGE_BIT)
        strength = ICHOR_WIND_STRONG;
    sEpics.wind = (sEpics.wind & (ICHOR_WIND_GRUDGE_BIT | ICHOR_WIND_BECALMED_BIT))
                | ((seed >> 3) & ICHOR_WIND_DIR_MASK)
                | (strength << ICHOR_WIND_STRENGTH_SHIFT);
}

static const u8 *const sWindNames[ICHOR_WIND_DIRECTIONS] =
{
    [ICHOR_WIND_N]  = COMPOUND_STRING("north"),
    [ICHOR_WIND_NE] = COMPOUND_STRING("north-east"),
    [ICHOR_WIND_E]  = COMPOUND_STRING("east"),
    [ICHOR_WIND_SE] = COMPOUND_STRING("south-east"),
    [ICHOR_WIND_S]  = COMPOUND_STRING("south"),
    [ICHOR_WIND_SW] = COMPOUND_STRING("south-west"),
    [ICHOR_WIND_W]  = COMPOUND_STRING("west"),
    [ICHOR_WIND_NW] = COMPOUND_STRING("north-west"),
};

// "west, fresh", "calm", or "ahead, strong" under Poseidon's grudge.
static u8 *BufferWind(u8 *dst)
{
    u32 strength = Ichor_GetWindStrength();

    if (strength == ICHOR_WIND_CALM)
        return StringCopy(dst, COMPOUND_STRING("calm"));
    if (sEpics.wind & ICHOR_WIND_GRUDGE_BIT)
        dst = StringCopy(dst, COMPOUND_STRING("ahead"));
    else
        dst = StringCopy(dst, sWindNames[Ichor_GetWindDirection()]);
    return StringCopy(dst, strength == ICHOR_WIND_STRONG ? COMPOUND_STRING(", strong") : COMPOUND_STRING(", fresh"));
}

// special Ichor_SetWind: VAR_0x8004 = ICHOR_WIND_N..NW, VAR_0x8005 = ICHOR_WIND_CALM,
// _FRESH, _STRONG, or _BECALMED (a calm the daily reset leaves alone).
void Ichor_SetWind(void)
{
    SetWind(gSpecialVar_0x8004, gSpecialVar_0x8005);
    RefreshSail();
}

// specialvar Ichor_GetWind: the wind's direction (ICHOR_WIND_*). Also VAR_0x8004 =
// the direction, VAR_0x8005 = the strength that counts (calm when becalmed), and
// VAR_0x8006 = TRUE under Poseidon's grudge.
u16 Ichor_GetWind(void)
{
    gSpecialVar_0x8004 = Ichor_GetWindDirection();
    gSpecialVar_0x8005 = Ichor_GetWindStrength();
    gSpecialVar_0x8006 = (sEpics.wind & ICHOR_WIND_GRUDGE_BIT) != 0;
    return gSpecialVar_0x8004;
}

// special Ichor_BufferWind: STR_VAR_1 = "west, fresh" (or "calm", or "ahead,
// strong" under the grudge); STR_VAR_2 = the direction alone ("west") and
// STR_VAR_3 = the strength alone ("fresh"), for lines like Nausikles's.
void Ichor_BufferWind(void)
{
    u32 strength = Ichor_GetWindStrength();

    BufferWind(gStringVar1);
    StringCopy(gStringVar2, sWindNames[Ichor_GetWindDirection()]);
    if (strength == ICHOR_WIND_STRONG)
        StringCopy(gStringVar3, COMPOUND_STRING("strong"));
    else if (strength == ICHOR_WIND_FRESH)
        StringCopy(gStringVar3, COMPOUND_STRING("fresh"));
    else
        StringCopy(gStringVar3, COMPOUND_STRING("calm"));
}

// special Ichor_SetGrudge / Ichor_LiftGrudge: Poseidon's grudge (ODYSSEY §4). The
// Cyclops's island raises it; a loved offering at a sea altar lifts it.
void Ichor_SetGrudge(void)
{
    sEpics.wind |= ICHOR_WIND_GRUDGE_BIT;
    RefreshSail();
}

void Ichor_LiftGrudge(void)
{
    sEpics.wind &= ~ICHOR_WIND_GRUDGE_BIT;
    RefreshSail();
}

// specialvar Ichor_GetSailingEncounterRate: the wild encounter rate at sea for the
// ship's heading, in percent of the map's own (50 downwind, 150 upwind, else 100;
// 100 when not sailing). For scripts and tests; wild_encounter.c applies it.
u16 Ichor_GetSailingEncounterRate(void)
{
    return Ichor_ModifySailingEncounterRate(100);
}

// wild_encounter.c: rowing is loud, running before the wind is quiet.
u32 Ichor_ModifySailingEncounterRate(u32 encounterRate)
{
    if (!Ichor_IsSailing())
        return encounterRate;
    switch (Ichor_GetSailing(GetPlayerMovementDirection()))
    {
    case ICHOR_SAIL_DOWNWIND:
        return encounterRate / 2;
    case ICHOR_SAIL_UPWIND:
        return encounterRate * 3 / 2;
    default:
        return encounterRate;
    }
}

// start_menu.c: the info panel's line while you're at sea in the ship.
bool32 Ichor_HasWindPanel(void)
{
    return Ichor_IsSailing();
}

u8 *Ichor_BufferWindPanel(u8 *dst)
{
    dst = StringCopy(dst, COMPOUND_STRING("Wind: "));
    return BufferWind(dst);
}

// --- The ship avatar --------------------------------------------------------------------

bool32 Ichor_IsSailing(void)
{
    return FlagGet(FLAG_ICHOR_ON_SHIP) && TestPlayerAvatarFlags(PLAYER_AVATAR_FLAG_SURFING);
}

bool32 Ichor_IsShipGraphics(u16 graphicsId)
{
    return graphicsId == ICHOR_SHIP_GFX || graphicsId == ICHOR_SHIP_GFX_SLACK;
}

// The sail fills downwind and crosswind, and hangs slack upwind and in a calm.
u16 Ichor_GetShipGraphicsId(u32 direction)
{
    switch (Ichor_GetSailing(direction))
    {
    case ICHOR_SAIL_DOWNWIND:
    case ICHOR_SAIL_CROSSWIND:
        return ICHOR_SHIP_GFX;
    default:
        return ICHOR_SHIP_GFX_SLACK;
    }
}

// Swap the sail for a new heading, at a tile's center only (setting graphics puts
// the sprite back on its tile). Leaves a fishing or relic pose alone.
static void UpdateSail(u32 direction)
{
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    u16 graphicsId = Ichor_GetShipGraphicsId(direction);

    if (Ichor_IsShipGraphics(player->graphicsId) && player->graphicsId != graphicsId)
        ObjectEventSetGraphicsId(player, graphicsId);
}

// The wind changed under a ship at rest (an event's Ichor_SetWind, the grudge).
static void RefreshSail(void)
{
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];

    if (!Ichor_IsSailing() || !Ichor_IsShipGraphics(player->graphicsId))
        return;
    UpdateSail(player->facingDirection);
    ObjectEventTurn(player, player->facingDirection);
}

// field_player_avatar.c: turning in place in the ship (the turn itself follows).
void Ichor_SailTurn(u32 direction)
{
    UpdateSail(direction);
}

// A strong wind behind her carries her one tile further on the first step from
// rest: armed here, spent by Ichor_SailPushDirection on the very next input frame.
// sStepEnd is when the last sail step ends (in vblanks): a step that starts within
// a couple of frames of it continues the voyage; any later one starts from rest.
static EWRAM_DATA u8 sPushDirection = DIR_NONE;
static EWRAM_DATA u32 sPushDeadline = 0;
static EWRAM_DATA u32 sStepEnd = 0;

// Speeds, in frames per tile (ODYSSEY §4). The surf state already moves at the
// running speed (8), so rowing keeps it and the wind goes one step faster: the
// current's speed (6) downwind, the Mach Bike's (4) with the new sail.
#define SAIL_FRAMES_ROWING    8
#define SAIL_FRAMES_DOWNWIND  6
#define SAIL_FRAMES_NEW_SAIL  4

// field_player_avatar.c: one step of the ship, from the surf state's step.
void Ichor_SailStep(u32 direction)
{
    u32 now = gMain.vblankCounter1;
    bool32 fromRest = now > sStepEnd + 2;
    u32 sailing = Ichor_GetSailing(direction);
    u32 frames;
    u8 action;

    UpdateSail(direction);
    if (sailing != ICHOR_SAIL_DOWNWIND)
    {
        frames = SAIL_FRAMES_ROWING;
        action = GetWalkFastMovementAction(direction);
    }
    else if (FlagGet(FLAG_ICHOR_SHIP_SAIL))
    {
        frames = SAIL_FRAMES_NEW_SAIL;
        action = GetWalkFasterMovementAction(direction);
    }
    else
    {
        frames = SAIL_FRAMES_DOWNWIND;
        action = GetRideWaterCurrentMovementAction(direction);
    }
    PlayerSetAnimId(action, COPY_MOVE_WALK);

    sStepEnd = now + frames;
    sPushDirection = DIR_NONE;
    if (fromRest && sailing == ICHOR_SAIL_DOWNWIND && Ichor_GetWindStrength() == ICHOR_WIND_STRONG)
    {
        sPushDirection = direction;
        sPushDeadline = sStepEnd + 2;
    }
}

// field_player_avatar.c, MovePlayerNotOnBike: the wind's extra tile. If the player
// let go of the pad as the first step ended, the step goes on once more. Steering
// another way, a script or a battle in between (the deadline) spends it.
u32 Ichor_SailPushDirection(u32 direction)
{
    u32 push = sPushDirection;

    if (push == DIR_NONE)
        return direction;
    sPushDirection = DIR_NONE;
    if (direction != DIR_NONE || !Ichor_IsSailing() || gMain.vblankCounter1 > sPushDeadline)
        return direction;
    return push;
}

// --- Ports, boarding and landing -------------------------------------------------------

// specialvar Ichor_GetShipPort: the VOYAGE_* port she's moored at, or VOYAGE_NONE
// while she's at sea. A ship nobody has sailed yet waits at Akti, her home port.
u16 Ichor_GetShipPort(void)
{
    if (FlagGet(FLAG_ICHOR_ON_SHIP))
        return VOYAGE_NONE;
    if (sEpics.shipPort == VOYAGE_NONE || sEpics.shipPort >= ARRAY_COUNT(sIchorVoyages))
        return VOYAGE_AKTI;
    return sEpics.shipPort;
}

// specialvar Ichor_IsMooredAt: TRUE if she's moored at the port in VAR_0x8004
// (a gangplank's check, or Nolan's "if the Euploia is moored in Lechaion").
bool8 Ichor_IsMooredAt(void)
{
    return Ichor_GetShipPort() == gSpecialVar_0x8004;
}

// The facing to give the player once a ship warp has landed.
static EWRAM_DATA u8 sArrivalFacing = DIR_NONE;

// overworld.c, GetAdjustedInitialDirection: the next map load creates the player
// facing this way (so the ship's sail is right from the first frame). Read once.
u32 Ichor_TakeArrivalFacing(void)
{
    u32 facing = sArrivalFacing;
    sArrivalFacing = DIR_NONE;
    return facing;
}

// Every ship warp: the next map, facing `facing` (DIR_NONE leaves the map's own).
// `quiet` skips the door sound, for a crossing that has already faded out.
// The calling script follows the special with waitstate.
static void ShipWarp(u16 map, u32 x, u32 y, u32 facing, bool32 quiet)
{
    SetWarpDestination(map >> 8, map & 0xFF, WARP_ID_NONE, x, y);
    if (quiet)
        DoDiveWarp();
    else
        DoWarp();
    ResetInitialPlayerAvatarState();
    sArrivalFacing = facing;
}

// Out onto `port`'s sea, in the ship. (Nothing to do for a port with no sea.)
static void PutToSea(const struct IchorVoyage *voyage, bool32 quiet)
{
    if (!HasSea(voyage))
    {
        ScriptContext_Enable();
        return;
    }
    FlagSet(FLAG_ICHOR_ON_SHIP);
    sEpics.shipPort = VOYAGE_NONE;
    ShipWarp(voyage->seaMap, voyage->seaX, voyage->seaY, voyage->seaDir, quiet);
}

// Ashore on `port`'s quay; she's moored there now. A port with no quay goes
// nowhere (the scripts check first), so the waiting script just goes on.
static void PutAshore(u32 port, bool32 quiet)
{
    const struct IchorVoyage *voyage = GetVoyage(port);
    if (!HasQuay(voyage))
    {
        ScriptContext_Enable();
        return;
    }
    FlagClear(FLAG_ICHOR_ON_SHIP);
    sEpics.shipPort = port;
    ShipWarp(voyage->quayMap, voyage->quayX, voyage->quayY, DIR_SOUTH, quiet);
}

static void WarpToDeck(void)
{
    ShipWarp(ICHOR_SHIP_DECK_MAP, ICHOR_SHIP_DECK_X, ICHOR_SHIP_DECK_Y, DIR_NORTH, FALSE);
}

// specialvar Ichor_PortHasSea: VAR_0x8004 = a port. TRUE if she puts out onto a
// sea map there (boarding goes to sea), FALSE if she moors (boarding goes on deck).
bool8 Ichor_PortHasSea(void)
{
    return HasSea(GetVoyage(gSpecialVar_0x8004));
}

// specialvar Ichor_PortHasQuay: VAR_0x8004 = a port. TRUE if you can go ashore there.
bool8 Ichor_PortHasQuay(void)
{
    return HasQuay(GetVoyage(gSpecialVar_0x8004));
}

// special Ichor_BufferPortName: STR_VAR_1 = the port in VAR_0x8004, in prose.
void Ichor_BufferPortName(void)
{
    StringCopy(gStringVar1, GetVoyage(gSpecialVar_0x8004)->name);
}

// special Ichor_BoardShip (waitstate): from a gangplank, VAR_0x8004 = the port.
// Out onto the port's sea in the ship, or onto the deck, moored there.
void Ichor_BoardShip(void)
{
    const struct IchorVoyage *voyage = GetVoyage(gSpecialVar_0x8004);

    if (HasSea(voyage))
    {
        PutToSea(voyage, FALSE);
    }
    else
    {
        FlagClear(FLAG_ICHOR_ON_SHIP);
        sEpics.shipPort = gSpecialVar_0x8004;
        WarpToDeck();
    }
}

// special Ichor_GoAshore (waitstate): a sea map's landing, VAR_0x8004 = the port.
void Ichor_GoAshore(void)
{
    PutAshore(gSpecialVar_0x8004, FALSE);
}

// special Ichor_LeaveShip (waitstate): the deck's gangplank, to the quay where
// she's moored. The script checks Ichor_GetShipPort first.
void Ichor_LeaveShip(void)
{
    PutAshore(Ichor_GetShipPort(), FALSE);
}

// special Ichor_CastOff (waitstate): the helm's CAST OFF, from the deck of a ship
// moored at a port with a sea map.
void Ichor_CastOff(void)
{
    PutToSea(GetVoyage(Ichor_GetShipPort()), FALSE);
}

// special Ichor_PutShipAtSea (waitstate): put the player in the ship at sea
// anywhere, for a story beat (a storm, the Phaeacians' night crossing).
// VAR_0x8004 = the map (MAP_*), VAR_0x8005/6 = x, y, VAR_0x8007 = facing (DIR_*).
void Ichor_PutShipAtSea(void)
{
    FlagSet(FLAG_ICHOR_ON_SHIP);
    sEpics.shipPort = VOYAGE_NONE;
    ShipWarp(gSpecialVar_0x8004, gSpecialVar_0x8005, gSpecialVar_0x8006, gSpecialVar_0x8007, FALSE);
}

// --- Below deck and back ------------------------------------------------------------------

// The Relic Ring's DECK: in the ship, at sea.
bool32 Ichor_CanGoBelowDeck(void)
{
    return Ichor_IsSailing();
}

// special Ichor_GoBelowDeck (waitstate): note where she is, then down to the deck.
void Ichor_GoBelowDeck(void)
{
    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];

    sEpics.seaMapGroup = gSaveBlock1Ptr->location.mapGroup;
    sEpics.seaMapNum = gSaveBlock1Ptr->location.mapNum;
    sEpics.seaX = player->currentCoords.x - MAP_OFFSET;
    sEpics.seaY = player->currentCoords.y - MAP_OFFSET;
    sEpics.seaFacing = player->facingDirection;
    WarpToDeck();
}

// special Ichor_ReturnToSea (waitstate): the helm's TAKE HER OUT, back to the
// tile and heading she was on when you went below.
void Ichor_ReturnToSea(void)
{
    FlagSet(FLAG_ICHOR_ON_SHIP);
    ShipWarp((sEpics.seaMapGroup << 8) | sEpics.seaMapNum, sEpics.seaX, sEpics.seaY, sEpics.seaFacing, FALSE);
}

// --- The helm ---------------------------------------------------------------------------

static void PushEntry(const u8 *text, u16 id)
{
    struct ListMenuItem item;
    u8 *name = Alloc(32); // freed by the menu, as dynmultipush's are
    StringCopy(name, text);
    item.name = name;
    item.id = id;
    MultichoiceDynamic_PushElement(item);
}

// special Ichor_BuildHelmMenu: Nausikles's menu, ids ICHOR_HELM_*. VAR_0x8001 is
// the box's left column, against the screen's right edge.
void Ichor_BuildHelmMenu(void)
{
    u32 port = Ichor_GetShipPort();

    if (port == VOYAGE_NONE)
        PushEntry(COMPOUND_STRING("TAKE HER OUT"), ICHOR_HELM_TAKE_HER_OUT);
    else if (HasSea(GetVoyage(port)))
        PushEntry(COMPOUND_STRING("CAST OFF"), ICHOR_HELM_CAST_OFF);
    if (!FlagGet(FLAG_ICHOR_AT_SEA))
        PushEntry(COMPOUND_STRING("SET A COURSE"), ICHOR_HELM_SET_COURSE);
    PushEntry(COMPOUND_STRING("THE WIND?"), ICHOR_HELM_WIND);
    PushEntry(COMPOUND_STRING("STAY"), ICHOR_HELM_STAY);
    gSpecialVar_0x8001 = DISPLAY_TILE_WIDTH - 2;
}

// special Ichor_BuildVoyageMenu: every open port but the one she's moored at, its
// id the VOYAGE_* port, in capitals. VAR_RESULT is how many.
void Ichor_BuildVoyageMenu(void)
{
    u32 port, here = Ichor_GetShipPort(), count = 0;
    u8 name[32];

    for (port = VOYAGE_NONE + 1; port < ARRAY_COUNT(sIchorVoyages); port++)
    {
        u8 *c;
        if (port == here || !IsPortOpen(port))
            continue;
        StringCopyN(name, GetVoyage(port)->name, sizeof(name) - 1);
        name[sizeof(name) - 1] = EOS;
        for (c = name; *c != EOS; c++)
        {
            if (*c >= CHAR_a && *c <= CHAR_z)
                *c = *c - CHAR_a + CHAR_A;
        }
        PushEntry(name, port);
        count++;
    }
    gSpecialVar_0x8001 = DISPLAY_TILE_WIDTH - 2;
    gSpecialVar_Result = count;
}

// special Ichor_BufferCrossing: gStringVar4 = Nausikles's line for the course to
// VAR_0x8004, for msgbox(gStringVar4).
void Ichor_BufferCrossing(void)
{
    StringExpandPlaceholders(gStringVar4, GetVoyage(gSpecialVar_0x8004)->crossing);
}

// special Ichor_SetCourse (waitstate): the crossing's end, after the script has
// faded out. Ashore at VAR_0x8004's quay, or out on its sea for a port of open sea.
void Ichor_SetCourse(void)
{
    const struct IchorVoyage *voyage = GetVoyage(gSpecialVar_0x8004);

    if (HasQuay(voyage))
        PutAshore(gSpecialVar_0x8004, TRUE);
    else
        PutToSea(voyage, TRUE);
}

// --- The at-sea lock --------------------------------------------------------------------

const u8 gText_IchorNoHermAtSea[] = _("No herm out here. The sea has no roads.");

// Daedalus's Wings, the Town Map's R and herm flight refuse once you've rounded
// Maleia (ODYSSEY §4, O1).
bool32 Ichor_IsSeaLocked(void)
{
    return FlagGet(FLAG_ICHOR_AT_SEA);
}

// --- The Great Bear -----------------------------------------------------------------------

#define GREAT_BEAR_TAG  0x7A20

static const u32 sGreatBear_Gfx[] = INCGFX_U32("graphics/field_effects/pics/ichor_great_bear.png", ".4bpp");
static const u16 sGreatBear_Pal[] = INCGFX_U16("graphics/field_effects/pics/ichor_great_bear.png", ".gbapal");

static const struct SpriteSheet sGreatBearSheet = {sGreatBear_Gfx, 32 * 16 / 2, GREAT_BEAR_TAG};
// Blend-immune: the stars keep their gold under the night tint.
static const struct SpritePalette sGreatBearPalette = {sGreatBear_Pal, GREAT_BEAR_TAG | BLEND_IMMUNE_FLAG};

static const struct OamData sGreatBearOam =
{
    .shape = SPRITE_SHAPE(32x16),
    .size = SPRITE_SIZE(32x16),
    .priority = 1,
};

void Ichor_SpriteCB_GreatBear(struct Sprite *sprite)
{
}

static const struct SpriteTemplate sGreatBearTemplate =
{
    .tileTag = GREAT_BEAR_TAG,
    .paletteTag = GREAT_BEAR_TAG | BLEND_IMMUNE_FLAG,
    .oam = &sGreatBearOam,
    .anims = gDummySpriteAnimTable,
    .images = NULL,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = Ichor_SpriteCB_GreatBear,
};

static EWRAM_DATA u8 sGreatBearSpriteId = 0; // valid only while that sprite runs the bear's callback

static bool32 IsStarsOutAt(u32 timeOfDay)
{
    return timeOfDay == TIME_NIGHT && gMapHeader.mapType == MAP_TYPE_OCEAN_ROUTE && Ichor_IsSailing();
}

// specialvar Ichor_IsStarsOut: night, on a sea map, in the ship. The Outer Sea's
// night exit and Alethea's star reading check it.
bool8 Ichor_IsStarsOut(void)
{
    return IsStarsOutAt(GetTimeOfDay());
}

static bool32 IsGreatBearShown(void)
{
    return sGreatBearSpriteId < MAX_SPRITES && gSprites[sGreatBearSpriteId].inUse
        && gSprites[sGreatBearSpriteId].callback == Ichor_SpriteCB_GreatBear;
}

// overworld.c, once a field frame: the seven stars hang at the top of the screen,
// fixed to north, while they're out. Map loads and battles free every sprite, so
// this puts them back when the field returns.
void Ichor_SailingFrame(void)
{
    bool32 want = IsStarsOutAt(gTimeOfDay);
    bool32 shown = IsGreatBearShown();

    if (want && !shown)
    {
        u8 paletteNum;
        LoadSpriteSheet(&sGreatBearSheet);
        paletteNum = LoadSpritePalette(&sGreatBearPalette);
        if (paletteNum != 0xFF)
            UpdateSpritePaletteWithWeather(paletteNum, FALSE);
        sGreatBearSpriteId = CreateSprite(&sGreatBearTemplate, DISPLAY_WIDTH / 2, 14, 0);
    }
    else if (!want && shown)
    {
        DestroySpriteAndFreeResources(&gSprites[sGreatBearSpriteId]);
        sGreatBearSpriteId = MAX_SPRITES;
    }
}
