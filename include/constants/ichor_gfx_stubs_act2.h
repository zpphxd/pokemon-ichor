#ifndef GUARD_CONSTANTS_ICHOR_GFX_STUBS_ACT2_H
#define GUARD_CONSTANTS_ICHOR_GFX_STUBS_ACT2_H

// ICHOR_STUB_TRAINER_ART (world-act2): Act II batch 1's new walkers and objects, named now so
// map scripts and map.json files can use their final names before the art exists. Each one
// points at an existing Ichor walker of the nearest look.
//
// When you add a real OBJ_EVENT_GFX_ICHOR_<NAME> to event_objects.h's enum, DELETE its line
// here in the same commit. A leftover line silently redirects the real sprite to the stand-in.
// design/phase3/BUILD.md lists who uses which.

// The four new trainer classes
#define OBJ_EVENT_GFX_ICHOR_MAENAD          OBJ_EVENT_GFX_ICHOR_YOUTH_F
#define OBJ_EVENT_GFX_ICHOR_SATYR           OBJ_EVENT_GFX_ICHOR_GOATHERD
#define OBJ_EVENT_GFX_ICHOR_ACTOR           OBJ_EVENT_GFX_ICHOR_ACOLYTE_M
#define OBJ_EVENT_GFX_ICHOR_VINTNER         OBJ_EVENT_GFX_ICHOR_HARVESTER

// People
#define OBJ_EVENT_GFX_ICHOR_THESPIS         OBJ_EVENT_GFX_ICHOR_ACOLYTE_M
#define OBJ_EVENT_GFX_ICHOR_SILENOS         OBJ_EVENT_GFX_ICHOR_ELDER_M
#define OBJ_EVENT_GFX_ICHOR_MANTO           OBJ_EVENT_GFX_ICHOR_ELDER_F
#define OBJ_EVENT_GFX_ICHOR_HERALD          OBJ_EVENT_GFX_ICHOR_YOUTH_M
#define OBJ_EVENT_GFX_ICHOR_KRONIST         OBJ_EVENT_GFX_ICHOR_MAN

// The Dionysia's cast (beat 32)
#define OBJ_EVENT_GFX_ICHOR_CHORUS_LEADER   OBJ_EVENT_GFX_ICHOR_ACOLYTE_M
#define OBJ_EVENT_GFX_ICHOR_BEE_WOMAN       OBJ_EVENT_GFX_ICHOR_PRIESTESS
#define OBJ_EVENT_GFX_ICHOR_FATE_SPINNER    OBJ_EVENT_GFX_ICHOR_ACOLYTE_F
#define OBJ_EVENT_GFX_ICHOR_FATE_MEASURER   OBJ_EVENT_GFX_ICHOR_ACOLYTE_F
#define OBJ_EVENT_GFX_ICHOR_FATE_CUTTER     OBJ_EVENT_GFX_ICHOR_ACOLYTE_F
#define OBJ_EVENT_GFX_ICHOR_GOLD_MASK_KING  OBJ_EVENT_GFX_ICHOR_ACOLYTE_M
#define OBJ_EVENT_GFX_ICHOR_UNWOVEN_ACTOR   OBJ_EVENT_GFX_ICHOR_YOUTH_M

// Extra poses for the cast (sitting, kneeling, at a table); the sprites agent chooses whether
// each is a new sheet or new frames on the existing one
#define OBJ_EVENT_GFX_ICHOR_KLEON_SEATED    OBJ_EVENT_GFX_ICHOR_KLEON
#define OBJ_EVENT_GFX_ICHOR_ALETHEA_KNEEL   OBJ_EVENT_GFX_ICHOR_ALETHEA

// Objects
#define OBJ_EVENT_GFX_ICHOR_WOODEN_IMAGE    OBJ_EVENT_GFX_ICHOR_TABLET
#define OBJ_EVENT_GFX_ICHOR_MASK            OBJ_EVENT_GFX_ICHOR_TABLET
#define OBJ_EVENT_GFX_ICHOR_CROWS           OBJ_EVENT_GFX_ICHOR_TABLET

#endif // GUARD_CONSTANTS_ICHOR_GFX_STUBS_ACT2_H
