// Ichor: the omen entries (design/SYSTEMS.md §6; design/ENGINE_API.md §7).
//
// One row per swarm, rare visitor, weather spot or stranger. Each new day the
// engine draws a kind by SYSTEMS §6's weights, then one of that kind's rows
// whose unlockFlag is set and lockFlag isn't (so augurs only name places you
// can reach). A kind with no such row isn't drawn. Good signs need no rows.
//
// Number each kind's entries in include/constants/ichor.h (OMEN_WEATHER_*,
// OMEN_SWARM_*, OMEN_VISITOR_*, ...), and add rows at the end.
//
//   Swarm:   .species, .level and .map. Half that map's land encounters are
//            the species today (the expansion's mass outbreak).
//   Visitor: .hideFlag. The engine sets every visitor's hide flag each day and
//            clears today's; a map's script sets it again once it's caught or
//            beaten.
//   Weather: the map's ON_TRANSITION checks Ichor_CheckOmen and sets its weather.

static const struct IchorOmenEntry sOmenEntries[] =
{
    {
        .kind = OMEN_WEATHER,
        .entry = OMEN_WEATHER_KRYOPUFF,     // snow on the Ascent's lowest slopes
        .unlockFlag = FLAG_BADGE07_GET,     // world-act3: the Ascent's own flag when it exists
    },
    {
        .kind = OMEN_WEATHER,
        .entry = OMEN_WEATHER_LERNIP,       // rain over Lake Stymphalia
        .unlockFlag = FLAG_BADGE07_GET,     // world-act3: Akanthis's rumor forces it first
    },
#if TESTING
    // test/ichor_world.c's rows, opened by FLAG_BADGE08_GET
    { .kind = OMEN_SWARM, .entry = 0, .unlockFlag = FLAG_BADGE08_GET, .species = SPECIES_WOBBUFFET, .map = MAP_KALLISTE_ROUTE1, .level = 7 },
    { .kind = OMEN_VISITOR, .entry = 0, .unlockFlag = FLAG_BADGE08_GET, .hideFlag = FLAG_TEMP_1 },
    { .kind = OMEN_VISITOR, .entry = 1, .unlockFlag = FLAG_BADGE08_GET, .hideFlag = FLAG_TEMP_2 },
#endif
};
