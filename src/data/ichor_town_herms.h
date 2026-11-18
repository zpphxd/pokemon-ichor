// Ichor: the travel herms (design/SYSTEMS.md §4; design/ENGINE_API.md §4).
//
// One row per town, hamlet or major rest stop: the map its herm stands on, the
// landing tile beside the herm on the main path (where travel sets the player
// down), the town's Asclepeion or healer heal location (using it registers the
// herm; HEAL_LOCATION_NONE where an inn heals instead), and the name the herm,
// its plaque and the travel menu show.
//
// The herm and plaque objects are placed by tools/ichor/maps/town_herms.py,
// whose landing tiles must match these; tools/ichor/herm_audit.py checks both,
// and fails when a town with a heal location has no row here.
const struct IchorTownHerm gIchorTownHerms[TOWN_HERM_MAX] =
{
    [TOWN_HERM_ELAIA]      = { MAP_ELAIA_VILLAGE,      15,  3, HEAL_LOCATION_ELAIA_VILLAGE,       COMPOUND_STRING("Elaia") },
    [TOWN_HERM_AKTI]       = { MAP_AKTI_TOWN,          13, 26, HEAL_LOCATION_AKTI_TOWN,           COMPOUND_STRING("Akti") },
    [TOWN_HERM_AIGINA]     = { MAP_AEGINA_TOWN,         9, 12, HEAL_LOCATION_NONE,                COMPOUND_STRING("Aigina") },
    [TOWN_HERM_EMPORION]   = { MAP_EMPORION_CITY,      19, 41, HEAL_LOCATION_EMPORION_CITY,       COMPOUND_STRING("Emporion") },
    [TOWN_HERM_ELEUSA]     = { MAP_ELEUSA_VILLAGE,      5, 24, HEAL_LOCATION_ELEUSA_VILLAGE,      COMPOUND_STRING("Eleusa") },
    [TOWN_HERM_THYRSA]     = { MAP_THYRSA_CITY,        26, 41, HEAL_LOCATION_THYRSA_CITY,         COMPOUND_STRING("Thyrsa") },
    [TOWN_HERM_LEBADEIA]   = { MAP_LEBADEIA,           33, 17, HEAL_LOCATION_LEBADEIA,            COMPOUND_STRING("Lebadeia") },
    [TOWN_HERM_KIRRHA]     = { MAP_KIRRHA,             14,  2, HEAL_LOCATION_KIRRHA,              COMPOUND_STRING("Kirrha") },
    [TOWN_HERM_AIGION]     = { MAP_AIGION,             16, 29, HEAL_LOCATION_AIGION,              COMPOUND_STRING("Aigion") },
    [TOWN_HERM_STYX_FALLS] = { MAP_STYX_FALLS,         15, 13, HEAL_LOCATION_NONE,                COMPOUND_STRING("Styx Falls") },
    [TOWN_HERM_ARKADIA]    = { MAP_ARKADIA,            22,  3, HEAL_LOCATION_ARKADIA,             COMPOUND_STRING("Arkadia") },
    [TOWN_HERM_NEMEA]      = { MAP_NEMEA,               2, 17, HEAL_LOCATION_NEMEA,               COMPOUND_STRING("Nemea") },
    [TOWN_HERM_DAPHNI]     = { MAP_DAPHNI,              2, 10, HEAL_LOCATION_DAPHNI,              COMPOUND_STRING("Daphni") },
    [TOWN_HERM_ASTYRA]     = { MAP_ASTYRA,              4, 33, HEAL_LOCATION_ASTYRA,              COMPOUND_STRING("Astyra") },
    [TOWN_HERM_KALDERA]    = { MAP_KALDERA,            17, 34, HEAL_LOCATION_KALDERA,             COMPOUND_STRING("Kaldera") },
    [TOWN_HERM_SKANDEIA]   = { MAP_KYTHERA_SKANDEIA,   28, 11, HEAL_LOCATION_KYTHERA_SKANDEIA,    COMPOUND_STRING("Skandeia") },
    [TOWN_HERM_PAPHIA]     = { MAP_KYTHERA_PAPHIA,     40, 22, HEAL_LOCATION_KYTHERA_PAPHIA,      COMPOUND_STRING("Paphia") },
    [TOWN_HERM_AMNISOS]    = { MAP_KNOSSA_AMNISOS,     14,  7, HEAL_LOCATION_KNOSSA_AMNISOS,      COMPOUND_STRING("Amnisos") },
    [TOWN_HERM_OLYMPUS]    = { MAP_ASCENT_3F,          21,  7, HEAL_LOCATION_OLYMPUS_PROPYLAIA,   COMPOUND_STRING("Olympus") },
};
