#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/flags.h"
#include "constants/items.h"
#include "constants/map_scripts.h"
#include "constants/maps.h"
#include "constants/moves.h"
#include "constants/pokemon.h"
#include "constants/species.h"
#include "constants/vars.h"
#include "constants/rtc.h"
    .include "asm/macros.inc"
    .include "asm/macros/event.inc"
    .include "constants/constants.inc"
    .text
    .align 2
    .macro test_header name:req, script:req
    .global \name
\name:
    map_script MAP_SCRIPT_ON_FRAME_TABLE, \name\()_Table
    .byte 0
    .align 2
\name\()_Table:
    map_script_2 VAR_TEMP_F, 0, \script
    .2byte 0
    .align 2
    .endm

@ The state Delphoi's chapter hands over (III-8): eight Laurels, Melitta's Honey and
@ Elpis's sealed tablet in the bag, the Omphalos open (VAR_ICHOR_ACT3 14), the night
@ held, and the player at the top of the Omphalos stair (3,2), as delphoi.sh ends.
@ Kynder was the starter, so Kleon fights beside you with Seismare.
    test_header Climax_SetupHeader, Climax_Setup
Climax_Setup:
    lockall
    setvar VAR_TEMP_F, 1
    givemon SPECIES_KYUREM, 100, ITEM_CHOICE_SPECS, move1=MOVE_ICE_BEAM, move2=MOVE_GROWL
    givemon SPECIES_METAGROSS, 100, move1=MOVE_IRON_HEAD
    setflag FLAG_SYS_POKEMON_GET
    setflag FLAG_BADGE01_GET
    setflag FLAG_BADGE02_GET
    setflag FLAG_BADGE03_GET
    setflag FLAG_BADGE04_GET
    setflag FLAG_BADGE05_GET
    setflag FLAG_BADGE06_GET
    setflag FLAG_BADGE07_GET
    setflag FLAG_BADGE08_GET
    setflag FLAG_ICHOR_MOM_MISSING
    setflag FLAG_ICHOR_MET_PHAEDON
    setflag FLAG_ICHOR_PHAEDON_DAPHNE_VISIT
    setflag FLAG_ICHOR_ASTYRA_OSTRACISM_DONE
    setflag FLAG_ICHOR_OMPHALOS_NIGHT
    setflag FLAG_ICHOR_OMPHALOS_OPEN
    setflag FLAG_ICHOR_VISITED_DELPHOI
    setflag FLAG_ICHOR_DELPHOI_ARRIVED
    setflag FLAG_ICHOR_MOM_SPRING
    additem ITEM_MELITTAS_HONEY
    additem ITEM_SEALED_TABLET
    setvar VAR_STARTER_MON, 1
    setvar VAR_ICHOR_ACT3, 14
    setvar VAR_REPEL_STEP_COUNT, 999
    setvar VAR_0x8004, TIME_NIGHT
    special Ichor_HoldTimeOfDay
    warp MAP_DELPHOI_OMPHALOS_STAIR, 3, 2
    waitstate
    releaseall
    end

@ The Wings, stood in for: each header lands at a door of the map the herms point to.
    .macro fly_header name:req, map:req, warpid:req
    test_header \name\()Header, \name
\name:
    lockall
    setvar VAR_TEMP_F, 1
    warp \map, \warpid
    waitstate
    releaseall
    end
    .endm

    fly_header Climax_ToForge, MAP_KALDERA_TELCHINES_FORGE, 0
    fly_header Climax_ToArkadia, MAP_ARKADIA, 0
    fly_header Climax_ToStoa, MAP_ASTYRA_STOA, 0
    fly_header Climax_ToPhaedonsHouse, MAP_ASTYRA_PHAEDONS_HOUSE, 0
    fly_header Climax_ToElaia, MAP_ELAIA_VILLAGE, 1
    fly_header Climax_ToHome, MAP_ELAIA_VILLAGE_PLAYERS_HOUSE_1F, 0

@ Delphoi's court, below the gate where Kleon stands frozen mid-swing.
    test_header Climax_ToDelphoiHeader, Climax_ToDelphoi
Climax_ToDelphoi:
    lockall
    setvar VAR_TEMP_F, 1
    warp MAP_DELPHOI, 23, 21
    waitstate
    releaseall
    end

@ Back to the Loom's west end, at the foot of the Stair's lowest flight.
    test_header Climax_ToLoomWestHeader, Climax_ToLoomWest
Climax_ToLoomWest:
    lockall
    setvar VAR_TEMP_F, 1
    warp MAP_THE_LOOM, 2, 12
    waitstate
    releaseall
    end

    test_header Climax_SaveHeader, Climax_Save
Climax_Save:
    lockall
    setvar VAR_TEMP_F, 1
    special SaveGame
    releaseall
    end
