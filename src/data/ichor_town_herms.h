// Ichor: the travel herms (design/SYSTEMS.md §4; design/ENGINE_API.md §4).
//
// One row per town, hamlet or major rest stop: the map its herm stands on, the
// landing tile beside the herm on the main path (where travel sets the player
// down), the town's Asclepeion or healer heal location (using it registers the
// herm; HEAL_LOCATION_NONE where an inn heals instead), the name the herm, its
// plaque and the travel map show, and where the travel map marks it: the map
// section and its cell on the Aethos region map (design/AETHOS_MAP.md). Each
// herm has a cell of its own; a section with two herms (Kythera) has two cells.
//
// The herm and plaque objects are placed by tools/ichor/maps/town_herms.py,
// whose landing tiles must match these; tools/ichor/herm_audit.py checks both,
// checks each cell against src/data/region_map/region_map_layout.h, and fails
// when a town with a heal location has no row here.
const struct IchorTownHerm gIchorTownHerms[TOWN_HERM_MAX] =
{
    [TOWN_HERM_ELAIA]      = { MAP_ELAIA_VILLAGE,      15,  3, HEAL_LOCATION_ELAIA_VILLAGE,       COMPOUND_STRING("Elaia"),      MAPSEC_ELAIA_VILLAGE,    23,  9 },
    [TOWN_HERM_AKTI]       = { MAP_AKTI_TOWN,          13, 26, HEAL_LOCATION_AKTI_TOWN,           COMPOUND_STRING("Akti"),       MAPSEC_AKTI_TOWN,        23,  7 },
    [TOWN_HERM_AIGINA]     = { MAP_AEGINA_TOWN,         9, 12, HEAL_LOCATION_NONE,                COMPOUND_STRING("Aigina"),     MAPSEC_AIGINA,           14, 10 },
    [TOWN_HERM_EMPORION]   = { MAP_EMPORION_CITY,      19, 41, HEAL_LOCATION_EMPORION_CITY,       COMPOUND_STRING("Emporion"),   MAPSEC_EMPORION_CITY,    10,  9 },
    [TOWN_HERM_ELEUSA]     = { MAP_ELEUSA_VILLAGE,      5, 24, HEAL_LOCATION_ELEUSA_VILLAGE,      COMPOUND_STRING("Eleusa"),     MAPSEC_ELEUSA_VILLAGE,   14,  7 },
    [TOWN_HERM_THYRSA]     = { MAP_THYRSA_CITY,        26, 41, HEAL_LOCATION_THYRSA_CITY,         COMPOUND_STRING("Thyrsa"),     MAPSEC_THYRSA_CITY,      12,  4 },
    [TOWN_HERM_LEBADEIA]   = { MAP_LEBADEIA,           33, 17, HEAL_LOCATION_LEBADEIA,            COMPOUND_STRING("Lebadeia"),   MAPSEC_LEBADEIA,          9,  4 },
    [TOWN_HERM_KIRRHA]     = { MAP_KIRRHA,             14,  2, HEAL_LOCATION_KIRRHA,              COMPOUND_STRING("Kirrha"),     MAPSEC_KIRRHA,            7,  5 },
    [TOWN_HERM_AIGION]     = { MAP_AIGION,             16, 29, HEAL_LOCATION_AIGION,              COMPOUND_STRING("Aigion"),     MAPSEC_AIGION,            5,  7 },
    [TOWN_HERM_STYX_FALLS] = { MAP_STYX_FALLS,         15, 13, HEAL_LOCATION_NONE,                COMPOUND_STRING("Styx Falls"), MAPSEC_STYX_FALLS,        5,  9 },
    [TOWN_HERM_ARKADIA]    = { MAP_ARKADIA,            22,  3, HEAL_LOCATION_ARKADIA,             COMPOUND_STRING("Arkadia"),    MAPSEC_ARKADIA,           7, 10 },
    [TOWN_HERM_NEMEA]      = { MAP_NEMEA,               2, 17, HEAL_LOCATION_NEMEA,               COMPOUND_STRING("Nemea"),      MAPSEC_NEMEA,             8,  9 },
    [TOWN_HERM_DAPHNI]     = { MAP_DAPHNI,              2, 10, HEAL_LOCATION_DAPHNI,              COMPOUND_STRING("Daphni"),     MAPSEC_DAPHNI,           17,  7 },
    [TOWN_HERM_ASTYRA]     = { MAP_ASTYRA,              4, 33, HEAL_LOCATION_ASTYRA,              COMPOUND_STRING("Astyra"),     MAPSEC_ASTYRA,           18,  7 },
    [TOWN_HERM_KALDERA]    = { MAP_KALDERA,            17, 34, HEAL_LOCATION_KALDERA,             COMPOUND_STRING("Kaldera"),    MAPSEC_KALDERA,          23, 11 },
    [TOWN_HERM_SKANDEIA]   = { MAP_KYTHERA_SKANDEIA,   28, 11, HEAL_LOCATION_KYTHERA_SKANDEIA,    COMPOUND_STRING("Skandeia"),   MAPSEC_KYTHERA_ISLE,     12, 13 },
    [TOWN_HERM_PAPHIA]     = { MAP_KYTHERA_PAPHIA,     40, 22, HEAL_LOCATION_KYTHERA_PAPHIA,      COMPOUND_STRING("Paphia"),     MAPSEC_KYTHERA_ISLE,     12, 14 },
    [TOWN_HERM_AMNISOS]    = { MAP_KNOSSA_AMNISOS,     14,  7, HEAL_LOCATION_KNOSSA_AMNISOS,      COMPOUND_STRING("Amnisos"),    MAPSEC_AMNISOS,          21, 13 },
    [TOWN_HERM_OLYMPUS]    = { MAP_ASCENT_3F,          16,  5, HEAL_LOCATION_OLYMPUS_PROPYLAIA,   COMPOUND_STRING("Olympus"),    MAPSEC_MOUNT_OLYMPUS,     8,  0 },
    [TOWN_HERM_GYTHEION]   = { MAP_GYTHEION,           23, 14, HEAL_LOCATION_GYTHEION,            COMPOUND_STRING("Gytheion"),   MAPSEC_GYTHEION,         10, 13 },
    [TOWN_HERM_LAKONIA]    = { MAP_LAKONIA,            37, 36, HEAL_LOCATION_LAKONIA,             COMPOUND_STRING("Lakonia"),    MAPSEC_LAKONIA,           9, 12 },
    [TOWN_HERM_SACRED_OLIVES] = { MAP_ROUTE28_SACRED_OLIVES, 43, 2, HEAL_LOCATION_NONE,          COMPOUND_STRING("Sacred Olives"), MAPSEC_AETHOS_ROUTE_28, 7,  4 },
    [TOWN_HERM_DELPHOI]    = { MAP_DELPHOI,            38, 41, HEAL_LOCATION_DELPHOI,             COMPOUND_STRING("Delphoi"),    MAPSEC_DELPHOI,           7,  3 },
    [TOWN_HERM_ASCENT]     = { MAP_ASCENT_2F,           4, 41, HEAL_LOCATION_NONE,                COMPOUND_STRING("The Ascent"), MAPSEC_THE_ASCENT,        9,  1 },
    [TOWN_HERM_STYMPHALIA] = { MAP_LAKE_STYMPHALIA,    20, 32, HEAL_LOCATION_NONE,                COMPOUND_STRING("Stymphalia"), MAPSEC_LAKE_STYMPHALIA,   9, 10 },
};
