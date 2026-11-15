#ifndef GUARD_CONSTANTS_ICHOR_SPECIES_STUBS_H
#define GUARD_CONSTANTS_ICHOR_SPECIES_STUBS_H

// ICHOR_STUB_AETHOS_DEX: stand-ins for the Aethos dex until it is implemented.
//
// Phase 2's script (design/phase2/SCRIPT.md) names Aethos species
// (design/dex/ on claude/aethos-dex-a7c73a). Until those species exist in
// the species enum, each name below maps to a vanilla species of the same
// type and role, so trainers.party ("Harpeck" -> SPECIES_HARPECK), the wild
// encounter tables, givemon and the overworld sprites all build and play.
//
// When the dex lands, define ICHOR_AETHOS_DEX (or delete this file and its
// include at the end of constants/species.h). The enum then provides the real
// constants and nothing else changes.

#ifndef ICHOR_AETHOS_DEX

// The starters, in VAR_STARTER_MON's order (0 Grass, 1 Fire, 2 Water)
#define SPECIES_NEBREL      SPECIES_SNIVY        // Grass
#define SPECIES_KLADOE      SPECIES_SERVINE      // Grass
#define SPECIES_DAPHNYAD    SPECIES_SERPERIOR    // Grass/Fairy
#define SPECIES_KYNDER      SPECIES_CYNDAQUIL    // Fire
#define SPECIES_DIKYON      SPECIES_QUILAVA      // Fire
#define SPECIES_PYLAKYON    SPECIES_TYPHLOSION   // Fire/Ghost
#define SPECIES_HIPLING     SPECIES_PIPLUP       // Water
#define SPECIES_THALAMARE   SPECIES_PRINPLUP     // Water
#define SPECIES_SEISMARE    SPECIES_EMPOLEON     // Water/Ground

#define SPECIES_EPOPOI      SPECIES_PIDGEY       // Normal/Flying, the hoopoe
#define SPECIES_LOPHOPS     SPECIES_PIDGEOTTO    // Normal/Flying
#define SPECIES_BASILOPS    SPECIES_PIDGEOT      // Normal/Flying
#define SPECIES_GALEKIT     SPECIES_SENTRET      // Normal, the weasel
#define SPECIES_GELASABLE   SPECIES_FURRET       // Normal
#define SPECIES_ERGANT      SPECIES_NINCADA      // Bug, the Myrmidon ant
#define SPECIES_HOPLOMEX    SPECIES_HERACROSS    // Bug/Fighting
#define SPECIES_PEBBLITH    SPECIES_GEODUDE      // Rock/Ground
#define SPECIES_CAIRNOLITH  SPECIES_GRAVELER     // Rock/Ground
#define SPECIES_LAOLITH     SPECIES_GOLEM        // Rock/Fighting
#define SPECIES_ERIPIP      SPECIES_MAREEP       // Electric, Amalthea's kid
#define SPECIES_KERAZAP     SPECIES_FLAAFFY      // Electric
#define SPECIES_KERASTORM   SPECIES_AMPHAROS     // Electric/Fairy
#define SPECIES_HALCYLING   SPECIES_WINGULL      // Water/Flying, the halcyon
#define SPECIES_GALENYON    SPECIES_PELIPPER     // Water/Flying
#define SPECIES_KETOFRY     SPECIES_HORSEA       // Water, the ketos
#define SPECIES_KYNOKETOS   SPECIES_SEADRA       // Water/Dragon
#define SPECIES_KARKIPOOL   SPECIES_KRABBY       // Water, Hera's crab
#define SPECIES_KARKITOX    SPECIES_KINGLER      // Water/Poison
#define SPECIES_NEMECUB     SPECIES_LITLEO       // Normal, the Nemean lion
#define SPECIES_NEMELEON    SPECIES_PYROAR       // Normal
#define SPECIES_EOPEEP      SPECIES_MANKEY       // Fighting, Alectryon
#define SPECIES_ALEKROW     SPECIES_PRIMEAPE     // Fighting
#define SPECIES_HOPLEKTOR   SPECIES_HAWLUCHA     // Fighting/Flying
#define SPECIES_ONOTIS      SPECIES_LILLIPUP     // Normal, Midas's donkey
#define SPECIES_MIDONOS     SPECIES_HERDIER      // Normal/Steel
#define SPECIES_HARPECK     SPECIES_MURKROW      // Dark/Flying, the snatcher
#define SPECIES_HARPELLE    SPECIES_HONCHKROW    // Dark/Flying
#define SPECIES_CHELONET    SPECIES_SANDSHREW    // Ground, Hermes's tortoise
#define SPECIES_CHELYRA     SPECIES_SANDSLASH    // Ground/Fairy
#define SPECIES_PITHOUND    SPECIES_POOCHYENA    // Dark/Psychic, Diogenes's dog
#define SPECIES_NARKERAY    SPECIES_CHINCHOU     // Water/Electric, the torpedo ray
#define SPECIES_SPALUNK     SPECIES_DIGLETT      // Ground, Ploutos's mole
#define SPECIES_PLOUTERAS   SPECIES_DUGTRIO      // Ground
// Eleusa's fields (batch 4)
#define SPECIES_KAPLET      SPECIES_PHANPY       // Ground, Eubouleus's piglet
#define SPECIES_STACHYSS    SPECIES_SUNKERN      // Grass, the wheat serpent
#define SPECIES_MELIBEE     SPECIES_COMBEE       // Bug, Demeter's bee
#define SPECIES_ELALEAF     SPECIES_SEEDOT       // Grass, the olive sprout
#define SPECIES_RHOARIL     SPECIES_BOUNSWEET    // Grass, Persephone's pomegranate
// Emporion (batch 2)
#define SPECIES_PANACOIL    SPECIES_ARBOK        // Poison/Fairy, the healer serpent coiled in every Asclepeion
// Hecate's Hollow (batch 3): its two statics
#define SPECIES_LYKOPUP     SPECIES_POOCHYENA    // Dark, Hecate's black hound (the dex: Intimidate, Strong Jaw / Unnerve)
#define SPECIES_RAKNIT      SPECIES_SPINARAK     // Bug, Arachne's spiderling (the dex: Swarm, Frisk / Defiant)

#endif // ICHOR_AETHOS_DEX

#endif // GUARD_CONSTANTS_ICHOR_SPECIES_STUBS_H
